"""Corrections supplémentaires étayées par le texte incrusté dans la source.

Les temps d'une expression remplacée restent dans l'intervalle ASR initial :
ce sont des estimations, pas un nouvel alignement acoustique forcé.
"""
import json
from pathlib import Path
from transcrire import stamp, write

root=Path(__file__).resolve().parents[1]
out=root/'transcription'
words=json.loads((out/'transcription-mots.json').read_text(encoding='utf-8'))
corrections=json.loads((out/'corrections.json').read_text(encoding='utf-8'))

def replace(a,b,text,proof):
    global words
    selected=[w for w in words if a<=w['debut']<b]
    if not selected: raise ValueError((a,b))
    before=''.join(w['mot'] for w in selected).strip()
    if before==text: return
    start,end=selected[0]['debut'],selected[-1]['fin']
    tokens=text.split()
    new=[{'mot':' '+t,'debut':round(start+(end-start)*i/len(tokens),3),
          'fin':round(start+(end-start)*(i+1)/len(tokens),3),
          'probabilite':None,'correction_manuelle':True,'horodatage_estime':True}
         for i,t in enumerate(tokens)]
    words=[w for w in words if not a<=w['debut']<b]+new
    words.sort(key=lambda w:(w['debut'],w['fin']))
    corrections.append({'debut':start,'fin':end,'avant':before,'apres':text,'preuve':proof})

replace(131.24,131.44,'CAN','Trophée africain visible et mention du Maroc à 02:11')
replace(207.15,207.69,'MHSC','Logo de Montpellier visible à 03:27')
replace(226.55,227.91,"l’AS Saint-Étienne",'Logo de Saint-Étienne visible à 03:47')
replace(243.08,243.89,'US Mandelieu,','Logo et tableau des adversaires visibles à 04:03')
replace(244.34,245.16,'Cannet-Rocheville','Logo du Cannet-Rocheville visible à 04:05')
replace(276.54,277.24,'US Mandelieu','Même nom que le logo présenté à 04:03')
replace(314.91,315.31,'amateur','Sous-titre visible à 05:15 : reclassé amateur')
replace(624.58,624.93,'posé.','Sous-titre incrusté vers 10:24')
replace(645.48,645.76,'une dar','Sous-titre source à 10:46 : une dar à Marrakech')
replace(788.30,788.75,'un match à domicile,','Sous-titre incrusté à 13:09')
replace(793.64,794.16,'encore les noms derrière,','Sous-titre incrusté à 13:14')
replace(810.08,810.35,"l’Atlas.",'Sous-titre incrusté vers 13:30, nom du club déjà présenté')
replace(826.72,826.97,'à Atlas,','Sous-titre source à 13:47 : il est à Atlas')
replace(1142.12,1142.28,'pas','Sous-titre à 19:02 : on est pas dedans')
replace(1147.94,1148.63,"C’est puni,",'Sous-titre incrusté vers 19:08')
replace(1149.34,1149.55,"t’es puni.",'Même répétition à 19:09')
replace(1177.68,1177.95,'fou,','Sous-titre incrusté vers 19:38 : rendez ce match fou')
replace(1276.52,1277.00,'en marchant,','Sous-titre incrusté à 21:16')
replace(1309.56,1310.18,'demander des efforts','Sous-titre incrusté vers 21:50')

segments,group=[],[]
for w in words:
    if group and (w['debut']-group[-1]['fin']>1.2 or w['fin']-group[0]['debut']>10):
        segments.append({'debut':group[0]['debut'],'fin':group[-1]['fin'],
            'texte':''.join(x['mot'] for x in group).strip(),'mots':group})
        group=[]
    group.append(w)
if group:
    segments.append({'debut':group[0]['debut'],'fin':group[-1]['fin'],
        'texte':''.join(x['mot'] for x in group).strip(),'mots':group})
write(out/'transcription-mots.json',words)
write(out/'transcription-segments.json',segments)
write(out/'corrections.json',corrections)
(out/'transcription.srt').write_text('\n'.join(f"{i}\n{stamp(s['debut'])} --> {stamp(s['fin'])}\n{s['texte']}\n" for i,s in enumerate(segments,1)),encoding='utf-8')
(out/'transcription.txt').write_text('\n'.join(f"[{s['debut']:.2f}–{s['fin']:.2f}] {s['texte']}" for s in segments)+'\n',encoding='utf-8')
print(f'{len(words)} mots, {len(corrections)} corrections consignées')
