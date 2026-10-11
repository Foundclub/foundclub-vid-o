"""Corrections appuyées sur les sous-titres/logos visibles ; conservation des hésitations."""
import json
from pathlib import Path
from transcrire import stamp, write

root = Path(__file__).resolve().parents[1]
out = root / "transcription"
words = json.loads((out / "transcription-mots.json").read_text(encoding="utf-8"))
raw = json.loads((out / "transcription-brut-segments.json").read_text(encoding="utf-8"))
original = [w for r in raw for w in r["mots"]]
# Les relectures sans VAD ont omis certains échanges ; reprendre la reconnaissance
# initiale avec VAD quand elle reconnaissait les phrases au lieu du faux ST'501.
for a,b in [(575,602.5),(636.54,639),(639,671)]:
    words = [w for w in words if not a <= (w["debut"]+w["fin"])/2 < b]
    words.extend(w.copy() for w in original if a <= (w["debut"]+w["fin"])/2 < b)
words.sort(key=lambda w:(w["debut"],w["fin"]))
corrections = []
for w in words:
    old = w["mot"]
    replacements = {"Suissard":"Sussargue", "Espali":"Espaly", "Espagie":"Espaly",
                    "Luciana":"Lucciana", "Payad":"Paillade", "Bokérois":"Beaucairois",
                    "bokehrois":"Beaucairois", "Rivera":"Riviera", "espectre":"instinct"}
    for a,b in replacements.items():
        if a in w["mot"]: w["mot"]=w["mot"].replace(a,b)
    if old != w["mot"]:
        corrections.append({"debut":w["debut"],"avant":old.strip(),"apres":w["mot"].strip(),
                            "preuve":"Sous-titres, logos ou tableau incrustés dans la source"})

# Une erreur de sens reconnue dans le discours : les sous-titres disent « votre force ».
for i,w in enumerate(words):
    if 777<=w["debut"]<=784 and "enfance" in w["mot"]:
        corrections.append({"debut":w["debut"],"avant":w["mot"].strip(),"apres":"force","preuve":"Sous-titre visible vers 13:01"})
        w["mot"]=w["mot"].replace("enfance","force")

# Ne conserver aucun sous-titre fantôme créé par le moteur de reconnaissance.
words = [w for w in words if not (w["mot"].strip().lower() in ["sous-titrage","st'","501","501."])]
segments, group = [], []
for w in words:
    if group and (w["debut"]-group[-1]["fin"]>1.2 or w["fin"]-group[0]["debut"]>10):
        segments.append({"debut":group[0]["debut"],"fin":group[-1]["fin"],"texte":"".join(x["mot"] for x in group).strip(),"mots":group})
        group=[]
    group.append(w)
if group:
    segments.append({"debut":group[0]["debut"],"fin":group[-1]["fin"],"texte":"".join(x["mot"] for x in group).strip(),"mots":group})
write(out / "transcription-mots.json", words)
write(out / "transcription-segments.json", segments)
write(out / "corrections.json", corrections)
(out / "transcription.srt").write_text("\n".join(f"{i}\n{stamp(s['debut'])} --> {stamp(s['fin'])}\n{s['texte']}\n" for i,s in enumerate(segments,1)),encoding="utf-8")
(out / "transcription.txt").write_text("\n".join(f"[{s['debut']:.2f}–{s['fin']:.2f}] {s['texte']}" for s in segments)+"\n",encoding="utf-8")
print(f"{len(corrections)} corrections ; {len(words)} mots consolidés")
