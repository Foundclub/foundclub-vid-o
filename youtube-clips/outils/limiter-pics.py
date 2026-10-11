"""Refait les deux passes sur la source avec davantage de marge avant l'AAC."""
import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
clips=json.loads((root/'extraits.json').read_text(encoding='utf-8'))
for c in clips:
    n=c['numero']
    if n not in [3,5,6,16]:continue
    d=c['duree'];fade=f"afade=t=in:st=0:d=0.03,afade=t=out:st={d-.03:.6f}:d=0.03"
    base=['ffmpeg','-hide_banner','-ss',str(c['debut']),'-i',str(root/'source/ach10-source.mp4'),'-t',str(d),'-vn']
    first=subprocess.run(base+['-af',fade+',loudnorm=I=-14:TP=-6:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    def metrics(s):return json.loads(s[s.rfind('{'):s.rfind('}')+1])
    m=metrics(first.stderr)
    loud=f"loudnorm=I=-14:TP=-6:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
    audio=root/'travail'/f'clip-{n:02}-audio-pics-corriges.m4a'
    second=subprocess.run(base+['-af',fade+','+loud,'-ar','48000','-c:a','aac','-b:a','192k','-y',str(audio)],capture_output=True,text=True,check=True)
    for kind in ['horizontal','vertical']:
        path=root/kind/f"clip-{n:02}{'-9x16' if kind=='vertical' else ''}.mp4"
        tmp=root/'travail'/f'clip-{n:02}-{kind}-pics-corriges.mp4'
        subprocess.run(['ffmpeg','-v','error','-i',str(path),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c','copy','-t',str(d),'-movflags','+faststart','-y',str(tmp)],check=True)
        tmp.replace(path)
    p=root/'diagnostic'/f'son-{n:02}.json'
    data={'premiere_passe':m,'seconde_passe':metrics(second.stderr),'fondus_ms':30,'correction_pics':'Marge de -6 dBTP avant encodage AAC, pour absorber les dépassements après conversion','origine_audio':'Source YouTube téléchargée, sans cascade de réencodages audio'}
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Audio {n:02} refait depuis la source, marge AAC renforcée',flush=True)
