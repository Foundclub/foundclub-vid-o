"""Mesure le son de chaque rush (TRAVAIL/son48/*.wav) : niveau intégré (LUFS), plage (LRA), crête,
nombre d'échantillons écrêtés (à 0 dBFS ou presque) et part de passages très faibles (sous -50 dBFS sur 1 s).

python outils/mesurer_son.py [dossier_travail]   (sans -I : numpy est dans le dossier Python de l'utilisateur)
"""
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

TRAVAIL = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\App\video\rushs\interview\travail")

print(f"{'rush':<28} {'LUFS':>6} {'LRA':>5} {'crête':>7} {'écrêtés':>8} {'faible':>7}")
for w in sorted((TRAVAIL / "son48").glob("*.wav")):
    sortie = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(w), "-af", "ebur128", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    resume = sortie[sortie.rfind("Summary:"):]
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", resume).group(1)
    lra = re.search(r"LRA:\s+([\d.]+) LU", resume).group(1)
    with wave.open(str(w)) as f:
        x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, f.getnchannels())
        taux = f.getframerate()
    x = x.astype(np.float32) / 32768
    crete = 20 * np.log10(max(np.abs(x).max(), 1e-9))
    ecretes = int((np.abs(x) > 0.999).sum())
    mono = x.mean(axis=1)
    sec = mono[: len(mono) // taux * taux].reshape(-1, taux)
    faible = (20 * np.log10(np.sqrt((sec ** 2).mean(axis=1)) + 1e-9) < -50).mean() * 100 if len(sec) else 0
    print(f"{w.stem:<28} {lufs:>6} {lra:>5} {crete:>6.1f}  {ecretes:>8} {faible:>6.0f}%")
