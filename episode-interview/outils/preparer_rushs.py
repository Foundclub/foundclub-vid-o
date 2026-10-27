"""Prépare les rushs de l'épisode interview pour travailler vite, sans toucher aux originaux.

Pour chaque rush :
- une copie légère 720p à 29,97 i/s (H.264, son AAC si le rush en a) ;
- le son en WAV 48 kHz stéréo (synchronisation) et 16 kHz mono (transcription) ;
- une planche d'images toutes les 5 s, l'instant écrit sur chaque image.
Tout part dans TRAVAIL (hors du dépôt). Un fichier déjà fait n'est pas refait.

python -I outils/preparer_rushs.py [dossier_rushs] [dossier_travail] [encodeur]

ponytail: encodage libx264 sur le processeur, car h264_nvenc refuse de s'ouvrir avec le pilote NVIDIA 595.79
(les ffmpeg installés demandent 610+). Passer « h264_nvenc » en 3ᵉ argument une fois le pilote à jour.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

RUSHS = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\Foundclub média\ACh")
TRAVAIL = Path(sys.argv[2] if len(sys.argv) > 2 else r"D:\App\video\rushs\interview\travail")
ENCODEUR = sys.argv[3] if len(sys.argv) > 3 else "libx264"
OPTS = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23"] if ENCODEUR == "libx264" \
    else ["-c:v", ENCODEUR, "-preset", "p4", "-cq", "24"]


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", *args], check=True)


def sonde(chemin):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                        "-of", "json", str(chemin)], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    return float(j["format"]["duration"]), any(s["codec_type"] == "audio" for s in j["streams"])


for d in ("proxies", "son48", "son16", "planches"):
    (TRAVAIL / d).mkdir(parents=True, exist_ok=True)

for rush in sorted(p for p in RUSHS.iterdir() if p.suffix.lower() == ".mp4"):
    nom = rush.stem
    duree, a_son = sonde(rush)
    proxy = TRAVAIL / "proxies" / f"{nom}.mp4"
    if not proxy.exists():
        tmp = proxy.with_suffix(".tmp.mp4")
        son = ["-c:a", "aac", "-b:a", "128k"] if a_son else ["-an"]
        ffmpeg("-hwaccel", "cuda", "-i", str(rush), "-vf", "fps=30000/1001,scale=-2:720", *OPTS, "-g", "30",
               *son, "-movflags", "+faststart", "-y", str(tmp))
        tmp.replace(proxy)
    if a_son:
        w48, w16 = TRAVAIL / "son48" / f"{nom}.wav", TRAVAIL / "son16" / f"{nom}.wav"
        if not w48.exists():
            ffmpeg("-i", str(rush), "-vn", "-c:a", "pcm_s16le", "-ar", "48000", "-y", str(w48))
        if not w16.exists():
            ffmpeg("-i", str(rush), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", "-y", str(w16))
    planche = TRAVAIL / "planches" / f"{nom}.jpg"
    if not planche.exists():
        lignes = max(1, math.ceil(math.ceil(duree / 5) / 8))
        ffmpeg("-i", str(proxy), "-vf",
               "fps=1/5,scale=320:-2,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf'"
               ":text='%{pts\\:hms}':x=6:y=6:fontsize=20:fontcolor=white"
               f":box=1:boxcolor=black@0.6,tile=8x{lignes}:padding=4",
               "-frames:v", "1", "-q:v", "4", "-y", str(planche))
    print("OK", nom, flush=True)
print("FINI", flush=True)
