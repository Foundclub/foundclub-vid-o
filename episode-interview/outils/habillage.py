"""Fabrique l'habillage de l'épisode dans le style de l'épisode #42 (images transparentes et petites vidéos).

- habillage/carte-saison.mp4 : la carte « SAISON 3 / EPISODE 5 » ; le fond (cercles, trait) est celui du #42
  (10:09.6–10:12.0), le texte est refait par-dessus. PROVISOIRE tant qu'Achraf n'a pas envoyé son fichier.
- habillage/logo-provisoire.mp4 : la neige télé puis le logo AchhLife du #42 (10:01.2 et 10:08.9), tels quels.
- habillage/bandeau-<n>.png : bandeau de nom (deux cadres blancs, texte noir), comme « BEN ALI Mahfoud » du #42.
- habillage/dans-cet-episode.png : « Dans cet épisode.. » en bas à droite, comme « Dans l'épisode précédent.. ».
- habillage/abonne-1.png, abonne-2.png : le pop-up « like / abonné » du #42, redessiné avec la photo d'achh10.
- habillage/bandeau-reseaux-moussa.png : ses comptes, avec les icônes du carton de fin du #42.

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


def reseaux(comptes, nom):
    """Bandeau des réseaux : les icônes du carton de fin du #42 (22:04) et le compte, sur un cadre noir en bas à gauche."""
    fin42 = SORTIE / "_fin42.png"
    ffmpeg("-ss", "1324", "-i", str(EP42), "-frames:v", "1", str(fin42))
    icones = {"tiktok": (128, 683, 220, 780), "snapchat": (1532, 686, 1628, 782)}  # mesurés sur cette image
    source = Image.open(fin42).convert("RGBA")
    police = ImageFont.truetype(str(POLICES / "segoeuib.ttf"), 50)
    largeurs = [96 + 18 + police.getbbox(c)[2] for _, c in comptes]
    im = Image.new("RGBA", (L, H))
    d = ImageDraw.Draw(im)
    x, y = 198, 900
    d.rounded_rectangle((x, y, x + sum(largeurs) + 56 * len(comptes), y + 124), 18, fill=(0, 0, 0, 225))
    x += 28
    for (reseau, compte), w in zip(comptes, largeurs):
        icone = source.crop(icones[reseau]).resize((96, 96))
        im.alpha_composite(icone, (x, y + 14))
        d.text((x + 96 + 18, y + 62), compte, font=police, fill=(255, 255, 255, 255), anchor="lm")
        x += w + 56
    im.save(SORTIE / f"bandeau-{nom}.png")
    fin42.unlink()


def abonne():
    """Pop-up « like / abonné » du #42, redessiné : cadre blanc liseré d'or en bas au centre, photo d'achh10,
    pouce, pouce baissé, bouton, cloche ; abonne-1 = « S'ABONNER » en rouge, abonne-2 = aimé et « ABONNÉ »."""
    icones = ImageFont.truetype(str(POLICES / "segmdl2.ttf"), 64)
    texte = ImageFont.truetype(str(POLICES / "segoeuib.ttf"), 34)
    profil = Image.open(ICI.parent / "clips-bourbier" / "habillage" / "medias" / "profil-achh10.jpg").convert("RGBA")
    profil = profil.resize((104, 104))
    rond = Image.new("L", (104, 104))
    ImageDraw.Draw(rond).ellipse((0, 0, 103, 103), fill=255)
    x0, y0, x1, y1 = 560, 878, 1360, 1028
    for etat in (1, 2):
        im = Image.new("RGBA", (L, H))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((x0, y0, x1, y1), 22, fill=(255, 255, 255, 255), outline=(222, 184, 70, 255), width=5)
        im.paste(profil, (x0 + 28, y0 + 23), rond)
        aime = (20, 20, 20, 255) if etat == 2 else (120, 120, 120, 255)
        d.text((x0 + 215, y0 + 75), "", font=icones, fill=aime, anchor="mm")
        if etat == 2:
            d.rectangle((x0 + 175, y0 + 118, x0 + 255, y0 + 124), fill=(20, 20, 20, 255))
        d.text((x0 + 315, y0 + 75), "", font=icones, fill=(120, 120, 120, 255), anchor="mm")
        bouton, couleur, ecrit = (x0 + 390, y0 + 45, x0 + 660, y0 + 105), *(
            ((204, 0, 0, 255), (255, 255, 255, 255)) if etat == 1 else ((228, 228, 228, 255), (96, 96, 96, 255)))
        d.rounded_rectangle(bouton, 8, fill=couleur)
        d.text(((bouton[0] + bouton[2]) / 2, y0 + 75), "S'ABONNER" if etat == 1 else "ABONNÉ", font=texte,
               fill=ecrit, anchor="mm")
        d.text((x0 + 730, y0 + 75), "", font=icones, fill=(20, 20, 20, 255), anchor="mm")
        im.save(SORTIE / f"abonne-{etat}.png")


SORTIE.mkdir(parents=True, exist_ok=True)
carte_saison()
logo_provisoire()
dans_cet_episode()
abonne()
reseaux([("tiktok", "moussaldz34"), ("snapchat", "moussa.arim")], "reseaux-moussa")
papier = json.loads((ICI / "papier.json").read_text(encoding="utf-8"))
for seq in papier["sequences"]:
    for p in seq["paroles"]:
        if p.get("bandeau", {}).get("lignes"):  # « reseaux-moussa » est fait plus haut
            bandeau(p["bandeau"]["lignes"], p["bandeau"]["nom"])
print("habillage :", ", ".join(sorted(f.name for f in SORTIE.glob("*.*"))))
