"""Fabrique l'habillage de l'épisode dans le style de l'épisode #42 (images transparentes et petites vidéos).

- habillage/carte-saison.mp4 : la carte « SAISON 3 / EPISODE 5 » ; le fond (cercles, trait) est celui du #42
  (10:09.6–10:12.0), le texte est refait par-dessus. PROVISOIRE tant qu'Achraf n'a pas envoyé son fichier.
- habillage/logo-provisoire.mp4 : la neige télé puis le logo AchhLife du #42 (10:01.2 et 10:08.9), tels quels.
- habillage/bandeau-<n>.png : bandeau de nom (deux cadres blancs, texte noir), comme « BEN ALI Mahfoud » du #42.
- habillage/dans-cet-episode.png : « Dans cet épisode.. » en bas à droite, comme « Dans l'épisode précédent.. ».

python outils/habillage.py      (Pillow : lancer avec `python`, pas `python -I`)
"""
import json
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = Path(__file__).resolve().parents[1]
TRAVAIL = Path(r"D:\App\video\rushs\interview\travail")
SORTIE = TRAVAIL / "habillage"
EP42 = TRAVAIL / "reference" / "episode-42.mp4"
POLICES = Path(r"C:\Windows\Fonts")
L, H = 1920, 1080
SAISON, EPISODE = 3, 5


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *args], check=True)


def ligne_titre(texte, largeur, hauteur):
    """Une ligne de la carte : blanc, contour bleu nuit, halo turquoise, police large (Bahnschrift étirée)."""
    police = ImageFont.truetype(str(POLICES / "bahnschrift.ttf"), 160)
    police.set_variation_by_name("Bold")
    x0, y0, x1, y1 = police.getbbox(texte, stroke_width=8)
    marge = 40
    calque = Image.new("RGBA", (x1 - x0 + 2 * marge, y1 - y0 + 2 * marge))
    halo = calque.copy()
    ImageDraw.Draw(halo).text((marge - x0, marge - y0), texte, font=police, fill=(60, 200, 230, 255),
                              stroke_width=16, stroke_fill=(60, 200, 230, 255))
    calque.alpha_composite(halo.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(calque).text((marge - x0, marge - y0), texte, font=police, fill=(240, 250, 255, 255),
                                stroke_width=8, stroke_fill=(12, 52, 92, 255))
    m = round(marge * largeur / (x1 - x0))
    return calque.resize((largeur + 2 * m, hauteur + 2 * marge))


def carte_saison():
    trames = SORTIE / "carte-trames"
    trames.mkdir(parents=True, exist_ok=True)
    ffmpeg("-ss", "609.6", "-t", "2.4", "-i", str(EP42), "-vf", "fps=30", str(trames / "%03d.png"))
    # emplacement et taille des deux lignes du #42 (mesurés sur la trame de 10:11.0)
    l1 = ligne_titre(f"SAISON {SAISON}", 1035, 108)
    l2 = ligne_titre(f"EPISODE {EPISODE}", 1140, 112)
    hasard = random.Random(5)
    fichiers = sorted(trames.glob("*.png"))
    for i, f in enumerate(fichiers):
        t = i / 30
        im = Image.open(f).convert("RGBA")
        if t >= 0.12:  # le #42 commence à écrire « SAISON 3 » à 10:09.7 : on efface son texte dès là
            masque = Image.new("L", (L, H))
            ImageDraw.Draw(masque).rectangle((380, 378, 1554, 698), fill=255)
            im.paste((0, 0, 0, 255), mask=masque.filter(ImageFilter.GaussianBlur(5)))
            trait = Image.new("RGBA", (L, H))
            ImageDraw.Draw(trait).line((376, 555, 1558, 555), fill=(140, 235, 235, 255), width=4)
            im.alpha_composite(trait.filter(ImageFilter.GaussianBlur(3)))
            im.alpha_composite(trait)
        if t >= 0.25:
            texte = Image.new("RGBA", (L, H))
            texte.alpha_composite(l1, ((L - l1.width) // 2, 452 - l1.height // 2))
            texte.alpha_composite(l2, ((L - l2.width) // 2, 612 - l2.height // 2))
            if t < 0.85:  # apparition en glitch, comme le #42 : bandes décalées et couleurs séparées
                glitch = Image.new("RGBA", (L, H))
                y = 370
                while y < 700:
                    h = hasard.randint(8, 40)
                    bande = texte.crop((0, y, L, y + h))
                    glitch.alpha_composite(bande, (hasard.randint(-60, 60) if hasard.random() < 0.6 else 0, y))
                    y += h
                r, g, b, a = glitch.split()
                texte = Image.merge("RGBA", (r, g, b, a))
                decale = Image.merge("RGBA", (r, Image.new("L", (L, H)), Image.new("L", (L, H)), a))
                im.alpha_composite(decale, (-8, 0))
            im.alpha_composite(texte)
        im.convert("RGB").save(f)
    ffmpeg("-framerate", "30", "-i", str(trames / "%03d.png"), "-ss", "609.6", "-t", "2.4", "-i", str(EP42),
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac",
           "-b:a", "192k", "-shortest", str(SORTIE / "carte-saison.mp4"))


def logo_provisoire():
    ffmpeg("-i", str(EP42), "-filter_complex",
           "[0:v]trim=601.2:602.8,setpts=PTS-STARTPTS[g];[0:v]trim=608.9:609.6,setpts=PTS-STARTPTS,"
           "tpad=stop_mode=clone:stop_duration=0.7,fade=t=out:st=0.9:d=0.5[l];[g][l]concat=n=2:v=1:a=0[v];"
           "[0:a]atrim=601.2:602.8,asetpts=PTS-STARTPTS[ga];[0:a]atrim=608.9:610.3,asetpts=PTS-STARTPTS,"
           "afade=t=out:st=0.9:d=0.5[la];[ga][la]concat=n=2:v=0:a=1[a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac",
           "-b:a", "192k", str(SORTIE / "logo-provisoire.mp4"))


def bandeau(lignes, nom):
    """Deux cadres blancs en bas à gauche, texte noir gras (mesuré sur le bandeau du #42 : x 198, y 892 et 962)."""
    im = Image.new("RGBA", (L, H))
    d = ImageDraw.Draw(im)
    for (texte, y, taille) in ((lignes[0], 892, 52), (lignes[1], 962, 50)):
        police = ImageFont.truetype(str(POLICES / "segoeuib.ttf"), taille)
        x0, _, x1, _ = police.getbbox(texte)
        d.rectangle((198, y, 198 + (x1 - x0) + 28, y + 64), fill=(255, 255, 255, 255))
        d.text((198 + 14 - x0, y + 32), texte, font=police, fill=(0, 0, 0, 255), anchor="lm")
    im.save(SORTIE / f"bandeau-{nom}.png")


def dans_cet_episode():
    im = Image.new("RGBA", (L, H))
    police = ImageFont.truetype(str(POLICES / "Oswald-BoldItalic.ttf"), 54)
    ImageDraw.Draw(im).text((1892, 1050), "Dans cet épisode..", font=police, fill=(255, 255, 255, 255),
                            anchor="rs", stroke_width=3, stroke_fill=(0, 0, 0, 255))
    im.save(SORTIE / "dans-cet-episode.png")


SORTIE.mkdir(parents=True, exist_ok=True)
carte_saison()
logo_provisoire()
dans_cet_episode()
papier = json.loads((ICI / "papier.json").read_text(encoding="utf-8"))
for seq in papier["sequences"]:
    for p in seq["paroles"]:
        if p.get("bandeau"):
            bandeau(p["bandeau"]["lignes"], p["bandeau"]["nom"])
print("habillage :", ", ".join(sorted(f.name for f in SORTIE.glob("*.*"))))
