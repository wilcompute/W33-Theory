import itertools, json, sys
from fractions import Fraction as F
from collections import Counter
sys.path.insert(0,'C:/tmp/toe_wt/analysis/orbifolder_n0_drivers')
src=open('C:/tmp/toe_wt/analysis/orbifolder_n0_drivers/a8_so16.py').read().split("oka = [a for a")[0]
exec(src)
V1S={'E6SU3_E8':((F(1,3),F(1,3),F(-2,3))+(F(0),)*5,(F(0),)*8),
     'E6SU3_E6SU3':((F(1,3),F(1,3),F(-2,3))+(F(0),)*5,(F(1,3),F(1,3),F(-2,3))+(F(0),)*5),
     'E7U1_SO14U1':((F(1,3),F(1,3))+(F(0),)*6,(F(2,3),)+(F(0),)*7)}
out={}
for nm,(va,vb) in V1S.items():
    adm=[(a,b) for a in HALF for b in HALF if (dot(a,va)+dot(b,vb)).denominator==1]
    groups={}
    ga={a:name(components(kept(a,va))) for a in {a for a,_ in adm}}
    gb={b:name(components(kept(b,vb))) for b in {b for _,b in adm}}
    cnt=Counter()
    for a,b in adm:
        g=(ga[a],gb[b]); cnt[g]+=1; groups.setdefault(g,(a,b))
    print(nm,len(adm),'groups',len(groups))
    for g,c in cnt.most_common(8): print('   ',c,g)
    out[nm]=[(g,[str(x) for x in ab[0]+ab[1]]) for g,ab in groups.items()]
json.dump(out,open('groups.json','w'),indent=1)
