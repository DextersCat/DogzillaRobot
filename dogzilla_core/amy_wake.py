import os, sys, time, threading, queue, subprocess, tempfile
import numpy as np

# -------- CONFIG --------
PLAYBACK_ALSA = os.environ.get("AUDIODEV", "plughw:2,0")   # HiFiBerry DAC
MIC_DEVICE    = "plughw:3,0"                               # USB mic
WAKE_PROMPT = 'Astra'
KEYWORD_PATH = os.path.expanduser('~/amy_core/keywords/astra.ppn')
WAKE_PROMPT = 'Astra'
KEYWORD_PATH = os.path.expanduser('~/amy_core/keywords/astra.ppn')
ACCESS_KEY    = os.environ.get("PICOVOICE_ACCESS_KEY")     # required
PIPER_MODEL   = os.path.expanduser("~/voices/en_US-amy-medium.onnx")

if not ACCESS_KEY:
    raise RuntimeError("Set PICOVOICE_ACCESS_KEY first.")

# -------- TTS (Piper, fallback to espeak) --------
def say(text: str):
    try:
        if os.path.exists(PIPER_MODEL):
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            subprocess.run(
                ["piper", "--model", PIPER_MODEL, "--text", text, "--output_file", tmp],
                check=True
            )
            subprocess.run(["aplay", "-D", PLAYBACK_ALSA, tmp], check=False)
            try: os.remove(tmp)
            except: pass
        else:
            subprocess.run(["espeak-ng", text], check=False)
    except Exception as e:
        print("TTS error:", e, file=sys.stderr)

# -------- Safe wave action --------
def safe_wave():
    try:
        sys.path.insert(0, "/home/spencer/picrawler")
        from picrawler import Picrawler
        bot = Picrawler()
        try:
            bot.do_action("wave")
        except Exception:
            bot.do_action("wave_hand")
    except Exception as e:
        print("wave action error:", e)

# -------- arecord reader (ALSA resampling) --------
def arecord_stream(device='plughw:3,0', rate=16000, channels=1):
    # -q quiet; S16_LE 16k mono
    cmd = ["arecord","-D",device,"-f","S16_LE","-r",str(rate),"-c",str(channels),"-q"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    q = queue.Queue()
    def reader():
        try:
            while True:
                data = p.stdout.read(1024)
                if not data:
                    break
                q.put(data)
        finally:
            try: p.kill()
            except: pass
    threading.Thread(target=reader, daemon=True).start()
    return p, q

def main():
    import pvporcupine
    print("Initializing Porcupine...")
    porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_PATH])

    # define after create:
    sample_rate  = getattr(porcupine, "sample_rate", 16000)
    frame_length = getattr(porcupine, "frame_length", 512)
    bytes_per_sample = 2  # S16_LE
    frame_bytes = frame_length * bytes_per_sample
    dtype = np.int16

    print(f"Mic via arecord: {MIC_DEVICE}  sr={sample_rate}  frame={frame_length}")
    say(f"Amy wake test ready. Say the word: {WAKE_PROMPT}.")
    print("Listening (arecord)…")

    proc, q = arecord_stream(device=MIC_DEVICE, rate=sample_rate, channels=1)
    buf = b""
    try:
        while True:
            buf += q.get()
            while len(buf) >= frame_bytes:
                chunk = buf[:frame_bytes]
                buf = buf[frame_bytes:]
                frame = np.frombuffer(chunk, dtype=dtype)
                res = porcupine.process(frame)
                if res >= 0:
                    print("Wake word detected!")
                    say("Hi Spencer, I’m listening.")
                    threading.Thread(target=safe_wave, daemon=True).start()
                    time.sleep(1.2)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        try: proc.kill()
        except: pass

if __name__ == "__main__":
    main()
