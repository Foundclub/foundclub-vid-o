"""Refait bibliotheque-20-scripts-suivi.pdf : le PDF d'origine (bibliotheque-20-scripts.pdf, jamais modifié) avec une page
de suivi en tête, une pastille d'état devant chaque ligne de la liste des 20 vidéos et un bandeau d'état sur la page de
chaque script. L'état vient de suivi.json (« fait », « en cours », ou rien = à tourner).
Usage : python3 -I scripts-foundclub/outils/suivi.py   (depuis la racine du dépôt)"""
import io, json, datetime
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit

ICI = Path(__file__).resolve().parent.parent
TITRES = ["Un mois sans toucher un ballon... en match", "Les Pep Guardiola du dimanche", "Le week-end gâché",
          "Frérot, je suis pas Kimmich", "Le match annulé à la dernière minute", "J'attends la convocation pour organiser ma vie",
          "La trêve qui n'en finit pas", "Le sélectionneur de district", "Coach : personne ne répond", "Éliminés de la coupe, et alors ?",
          "Sois pas bête : c'est les vacances !", "La fausse question Instagram", "Coach, arrête de galérer", "Marre de chercher des matchs ?",
          "Vacances de Toussaint : on joue !", "Tu savais que ça existait ?", "Avant / après FoundClub", "Je réponds à ton commentaire",
          "Trouver un match en trois étapes", "Aucun match ? Publie le tien"]
CONVOCATION = {2, 4, 6, 8}
ETATS = {"fait": ("FAIT", HexColor("#1fae6b")), "en cours": ("EN COURS", HexColor("#f2a516"))}
A_FAIRE = ("À TOURNER", HexColor("#9aa3ad"))
NUIT, GRIS = HexColor("#0c1b2e"), HexColor("#5b6470")
W, H = 595.2756, 841.8898

suivi = json.load(open(ICI / "suivi.json", encoding="utf-8"))
etat = lambda n: suivi.get(f"{n:02d}", {})
pastille = lambda n: ETATS.get(etat(n).get("etat"), A_FAIRE)

def coche(c, x, y, r, couleur, plein):
    """Rond de couleur ; coché s'il est fait, demi-plein s'il est en cours, vide sinon."""
    c.setStrokeColor(couleur); c.setLineWidth(1.6)
    if plein == "fait":
        c.setFillColor(couleur); c.circle(x, y, r, stroke=0, fill=1)
        c.setStrokeColor(white); c.setLineWidth(1.8); c.setLineCap(1); c.setLineJoin(1)
        p = c.beginPath(); p.moveTo(x - r * .5, y); p.lineTo(x - r * .12, y - r * .42); p.lineTo(x + r * .55, y + r * .42); c.drawPath(p, stroke=1, fill=0)
    elif plein == "en cours":
        c.circle(x, y, r, stroke=1, fill=0); c.setFillColor(couleur); c.wedge(x - r, y - r, x + r, y + r, 90, 180, stroke=0, fill=1)
    else:
        c.circle(x, y, r, stroke=1, fill=0)

def calque(dessin):
    tampon = io.BytesIO(); c = canvas.Canvas(tampon, pagesize=(W, H)); dessin(c); c.save(); tampon.seek(0)
    return PdfReader(tampon).pages[0]

def page_suivi(c):
    c.setFillColor(NUIT); c.rect(0, H - 64, W, 64, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 13); c.drawString(42, H - 38, "FOUNDCLUB")
    c.setFont("Helvetica", 8.5); c.drawRightString(W - 42, H - 38, "SUIVI DES TOURNAGES")
    c.setFillColor(NUIT); c.setFont("Helvetica-Bold", 22); c.drawString(42, H - 112, "Suivi des 20 vidéos")
    faits = sum(1 for n in range(1, 21) if etat(n).get("etat") == "fait")
    en_cours = sum(1 for n in range(1, 21) if etat(n).get("etat") == "en cours")
    c.setFillColor(GRIS); c.setFont("Helvetica", 10)
    c.drawString(42, H - 132, f"{faits} faite(s) · {en_cours} en cours · {20 - faits - en_cours} à tourner — mis à jour le {datetime.date.today():%d/%m/%Y}")
    y = H - 160
    c.setFont("Helvetica-Bold", 8); c.setFillColor(GRIS)
    for x, t in ((42, "N°"), (70, "VIDÉO"), (300, "ÉTAT"), (372, "DÉTAIL")): c.drawString(x, y, t)
    y -= 8; c.setStrokeColor(HexColor("#d9dee4")); c.setLineWidth(.6)
    for n in range(1, 21):
        e = etat(n); lib, coul = pastille(n)
        c.setStrokeColor(HexColor("#d9dee4")); c.setLineWidth(.6); c.line(42, y, W - 42, y); y -= 15
        c.setFillColor(NUIT); c.setFont("Helvetica-Bold", 10); c.drawString(42, y, f"{n:02d}")
        c.setFont("Helvetica", 10); c.drawString(70, y, simpleSplit(TITRES[n - 1], "Helvetica", 10, 222)[0])
        c.setFont("Helvetica", 7); c.setFillColor(GRIS); c.drawString(70, y - 10, "CONVOCATION" if n in CONVOCATION else "AMICAL")
        coche(c, 306, y + 3, 5, coul, e.get("etat")); c.setFillColor(coul); c.setFont("Helvetica-Bold", 8.5); c.drawString(316, y, lib)
        c.setFillColor(GRIS); c.setFont("Helvetica", 7.5)
        texte = " · ".join(x for x in (e.get("date", ""), e.get("detail", "")) if x)
        if texte: c.drawString(372, y, simpleSplit(texte, "Helvetica", 7.5, W - 42 - 372)[0])
        if e.get("fichier"): c.setFont("Helvetica", 6.5); c.drawString(372, y - 10, simpleSplit(e["fichier"], "Helvetica", 6.5, W - 42 - 372)[0])
        y -= 14
    c.line(42, y, W - 42, y)
    c.setFont("Helvetica", 7.5); c.setFillColor(GRIS)
    c.drawString(42, 40, "Les pages suivantes sont la bibliothèque d'origine ; l'état de chaque script est rappelé en haut de sa page.")

def marques_liste(c):   # devant chaque ligne de « Ordre des 20 vidéos » (page 2 du PDF d'origine)
    for n in range(1, 21):
        y = H - (206.9 + 25 * (n - 1) + 5); coche(c, 44, y, 6, pastille(n)[1], etat(n).get("etat"))

def bandeau(n):
    def dessin(c):
        e = etat(n); lib, coul = pastille(n)
        texte = lib + (f"  ·  {e['date']}" if e.get("date") else "") + (f"  ·  {e['detail']}" if e.get("detail") else "")
        c.setFillColor(coul); c.roundRect(58, H - 92, W - 116, 20, 5, stroke=0, fill=1)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 8.5); c.drawString(68, H - 85, simpleSplit(texte, "Helvetica-Bold", 8.5, W - 136)[0])
    return dessin

origine = PdfReader(ICI / "bibliotheque-20-scripts.pdf")
sortie = PdfWriter()
sortie.add_page(calque(page_suivi))
for i, page in enumerate(origine.pages):
    if i == 1: page.merge_page(calque(marques_liste))
    if 2 <= i <= 21: page.merge_page(calque(bandeau(i - 1)))   # la vidéo N est à la page N + 2
    sortie.add_page(page)
with open(ICI / "bibliotheque-20-scripts-suivi.pdf", "wb") as f: sortie.write(f)
print(f"bibliotheque-20-scripts-suivi.pdf : {len(sortie.pages)} pages ;",
      ", ".join(f"{k} {v['etat']}" for k, v in sorted(suivi.items()) if not k.startswith("_")))
