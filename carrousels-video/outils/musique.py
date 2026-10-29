"""Fond musical synthétisé (aucun fichier tiers, aucun droit) : une boucle pop légère, un accord par page.
La mesure (4 temps) dure ce que dure une page, donc l'accord change pile quand la page glisse.
Mesure 1 : nappe et charleston seuls ; mesures 2 à n-1 : grosse caisse, claquement, basse ; dernière mesure (carton) :
la nappe seule, qui s'éteint.
Usage : python -I outils/musique.py [musique.json] [sortie.wav]"""
import sys, json
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from wav import ecrire

SR = 48000
rng = np.random.default_rng(29102026)
P = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "musique.json", encoding="utf-8"))
SORTIE = sys.argv[2] if len(sys.argv) > 2 else "medias/sons/musique.wav"
M, DUREE = P["mesure"], P["duree"]
NB = int(round(DUREE / M))
TEMPS = M / 4
n = int(DUREE * SR) + SR
G, D = np.zeros(n), np.zeros(n)

def poser(x, t, pan=0.0, gain=1.0):
    i = int(round(t * SR)); x = x[: max(0, n - i)] * gain
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    G[i:i + len(x)] += x * np.cos(a); D[i:i + len(x)] += x * np.sin(a)

t_ = lambda d: np.arange(int(d * SR)) / SR
def kick():
    t = t_(0.35); f = 45 + 85 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
def passe_haut(x, k=0.97):          # un filtre d'une ligne suffit pour un charleston
    y = np.empty_like(x); p = 0.0; q = 0.0
    for i, v in enumerate(x):
        p = k * (p + v - q); q = v; y[i] = p
    return y
CH = passe_haut(rng.standard_normal(int(0.05 * SR))) * np.exp(-t_(0.05) / 0.012)
def clap():
    t = t_(0.18); x = rng.standard_normal(len(t)) * np.exp(-t / 0.05)
    for k in (0.008, 0.016):        # trois mains qui ne frappent pas tout à fait ensemble
        j = int(k * SR); x[j:] += rng.standard_normal(len(t) - j) * np.exp(-t[: len(t) - j] / 0.05)
    return passe_haut(x, 0.9) * 0.5
def note(f, d, forme="basse"):
    t = t_(d)
    if forme == "basse":
        x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
        return x * np.minimum(1, t / 0.005) * np.exp(-t / 0.25)
    # nappe : trois voix légèrement désaccordées, attaque lente, harmoniques qui décroissent
    x = sum(np.sin(2 * np.pi * f * (1 + dt) * h * t) / h ** 1.6 for dt in (-0.004, 0, 0.004) for h in (1, 2, 3))
    env = np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4)
    return x * env / 4

hz = lambda m: 440 * 2 ** ((m - 69) / 12)
# la mineur, fa, do, sol : la suite d'accords la plus banale qui soit, exprès (elle ne détourne pas l'œil des écrans)
ACCORDS = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
for b in range(NB):
    t0 = b * M; acc = ACCORDS[b % 4]; derniere = b == NB - 1
    for k, m in enumerate(acc):
        poser(note(hz(m + 12), M, "nappe"), t0, pan=(k - 1) * 0.5, gain=0.16)
    for q in range(8):                                  # charleston sur chaque croche, plus fort à contretemps
        if not derniere:
            poser(CH, t0 + q * TEMPS / 2, pan=0.3, gain=0.10 if q % 2 == 0 else 0.18)
    if 0 < b < NB - 1:
        for q in range(4):
            poser(kick(), t0 + q * TEMPS, gain=0.55)
        for q in (1, 3):
            poser(clap(), t0 + q * TEMPS, pan=-0.1, gain=0.22)
        for q in range(8):                              # basse en croches sur la fondamentale
            poser(note(hz(acc[0] - 12), TEMPS / 2 * 0.9), t0 + q * TEMPS / 2, gain=0.30)
x = np.stack([G, D], 1)[: int(DUREE * SR)]
fondu = int(1.2 * SR); x[-fondu:] *= np.linspace(1, 0, fondu)[:, None] ** 1.5
x[: int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
x /= np.abs(x).max() / 0.5
ecrire(SORTIE, x, SR)
print(f"musique : {NB} mesures de {M} s ({60 / TEMPS:.1f} temps/min), {DUREE:.2f} s -> {SORTIE}")
