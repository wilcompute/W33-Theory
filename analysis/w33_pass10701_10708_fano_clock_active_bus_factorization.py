#!/usr/bin/env python3
"""Pass10701-10708 outside-box: exact Fano clock x local-state factorization of the 168 active bus.

Pass10677 identifies the C7 harmonic factor through the Singer difference set
D={1,2,4}.  Its affine Singer normalizer

    H = {x -> a + 2^k x : a in C7, k in C3}

has order 21 and acts regularly on the 21 Fano flags.

BT1422 independently identifies the active Holonet bus with the full Fano group
G=GL(3,2), |G|=168, indexed as 21 flags x 8 states of a base-flag stabilizer
K of order 8 (D8).

Because H acts regularly on flags, H intersects K trivially.  Since
|H||K|=21*8=168=|G|, multiplication gives an exact factorization

    G = H K, H intersect K = 1.

This is a Zappa-Szep/exact factorization, not asserted to be a direct or
semidirect product.  It upgrades the hardware indexing from an orbit-count
identity to an objectwise controller: every active Fano automorphism is uniquely
(clock element h in C7:C3) times (local D8 flag-state k).
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10701_10708_FANO_CLOCK_ACTIVE_BUS_FACTORIZATION.json'
D={1,2,4}

def lines(): return {tuple(sorted((b+d)%7 for d in D)) for b in range(7)}

def perm_comp(p,q): return tuple(p[q[i]] for i in range(7))
def perm_inv(p):
    z=[0]*7
    for i,j in enumerate(p):z[j]=i
    return tuple(z)

def H_group():
    return {tuple((a+pow(2,k,7)*x)%7 for x in range(7)) for a in range(7) for k in range(3)}

def full_fano_auts(L):
    Lset=set(L);out=[]
    for p in itertools.permutations(range(7)):
      image={tuple(sorted(p[x] for x in line)) for line in L}
      if image==Lset:out.append(tuple(p))
    return set(out)

def main():
    L=lines();assert len(L)==7
    flags={(p,line) for line in L for p in line};assert len(flags)==21
    H=H_group();assert len(H)==21
    G=full_fano_auts(L);assert len(G)==168 and H<=G
    base_flag=next(iter(flags));bp,bl=base_flag
    K={g for g in G if g[bp]==bp and tuple(sorted(g[x] for x in bl))==bl}
    assert len(K)==8
    # H is regular on flags.
    def act_flag(g,f):
      p,line=f;return (g[p],tuple(sorted(g[x] for x in line)))
    orbit={act_flag(h,base_flag) for h in H};assert orbit==flags
    HcapK=H&K;assert len(HcapK)==1
    HK={perm_comp(h,k) for h in H for k in K}
    assert HK==G and len(HK)==168
    # Unique decomposition follows from trivial intersection and cardinality.
    decomps={g:0 for g in G}
    for h in H:
      for k in K:decomps[perm_comp(h,k)]+=1
    assert set(decomps.values())=={1}

    bt=json.loads((ROOT/'data/bt1422_fano_168_s3_optimizer_bridge.json').read_text())
    assert bt['verified'] and bt['counts']['fano_flags']==21 and bt['counts']['flag_stabilizer']==8 and bt['counts']['active_bins']==168

    out={
      'schema':'w33.pass10701_10708.fano_clock_active_bus_factorization.v1','status':'PASS','passes':'10701-10708','outside_box':True,
      'Fano':{'points':7,'lines':7,'flags':21,'full_group':'GL(3,2)=PSL(2,7)','full_group_order':168},
      'clock_factor':{'group':'C7:C3','order':21,'model':'x -> a + 2^k x on C7','difference_set':[1,2,4],'acts_regularly_on_flags':True},
      'local_factor':{'group':'base-flag stabilizer D8','order':8,'source':'BT1422'},
      'exact_factorization':{'identity':'GL(3,2) = (C7:C3) * D8','intersection_order':1,'unique_decomposition':True,'type':'exact/Zappa-Szep factorization; not claimed direct or semidirect'},
      'Holonet_bridge':{
        'BT1422_active_bins':168,'old_indexing':'21 Fano flags x 8 local D8 flag-stabilizer states',
        'new_indexing':'21 Singer-clock elements x 8 local D8 states',
        'objectwise_reason':'a unique clock element sends the base flag to each of the 21 hardware flag channels; the residual unique factor is the local flag stabilizer state'},
      'theorem':'The C7:C3 harmonic clock factor is an exact global controller for the already-certified 168-bin Fano active bus. With K=D8 the base-flag stabilizer, GL(3,2) factors exactly as (C7:C3)K with trivial intersection, so every active Fano automorphism has a unique clock-element times local-state decomposition.',
      'boundary':'Exact finite-group and existing-hardware-index theorem. It does not assert that the full 105:6 arithmetic controller is a hardware symmetry, nor that the 10 BT1421 theta packets already carry D10 without an additional routing design.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','factorization':'GL3(2)=(C7:C3)*D8','unique':True,'active_bins':168}))
if __name__=='__main__':main()
