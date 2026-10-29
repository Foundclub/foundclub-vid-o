"""Sound design : fabrique les bruitages (synthétisés, aucun fichier tiers, aucun droit) et les pose aux
instants listés dans sons.json, en une seule piste medias/sons/sons.wav que la composition joue sous la voix.
Usage : python3 -I outils/sons.py [sons.json] [sortie.wav] [durée en s]
sons.json : [{"t": 1.22, "son": "swish", "db": 0, "note": 0, "pan": 0}, …] — db : réglage fin du niveau,
note : demi-tons (pour les suites de pops qui montent), pan : -1 gauche … +1 droite."""
import sys, json
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from wav import ecrire

SR = 48000
rng = np.random.default_rng(10102026)          # graine fixe : la piste est la même à chaque fabrication
t_ = lambda d: np.arange(int(d * SR)) / SR

def bruit(d):
    return rng.standard_normal(int(d * SR))

def bande(x, f_debut, f_fin, largeur=0.9):
    """Filtre passe-bande dont le centre glisse de f_debut à f_fin (Hz), largeur en octaves."""
    n, hop = 1024, 256
    fen = np.hanning(n); pad = np.r_[np.zeros(n), x, np.zeros(n)]
    out = np.zeros_like(pad); norme = np.zeros_like(pad)
    fq = np.fft.rfftfreq(n, 1 / SR); nb = 1 + (len(pad) - n) // hop
    for k in range(nb):
        i = k * hop; r = min(1, max(0, (i - n) / max(1, len(x))))
        fc = f_debut * (f_fin / f_debut) ** r
        g = np.exp(-0.5 * (np.log2(np.maximum(fq, 1) / fc) / (largeur / 2)) ** 2)
        out[i:i + n] += np.fft.irfft(np.fft.rfft(pad[i:i + n] * fen) * g, n) * fen
        norme[i:i + n] += fen ** 2
    return (out / np.maximum(norme, 1e-6))[n:n + len(x)]

def enveloppe(n, pic=0.6, montee=2.0, descente=2.0):
    u = np.linspace(0, 1, n)
    return np.where(u < pic, (u / pic) ** montee, ((1 - u) / (1 - pic)) ** descente)

def stereo(x, pan=0.0, balayage=0.0):
    """pan fixe (-1 … 1) plus un balayage gauche -> droite pendant le son."""
    p = np.clip(pan + balayage * np.linspace(-1, 1, len(x)), -1, 1)
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1)

def reverb(x, duree=0.45, mix=0.18):
    ir_t = t_(duree); ir = np.stack([rng.standard_normal(len(ir_t)), rng.standard_normal(len(ir_t))], 1)
    ir *= np.exp(-ir_t / (duree / 6))[:, None]; ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([np.convolve(x[:, c], ir[:, c]) for c in range(2)], 1)
    x2 = np.r_[x, np.zeros((len(y) - len(x), 2))]
    return x2 * (1 - mix) + y * mix

def normer(x):
    return x / (np.abs(x).max() + 1e-12)

def sinus_glisse(f_debut, f_fin, d, courbe=0.02):
    t = t_(d); f = f_fin + (f_debut - f_fin) * np.exp(-t / courbe)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ---- la bibliothèque ----
def whoosh(d=0.6, f0=250, f1=3500, pic=0.65, balayage=0.6):      # transition, gros mouvement
    x = bande(bruit(d), f0, f1, 1.1) * enveloppe(int(d * SR), pic, 2.2, 1.6)
    return reverb(stereo(normer(x), 0, balayage), 0.5, 0.15)
def swish(d=0.24):                                                  # texte qui entre
    return whoosh(d, 900, 5000, 0.7, 0.35)
def souffle(d=0.4):                                                 # sortie : le mouvement retombe
    x = bande(bruit(d), 3000, 400, 1.0) * enveloppe(int(d * SR), 0.25, 1.5, 2.5)
    return reverb(stereo(normer(x), 0, -0.4), 0.4, 0.12)
def zip_(d=0.26):                                                   # surligneur qui se déroule
    x = bande(bruit(d), 700, 6000, 0.7) * enveloppe(int(d * SR), 0.85, 1.4, 1.0)
    ton = np.sin(2 * np.pi * np.cumsum(np.linspace(600, 2400, int(d * SR))) / SR)
    x = normer(x) + 0.12 * ton * enveloppe(int(d * SR), 0.85, 1.4, 1.0)
    return reverb(stereo(normer(x), 0, 0.5), 0.3, 0.1)
def pop(note=0, d=0.12):                                            # bulle, étiquette, pastille
    f = 620 * 2 ** (note / 12); t = t_(d)
    x = sinus_glisse(f * 2.2, f, d, 0.012) * np.exp(-t / 0.035)
    x[:96] += np.hanning(192)[96:] * rng.standard_normal(96) * 0.3   # attaque
    return reverb(stereo(normer(x)), 0.35, 0.16)
def bulle(note=0):                                                  # message reçu (deux notes)
    f = 1046 * 2 ** (note / 12); t = t_(0.07)
    a = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.025)
    b = np.sin(2 * np.pi * f * 1.335 * t) * np.exp(-t / 0.04)
    x = np.r_[a, np.zeros(int(0.012 * SR)), b, np.zeros(int(0.02 * SR))]
    return reverb(stereo(normer(x)), 0.4, 0.2)
def tick(d=0.04):                                                   # l'écran du téléphone change
    t = t_(d); x = np.sin(2 * np.pi * 3800 * t) * np.exp(-t / 0.006) + 0.5 * bande(bruit(d), 6000, 6000, 1.5) * np.exp(-t / 0.004)
    return reverb(stereo(normer(x)), 0.2, 0.08)
def tap(d=0.09):                                                    # doigt qui appuie
    t = t_(d); x = sinus_glisse(420, 160, d, 0.01) * np.exp(-t / 0.018) + 0.4 * bande(bruit(d), 2500, 1200, 1.2) * np.exp(-t / 0.005)
    return reverb(stereo(normer(x)), 0.25, 0.1)
def impact(d=0.9):                                                  # logo, mot-choc
    t = t_(d)
    grave = np.tanh(2.2 * sinus_glisse(120, 42, d, 0.05) * np.exp(-t / 0.22))
    claque = bande(bruit(d), 1800, 300, 2.0) * np.exp(-t / 0.035)
    x = normer(grave) + 0.55 * normer(claque)
    return reverb(stereo(normer(x)), 0.9, 0.22)
def scintille(d=0.9):                                               # reflet qui balaie le logo
    t = t_(d); x = np.zeros_like(t)
    for k, f in enumerate([2637, 3136, 3951, 4699, 5274, 6272]):
        dep = int(k * 0.07 * SR); tt = t[:len(t) - dep]
        x[dep:] += np.sin(2 * np.pi * f * tt * (1 + 0.002 * np.sin(2 * np.pi * 7 * tt))) * np.exp(-tt / 0.18) / (1 + 0.3 * k)
    return reverb(stereo(normer(x), 0, 0.7), 0.8, 0.3)
def montee(d=0.9):                                                  # ça va arriver (avant un impact)
    n = int(d * SR); env = np.linspace(0, 1, n) ** 2.5
    x = normer(bande(bruit(d), 300, 6000, 1.0)) * env + 0.3 * np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 720, n)) / SR) * env
    x[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return stereo(normer(x), 0, 0.4)                                # sans réverbération : elle finit pile sur l'impact
def coupe(d=0.14):                                                  # changement de plan (saut de cadre)
    t = t_(d); x = 0.7 * normer(bande(bruit(d), 2500, 900, 1.0) * enveloppe(len(t), 0.2, 1.0, 2.0)) + normer(sinus_glisse(160, 70, d, 0.02) * np.exp(-t / 0.03))
    return reverb(stereo(normer(x)), 0.3, 0.12)
def choix(note=0):                                                  # bonne réponse au sondage
    f = 784 * 2 ** (note / 12); t = t_(0.09); seg = lambda f: np.sin(2 * np.pi * f * t) * np.exp(-t / 0.05)
    x = np.r_[seg(f), seg(f * 1.5), np.zeros(int(0.1 * SR))]
    return reverb(stereo(normer(x)), 0.6, 0.25)
def secousse(d=0.32):                                               # le texte tremble
    t = t_(d); x = bande(bruit(d), 160, 120, 1.2) * (0.6 + 0.4 * np.sin(2 * np.pi * 22 * t)) * enveloppe(len(t), 0.1, 1.0, 1.4)
    return reverb(stereo(normer(x)), 0.3, 0.1)

# ---- sons ajoutés pour « Le week-end gâché » (28/10/2026) : Adel trouvait les mêmes pops et whooshs partout trop « IA ».
# Peu de sons, et seulement des bruits du monde réel : un tampon, un sticker, une vibration, un clic, une bande qui s'arrête.
def tampon(d=0.28):                                                 # tampon encreur qui s'écrase sur le papier
    t = t_(d); coup = sinus_glisse(110, 48, d, 0.03) * np.exp(-t / 0.05)
    bois = bande(bruit(d), 700, 380, 1.4) * np.exp(-t / 0.018)
    return reverb(stereo(normer(coup + 0.55 * normer(bois))), 0.25, 0.08)
def sticker(d=0.09):                                                # autocollant plaqué : un claquement de papier, sec
    t = t_(d); x = bande(bruit(d), 2600, 1700, 1.2) * np.exp(-t / 0.012) + 0.35 * np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.02)
    return stereo(normer(x))
def vibre(d=0.95):                                                  # téléphone qui vibre : deux bourdonnements
    t = t_(d); porte = ((t % 0.5) < 0.32).astype(float)
    x = np.sign(np.sin(2 * np.pi * 172 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 31 * t)) * porte
    x = bande(x, 260, 260, 2.0); x *= np.convolve(porte, np.ones(240) / 240, mode="same")
    return stereo(normer(x))
def clic(d=0.03):                                                   # doigt sur l'écran : un petit clic net
    t = t_(d); x = bande(bruit(d), 4200, 3000, 1.0) * np.exp(-t / 0.003) + 0.3 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.006)
    return stereo(normer(x))
def arret(d=0.75):                                                  # bande qui s'arrête (« tape stop ») : tout retombe
    t = t_(d); f = 210 * (1 - t / d) ** 1.6 + 22
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.25 * np.sign(np.sin(3 * ph))) * (1 - (t / d) ** 3)
    return reverb(stereo(normer(np.tanh(1.6 * x))), 0.3, 0.1)

SONS = {"whoosh": whoosh, "swish": swish, "souffle": souffle, "zip": zip_, "pop": pop, "bulle": bulle, "tick": tick,
        "tap": tap, "impact": impact, "scintille": scintille, "montee": montee, "coupe": coupe, "choix": choix, "secousse": secousse,
        "tampon": tampon, "sticker": sticker, "vibre": vibre, "clic": clic, "arret": arret}
AVEC_NOTE = {"pop", "bulle", "choix"}
# Niveau de crête de chaque famille (dBFS, avant la normalisation finale à -14 LUFS), réglé à la mesure (outils/mesurer-sons.py)
# pour tomber, au plus fort, de 8 dB (impact) à 18 dB (tick, souffle) sous la voix qui parle au même moment
NIVEAU = {"whoosh": -6, "swish": -10, "souffle": -17, "zip": -12, "pop": -9, "bulle": -10, "tick": -8, "tap": -7,
          "impact": -8, "scintille": -14, "montee": -9, "coupe": -16, "choix": -9, "secousse": -16,
          "tampon": -9, "sticker": -13, "vibre": -15, "clic": -12, "arret": -12}
# Ce qui doit tomber pile sur l'image : la montée finit à l'instant donné, les autres commencent à l'instant donné
FINIT_A_T = {"montee"}

if __name__ == "__main__":
    liste_f = sys.argv[1] if len(sys.argv) > 1 else "sons.json"
    sortie = sys.argv[2] if len(sys.argv) > 2 else "medias/sons/sons.wav"
    duree = float(sys.argv[3]) if len(sys.argv) > 3 else 60.0
    piste = np.zeros((int(duree * SR) + SR, 2))
    reperes = json.load(open(liste_f, encoding="utf-8"))
    for r in reperes:
        f = SONS[r["son"]]
        x = f(r.get("note", 0)) if r["son"] in AVEC_NOTE else f()
        if r.get("pan"):
            g = np.clip(1 + np.array([-1, 1]) * r["pan"], 0, 1); x = x * g
        x *= 10 ** ((NIVEAU[r["son"]] + r.get("db", 0)) / 20)
        i = int(round(r["t"] * SR)) - (len(x) if r["son"] in FINIT_A_T else 0)
        i0 = max(0, i); piste[i0:i + len(x)] += x[i0 - i:len(piste) - i]
    piste = piste[:int(duree * SR)]
    ecrire(sortie, piste, SR)
    print(f"{len(reperes)} bruitages, crête {20 * np.log10(np.abs(piste).max() + 1e-12):.1f} dBFS -> {sortie}")
