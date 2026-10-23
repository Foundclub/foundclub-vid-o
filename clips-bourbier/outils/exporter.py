"""Découpe les extraits de extraits.json dans l'épisode « Match bourbier » : une version horizontale (1920×1080) et un
brouillon vertical (1080×1920, l'image entière sur un fond flou), son normalisé à -14 LUFS en deux passes, plus une
planche de 8 images par extrait. Même méthode que youtube-clips/outils/exporter.py (épisode #41).
Usage : python3 -I outils/exporter.py [numéros…]   (depuis clips-bourbier/, après outils/recoller.sh)"""
import json, subprocess, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "source" / "episode.mp4"
VERTICAL = ("[0:v]split=2[bg][fg];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=12,"
            "scale=1080:1920[back];[fg]scale=1080:608[front];[back][front]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")

def lancer(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)

def exporter(c):
    n, debut, d = c["numero"], c["debut"], round(c["fin"] - c["debut"], 3)
    fondu = f"afade=t=in:st=0:d=0.03,afade=t=out:st={d - .03:.3f}:d=0.03"
    mesure = lancer(["ffmpeg", "-hide_banner", "-ss", str(debut), "-i", str(SOURCE), "-t", str(d), "-vn", "-af",
                     fondu + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr
    m = json.loads(mesure[mesure.rindex("{"):])
    loud = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    for dossier, filtre, nom in (("horizontal", "[0:v]scale=1920:1080,setsar=1[v]", f"clip-{n:02}.mp4"),
                                 ("vertical", VERTICAL, f"clip-{n:02}-9x16.mp4")):
        (RACINE / dossier).mkdir(exist_ok=True)
        lancer(["ffmpeg", "-v", "error", "-y", "-ss", str(debut), "-i", str(SOURCE), "-t", str(d), "-filter_complex", filtre,
                "-map", "[v]", "-map", "0:a:0", "-af", fondu + "," + loud, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                str(RACINE / dossier / nom)])
    (RACINE / "planches").mkdir(exist_ok=True)
    lancer(["ffmpeg", "-v", "error", "-y", "-i", str(RACINE / "horizontal" / f"clip-{n:02}.mp4"), "-vf",
            f"fps=8/{d},scale=400:225,tile=4x2:nb_frames=8:padding=4:margin=4", "-frames:v", "1", "-q:v", "3",
            str(RACINE / "planches" / f"clip-{n:02}.jpg")])
    print(f"clip {n:02} : {debut:.2f}-{c['fin']:.2f} s ({d:.1f} s) — {c['titre']}")

extraits = json.load(open(RACINE / "extraits.json", encoding="utf-8"))
voulus = {int(a) for a in sys.argv[1:]}
for c in extraits:
    if not voulus or c["numero"] in voulus:
        exporter(c)
