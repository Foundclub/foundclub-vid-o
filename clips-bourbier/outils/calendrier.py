"""Écrit le calendrier de publication des clips « Match bourbier » : CALENDRIER.md et CALENDRIER.html (rendu en PDF
par outils/pdf.mjs), avec une vignette de chaque clip tirée de son rendu final.
Ordre décidé avec Adel le 26/10/2026 : rien qui dévoile le score avant la fin, au moins 2 clips par jour ; le 01 a été
publié par Achraf le 26/10, l'ancien jour 4 devient le jour 1.
Usage : python3 -I outils/calendrier.py   (depuis clips-bourbier/)"""
import datetime as dt, subprocess, os, html

DEBUT = dt.date(2026, 10, 26)
HEURES = {"semaine": ("12:30", "19:00"), "week-end": ("11:30", "18:00")}
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
ORDRE = [(1, 14), (4, 7), (2, 15), (3, 13), (6, 20), (12, 8), (5, 18), (16, 17), (10, 19), (9, 21)]
PUBLIE = {1}

os.makedirs("calendrier", exist_ok=True)
for jour in ORDRE:
    for n in jour:   # vignette : l'accroche et l'image, à 2 s du rendu final
        sortie = f"calendrier/clip-{n:02d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.0", "-i", f"habillage/rendus/clip-{n:02d}-tiktok.mp4", "-frames:v", "1",
                        "-vf", "crop=1080:1500:0:120,scale=160:-2", "-q:v", "3", sortie], check=True)
lignes, md = [], ["# Calendrier de publication — clips « Match bourbier » (épisode #42)", "",
                  "Au moins 2 clips par jour. Rien qui dévoile le score avant la fin : ce qui en montre un peu est publié les derniers jours.",
                  "Heures : 12:30 et 19:00 en semaine, 11:30 et 18:00 le week-end.", "",
                  "| Jour | Date | Heure | Clip | Titre | Spoil |", "|---|---|---|---|---|---|"]
for i, jour in enumerate(ORDRE):
    date = DEBUT + dt.timedelta(i)
    heures = HEURES["week-end" if date.weekday() >= 5 else "semaine"]
    if i == 0: heures = ("publié", "19:00")
    libelle = f"{JOURS_FR[date.weekday()].capitalize()} {date.day} {MOIS_FR[date.month]}"
    for k, (n, h) in enumerate(zip(jour, heures)):
        statut = "✅ publié par Achraf" if n in PUBLIE else ""
        spoil = SPOIL.get(n, "")
        md.append(f"| {i + 1} | {libelle} | {h} | {n:02d} | {TITRES[n]} | {spoil or '—'} |")
        lignes.append(f'''<tr class="{'fait' if n in PUBLIE else ''} {'nouveau-jour' if k == 0 else ''}">
  {'<td class="jour" rowspan="2"><b>Jour ' + str(i + 1) + '</b><br>' + libelle + '</td>' if k == 0 else ''}
  <td class="heure">{h}</td><td><img src="calendrier/clip-{n:02d}.jpg"></td>
  <td><span class="num">{n:02d}</span> {html.escape(TITRES[n])}<div class="fichier">clip-{n:02d}-tiktok.mp4</div></td>
  <td class="etat">{statut or (('🟠 ' + spoil) if spoil else '🟢 aucun')}</td></tr>''')
md += ["", "Le 21 (bande-annonce) se cale la veille ou le jour du prochain épisode ; s'il sort plus tard, décaler le jour 10.",
       "Pas encore publiable : le 11 (Achraf annonce « victoire 3-0 »), à garder pour quand l'épisode aura bien tourné.",
       "Avant de publier le 02 et le 03 : faire confirmer par Achraf les noms des joueurs et des clubs."]
open("CALENDRIER.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Calendrier des clips</title><style>
@page {{ size: A4; margin: 14mm 12mm; }}
body {{ font-family: "DejaVu Sans", sans-serif; color: #141414; font-size: 10.5pt; }}
h1 {{ font-size: 18pt; margin: 0 0 4px; }} .sous {{ color: #555; margin: 0 0 10px; }}
.regles {{ background: #f4f5f8; border-left: 4px solid #e30613; padding: 8px 12px; margin: 0 0 12px; font-size: 9.5pt; }}
.regles li {{ margin: 2px 0; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: left; font-size: 9pt; color: #555; border-bottom: 2px solid #141414; padding: 4px; }}
td {{ padding: 4px; vertical-align: middle; border-bottom: 1px solid #e3e3e3; }}
tr.nouveau-jour td {{ border-top: 2px solid #141414; }}
td.jour {{ width: 92px; font-size: 9.5pt; }} td.heure {{ width: 46px; font-weight: bold; font-size: 11pt; }}
td img {{ width: 52px; border-radius: 4px; display: block; }}
.num {{ display: inline-block; background: #141414; color: #fff; border-radius: 4px; padding: 0 5px; font-weight: bold; margin-right: 4px; }}
.fichier {{ color: #888; font-size: 8pt; margin-top: 2px; }} td.etat {{ width: 120px; font-size: 9pt; }}
tr.fait td {{ color: #888; }} tr {{ page-break-inside: avoid; }}
.notes {{ margin-top: 12px; font-size: 9.5pt; }}
</style></head><body>
<h1>Calendrier des clips — « Match bourbier »</h1>
<p class="sous">Épisode #42 « Match piège pour notre entrée en Coupe de France ! » · AchhLife saison 3 · du lundi 26 octobre au mercredi 4 novembre 2026</p>
<div class="regles"><ul>
<li><b>Au moins 2 clips par jour</b> : 12:30 et 19:00 en semaine, 11:30 et 18:00 le week-end.</li>
<li><b>Rien qui dévoile le score avant la fin</b> : le tableau d'affichage est flouté sur les clips de match, les buts n'ont plus de score, ce qui en montre un peu (🟠) passe les derniers jours.</li>
<li>Chaque jour, une histoire d'Achraf et un moment du match.</li></ul></div>
<table><tr><th>Jour</th><th>Heure</th><th></th><th>Clip</th><th>Spoil</th></tr>
{"".join(lignes)}
</table>
<div class="notes"><p><b>Le 21</b> (bande-annonce) se cale la veille ou le jour du prochain épisode ; s'il sort plus tard, décaler le jour 10.</p>
<p><b>Pas encore publiable</b> : le 11 (Achraf annonce « victoire 3-0 »), à garder pour quand l'épisode aura bien tourné.</p>
<p><b>Avant de publier le 02 et le 03</b> : faire confirmer par Achraf les noms (Lees-Melou, Marvin Martin, Balmont ; Jura Sud Foot, Haguenau, FC Les Bournes).</p>
<p>Les fichiers : <code>clips-bourbier/habillage/rendus/clip-NN-tiktok.mp4</code></p></div>
</body></html>'''
open("CALENDRIER.html", "w", encoding="utf-8").write(page)
print(len(lignes), "publications sur", len(ORDRE), "jours")
