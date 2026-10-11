"""Planches de la source (une image/5 s), audio et silences, sans montage."""
import json
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "source/ach10-source.mp4"
work = root / "travail"
sheets = root / "planches/source"
work.mkdir(exist_ok=True)
sheets.mkdir(parents=True, exist_ok=True)

subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-threads", "4", "-i", str(source),
                "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", "-y",
                str(work / "source-16k.wav")], check=True)
print("Audio mono 16 kHz extrait", flush=True)
silence = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(work / "source-16k.wav"),
             "-af", "silencedetect=noise=-32dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True)
if silence.returncode:
    raise RuntimeError(silence.stderr)
intervals, start = [], None
for line in silence.stderr.splitlines():
    match = re.search(r"silence_start: ([\d.]+)", line)
    if match:
        start = float(match[1])
    match = re.search(r"silence_end: ([\d.]+)", line)
    if match and start is not None:
        intervals.append({"debut": start, "fin": float(match[1])})
        start = None
(root / "diagnostic/silences.json").write_text(json.dumps(intervals, indent=2) + "\n", encoding="utf-8")
print(f"{len(intervals)} silences détectés", flush=True)
vf = "fps=1/5,scale=320:180,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='%{pts\\:hms}':x=6:y=h-24:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7,tile=5x5:padding=4:margin=4"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-threads", "4", "-i", str(source),
                "-vf", vf, "-an", "-threads", "2", "-q:v", "3", "-y",
                str(sheets / "source-%02d.jpg")], check=True)
print(f"{len(list(sheets.glob('source-*.jpg')))} planches de la source", flush=True)
