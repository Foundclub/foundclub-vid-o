"""Transcription locale française avec mots horodatés et journal de progression."""
import argparse
import json
import os
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
from faster_whisper import WhisperModel


def stamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROMPT = "Football. Achh10, AchhLife, National 2, Berre SC, FC Rousset, FoundClub, Ergysport."


def transcribe(model, source, out, stem, beam=5, prompt=PROMPT):
    out.mkdir(parents=True, exist_ok=True)
    begin = time.monotonic()
    segments, info = model.transcribe(
        str(source), language="fr", beam_size=beam, word_timestamps=True,
        vad_filter=True, condition_on_previous_text=False,
        initial_prompt=prompt,
    )
    rows, words, subtitles = [], [], []
    for i, s in enumerate(segments, 1):
        sw = [{"mot": w.word, "debut": round(w.start, 3), "fin": round(w.end, 3),
               "probabilite": round(w.probability, 4)} for w in s.words or []]
        words.extend(sw)
        rows.append({"debut": round(s.start, 3), "fin": round(s.end, 3),
                     "texte": s.text.strip(), "mots": sw})
        subtitles.append(f"{i}\n{stamp(s.start)} --> {stamp(s.end)}\n{s.text.strip()}\n")
        write(out / f"{stem}-segments-partiel.json", rows)
        if i % 5 == 0 or i == 1:
            print(f"{stem}: {s.end:.1f}/{info.duration:.1f} s, calcul {time.monotonic()-begin:.1f} s", flush=True)
    write(out / f"{stem}-segments.json", rows)
    write(out / f"{stem}-mots.json", words)
    (out / f"{stem}.srt").write_text("\n".join(subtitles), encoding="utf-8")
    (out / f"{stem}.txt").write_text("\n".join(
        f"[{r['debut']:.2f}–{r['fin']:.2f}] {r['texte']}" for r in rows), encoding="utf-8")
    write(out / f"{stem}-mesures.json", {"langue": info.language, "duree": info.duration,
          "duree_calcul": round(time.monotonic()-begin, 2), "mots": len(words), "segments": len(rows)})
    (out / f"{stem}-segments-partiel.json").unlink(missing_ok=True)
    return rows, words


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("--sortie", type=Path, required=True)
    p.add_argument("--nom", default="transcription")
    p.add_argument("--modele", default="large-v3-turbo")
    p.add_argument("--cache", type=Path, required=True)
    a = p.parse_args()
    print(f"Chargement {a.modele}, CPU int8, 8 threads", flush=True)
    model = WhisperModel(a.modele, device="cpu", compute_type="int8", cpu_threads=8,
                         num_workers=1, download_root=str(a.cache))
    transcribe(model, a.source, a.sortie, a.nom)
