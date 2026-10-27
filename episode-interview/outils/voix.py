"""Reconnaît qui parle, mot par mot, dans les phrases du papier (Achraf, Moussa ou une autre voix).

Modèle WeSpeaker ResNet34 (voxceleb_resnet34_LM.onnx, CC-BY-4.0) lu par onnxruntime ; empreinte de voix sur des
fenêtres de 1,5 s tous les 0,25 s, comparée à des passages où l'on sait qui parle (REFERENCES). Un mot prend la
voix majoritaire des fenêtres qui le couvrent ; sous le seuil, c'est « autre » (un coéquipier, un dirigeant…).

Sortie : TRAVAIL/voix/<rush>.json  {"<séquence>-<phrase>": {indice du mot dans <rush>-mots.json: "achraf" | "moussa" |
et un relevé par phrase du papier, à comparer à son champ « qui ».

python outils/voix.py      (numpy et onnxruntime : lancer avec `python`, pas `python -I`)
"""
import json
import wave
from pathlib import Path

import numpy as np
import onnxruntime

ICI = Path(__file__).resolve().parents[1]
TRAVAIL = Path(r"D:\App\video\rushs\interview\travail")
MODELE = Path(r"D:\App\video\rushs\interview\modeles\wespeaker\voxceleb_resnet34_LM.onnx")
SR, FENETRE, PAS = 16000, 1.5, 0.25
SEUIL = 0.40  # similarité minimale pour dire « Achraf » ou « Moussa »
REFERENCES = {  # passages où une seule personne parle (vérifiés à la lecture du papier)
    "achraf": [("1", 0.0, 19.3), ("DJI_20261026201400_0016_D", 557.8, 562.9)],
    "moussa": [("DJI_20261026190240_0010_D", 160.0, 200.0), ("DJI_20261026190240_0010_D", 255.0, 275.0)],
}

session = onnxruntime.InferenceSession(str(MODELE), providers=["CPUExecutionProvider"])
_sons = {}


def son(rush):
    if rush not in _sons:
        with wave.open(str(TRAVAIL / "son16" / f"{rush}.wav")) as w:
            _sons[rush] = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    return _sons[rush]


def _filtres_mel(n_fft=512, n_mel=80, bas=20.0, haut=8000.0):
    mel = lambda f: 1127.0 * np.log(1.0 + f / 700.0)
    points = np.linspace(mel(bas), mel(haut), n_mel + 2)
    freqs = mel(np.arange(n_fft // 2 + 1) * SR / n_fft)
    f = np.zeros((n_mel, n_fft // 2 + 1), dtype=np.float32)
    for i in range(n_mel):
        g, c, d = points[i:i + 3]
        f[i] = np.clip(np.minimum((freqs - g) / (c - g), (d - freqs) / (d - c)), 0, None)
    return f


MEL = _filtres_mel()
HANN = (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(400) / 399)) ** 0.85  # fenêtre « povey » de Kaldi


def fbank(x):
    """80 bandes mel à la manière de Kaldi (25 ms, pas de 10 ms), moyenne retirée."""
    n = 1 + (len(x) - 400) // 160
    trames = np.lib.stride_tricks.as_strided(x, (n, 400), (x.strides[0] * 160, x.strides[0])).copy()
    trames -= trames.mean(axis=1, keepdims=True)
    trames[:, 1:] -= 0.97 * trames[:, :-1]
    trames[:, 0] *= 0.03
    spectre = np.abs(np.fft.rfft(trames * HANN, 512)) ** 2
    f = np.log(np.maximum(spectre @ MEL.T, 1.19e-7))
    return (f - f.mean(axis=0)).astype(np.float32)


def empreintes(rush, debut, fin):
    x = son(rush)
    centres = np.arange(debut + FENETRE / 2, max(fin - FENETRE / 2, debut + FENETRE / 2) + 1e-6, PAS)
    lot = []
    for c in centres:
        a = int(max(0, c - FENETRE / 2) * SR)
        lot.append(fbank(x[a:a + int(FENETRE * SR)]))
    t = min(len(f) for f in lot)
    e = session.run(None, {"feats": np.stack([f[:t] for f in lot])})[0]
    return centres, e / np.linalg.norm(e, axis=1, keepdims=True)


modeles = {}
for qui, passages in REFERENCES.items():
    e = np.concatenate([empreintes(*p)[1] for p in passages])
    m = e.mean(axis=0)
    modeles[qui] = m / np.linalg.norm(m)
print("ressemblance Achraf / Moussa :", round(float(modeles["achraf"] @ modeles["moussa"]), 2))

TIERS = {"coéquipier": "UN ANCIEN COÉQUIPIER", "dirigeant": "UN DIRIGEANT", "groupe": "LES POTES",
         "slimane": "SLIMANE"}


def voix_du_papier(qui):
    """« Achraf, puis Moussa » → ["achraf", "moussa"] ; « un dirigeant » → ["autre:UN DIRIGEANT"]."""
    qui = qui.lower().split("(")[0]
    possibles = [q for q in ("achraf", "moussa") if q in qui]
    possibles += [f"autre:{nom}" for mot, nom in TIERS.items() if mot in qui]
    return possibles or ["achraf"]


papier = json.loads((ICI / "papier.json").read_text(encoding="utf-8"))
sortie = TRAVAIL / "voix"
sortie.mkdir(exist_ok=True)
resultats, releve = {}, []
for n, seq in enumerate(papier["sequences"]):
    for i, p in enumerate(seq["paroles"]):
        rush = p["rush"]
        mots = json.loads((TRAVAIL / "transcriptions" / f"{rush}-mots.json").read_text(encoding="utf-8"))
        centres, e = empreintes(rush, max(0.0, p["debut"] - 0.5), p["fin"] + 0.5)
        sa, sm = e @ modeles["achraf"], e @ modeles["moussa"]
        # recalage sur le lieu (voiture, rue, tribune) : les fenêtres sûres affinent les deux modèles
        locaux = {}
        for qui, s, autre_s in (("achraf", sa, sm), ("moussa", sm, sa)):
            sures = (s > 0.5) & (s - autre_s > 0.15)
            m = modeles[qui] + (e[sures].mean(axis=0) if sures.any() else 0)
            locaux[qui] = m / np.linalg.norm(m)
        sa, sm = e @ locaux["achraf"], e @ locaux["moussa"]
        # le papier dit qui parle dans la phrase : une seule voix, on la prend ; sinon le modèle départage
        possibles = voix_du_papier(p["qui"])
        if len(possibles) == 1:
            etiquette = np.full(len(centres), possibles[0], dtype=object)
        else:
            tiers = next((q for q in possibles if q.startswith("autre")), None)
            etiquette = np.where(sa > sm, "achraf", "moussa").astype(object)
            if tiers:
                etiquette[np.maximum(sa, sm) < SEUIL] = tiers
            etiquette = np.array([e_ if e_ in possibles else possibles[0] for e_ in etiquette], dtype=object)
        compte = {}
        voix = resultats.setdefault(rush, {}).setdefault(f"{n}-{i}", {})
        for k, m in enumerate(mots):
            if not (p["debut"] - 0.05 <= m["debut"] < p["fin"]):
                continue
            proches = np.abs(centres - (m["debut"] + m["fin"]) / 2) <= FENETRE / 2
            choix = etiquette[proches] if proches.any() else etiquette[[np.argmin(np.abs(centres - m["debut"]))]]
            vals, nb = np.unique(choix, return_counts=True)
            voix[str(k)] = str(vals[np.argmax(nb)])
            compte[voix[str(k)]] = compte.get(voix[str(k)], 0) + 1
        total = max(1, sum(compte.values()))
        releve.append(f"seq {n} phrase {i} ({p['qui']}) : " + ", ".join(
            f"{q} {100 * c // total} %" for q, c in compte.items() if c))
for rush, voix in resultats.items():
    (sortie / f"{rush}.json").write_text(json.dumps(voix, indent=0) + "\n", encoding="utf-8")
print("\n".join(releve))
