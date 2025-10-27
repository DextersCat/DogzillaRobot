#!/usr/bin/env python3
import os, re, sys, time, json, shlex, subprocess, tempfile, datetime
from pathlib import Path

# Suppress ONNX Runtime warnings about GPU detection
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['ORT_LOGGING_LEVEL'] = '3'  # Only show errors, suppress warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="onnxruntime")

# SAFETY CONFIGURATION
DESK_SAFE_MODE = True  # Set to False only when Amy is in safe open space for full mobility

# ENV / paths
AUDIODEV   = os.environ.get("AUDIODEV", "plughw:CARD=sndrpihifiberry,DEV=0")
AREC_DEV   = os.environ.get("AREC_DEV", "plughw:CARD=Device,DEV=0")
VOICE_MODEL= str(Path.home()/ "voices/en_US-amy-medium.onnx")
LOGDIR     = Path.home()/ "logs"; LOGDIR.mkdir(parents=True, exist_ok=True)
LOG        = LOGDIR / f"pipeline_{datetime.datetime.now():%Y-%m-%d_%H%M%S}.log"

# --- utilities ---
def log(msg, obj=None):
    ts = time.strftime("%H:%M:%S")
    with LOG.open("a") as f:
        f.write(f"[{ts}] {msg}\n")
        if obj is not None:
            f.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def say(text):
    # Serialize TTS before any motion to avoid stutter
    wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav"); wav.close()
    # Use stdin instead of --text parameter to avoid "text" prefix in audio
    cmd = ["piper", "--model", VOICE_MODEL, "--output_file", wav.name]
    # Set environment for subprocess to suppress ONNX warnings
    env = os.environ.copy()
    env['ORT_LOGGING_LEVEL'] = '3'
    env['OMP_NUM_THREADS'] = '1'
    # Run with stderr filtering to suppress GPU warnings
    result = subprocess.run(cmd, input=text, text=True, check=False, env=env, 
                          stderr=subprocess.PIPE)
    # Filter out GPU-related warnings from stderr
    if result.stderr:
        filtered_stderr = '\n'.join(line for line in result.stderr.split('\n') 
                                   if 'GPU device discovery failed' not in line and
                                      'ReadFileContents Failed' not in line and
                                      'device_discovery.cc' not in line)
        if filtered_stderr.strip():
            sys.stderr.write(filtered_stderr)
    
    subprocess.run(["aplay", "-D", AUDIODEV, wav.name], check=False, 
                  stderr=subprocess.DEVNULL)
    try: os.unlink(wav.name)
    except: pass

def record_wav(out_path="/tmp/postwake.wav", secs=4, rate=48000):
    cmd = ["arecord", "-D", AREC_DEV, "-r", str(rate), "-c", "1", "-f", "S16_LE", "-d", str(secs), out_path]
    return subprocess.run(cmd, check=False).returncode == 0

def transcribe(wav_path):
    # Simple audio enhancement using sox (much more stable)
    enhanced_path = wav_path.replace('.wav', '_enhanced.wav')
    
    # Use sox for simple but effective audio enhancement
    sox_cmd = [
        "sox", wav_path, enhanced_path,
        "gain", "15",          # 15dB gain boost (reduced from 20 to prevent clipping)
        "compand", "0.02,0.20", "-60,-40,-30,-20,-10,-8", "3", "-90", "0.1",  # Gentler compression
        "highpass", "80",      # Remove low frequency noise
        "norm", "-3"           # Normalize with -3dB headroom
    ]
    
    try:
        subprocess.run(sox_cmd, check=True, capture_output=True)
        transcribe_path = enhanced_path
        log("audio_enhancement", {"method": "sox", "gain_db": 20})
    except Exception as e:
        log("audio_enhancement_failed", {"error": str(e), "fallback": "original"})
        transcribe_path = wav_path
    
    # Transcribe enhanced or original audio
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(transcribe_path, language="en")
    
    text_parts = []
    for segment in segments:
        clean_text = segment.text.strip()
        if clean_text and clean_text not in ['.', '']:
            text_parts.append(clean_text)
    
    full_text = " ".join(text_parts)
    return full_text, {"lang": info.language, "prob": info.language_probability, "dur": info.duration}

def do_wave():
    # Desk-safe wave using preset coordinates from examples/preset_actions.py
    try:
        sys.path.extend([str(Path.home()/ "picrawler"), str(Path.home()/ "robot-hat")])
        from picrawler import Picrawler
        c = Picrawler()
        
        # Wave hand coordinates from preset_actions.py
        coords = [
            # stand
            [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
            # wave hand
            [[45, 45, -70], [60, 0, 120], [45, 0, -60], [45, 45, -30]],
            [[45, 45, -70], [-20, 60, 120], [45, 0, -60], [45, 45, -30]],
            [[45, 45, -70], [60, 0, 120], [45, 0, -60], [45, 45, -30]],
            # return to stand
            [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        ]
        
        for coord in coords:
            c.do_step(coord, 95)  # Slightly faster speed
            time.sleep(0.05)  # Reduced delay for quicker response
        
        return True
    except Exception as e:
        log("wave error", {"error": str(e)})
        return False

# --- simple intent router (desk-safe) ---
INTENTS = {
    "wave": re.compile(r"\b(wave|hello|hi there)\b", re.I),
    "lights_on": re.compile(r"\blights?\s+(on|up)\b", re.I),
    "lights_off": re.compile(r"\blights?\s+off\b", re.I),
    "say": re.compile(r"\bsay\s+(.+)$", re.I),
    "time": re.compile(r"\b(what(?:'s| is)?\s+)?time\b", re.I),
    "status": re.compile(r"\bstatus\b", re.I),
}

def route(text):
    text = text.strip()
    if not text: return ("none", {})
    if INTENTS["wave"].search(text): return ("wave", {})
    m = INTENTS["say"].search(text);  # capture text to speak
    if m: return ("say", {"utterance": m.group(1).strip()})
    if INTENTS["lights_on"].search(text):  return ("lights_on", {})
    if INTENTS["lights_off"].search(text): return ("lights_off", {})
    if INTENTS["time"].search(text):   return ("time", {})
    if INTENTS["status"].search(text): return ("status", {})
    return ("unknown", {"raw": text})

def do_action(intent, slots):
    if intent == "wave":
        say("Okay, waving.")
        ok = do_wave()
        if not ok: say("I could not wave.")
    elif intent == "say":
        say(slots["utterance"])
    elif intent == "lights_on":
        say("Okay, turning lights on.")  # placeholder hook
    elif intent == "lights_off":
        say("Okay, turning lights off.") # placeholder hook
    elif intent == "time":
        now = datetime.datetime.now().strftime("%H:%M")
        say(f"The time is {now}.")
        # Add wave gesture after time announcement
        do_wave()
    elif intent == "status":
        # lightweight status
        try:
            temp = subprocess.check_output(["vcgencmd","measure_temp"], text=True).strip()
        except Exception:
            temp = "temp=n/a"
        mode_status = "desk safe mode" if DESK_SAFE_MODE else "full mobility mode"
        say(f"Amy is online. {temp}. Currently in {mode_status}. Audio ok.")
    elif intent == "unknown":
        say("Sorry, I did not understand that.")
    else:
        if DESK_SAFE_MODE:
            say("Intent not allowed in desk safe mode. Amy is protecting equipment.")
        else:
            say("Intent not recognized.")

def main():
    log("START", {"arec_dev": AREC_DEV, "audiodev": AUDIODEV})
    wav = "/tmp/postwake.wav"
    # settle time: 0.35s in astra_listen_loop.sh + 1.5s here = 1.85s total (more generous)
    time.sleep(1.5)
    # Increased recording duration: 5s → 8s for more forgiving timing
    ok = record_wav(wav, secs=8, rate=48000)
    log("record", {"ok": ok, "path": wav, "duration_secs": 8, "fault_tree_fix": "v1.1_timing_improved"})
    if not ok:
        say("I could not capture audio."); return
    text, meta = transcribe(wav)
    log("stt", {"text": text, "meta": meta})
    if not text:
        say("I heard nothing."); return
    intent, slots = route(text)
    log("nlu", {"intent": intent, "slots": slots})
    do_action(intent, slots)
    log("DONE")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("FATAL", {"error": str(e)})
        say("There was an error in the pipeline.")
