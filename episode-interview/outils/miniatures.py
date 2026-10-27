"""Trois maquettes de miniature YouTube (1280×720) à partir d'images de l'épisode monté.

Images prises dans TRAVAIL/final/pieces (s04 tribune au coucher du soleil, s09 la Paillade la nuit) et dans le
premier TikTok de Moussa (2022). Texte en Oswald gras italique, blanc contour noir, accent jaune (sa couleur dans
les sous-titres). Sortie : TRAVAIL/final/miniatures/miniature-1.jpg … 3.jpg ; à choisir par Adel, rien n'est publié.

python outils/miniatures.py      (Pillow : lancer avec `python`, pas `python -I`)
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

TRAVAIL = Path(r"D:\App\video\rushs\interview\travail")
PIECES = TRAVAIL / "final" / "pieces"
SORTIE = TRAVAIL / "final" / "miniatures"
L, H = 1280, 720
POLICE = r"C:\Windows\Fonts\Oswald-BoldItalic.ttf"
JAUNE, BLANC, NOIR = (255, 212, 0), (255, 255, 255), (0, 0, 0)


def image(video, t):
    f = SORTIE / f"_{Path(video).stem}-{t}.png"
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-ss", str(t), "-i", str(video),
                    "-frames:v", "1", str(f)], check=True)
    im = Image.open(f).convert("RGB")
    f.unlink()
    return im


def cadre(im, x, y, largeur):
    """Recadre en 16:9 à partir du coin (x, y) sur une largeur donnée, puis ramène à 1280×720."""
    return im.crop((x, y, x + largeur, y + largeur * 9 // 16)).resize((L, H), Image.LANCZOS)


def texte(im, lignes, x, y, taille):
    """Lignes [(texte, couleur)] empilées à partir de (x, y)."""
    d = ImageDraw.Draw(im)
    police = ImageFont.truetype(POLICE, taille)
    for mot, couleur in lignes:
        d.text((x, y), mot, font=police, fill=couleur, stroke_width=max(4, taille // 14), stroke_fill=NOIR)
        y += round(taille * 1.08)


def punch(im):
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.25)).enhance(1.1)


SORTIE.mkdir(parents=True, exist_ok=True)

# 1. la tribune au coucher du soleil, serré sur Moussa : « DE LA D5 À LA N2 »
m1 = punch(cadre(image(PIECES / "s04.mkv", 40), 380, 200, 1100))  # à 40 s, plan serré : Moussa en x 700-1150
texte(m1, [("DE LA D5", BLANC), ("À LA N2", JAUNE)], 30, 300, 130)
m1.save(SORTIE / "miniature-1.jpg", quality=92)

# 2. la Paillade la nuit, les deux qui marchent vers la caméra : « VIRÉ CAR TROP FRÊLE »
m2 = punch(cadre(image(PIECES / "s09.mkv", 63), 0, 0, 1920))
texte(m2, [("VIRÉ CAR", BLANC), ("« TROP FRÊLE »", JAUNE)], 40, 400, 120)
m2.save(SORTIE / "miniature-2.jpg", quality=92)

# 3. avant / maintenant (retravaillée, Adel 27/10 : « DE LA D5 À LA N2 ») : son premier TikTok (2022, à 4,4 s, sans
# texte incrusté) à gauche, la tribune (2026, face caméra) à droite, coupure en biais jaune, titre en bas
P = 700  # largeur de chaque moitié ; elles se chevauchent sous la coupure en biais (de x 700 en haut à 580 en bas)
gauche = image(TRAVAIL / "tiktok" / "20220711_7119236617642069253.mp4", 4.4).crop((0, 40, 345, 40 + 355))
gauche = gauche.resize((P, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80))
droite = image(PIECES / "s05.mkv", 60).crop((362, 160, 362 + P, 160 + H))
m3 = Image.new("RGB", (L, H))
m3.paste(punch(droite), (L - P, 0))
biais = Image.new("L", (L, H))
ImageDraw.Draw(biais).polygon([(0, 0), (P, 0), (L - P, H), (0, H)], fill=255)
m3.paste(punch(gauche), (0, 0), biais.crop((0, 0, P, H)))
d3 = ImageDraw.Draw(m3)
d3.line([(P, 0), (L - P, H)], fill=JAUNE, width=12)
fond = Image.new("RGBA", (L, H))
for y in range(400, H):  # dégradé noir sous le titre
    ImageDraw.Draw(fond).line([(0, y), (L, y)], fill=(0, 0, 0, round(215 * (y - 400) / (H - 400))))
m3 = Image.alpha_composite(m3.convert("RGBA"), fond).convert("RGB")
d3 = ImageDraw.Draw(m3)
annee = ImageFont.truetype(POLICE, 64)
for x, mot in ((34, "2022"), (L - 34 - annee.getbbox("2026")[2] - 28, "2026")):
    d3.rectangle((x, 30, x + annee.getbbox(mot)[2] + 28, 30 + 86), fill=JAUNE)
    d3.text((x + 14, 30 + 43), mot, font=annee, fill=NOIR, anchor="lm")
titre = ImageFont.truetype(POLICE, 128)
blanc, jaune = "DE LA D5 ", "À LA N2"
x = (L - titre.getbbox(blanc + jaune)[2]) // 2
for mot, couleur in ((blanc, BLANC), (jaune, JAUNE)):
    d3.text((x, 640), mot, font=titre, fill=couleur, anchor="ls", stroke_width=8, stroke_fill=NOIR)
    x += titre.getlength(mot)
m3.save(SORTIE / "miniature-3.jpg", quality=92)
print("miniatures :", ", ".join(sorted(f.name for f in SORTIE.glob("miniature-*.jpg"))))
