"""Exports sobres, normalisation mesurée et recadrage suivi ou cadre entier flouté."""
import argparse
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import FaceDetector, FaceDetectorOptions

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/ach10-source.mp4"
WORK = ROOT / "travail"
DIAG = ROOT / "diagnostic"


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-8000:])
    return r


def norm_json(stderr):
    return json.loads(stderr[stderr.rfind("{"):stderr.rfind("}")+1])


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def track(c):
    d = c["duree"]
    decoder = subprocess.Popen(["ffmpeg", "-v", "error", "-threads", "2", "-ss", str(c["debut"]),
        "-i", str(SOURCE), "-t", str(d), "-an", "-vf", "fps=4,scale=640:360",
        "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    detector = FaceDetector.create_from_options(FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=str(ROOT / ".cache/modeles/blaze-face-short-range.tflite")),
        min_detection_confidence=.55))
    centers, counts, samples = [], [], []
    frame_size = 640 * 360 * 3
    i = 0
    while True:
        data = decoder.stdout.read(frame_size)
        if not data:
            break
        if len(data) != frame_size:
            raise RuntimeError("Image de détection incomplète")
        frame = np.frombuffer(data, dtype=np.uint8).reshape(360, 640, 3)
        detections = detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)).detections
        faces = [f for f in detections if f.bounding_box.width >= 18]
        counts.append(len(faces))
        if faces:
            best = max(faces, key=lambda f: f.bounding_box.width * f.bounding_box.height)
            box = best.bounding_box
            center = (box.origin_x + box.width / 2) * 3
        else:
            center = centers[-1] if centers else 960
        centers.append(center)
        samples.append({"t": round(i/4, 3), "visages": len(faces), "centre_x": round(center, 1)})
        i += 1
    detector.close()
    error = decoder.stderr.read().decode("utf-8", errors="replace")
    if decoder.wait():
        raise RuntimeError(error)
    valid = sum(n == 1 for n in counts) / max(1, len(counts))
    multi = sum(n > 1 for n in counts)
    blur = c.get("fond_flou_impose", False) or multi > 0 or valid < .9
    reason = c.get("raison_fond_flou") if c.get("fond_flou_impose") else (
        "Plusieurs visages détectés" if multi else "Visage unique insuffisamment détecté" if valid < .9 else "Visage unique")
    if blur:
        vf = "[0:v]split=2[bg][fg];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=12,scale=1080:1920[back];[fg]scale=1080:608[front];[back][front]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
    else:
        # Médiane sur cinq échantillons, amortissement, puis interpolation continue.
        median = [float(np.median(centers[max(0,j-2):min(len(centers),j+3)])) for j in range(len(centers))]
        smooth = [median[0]]
        for x in median[1:]:
            smooth.append(smooth[-1] + .25 * (x-smooth[-1]))
        knots = [(j/4, min(1312, max(0, smooth[j]-304))) for j in range(0, len(smooth), 4)]
        if knots[-1][0] < d:
            knots.append((d, min(1312, max(0, smooth[-1]-304))))
        expr = f"{knots[0][1]:.3f}"
        for (t0, x0), (t1, x1) in zip(knots, knots[1:]):
            if abs(x1-x0) > .01:
                expr += f"+({x1-x0:.3f})*clip((t-{t0:.3f})/{t1-t0:.3f},0,1)"
        vf = f"[0:v]crop=608:1080:x='{expr}':y=0,scale=1080:1920,setsar=1[v]"
    result = {"numero": c["numero"], "mode": "fond flou" if blur else "visage",
              "raison": reason, "fraction_visage_unique": round(valid, 3), "images_plusieurs_visages": multi,
              "methode": "MediaPipe BlazeFace à 4 images/s; médiane, amortissement et interpolation continue",
              "echantillons": samples}
    save(DIAG / f"recadrage-{c['numero']:02}.json", result)
    return vf, result


def encode(c):
    started = time.monotonic()
    n, d = c["numero"], c["duree"]
    print(f"Clip {n:02} : analyse et son", flush=True)
    fade = f"afade=t=in:st=0:d=0.03,afade=t=out:st={d-.03:.6f}:d=0.03"
    first = run(["ffmpeg", "-hide_banner", "-ss", str(c["debut"]), "-i", str(SOURCE), "-t", str(d),
          "-vn", "-af", fade+",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = norm_json(first.stderr)
    loud = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
    audio = WORK / f"clip-{n:02}-audio.m4a"
    second = run(["ffmpeg", "-hide_banner", "-ss", str(c["debut"]), "-i", str(SOURCE), "-t", str(d),
       "-vn", "-af", fade+","+loud, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-y", str(audio)])
    save(DIAG / f"son-{n:02}.json", {"premiere_passe": m, "seconde_passe": norm_json(second.stderr), "fondus_ms": 30})
    vf, crop = track(c)
    sizes, lowered = {}, []
    for kind in ["horizontal", "vertical"]:
        suffix = "-9x16" if kind == "vertical" else ""
        path = ROOT / kind / f"clip-{n:02}{suffix}.mp4"
        filt = vf if kind == "vertical" else "[0:v]scale=1920:1080,setsar=1[v]"
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-threads", "2", "-ss", str(c["debut"]),
            "-i", str(SOURCE), "-i", str(audio), "-t", str(d), "-filter_complex_threads", "2", "-filter_complex", filt,
            "-map", "[v]", "-map", "1:a:0", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-y", str(path)]
        run(command)
        if path.stat().st_size >= 100_000_000:
            limit = int((94_000_000 * 8 / d - 220000) / 1000)
            run(command[:-2] + ["-maxrate", f"{limit}k", "-bufsize", f"{limit*2}k"] + command[-2:])
            lowered.append({"format": kind, "maxrate_kbit": limit})
        if path.stat().st_size >= 100_000_000:
            raise RuntimeError(f"Fichier trop volumineux : {path}")
        sizes[kind] = path.stat().st_size
        print(f"Clip {n:02} {kind} : {sizes[kind]/1e6:.1f} Mo", flush=True)
    # Huit images régulièrement réparties dans la coupe réellement exportée.
    horizontal = ROOT / "horizontal" / f"clip-{n:02}.mp4"
    run(["ffmpeg", "-v", "error", "-i", str(horizontal), "-vf",
        f"fps=8/{d},scale=400:225,tile=4x2:nb_frames=8:padding=4:margin=4", "-frames:v", "1", "-q:v", "3", "-y",
        str(ROOT / "planches" / f"clip-{n:02}.jpg")])
    run(["ffmpeg", "-v", "error", "-i", str(ROOT / "vertical" / f"clip-{n:02}-9x16.mp4"), "-vf",
        f"fps=8/{d},scale=180:320,tile=4x2:nb_frames=8:padding=4:margin=4", "-frames:v", "1", "-q:v", "3", "-y",
        str(ROOT / "planches" / f"clip-{n:02}-vertical.jpg")])
    result = {"numero": n, "recadrage": crop["mode"], "raison_recadrage": crop["raison"],
              "tailles_octets": sizes, "debit_reduit": lowered, "duree_calcul": round(time.monotonic()-started, 2)}
    save(DIAG / f"export-{n:02}.json", result)
    print(f"Clip {n:02} terminé en {result['duree_calcul']} s", flush=True)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--numeros", type=int, nargs="*")
    p.add_argument("--parallele", type=int, default=2)
    args = p.parse_args()
    for folder in [WORK, DIAG, ROOT/"horizontal", ROOT/"vertical", ROOT/"planches"]:
        folder.mkdir(parents=True, exist_ok=True)
    clips = json.loads((ROOT / "extraits.json").read_text(encoding="utf-8"))
    selected = [c for c in clips if not args.numeros or c["numero"] in args.numeros]
    with ThreadPoolExecutor(max_workers=args.parallele) as pool:
        results = list(pool.map(encode, selected))
    for c in clips:
        for r in results:
            if c["numero"] == r["numero"]:
                c.update({k: v for k, v in r.items() if k != "numero"})
    save(ROOT / "extraits.json", clips)
