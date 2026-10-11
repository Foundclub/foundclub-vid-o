"""Petite correction de gain après mesure AAC ; vidéo copiée sans réencodage."""
import argparse
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--numeros",nargs="*",type=int)
args=parser.parse_args()
for clip in json.loads((root/"extraits.json").read_text(encoding="utf-8")):
    n=clip["numero"]
    if args.numeros and n not in args.numeros: continue
    path=root/"horizontal"/f"clip-{n:02}.mp4"
    r=subprocess.run(["ffmpeg","-hide_banner","-i",str(path),"-vn","-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True,check=True)
    measured=json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}")+1])
    delta=-14-float(measured["input_i"])
    if abs(delta)<=.10:
        print(f"Son {n:02} déjà à {measured['input_i']} LUFS",flush=True)
        continue
    print(f"Son {n:02} : gain {delta:.2f} dB",flush=True)
    for kind in ["horizontal","vertical"]:
        path=root/kind/f"clip-{n:02}{'-9x16' if kind=='vertical' else ''}.mp4"
        temp=root/"travail"/f"clip-{n:02}-{kind}-son-corrige.mp4"
        subprocess.run(["ffmpeg","-v","error","-i",str(path),"-map","0:v:0","-map","0:a:0",
            "-c:v","copy","-af",f"volume={delta:.3f}dB","-c:a","aac","-b:a","192k","-movflags","+faststart","-y",str(temp)],check=True)
        temp.replace(path)
    p=root/"diagnostic"/f"son-{n:02}.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    data["ajustement_final_gain_db"]=round(delta,3)
    data["niveau_aac_avant_ajustement"]=float(measured["input_i"])
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
