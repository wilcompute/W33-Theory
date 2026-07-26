from __future__ import annotations
import itertools, json, math, time
from collections import Counter, deque
from pathlib import Path
import numpy as np
from w33_pass1060_1064_core import build_w33, J, normalize

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1075_gsp43_character_fingerprint.json'
GENERATOR_POINT_INDICES=[0,1,4,5,13]
POW3=np.array([3**i for i in range(16)],dtype=np.int64)

def mm(A,B):return tuple(sum(A[4*i+k]*B[4*k+j] for k in range(4))%3 for i in range(4) for j in range(4))
def eye():return tuple(1 if i==j else 0 for i in range(4) for j in range(4))
def transvection(v):
    vv=np.array(v,dtype=np.int64)%3;M=(np.eye(4,dtype=np.int64)+np.outer(vv,J@vv))%3
    return tuple(int(x) for x in M.flat)
def inv4(A):
    M=np.array(A,dtype=np.int64).reshape(4,4)%3;aug=np.concatenate([M,np.eye(4,dtype=np.int64)],axis=1);r=0
    for c in range(4):
        p=next(i for i in range(r,4) if aug[i,c]%3);aug[[r,p]]=aug[[p,r]];aug[r]=aug[r]*pow(int(aug[r,c]),-1,3)%3
        for i in range(4):
            if i!=r and aug[i,c]:aug[i]=(aug[i]-aug[i,c]*aug[r])%3
        r+=1
    return tuple(int(x) for x in aug[:,4:].flat)
def mat_order(A):
    x=eye()
    for n in range(1,200):
        x=mm(A,x)
        if x==eye():return n
    raise RuntimeError
def det_mod3(A):
    M=np.array(A,dtype=np.int64).reshape(4,4)%3;d=1
    for c in range(4):
        p=next((i for i in range(c,4) if M[i,c]),None)
        if p is None:return 0
        if p!=c:M[[c,p]]=M[[p,c]];d=(-d)%3
        d=d*int(M[c,c])%3;M[c]=M[c]*pow(int(M[c,c]),-1,3)%3
        for i in range(c+1,4):M[i]=(M[i]-M[i,c]*M[c])%3
    return d
def rank_mod3(A):
    M=np.array(A,dtype=np.int64)%3;r=0
    for c in range(M.shape[1]):
        p=next((i for i in range(r,M.shape[0]) if M[i,c]),None)
        if p is None:continue
        M[[r,p]]=M[[p,r]];M[r]=M[r]*pow(int(M[r,c]),-1,3)%3
        for i in range(M.shape[0]):
            if i!=r and M[i,c]:M[i]=(M[i]-M[i,c]*M[r])%3
        r+=1
    return r
def enumerate_group(gens):
    I=eye();seen={I:0};elems=[I];q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=mm(g,x)
            if y not in seen:seen[y]=len(elems);elems.append(y);q.append(y)
    return elems
def packed_keys(arr):return (arr.reshape(len(arr),16).astype(np.int64)*POW3).sum(axis=1)
def conj_transitions(elems,gens):
    arr=np.array(elems,dtype=np.int16).reshape(-1,4,4);keys=packed_keys(arr);order=np.argsort(keys);sk=keys[order];out=[]
    for g in gens:
        G=np.array(g,dtype=np.int16).reshape(4,4);Gi=np.array(inv4(g),dtype=np.int16).reshape(4,4)
        C=np.einsum('nab,bc->nac',np.einsum('ab,nbc->nac',Gi,arr,optimize=True)%3,G,optimize=True)%3
        ck=packed_keys(C);pos=np.searchsorted(sk,ck);assert np.all(sk[pos]==ck);out.append(order[pos].astype(np.int32))
    return np.stack(out)
def conjugacy_classes(trans):
    n=trans.shape[1];unseen=np.ones(n,dtype=bool);classes=[]
    for seed in range(n):
        if not unseen[seed]:continue
        unseen[seed]=False;orb=[seed];q=deque([seed])
        while q:
            x=q.popleft()
            for y in trans[:,x]:
                y=int(y)
                if unseen[y]:unseen[y]=False;orb.append(y);q.append(y)
        classes.append(orb)
    return classes
def all_spreads(lines,npts=40):
    onpt=[[li for li,L in enumerate(lines) if p in L] for p in range(npts)];sol=[]
    def rec(ch,used):
        if len(used)==npts:sol.append(tuple(sorted(ch)));return
        p=next(x for x in range(npts) if x not in used)
        for li in onpt[p]:
            if set(lines[li])&used:continue
            rec(ch+[li],used|set(lines[li]))
    rec([],set());return sorted(set(sol))
def perm_profile(im):
    seen=[False]*len(im);C=Counter()
    for i in range(len(im)):
        if not seen[i]:
            j=i;l=0
            while not seen[j]:seen[j]=True;j=im[j];l+=1
            C[l]+=1
    return dict(sorted(C.items()))
def action_data(A,w,spreads,frames):
    M=np.array(A,dtype=int).reshape(4,4);pim=[w.pidx[normalize(M@np.array(p,dtype=int)%3)] for p in w.points]
    lidx={tuple(L):i for i,L in enumerate(w.lines)};lim=[lidx[tuple(sorted(pim[x] for x in L))] for L in w.lines]
    sidx={s:i for i,s in enumerate(spreads)};sim=[sidx[tuple(sorted(lim[x] for x in s))] for s in spreads]
    fidx={f:i for i,f in enumerate(frames)};fim=[fidx[tuple(sorted((lim[a],lim[b])))] for a,b in frames]
    return {'fixed_points':sum(i==x for i,x in enumerate(pim)),'point_cycles':perm_profile(pim),'fixed_lines':sum(i==x for i,x in enumerate(lim)),'fixed_spreads':sum(i==x for i,x in enumerate(sim)),'fixed_frames':sum(i==x for i,x in enumerate(fim))}
def main():
    started=time.time();w=build_w33();spgens=[transvection(w.points[i]) for i in GENERATOR_POINT_INDICES];S=tuple(int(x) for x in np.diag([1,2,1,2]).flat)
    Sm=np.array(S).reshape(4,4);assert np.array_equal((Sm.T@J@Sm)%3,(2*J)%3)
    elems=enumerate_group(spgens+[S]);assert len(elems)==103680;classes=conjugacy_classes(conj_transitions(elems,spgens+[S]))
    spreads=all_spreads(w.lines);frames=[(a,b) for a in range(40) for b in range(a+1,40) if not(set(w.lines[a])&set(w.lines[b]))];assert len(spreads)==36 and len(frames)==540
    records=[]
    for cls in classes:
        A=elems[min(cls)];M=np.array(A,dtype=int).reshape(4,4);mult=1 if np.array_equal((M.T@J@M)%3,J) else 2;ad=action_data(A,w,spreads,frames)
        records.append({'class_size':len(cls),'centralizer_order':103680//len(cls),'order':mat_order(A),'multiplier':mult,'det_mod3':det_mod3(A),'trace_mod3':int(np.trace(M)%3),'fixed_space_dim':4-rank_mod3((M-np.eye(4,dtype=int))%3),**ad,'representative':list(A)})
    records.sort(key=lambda r:(r['multiplier'],r['order'],r['class_size'],r['trace_mod3'],r['fixed_points'],r['fixed_spreads'],r['fixed_frames']))
    def ip(a,b,N=103680,inner=False):return sum(r['class_size']*r[a]*r[b] for r in records if not inner or r['multiplier']==1)//N
    ranks={'full_point_action_rank':ip('fixed_points','fixed_points'),'full_spread_action_rank':ip('fixed_spreads','fixed_spreads'),'full_frame_action_rank':ip('fixed_frames','fixed_frames'),'inner_point_action_rank':ip('fixed_points','fixed_points',51840,True),'inner_spread_action_rank':ip('fixed_spreads','fixed_spreads',51840,True),'inner_frame_action_rank':ip('fixed_frames','fixed_frames',51840,True)}
    eps_point=sum(r['class_size']*r['fixed_points']*(1 if r['multiplier']==1 else -1) for r in records)//103680
    checks={'explicit_group_is_GSp43_by_defining_similitude_generators':len(elems)==103680,'order_is_103680':len(elems)==103680,'class_sizes_sum_to_group_order':sum(r['class_size'] for r in records)==103680,'every_centralizer_divides_order':all(103680%r['class_size']==0 for r in records),'inner_half_has_order_51840':sum(r['class_size'] for r in records if r['multiplier']==1)==51840,'outer_half_has_order_51840':sum(r['class_size'] for r in records if r['multiplier']==2)==51840,'full_point_permutation_character_has_rank3':ranks['full_point_action_rank']==3,'full_spread_permutation_character_has_rank3':ranks['full_spread_action_rank']==3,'inner_frame_permutation_character_has_rank32':ranks['inner_frame_action_rank']==32,'outer_extension_fuses_frame_orbitals_to_rank22':ranks['full_frame_action_rank']==22,'outer_sign_not_contained_in_point_permutation_character':eps_point==0}
    assert all(checks.values()),(checks,ranks,eps_point,len(records))
    out={'schema':'w33.pass1075.gsp43.character_fingerprint.v1','status':'PASS','headline':'The order-103680 signed outer extension is identified intrinsically as GSp(4,3): the exact matrix group generated by Sp(4,3) transvections and one multiplier-2 similitude. Its complete conjugacy-class fingerprint is computed, together with the point, spread, and frame permutation characters.','identification':{'group':'GSp(4,3)','order':103680,'derived_subgroup_expected':'Sp(4,3), order 51840','quotient':'multiplier C2','reason':'Every enumerated matrix satisfies M^T J M = mu(M) J with mu in {1,2}; the generators contain Sp(4,3) and a multiplier-2 similitude, and the enumeration has the defining GSp order 103680.'},'number_of_conjugacy_classes':len(records),'class_records':records,'permutation_character_inner_products':ranks,'outer_sign_inner_product_with_point_character':eps_point,'check_count':len(checks),'checks':checks,'gap_ctbllib_script':'analysis/w33_pass1075_gsp43_character_table.g','scope':'Exact F3 matrix enumeration and exact finite permutation characters. The native computation identifies the group as GSp(4,3) without guessing an ATLAS suffix. The companion GAP script requests the irreducible character table when GAP/CTblLib is available.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','classes':len(records),'ranks':ranks,'seconds':round(time.time()-started,3)},indent=2))
if __name__=='__main__':main()
