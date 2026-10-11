"""Relecture ASR sans VAD des zones parlées, pour éviter les omissions dans le bruit."""
import argparse
import json
import time
from pathlib import Path
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from transcrire import stamp, write

parser = argparse.ArgumentParser()
parser.add_argument("--modele", default=".cache/modeles/turbo-local")
parser.add_argument("--zones", choices=["toutes", "difficiles"], default="toutes")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = root / "transcription"
original = json.loads((out / "transcription-segments.json").read_text(encoding="utf-8"))
if not (out / "transcription-brut-segments.json").exists():
    write(out / "transcription-brut-segments.json", original)
audio = decode_audio(str(root / "travail/source-16k.wav"))
model = WhisperModel(str(root / args.modele), device="cpu", compute_type="int8", cpu_threads=8)
ranges = [(0, 38), (123, 159.75), (159.75, 233), (233, 299.65), (299.65, 330.5),
          (371, 410.2), (410.2, 450), (572, 629), (629, 673.5), (673.5, 720),
          (744, 777), (777, 834), (1135, 1165.5), (1165.5, 1192.5),
          (1192.5, 1234), (1234, 1280), (1280, 1319)]
if args.zones == "difficiles":
    ranges = [(572, 608), (608, 638.5), (639, 674), (674, 721), (744, 777), (777, 832),
              (1136, 1165.5), (1165.5, 1192.5), (1192.5, 1218.5),
              (1218.5, 1244.5), (1244.5, 1280), (1280, 1319)]
words = [w for s in original for w in s["mots"]
         if not any(a <= (w["debut"] + w["fin"]) / 2 < b for a, b in ranges)]
for a, b in ranges:
    begin = time.monotonic()
    segs, info = model.transcribe(audio[round(a*16000):round(b*16000)], language="fr",
        beam_size=5, vad_filter=False, word_timestamps=True, condition_on_previous_text=False,
        initial_prompt="Football. National 2, Montpellier Atlas Paillade, FC Rousset, Berre, contre-pressing, Souillard.")
    rows = []
    for s in segs:
        sw = [{"mot": w.word, "debut": round(a+w.start, 3), "fin": round(a+w.end, 3),
               "probabilite": round(w.probability, 4)} for w in s.words or []]
        rows.append({"debut": round(a+s.start, 3), "fin": round(a+s.end, 3), "texte": s.text.strip(), "mots": sw})
        words.extend(sw)
    write(out / f"relecture-{a:g}-{b:g}.json", rows)
    print(f"Relecture {a:g}–{b:g} : {time.monotonic()-begin:.1f} s", flush=True)
    for s in rows:
        print(f"[{s['debut']:.2f}–{s['fin']:.2f}] {s['texte']}", flush=True)

words.sort(key=lambda w: (w["debut"], w["fin"]))
segments, group = [], []
for w in words:
    if group and (w["debut"] - group[-1]["fin"] > 1.2 or w["fin"] - group[0]["debut"] > 10):
        segments.append({"debut": group[0]["debut"], "fin": group[-1]["fin"],
                         "texte": "".join(x["mot"] for x in group).strip(), "mots": group})
        group = []
    group.append(w)
if group:
    segments.append({"debut": group[0]["debut"], "fin": group[-1]["fin"],
                     "texte": "".join(x["mot"] for x in group).strip(), "mots": group})
write(out / "transcription-segments.json", segments)
write(out / "transcription-mots.json", words)
(out / "transcription.srt").write_text("\n".join(
    f"{i}\n{stamp(s['debut'])} --> {stamp(s['fin'])}\n{s['texte']}\n" for i, s in enumerate(segments, 1)), encoding="utf-8")
(out / "transcription.txt").write_text("\n".join(
    f"[{s['debut']:.2f}–{s['fin']:.2f}] {s['texte']}" for s in segments) + "\n", encoding="utf-8")
print(f"Transcription consolidée : {len(words)} mots, {len(segments)} sous-titres", flush=True)
