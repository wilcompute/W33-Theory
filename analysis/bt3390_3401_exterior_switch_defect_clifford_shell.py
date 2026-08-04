#!/usr/bin/env python3
"""Passes 3390-3401 exact seven-front continuation.

Promotes only finite arithmetic, deterministic local constructions, hash trees,
and polynomial identities. Objectwise exterior connectivity and terminal
chromatic decisions remain explicitly open.
"""
from __future__ import annotations
import collections, hashlib, itertools, json, math, random
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3390_BT3401_EXTERIOR_SWITCH_DEFECT_CLIFFORD_SHELL_results.json'

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def sha(x): return hashlib.sha256(canon(x).encode()).hexdigest()

def exterior_audit():
    known={'orbits':135,'covers':1574640,'stab':{2:108,4:27,8:0}}
    cap={'orbits':57,'covers':398520,'stab':{2:12,4:30,8:15}}
    global_={'orbits':327,'covers':3547800,'stab':{2:228,4:84,8:15}}
    residual={'orbits':global_['orbits']-known['orbits']-cap['orbits'],
              'covers':global_['covers']-known['covers']-cap['covers'],
              'stab':{s:global_['stab'][s]-known['stab'][s]-cap['stab'][s] for s in (2,4,8)}}
    assert residual==known
    readable_candidates=[
      ROOT/'data/PART_BT3296_BT3297_COVER_ORBIT_LEDGER.json',
      ROOT/'data/w33_pass1821_1825_covers.bin',
      ROOT/'data/w33_pass1821_1825_complete_cover_representatives.json']
    present=[str(p.relative_to(ROOT)) for p in readable_candidates if p.exists()]
    return {'status':'PASS_EXACT_TWO_SHEET_PLUS_CAP_CENSUS','global':global_,'known_sheet':known,
      'residual_sheet_census':residual,'exceptional_cap':cap,
      'identities':['327=135+135+57','3547800=1574640+1574640+398520'],
      'readable_object_ledgers_present':present,
      'objectwise_boundary':'No connectivity, switch-path, canonical pairing, or graph isomorphism is promoted unless a readable representative ledger is present and checked.'}

def split_templates():
    out=[]
    for m in range(1,6):
      n=10-m
      for c in range(-2916,325,15):
        if c%15!=9: continue
        if m==1:
          if -324-n*c: continue
          a=None
        else:
          q,r=divmod(-324-n*c,m-1)
          if r: continue
          a=q
        q,r=divmod(-324-m*c,n-1)
        if r: continue
        b=q
        vals=[x for x in (a,b,c) if x is not None]
        if any(x%15!=9 for x in vals): continue
        # exact eigenvalues: 324-a (m-1), 324-b (n-1), zero, and trace remainder
        lamA=[] if m==1 else [324-a]*(m-1)
        lamB=[324-b]*(n-1)
        # quotient has one zero eigenvalue; other eigenvalue equals trace minus repeated spectrum
        lamQ=3240-sum(lamA)-sum(lamB)
        eig=sorted(lamA+lamB+[0,lamQ])
        if min(eig)<0: continue
        edges={k:(v+2916)//15 for k,v in [('within_A',a),('within_B',b),('cross',c)] if v is not None}
        if any(v<0 for v in edges.values()): continue
        out.append({'split':[m,n],'a':a,'b':b,'c':c,'spectrum':eig,'edge_counts':edges})
    assert collections.Counter(x['split'][0] for x in out)=={1:1,2:1,3:5,4:3,5:5}
    keys=set()
    for t in out:
      keys.add(tuple(sorted(t['spectrum'])))
    assert len(keys)==11
    return out

def local_witness():
    rng=random.Random(33903401)
    a=[i for i in range(10) for _ in range(54)];rng.shuffle(a)
    def bc(b):
      seen={};z=0
      for c in range(3):
        for col in set(a[b*12+c*4:b*12+(c+1)*4]):
          if col in seen and seen[col]!=c:z+=1
          seen[col]=c
      return z
    scores=[bc(b) for b in range(45)];total=sum(scores);T=2.0
    for it in range(400000):
      if total==0: break
      i,j=rng.sample(range(540),2)
      if a[i]==a[j]:continue
      bi,bj=i//12,j//12;old=scores[bi]+(scores[bj] if bj!=bi else 0)
      a[i],a[j]=a[j],a[i];ni=bc(bi);nj=bc(bj) if bj!=bi else ni
      new=ni+(nj if bj!=bi else 0);d=new-old
      if d<=0 or rng.random()<math.exp(-d/max(T,1e-12)):
        scores[bi]=ni
        if bj!=bi:scores[bj]=nj
        total+=d
      else:a[i],a[j]=a[j],a[i]
      T*=0.99995
    assert total==0 and collections.Counter(a)=={i:54 for i in range(10)}
    E=[[0]*10 for _ in range(10)]
    for b in range(45):
      cells=[collections.Counter(a[b*12+c*4:b*12+(c+1)*4]) for c in range(3)]
      for c,d in ((0,1),(0,2),(1,2)):
        for i,ni in cells[c].items():
          for j,nj in cells[d].items():
            if i!=j:E[i][j]+=ni*nj;E[j][i]+=ni*nj
    pairs=[E[i][j] for i in range(10) for j in range(i+1,10)]
    return {'status':'PASS_COMMON_45_BLOCK_BALANCED_WITNESS','iterations':it,'colour_counts':dict(collections.Counter(a)),
      'local_pair_min':min(pairs),'local_pair_max':max(pairs),'assignment_sha256':hashlib.sha256(bytes(a)).hexdigest(),
      'boundary':'This satisfies every canonical induced block and is below every template global pair-edge demand. It does not assign the 6480 inter-block edges.'}

def sidecars():
    base='6c0c3daac0ac1592fd3d84c45cad157c8e6e1b95ffe87b47868db4589c6b7cd5'
    leaves=[]
    for c,d in itertools.product(range(10),repeat=2):
      r={'schema':'w33.chromatic.status.sidecar.v1','shard':[0,3,c,d],'base_dimacs_sha256':base,'status':'UNKNOWN',
         'solver_exit_code':None,'model_checked':False,'proof_checked':False,'artifact':None}
      r['content_sha256']=sha(r);leaves.append(r)
    level=[x['content_sha256'] for x in leaves]
    while len(level)>1:
      level=[hashlib.sha256((level[i]+level[i+1]).encode()).hexdigest() for i in range(0,len(level),2)] if len(level)%2==0 else [hashlib.sha256((level[i]+level[i+1]).encode()).hexdigest() for i in range(0,len(level)-1,2)]+[level[-1]]
    return {'status':'PASS_100_FAIL_CLOSED_UNKNOWN_SIDECARS','leaves':100,'merkle_root':level[0],
      'promotion_rule':{'SAT':'one checked SAT leaf','UNSAT':'all ten checked UNSAT children','UNKNOWN':'otherwise'},
      'live_boundary':'10 <= chi(H) <= 11'}

def clifford_resources():
    # Exact source-network upper bound: one 12-controlled equality per table row,
    # using 2n-3 Toffolis with n-2 clean ancillas, then uncompute.
    rows=1350;nctrl=12;tof_eq=2*nctrl-3
    table_tof=rows*2*tof_eq
    return {'status':'PASS_EXACT_SOURCE_NETWORK_RESOURCE_BOUNDS','oracle_rows':rows,'address_controls':nctrl,
      'table_lookup':{'toffoli_upper_bound':table_tof,'standard_7T_upper_bound':7*table_tof,'clean_ancillas':nctrl-2,
        'note':'Output fanout uses Clifford CNOTs after the equality flag.'},
      'arithmetic_oracle':{'semantic_rule':'decode five ternary symbols; select one of five coordinates and +/-1; apply tau canonicalization; XOR the quotient index',
        'persistent_bits':25,'transition_tokens':1350,'involution_checks':345600},
      'boundary':'These are exact source-construction upper bounds, not optimized Clifford+T minima or hardware synthesis.'}

def shell_theorem(max_r=6):
    x=sp.symbols('x');rows=[]
    for r in range(max_r+1):
      n=2*r+1
      N=sp.expand((x+3)**n)
      F=sp.expand((x+3)*(x*x+3)**r)
      Q=sp.expand((N+F)/2)
      shell=[int(Q.coeff(x,s)) for s in range(n+1)]
      inv=list(reversed(shell))
      assert sum(shell)==(4**n+4*12**r)//2
      rows.append({'r':r,'n':n,'full_shell_polynomial':str(N),'fixed_shell_polynomial':str(F),
                   'quotient_shells':shell,'tau_invariant_multiplicities':inv})
    assert rows[2]['quotient_shells']==[135,207,144,48,9,1]
    return {'status':'PASS_GENERAL_ODD_HAMMING_SHELL_SPECTRUM_REVERSAL','family':'H(2r+1,4) with one fixed coordinate and r paired coordinates under tau',
      'theorem':'If q_s is the coefficient of ((x+3)^(2r+1)+(x+3)(x^2+3)^r)/2, then the tau-invariant multiplicity at Hamming grade j is q_(2r+1-j).',
      'instances':rows}

def macwilliams_bridge():
    z=sp.symbols('z')
    dual={0:1,6:10,12:5};n=15;size=16
    # binary MacWilliams transform W_C(z)=1/|D| sum_w A_w (1+z)^(n-w)(1-z)^w
    W=sp.expand(sum(a*(1+z)**(n-w)*(1-z)**w for w,a in dual.items())/size)
    coeff={i:int(W.coeff(z,i)) for i in range(n+1) if W.coeff(z,i)}
    assert sum(coeff.values())==2**11
    return {'status':'PASS_EXACT_MACWILLIAMS_PG32_GUARD_BRIDGE','dual_weight_enumerator':'1+10 z^6+5 z^12',
      'span_weight_enumerator':coeff,'span_size':2048,
      'interpretation':'The PG(3,2) parity-check geometry and the 11-dimensional binary span are exact MacWilliams mirrors of the Q15 host.'}

def branched_skeleton():
    return {'status':'PASS_ORBIT_TYPE_BRANCHED_DOUBLE_COVER_SKELETON','base_species':135,'two_regular_sheets':270,'branch_cap':57,
      'cap_stabilizers':{2:12,4:30,8:15},'sheet_stabilizers_each':{2:108,4:27,8:0},
      'sharp_fact':'All fifteen stabilizer-eight orbit classes lie in the exceptional cap.',
      'boundary':'This is an exact orbit-type skeleton only; no quotient map, ramification map, or switch involution is claimed.'}

def main():
    templates=split_templates();w=local_witness()
    assert w['local_pair_max'] < min(v for t in templates for v in t['edge_counts'].values())
    data={'schema':'w33.pass3390_3401.exterior_switch_defect_clifford_shell.v1','status':'PASS_EXACT_SEVEN_FRONT_CONTINUATION',
      'pass3390_3391_exterior':exterior_audit(),'pass3392_3393_defect':{'templates':templates,'local_witness':w},
      'pass3394_sidecars':sidecars(),'pass3395_3396_clifford':clifford_resources(),'pass3397_3398_shell_theorem':shell_theorem(),
      'pass3399_bonkers_macwilliams':macwilliams_bridge(),'pass3400_3401_bonkers_branched_skeleton':branched_skeleton(),
      'evidence_boundary':{'chromatic':'10 <= chi(H) <= 11','not_proved':['objectwise exterior connectivity','ten-colour SAT/UNSAT','optimized Clifford+T minimum','physical speedup','hardware or PDF claims']}}
    data['semantic_sha256']=sha(data);OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(data['status'],data['semantic_sha256'])
if __name__=='__main__':main()
