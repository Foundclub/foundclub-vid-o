"""Fabrique papier.md (lisible) à partir de papier.json (les coupes) et des transcriptions mot à mot.

Le texte de chaque phrase est relu dans TRAVAIL/transcriptions/<rush>-mots.json entre ses deux instants :
rien n'est recopié à la main. Un mot que Whisper a mal entendu (probabilité < 0,4) est suivi de « (?) ».
Les durées et l'instant de chaque phrase dans le futur montage sont calculés ici.

python -I outils/papier.py [dossier_travail]
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parents[1]
TRAVAIL = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\App\video\rushs\interview\travail")
papier = json.loads((ICI / "papier.json").read_text(encoding="utf-8"))
mots = {}


def texte(rush, debut, fin):
    if rush not in mots:
        mots[rush] = json.loads((TRAVAIL / "transcriptions" / f"{rush}-mots.json").read_text(encoding="utf-8"))
    for m in mots[rush]:  # une coupe qui tombe au milieu d'un mot se signale, elle ne se corrige pas en silence
        if m["debut"] < fin <= m["fin"] - 0.05 or m["debut"] < debut - 0.05 < m["fin"] - 0.05:
            print(f"  COUPE DANS UN MOT : rush {rush} {debut}–{fin} coupe « {m['mot'].strip()} » "
                  f"({m['debut']:.2f}–{m['fin']:.2f})")
    pris = [m for m in mots[rush] if debut - 0.05 <= m["debut"] < fin]
    # les mots courts sont souvent notés bas sans être faux : on ne signale que les mots d'au moins 4 lettres
    return "".join(m["mot"] + (" (?)" if m["probabilite"] < 0.4 and len(m["mot"].strip()) > 3 else "")
                   for m in pris).strip()


def hms(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def nom(rush):
    return rush[19:23] if rush.startswith("DJI_") else rush


lignes = [f"# Papier de montage — {papier['titre']}", "",
          "Fabriqué par `outils/papier.py` à partir de `papier.json` : on modifie le JSON, jamais ce fichier.", ""]
lignes += [f"- {n}" for n in papier["notes"]] + [""]
t, resume = 0.0, []
for seq in papier["sequences"]:
    debut_seq = t
    bloc = [f"## {seq['titre']}", "", f"*{seq['but']}* — Habillage : {seq['habillage']}", ""]
    for p in seq["paroles"]:
        d = p["fin"] - p["debut"]
        bloc.append(f"**{hms(t)}** · rush {nom(p['rush'])} {hms(p['debut'])}–{hms(p['fin'])} ({d:.1f} s) · {p['qui']}")
        bloc.append(f"> « {texte(p['rush'], p['debut'], p['fin'])} »")
        for c in p.get("plans", []):
            origine = f"rush {nom(c['rush'])}" if "rush" in c else c.get("source") or c["photo"]
            bloc.append(f"> ↳ plan de coupe à +{c['a']:.1f} s : {c['quoi']} ({origine} {hms(c['debut'])}–{hms(c['fin'])})")
        if p.get("note"):
            bloc.append(f"> ⚠ {p['note']}")
        bloc.append("")
        t += d
    for im in seq.get("images", []):
        d = im["fin"] - im["debut"]
        bloc += [f"**{hms(t)}** · image seule ({d:.1f} s) : {im['quoi']}", ""]
        t += d
    resume.append((seq["titre"], t - debut_seq))
    lignes += bloc

lignes[4:4] = ["## Les séquences en un coup d'œil", "", "| Séquence | Durée |", "|---|---|"] + \
    [f"| {s} | {hms(d)} |" for s, d in resume] + [f"| **Total (paroles et images, sans les respirations)** | **{hms(t)}** |", ""]
(ICI / "papier.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
print(f"papier.md : {len(resume)} séquences, {hms(t)}")
