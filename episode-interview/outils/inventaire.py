"""Écrit episode-interview/inventaire.json : pour chaque rush, caméra, début et fin de tournage, format, son,
et ce que la transcription en a tiré (nombre de mots). Signale les rushs qui se chevauchent dans le temps
(signe d'une deuxième caméra ou d'un micro séparé à synchroniser par le son).

python -I outils/inventaire.py [dossier_rushs] [dossier_travail]
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

RUSHS = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\Foundclub média\ACh")
TRAVAIL = Path(sys.argv[2] if len(sys.argv) > 2 else r"D:\App\video\rushs\interview\travail")
SORTIE = Path(__file__).resolve().parents[1] / "inventaire.json"

rushs = []
for p in sorted(x for x in RUSHS.iterdir() if x.suffix.lower() == ".mp4"):
    j = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:format_tags=creation_time,encoder"
         ":stream=codec_type,codec_name,width,height,r_frame_rate,channels,sample_rate", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    duree = float(j["format"]["duration"])
    # creation_time est en UTC ; les noms DJI portent l'heure de l'horloge de la caméra
    debut = datetime.fromisoformat(j["format"]["tags"]["creation_time"].replace("Z", "+00:00"))
    n, d = map(int, v["r_frame_rate"].split("/"))
    mesures = TRAVAIL / "transcriptions" / f"{p.stem}-mesures.json"
    rushs.append({
        "nom": p.name, "camera": j["format"]["tags"].get("encoder", "?"),
        "debut_utc": debut.isoformat(), "fin_utc": (debut + timedelta(seconds=duree)).isoformat(),
        "duree_s": round(duree, 2), "taille_mo": round(p.stat().st_size / 2**20),
        "video": f"{v['codec_name']} {v['width']}x{v['height']} {n / d:.2f} i/s",
        "son": f"{a['codec_name']} {a['channels']} canaux {a['sample_rate']} Hz" if a else None,
        "mots_transcrits": json.loads(mesures.read_text(encoding="utf-8"))["mots"] if mesures.exists() else None,
        "copie_legere": str(TRAVAIL / "proxies" / f"{p.stem}.mp4"),
        "planche": str(TRAVAIL / "planches" / f"{p.stem}.jpg"),
    })

chevauchements = [
    [a["nom"], b["nom"]] for i, a in enumerate(rushs) for b in rushs[i + 1:]
    if a["debut_utc"] < b["fin_utc"] and b["debut_utc"] < a["fin_utc"]
]
SORTIE.write_text(json.dumps({"rushs": rushs, "chevauchements": chevauchements,
                              "duree_totale_min": round(sum(r["duree_s"] for r in rushs) / 60, 1)},
                             ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(rushs)} rushs, {sum(r['duree_s'] for r in rushs) / 60:.1f} min, chevauchements : {chevauchements or 'aucun'}")
