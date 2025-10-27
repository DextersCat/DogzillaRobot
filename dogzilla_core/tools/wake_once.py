#!/usr/bin/env python3
import os, sys, struct
import pvporcupine

access_key = os.environ.get("PICOVOICE_ACCESS_KEY", "").strip()
if not access_key:
    print("no PICOVOICE_ACCESS_KEY", file=sys.stderr); sys.exit(2)

keyword_path = os.path.expanduser("~/amy_core/keywords/astra.ppn")
try:
    sens = float(os.environ.get("ASTRA_SENS","0.90"))
except Exception:
    sens = 0.90

porc = pvporcupine.create(access_key=access_key,
                          keyword_paths=[keyword_path],
                          sensitivities=[sens])
frame_len = porc.frame_length  # samples per frame (e.g., 512)
buf = sys.stdin.buffer.read

while True:
    data = buf(frame_len * 2)  # 2 bytes per sample (int16)
    if not data or len(data) < frame_len*2:
        sys.exit(1)
    pcm = struct.unpack_from("h"*frame_len, data, 0)
    if porc.process(pcm) >= 0:
        print("wake")
        sys.exit(0)
