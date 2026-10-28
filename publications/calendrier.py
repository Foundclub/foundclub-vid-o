"""Écrit le calendrier complet des publications : CALENDRIER.md et CALENDRIER.html (rendu en PDF par pdf.mjs), avec une
vignette de chaque vidéo tirée de son rendu final. Deux séries :
- les clips AchhLife « Match bourbier » (épisode #42), 2 par jour. Ordre décidé avec Adel le 26/10/2026 : rien qui
  dévoile le score avant la fin ; le 01 est sorti le 26/10, rien d'autre depuis ; le 28/10 au soir, Adel fait démarrer la
  liste le jeudi 29/10 au matin ;
- les vidéos FoundClub de la bibliothèque des 20 scripts, une tous les 2 jours (Adel, 28/10). Leurs titres et leur état
  viennent de scripts-foundclub/suivi.json ; une case vide attend la prochaine vidéo tournée.
Usage : python3 -I publications/calendrier.py && node publications/pdf.mjs publications/CALENDRIER.html publications/CALENDRIER.pdf
(depuis la racine du dépôt)"""
import datetime as dt, subprocess, os, sys, html
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "scripts-foundclub" / "outils"))
from suivi import TITRES as TITRES_FC, etat as etat_fc   # noqa: E402

DEBUT = dt.date(2026, 10, 29)
# Les heures changent d'un jour à l'autre (Adel, 28/10 : « varier les horaires pour voir quand ça marche le mieux ») :
# chaque tranche de la journée est essayée 3 ou 4 fois par les clips, et une fois par les vidéos FoundClub,
# jamais à moins de 2 h d'une autre publication.
HEURES = [("09:00", "19:00"), ("12:30", "21:30"), ("10:30", "17:00"), ("12:00", "20:00"), ("07:30", "18:00"),
          ("13:00", "21:00"), ("08:30", "16:00"), ("12:30", "22:00"), ("15:30", "19:00"), ("15:00",)]
TRANCHES = [("11:00", "Matin"), ("14:00", "Midi"), ("18:00", "Après-midi"), ("21:00", "Soirée"), ("24:00", "Nuit")]
tranche = lambda h: next(nom for fin, nom in TRANCHES if h < fin)
JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS_FR = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
TITRES = {
 1: "Et si la Coupe de France était la meilleure compétition ?", 2: "J'ai fait le match de ma vie face à une Ligue 1",
 3: "Quand j'ai failli jouer le match de ma vie contre l'OL", 4: "Quand j'ai joué devant 10 000 personnes à la Mosson",
 5: "En Coupe de France, on a le droit de rêver", 6: "Le système de la Coupe de France, vous le trouvez juste ?",
 7: "Y'a toujours ce collègue qu'il faut pas regarder pendant le discours", 8: "Mobiliser tout le monde à la mi-temps (enfin presque)",
 9: "Combien de buts dans ce match de Coupe ?", 10: "Le président a tranché : « Un champ de patate ! »",
 12: "Unique. Magique. La Coupe de France", 13: "Le niveau à l'entraînement d'une équipe de National 2",
 14: "Notre entrée en Coupe de France", 15: "Même sur un champ de patate, ça met des petits ponts",
 16: "Le premier but, avec une passe D de fou", 17: "Une passe D de ma part en Coupe de France",
 18: "Beaucoup d'action dans ce match de Coupe de France", 19: "Coup de sifflet final en Coupe de France",
 20: "Le discours du coach à la mi-temps", 21: "Dans le prochain épisode : le derby face au MHSC",
}
SPOIL = {16: "un but", 17: "un but", 10: "on devine que ça s'est bien passé", 9: "deux buts", 19: "la fin du match"}
ORDRE = [(4, 7), (6, 14), (12, 15), (2, 13), (3, 20), (5, 8), (18, 16), (17, 10), (19, 9), (21,)]
# Vidéos FoundClub : une tous les 2 jours, (heure, numéro) ; None = la prochaine vidéo tournée. Le 03 juste avant le
# week-end de la Toussaint (pas de match : c'est son sujet), le 02 le samedi à 22 h, l'heure des convocations de dernière
# minute dont il se moque. Une tranche différente à chaque fois.
FOUNDCLUB = {dt.date(2026, 10, 29): ("16:30", 3), dt.date(2026, 10, 31): ("22:00", 2), dt.date(2026, 11, 2): ("12:30", None),
             dt.date(2026, 11, 4): ("19:30", None), dt.date(2026, 11, 6): ("08:00", None)}
RENDUS_FC = {3: "week-end-gache/rendus/week-end-gache-final.mp4"}

os.makedirs(RACINE / "publications/vignettes", exist_ok=True)
def vignette(video, nom):   # l'accroche et l'image, à 2 s du rendu final
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.0", "-i", str(RACINE / video), "-frames:v", "1",
                    "-vf", "crop=1080:1500:0:120,scale=160:-2", "-q:v", "3", str(RACINE / "publications/vignettes" / nom)], check=True)
    return f"vignettes/{nom}"

publications = []   # (date, heure, série, numéro, titre, fichier, vignette, état)
for i, jour in enumerate(ORDRE):
    date = DEBUT + dt.timedelta(i)
    assert len(HEURES[i]) == len(jour)
    for n, h in zip(jour, HEURES[i]):
        f = f"clips-bourbier/habillage/rendus/clip-{n:02d}-tiktok.mp4"
        publications.append((date, h, "AchhLife", f"{n:02d}", TITRES[n], f, vignette(f, f"clip-{n:02d}.jpg"),
                             ("🟠 spoil : " + SPOIL[n]) if n in SPOIL else "🟢 sans spoil"))
for date, (h, n) in FOUNDCLUB.items():
    if n is None:
        publications.append((date, h, "FoundClub", "—", "Prochaine vidéo tournée", "", "", "⬜ à remplir dès qu'Achraf en tourne une"))
        continue
    e = etat_fc(n).get("etat")
    f = RENDUS_FC.get(n, etat_fc(n).get("fichier", ""))
    publications.append((date, h, "FoundClub", f"{n:02d}/20", TITRES_FC[n - 1], f, vignette(f, f"fc-{n:02d}.jpg") if e == "fait" else "",
                         "✅ prête" if e == "fait" else "🟠 en montage : à valider avant, sinon on décale"))
publications.sort(key=lambda p: (p[0], p[1]))
for a, b in zip(publications, publications[1:]):   # jamais deux publications à moins de 2 h
    if a[0] == b[0]:
        m = lambda h: int(h[:2]) * 60 + int(h[3:])
        assert m(b[1]) - m(a[1]) >= 120, (a[:2], b[:2])
essais = {nom: [sum(1 for p in publications if p[2] == s and tranche(p[1]) == nom) for s in ("AchhLife", "FoundClub")] for _, nom in TRANCHES}
jours = sorted({p[0] for p in publications})
libelle = lambda d: f"{JOURS_FR[d.weekday()].capitalize()} {d.day} {MOIS_FR[d.month]}"

md = ["# Calendrier des publications — du 29 octobre au 7 novembre 2026", "",
      "- **Clips AchhLife « Match bourbier »** (épisode #42) : 2 par jour. Rien qui dévoile le score avant la fin. "
      "Fichiers : `clips-bourbier/habillage/rendus/clip-NN-tiktok.mp4`.",
      "- **Vidéos FoundClub** (bibliothèque des 20 scripts) : une tous les 2 jours. État de chaque script : "
      "`scripts-foundclub/bibliotheque-20-scripts-suivi.pdf`.",
      "- **Les heures changent chaque jour** pour voir quand ça marche le mieux : noter les vues 24 h après chaque publication.", "",
      "| Tranche | Essais clips | Essais FoundClub |", "|---|---|---|"] + [f"| {nom} | {a} | {b} |" for nom, (a, b) in essais.items()] + ["",
      "| Jour | Date | Heure | Tranche | Série | N° | Titre | État | Vues 24 h |", "|---|---|---|---|---|---|---|---|---|"]
lignes = []
for k, d in enumerate(jours):
    du_jour = [p for p in publications if p[0] == d]
    for j, (_, h, serie, num, titre, f, img, et) in enumerate(du_jour):
        md.append(f"| {k + 1} | {libelle(d)} | {h} | {tranche(h)} | {serie} | {num} | {titre} | {et} | |")
        image = f'<img src="{img}">' if img else '<div class="vide"></div>'
        lignes.append(f'''<tr class="{'fc' if serie == 'FoundClub' else ''} {'nouveau-jour' if j == 0 else ''}">
  {f'<td class="jour" rowspan="{len(du_jour)}"><b>Jour {k + 1}</b><br>{libelle(d)}</td>' if j == 0 else ''}
  <td class="heure">{h}<div class="tranche">{tranche(h)}</div></td><td>{image}</td>
  <td><span class="serie">{serie}</span><span class="num">{num}</span> {html.escape(titre)}{f'<div class="fichier">{html.escape(f)}</div>' if serie == 'FoundClub' else ''}</td>
  <td class="etat">{et}</td><td class="vues"></td></tr>''')
notes = ["Le 21 (bande-annonce AchhLife) se cale la veille ou le jour du prochain épisode ; s'il sort plus tard, décaler le jour 10.",
         "Pas encore publiable : le clip 11 (Achraf annonce « victoire 3-0 »), à garder pour quand l'épisode aura bien tourné.",
         "Avant de publier les clips 02 et 03 : faire confirmer par Achraf les noms (Lees-Melou, Marvin Martin, Balmont ; Jura Sud Foot, Haguenau, FC Les Bournes).",
         "FoundClub : le 02 (Pep Guardiola) est encore en montage. S'il n'est pas validé le 31/10, on passe la case et il prend la suivante. "
         "Ensuite, on continue tous les 2 jours (8, 10, 12 novembre…) au fil des tournages.",
         "Les heures : chaque tranche de la journée est essayée plusieurs fois. Noter les vues 24 h après chaque publication "
         "dans la dernière colonne ; au bout des 10 jours, on garde les deux tranches qui marchent le mieux."]
md += [""] + ["- " + n for n in notes]
open(RACINE / "publications/CALENDRIER.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Calendrier des publications</title><style>
@page {{ size: A4; margin: 14mm 12mm; }}
body {{ font-family: "DejaVu Sans", sans-serif; color: #141414; font-size: 10.5pt; }}
h1 {{ font-size: 18pt; margin: 0 0 4px; }} .sous {{ color: #555; margin: 0 0 10px; }}
.regles {{ background: #f4f5f8; border-left: 4px solid #e30613; padding: 8px 12px; margin: 0 0 12px; font-size: 9.5pt; }}
.regles li {{ margin: 2px 0; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: left; font-size: 9pt; color: #555; border-bottom: 2px solid #141414; padding: 4px; }}
td {{ padding: 2px 4px; vertical-align: middle; border-bottom: 1px solid #e3e3e3; }}
tr.nouveau-jour td {{ border-top: 2px solid #141414; }}
td.jour {{ width: 92px; font-size: 9.5pt; background: #fff; }} td.heure {{ width: 46px; font-weight: bold; font-size: 11pt; }}
td img, .vide {{ width: 34px; height: 46px; object-fit: cover; border-radius: 4px; display: block; }}
.vide {{ border: 1.5px dashed #9aa3ad; box-sizing: border-box; }}
.serie {{ display: inline-block; font-size: 7pt; font-weight: bold; letter-spacing: .5px; text-transform: uppercase; color: #e30613; margin-right: 6px; }}
tr.fc td:not(.jour) {{ background: #eef6fd; }} tr.fc .serie {{ color: #0a7fc2; }}
.num {{ display: inline-block; background: #141414; color: #fff; border-radius: 4px; padding: 0 5px; font-weight: bold; margin-right: 4px; }}
tr.fc .num {{ background: #0a7fc2; }}
.fichier {{ color: #888; font-size: 8pt; margin-top: 2px; }} td.etat {{ width: 130px; font-size: 9pt; }}
tr {{ page-break-inside: avoid; }}
.notes {{ margin-top: 12px; font-size: 9.5pt; }}
.tranche {{ font-size: 7pt; font-weight: normal; color: #777; }}
td.vues {{ width: 46px; }} td.vues::after {{ content: ""; display: block; height: 18px; border-bottom: 1px solid #999; }}
table.essais {{ width: auto; margin: 0 0 12px; font-size: 9pt; }} table.essais td, table.essais th {{ padding: 2px 10px 2px 0; border: 0; }}
</style></head><body>
<h1>Calendrier des publications</h1>
<p class="sous">Du jeudi 29 octobre au samedi 7 novembre 2026 · déjà publié : clip AchhLife 01 « Et si la Coupe de France était la meilleure compétition ? » (26/10)</p>
<div class="regles"><ul>
<li><b><span style="color:#e30613">AchhLife</span> — les clips « Match bourbier »</b> (épisode #42) : 2 par jour. Fichiers : <code>clips-bourbier/habillage/rendus/clip-NN-tiktok.mp4</code>. Rien qui dévoile le score avant la fin : ce qui en montre un peu (🟠) passe les derniers jours.</li>
<li><b><span style="color:#0a7fc2">FoundClub</span> — la bibliothèque des 20 scripts</b> : une vidéo tous les 2 jours, au fil des tournages d'Achraf.</li>
<li><b>Les heures changent chaque jour</b>, pour voir quand ça marche le mieux : noter les vues 24 h après chaque publication dans la dernière colonne.</li></ul></div>
<table class="essais"><tr><th>Tranche</th>{"".join(f"<th>{nom}</th>" for nom in essais)}</tr>
<tr><td>Clips AchhLife</td>{"".join(f"<td>{a} essais</td>" for a, _ in essais.values())}</tr>
<tr><td>Vidéos FoundClub</td>{"".join(f"<td>{b} essai{'s' if b > 1 else ''}</td>" for _, b in essais.values())}</tr></table>
<table><tr><th>Jour</th><th>Heure</th><th></th><th>Vidéo</th><th>État</th><th>Vues 24 h</th></tr>
{"".join(lignes)}
</table>
<div class="notes">{"".join(f"<p>{html.escape(n)}</p>" for n in notes)}</div>
</body></html>'''
open(RACINE / "publications/CALENDRIER.html", "w", encoding="utf-8").write(page)
print(essais)
print(len(publications), "publications sur", len(jours), "jours :",
      sum(p[2] == "AchhLife" for p in publications), "clips AchhLife,", sum(p[2] == "FoundClub" for p in publications), "cases FoundClub")
