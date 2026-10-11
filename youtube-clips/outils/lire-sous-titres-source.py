"""Relevé des sous-titres déjà incrustés, comme aide à la relecture des voix bruitées."""
import json
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
from rapidocr_onnxruntime import RapidOCR

root = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
engine = RapidOCR(use_angle_cls=False, width_height_ratio=1000)
rows = []
for start, end in [(575, 721), (777, 829), (1138, 1318)]:
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-threads", "2", "-ss", str(start),
        "-i", str(root / "source/ach10-source.mp4"), "-t", str(end-start), "-vf",
        "fps=1,crop=1600:180:160:890,scale=1280:144", "-an", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    last = ""
    i = 0
    begin = time.monotonic()
    while True:
        data = proc.stdout.read(1280*144*3)
        if not data:
            break
        frame = np.frombuffer(data, dtype=np.uint8).reshape(144, 1280, 3)
        result, timing = engine(frame)
        text = " ".join(r[1] for r in result or [] if float(r[2]) >= .65)
        if text and text != last:
            rows.append({"t": start+i, "texte_visible": text})
            print(f"[{start+i}] {text}", flush=True)
            last = text
        i += 1
    if proc.wait():
        raise RuntimeError(proc.stderr.read().decode(errors="replace"))
    print(f"OCR {start}–{end}: {time.monotonic()-begin:.1f} s", flush=True)
    (root / "diagnostic/ocr-sous-titres.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
