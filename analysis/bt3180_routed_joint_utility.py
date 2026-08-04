#!/usr/bin/env python3
"""Pass 3180: joint detector/route/epoch/curvature/ISA utility."""
from __future__ import annotations
import json,math
from collections import Counter,deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT3180_ROUTED_JOINT_UTILITY_results.json'
TRIS=[(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),(1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),(1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),(3,6,8),(0,4,5),(4,6,7)]
CHANNEL=np.array([[.94,.03,.03],[.08,.86,.06],[.08,.06,.86]])
MODES={'current4':(1.8495219521538164,14.175585133744857,.1388888888888889),'low4':(1.905077507709372,15.216323969288219,.1111111111111111),'fast6':(2.41056972808296,13.72936957018747,.12962962962962962)}
COEFF={'curvature':.35,'route_distance':.025,'route_multiplicity':.008,'isa_capacity':.025,'runtime':.01,'epoch_noncurrent':.03}
def mi(pn,pf,pc,a,aware):
    p=[pn];c=[CHANNEL[0]]
    for t in range(23):p.extend((pf[t],pc[t]));c.extend((CHANNEL[1] if t==a else CHANNEL[0],CHANNEL[2] if t==a else CHANNEL[0]))
    p=np.array(p);c=np.array(c)
    if not aware:c=np.column_stack((c[:,0],c[:,1]+c[:,2]))
    py=p@c;z=0.
    for ph,row in zip(p,c):
        for j,q in enumerate(row):
            if ph>0 and q>0:z+=ph*q*math.log2(q/py[j])
    return z
def route_tables():
    adj=[[] for _ in range(23)]
    for i in range(23):
        for j in range(23):
            if i!=j and set(TRIS[i])&set(TRIS[j]):adj[i].append(j)
    D=[];W=[]
    for s in range(23):
        d=[-1]*23;w=[0]*23;d[s]=0;w[s]=1;q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if d[v]<0:d[v]=d[u]+1;w[v]=w[u];q.append(v)
                elif d[v]==d[u]+1:w[v]+=w[u]
        D.append(d);W.append(w)
    return adj,D,W
def main():
    adj,D,W=route_tables();rng=np.random.default_rng(3180);rows=[]
    for _ in range(64):
        shared=float(rng.uniform(.02,.65));tri=rng.dirichlet(np.ones(23)*.8);split=rng.beta(.8,.8,23);pf=shared*tri*split;pc=shared*tri*(1-split);pn=1-shared
        aware=np.array([mi(pn,pf,pc,a,True) for a in range(23)]);collapsed=np.array([mi(pn,pf,pc,a,False) for a in range(23)]);curv=aware-collapsed
        loc=int(rng.integers(23));epoch=float(rng.uniform(.6,1));price=float(rng.uniform(0,25));avail={'current4':True,'low4':bool(rng.random()<.9),'fast6':bool(rng.random()<.7)};scores={}
        for a in range(23):
            for mode,(cap,L,pcol) in MODES.items():
                if not avail[mode]:continue
                runtime=L*(1+price*pcol);scores[(a,mode)]=(aware[a]+COEFF['curvature']*curv[a]-COEFF['route_distance']*D[loc][a]-COEFF['route_multiplicity']*math.log2(max(1,W[loc][a]))+COEFF['isa_capacity']*cap-COEFF['runtime']*runtime-COEFF['epoch_noncurrent']*(1-epoch)*(mode!='current4'))
        best=max(scores,key=scores.get);base=(int(np.argmax(aware)),'current4');rows.append({'best_action':best[0],'best_mode':best[1],'detector_action':base[0],'utility_gain':scores[best]-scores[base],'origin':loc,'collision_price':price,'epoch_confidence':epoch})
    gains=[r['utility_gain'] for r in rows];out={'schema':'w33.pass3180.routed_joint_utility.v1','scenarios':64,'route_graph':{'connected':True,'degree_min':min(map(len,adj)),'degree_max':max(map(len,adj)),'diameter':max(max(d) for d in D)},'coefficients':COEFF,'action_changes':sum(r['best_action']!=r['detector_action'] for r in rows),'mode_counts':dict(Counter(r['best_mode'] for r in rows)),'utility_gain':{'minimum':min(gains),'mean':sum(gains)/len(gains),'maximum':max(gains)},'rows':rows,'boundary':'Exact for explicit synthetic posteriors, availability draws and programmable utility coefficients; not a physical optimum.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ('action_changes','mode_counts','utility_gain')},sort_keys=True))
if __name__=='__main__':main()
