"""Vérifie des vidéos rendues : décodage complet sans erreur, durée, niveau du son (LUFS) et crête vraie (dBFS).

python -I outils/verifier.py fichier.mp4 [fichier.mp4 …]
Sort avec le code 1 si un fichier ne se décode pas en entier.
"""
import re
import subprocess
import sys

echec = 0
for f in sys.argv[1:]:
    dec = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                 capture_output=True, text=True).stdout)
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1]
    crete = re.findall(r"Peak:\s+(-?[\d.inf]+) dBFS", err)[-1]
    ok = dec.returncode == 0 and not dec.stderr.strip()
    echec |= not ok
    print(f"{'OK ' if ok else 'ERREUR'} {f.rsplit(chr(92), 1)[-1]:<16} {int(duree // 60)}:{duree % 60:04.1f}  "
          f"{lufs} LUFS  crête {crete} dBFS" + ("" if ok else f"  {dec.stderr.strip()[:200]}"))
sys.exit(echec)
