"""Splits the content and Higgs conditions of missing_partner_search.py and runs the doublet-triplet control (50 with 75).  usage: py -3 missing_partner_detail.py"""
import json,sys
src=open('missing_partner_search.py',encoding='utf-8').read().split('HIGGS = {')[0]
g={'__name__':'x'};exec(src,g)
reps,has,lr,weights=g['reps'],g['has'],g['lr_product'],g['weights']
H={(2,1,1,1):'24',(2,2,1):'75',(2,2,2,2):'200',():'1'}
need={'10':((1,1),["(3,1,2/3)","(1,1,-1)"],["(3bar,2,-1/6)"]),'5':((1,),["(1,2,-1/2)"],["(3bar,1,1/3)"])}
res={}
for name,(F,must,mustnot) in need.items():
    content_ok=[]
    for sh,r in reps.items():
        c=r['content']
        if all(has(c,m) for m in must) and not any(has(c,m) for m in mustnot):
            prod=lr(F,sh); hig=[H[s] for s in prod if s in H]
            content_ok.append((r['dim'],sh,hig))
    content_ok.sort()
    res[name]=content_ok
    print(name,'content-ok reps:',len(content_ok),content_ok[:15])
# control: standard missing partner, F = 5_H, light doublet: R must contain conj of (3,1,-1/3) i.e. (3bar,1,1/3) and not (1,2,-1/2) conj of doublet: Higgs 75 with R = 50
c=[]
for sh,r in reps.items():
    cc=r['content']
    if has(cc,"(3bar,1,1/3)") and not has(cc,"(1,2,-1/2)"):
        prod=lr((1,),sh);hig=[H[s] for s in prod if s in H]
        if hig: c.append((r['dim'],sh,hig))
c.sort();print('control doublet-triplet partners:',c[:6]); res['control_DT']=c
json.dump({k:[list(map(str,x)) for x in v] for k,v in res.items()},open('missing_partner_detail.json','w'),indent=1)
