"""Décodage intégral, retranscription de chaque fichier et mesure du niveau livré."""
import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--numeros", type=int, nargs="*")
parser.add_argument("--modele",choices=["turbo","large-v3"],default="turbo")
parser.add_argument("--sans-vad",action="store_true")
parser.add_argument("--aide-vestiaire",action="store_true")
parser.add_argument("--aide-dialogue",action="store_true")
args = parser.parse_args()
model_path="large-v3-local" if args.modele=="large-v3" else "turbo-local"
model = WhisperModel(str(root / ".cache/modeles" / model_path), device="cpu", compute_type="int8", cpu_threads=8)


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("œ","oe"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    # Le s final d'important(s) n'a aucun son : variation orthographique ASR.
    aliases = {"importants":"important"}
    return [aliases.get(w,w) for w in re.findall(r"[a-z0-9]+", s)]


def asr(audio):
    padding=1 if args.aide_dialogue else .5 if args.aide_vestiaire else 0
    if padding: audio=np.pad(audio,(int(16000*padding),int(16000*padding)))
    prompt="Football. Atlas Paillade, Rousset, Berre, MHSC, contre-pressing. Entraîneur et joueurs dans le vestiaire."
    if args.aide_vestiaire:prompt+=" Vocabulaire : instinct, intuition, force, tête, cœur, engagement, Souley, Naït."
    if args.aide_dialogue:prompt="Dialogue entre joueurs. Vocabulaire : euros, patates, frère, doigt, Marrakech, PlayStation."
    segs, _ = model.transcribe(audio, language="fr", word_timestamps=True, vad_filter=not args.sans_vad,
                              beam_size=5, condition_on_previous_text=False,
                              initial_prompt=prompt)
    rows = []
    for s in segs:
        rows.append({"debut": round(max(0,s.start-padding),3), "fin": round(max(0,s.end-padding),3), "texte": s.text.strip(),
                     "mots": [{"mot":w.word,"debut":round(max(0,w.start-padding),3),"fin":round(max(0,w.end-padding),3)} for w in s.words or []]})
    return rows


clips = json.loads((root / "extraits.json").read_text(encoding="utf-8"))
for c in clips:
    if args.numeros and c["numero"] not in args.numeros:
        continue
    for kind in ["horizontal", "vertical"]:
        n = c["numero"]
        path = root / kind / f"clip-{n:02}{'-9x16' if kind=='vertical' else ''}.mp4"
        diag = root / "diagnostic" / f"verification-{n:02}-{kind}.json"
        if not (root / "diagnostic" / f"export-{n:02}.json").exists():
            raise RuntimeError(f"Export {n:02} pas encore terminé")
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        planned_sha = hashlib.sha256(c["texte_complet"].encode("utf-8")).hexdigest()
        previous = json.loads(diag.read_text(encoding="utf-8")) if diag.exists() else {}
        same_model = previous.get("modele_verification","turbo")==args.modele and previous.get("vad",True)==(not args.sans_vad) and previous.get("aide_vestiaire",False)==args.aide_vestiaire and previous.get("aide_dialogue",False)==args.aide_dialogue
        if previous.get("sha256") == sha and previous.get("texte_prevu_sha256") == planned_sha and same_model:
            print(f"Clip {n:02} {kind} déjà vérifié", flush=True)
            continue
        print(f"Vérification {n:02} {kind}", flush=True)
        decode = subprocess.run(["ffmpeg","-v","error","-threads","2","-i",str(path),"-f","null","-"],capture_output=True,text=True)
        audio = decode_audio(str(path))
        if previous and not same_model:
            history=root / "diagnostic" / f"verification-{n:02}-{kind}-{previous.get('modele_verification','turbo')}-historique.json"
            history.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        # Une correction du texte attendu ne change pas l'audio déjà retranscrit.
        # Réutilisation seulement si le fichier complet a la même empreinte SHA-256.
        rows = previous["transcription"] if previous.get("sha256")==sha and same_model else asr(audio)
        actual = " ".join(s["texte"] for s in rows)
        expected = norm(c["texte_complet"])
        got = norm(actual)
        k = min(4,len(expected))
        first_ok, last_ok = got[:k] == expected[:k], got[-k:] == expected[-k:]
        bounds = {}
        if not first_ok:
            start_rows = previous.get("relecture_limites",{}).get("debut") if previous.get("sha256")==sha and same_model else None
            if start_rows is None:start_rows = asr(audio[:min(len(audio),8*16000)])
            bounds["debut"] = start_rows
            first_ok = norm(" ".join(s["texte"] for s in start_rows))[:k] == expected[:k]
        if not last_ok:
            last_rows = previous.get("relecture_limites",{}).get("fin") if previous.get("sha256")==sha and same_model else None
            if last_rows is None:last_rows = asr(audio[max(0,len(audio)-8*16000):])
            bounds["fin"] = last_rows
            last_ok = norm(" ".join(s["texte"] for s in last_rows))[-k:] == expected[-k:]
        level = subprocess.run(["ffmpeg","-hide_banner","-i",str(path),"-vn","-af",
            "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
        measures = json.loads(level.stderr[level.stderr.rfind("{"):level.stderr.rfind("}")+1])
        probe = subprocess.run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(path)],capture_output=True,text=True,check=True)
        p = json.loads(probe.stdout)
        v = next(s for s in p["streams"] if s["codec_type"]=="video")
        a = next(s for s in p["streams"] if s["codec_type"]=="audio")
        problems = []
        if decode.returncode or decode.stderr.strip(): problems.append("Erreur de décodage intégral")
        if not first_ok: problems.append("Premiers mots différents dans la retranscription")
        if not last_ok: problems.append("Derniers mots différents dans la retranscription")
        if abs(float(p["format"]["duration"])-c["duree"]) > .10: problems.append("Durée différente")
        if (v["width"],v["height"]) != ((1080,1920) if kind=="vertical" else (1920,1080)): problems.append("Résolution incorrecte")
        if v["codec_name"]!="h264" or a["codec_name"]!="aac": problems.append("Codec incorrect")
        if path.stat().st_size>=100_000_000: problems.append("Taille supérieure ou égale à 100 Mo")
        if abs(float(measures["input_i"])+14)>.5: problems.append("Niveau sonore hors de -14 LUFS ±0,5")
        if float(measures["input_tp"])>0: problems.append("Pic audio supérieur à 0 dBTP")
        result = {"numero":n,"format":kind,"sha256":sha,"texte_prevu_sha256":planned_sha,"verification":"OK" if not problems else "; ".join(problems),
                  "modele_verification":args.modele,"vad":not args.sans_vad,"aide_vestiaire":args.aide_vestiaire,"aide_dialogue":args.aide_dialogue,
                  "decodage_integral":"OK" if not decode.returncode and not decode.stderr.strip() else decode.stderr,
                  "premiers_mots_attendus":expected[:k],"derniers_mots_attendus":expected[-k:],
                  "premiers_mots_reconnus":got[:k],"derniers_mots_reconnus":got[-k:],
                  "debut_correspond":first_ok,"fin_correspond":last_ok,"transcription":rows,"relecture_limites":bounds,
                  "lufs":float(measures["input_i"]),"pic_vrai_db":float(measures["input_tp"]),
                  "duree":float(p["format"]["duration"]),"taille_octets":path.stat().st_size}
        diag.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"Clip {n:02} {kind} : {result['verification']}, {result['lufs']} LUFS",flush=True)
