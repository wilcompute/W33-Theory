#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_fano_seven_qutrit_vm_fabric.json"

from analysis.w33_pass10941_qutrit_universal_instruction_bridge import (
    fourier, phase, cz, symplectic_form,
)
def standard_fano_heptad():
    return tuple(sorted({
        tuple(sorted((i%7,(i+1)%7,(i+3)%7)))
        for i in range(7)
    }))

def complementary_fano_heptad():
    return tuple(sorted({
        tuple(sorted((i%7,(i+2)%7,(i+3)%7)))
        for i in range(7)
    }))

P3=3
# Z7 labels chosen so the repo's cyclic Fano heptad is exactly xor-zero in F2^3.
MODE_TO_F2={
  0:(1,0,0), 1:(0,1,0), 2:(0,0,1), 3:(1,1,0),
  4:(0,1,1), 5:(1,1,1), 6:(1,0,1),
}
F2_TO_MODE={v:k for k,v in MODE_TO_F2.items()}

def xor(a,b):
    return tuple(int(x)^int(y) for x,y in zip(a,b))

def rank2(M):
    A=np.array(M,dtype=np.uint8)%2
    r=0
    for c in range(A.shape[1]):
        z=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if z is None: continue
        A[[r,z]]=A[[z,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
    return r
def gl32():
    out=[]
    for bits in itertools.product((0,1),repeat=9):
        M=np.array(bits,dtype=np.uint8).reshape(3,3)
        if rank2(M)==3: out.append(M)
    assert len(out)==168
    return out

def mode_perm(M):
    p=[]
    for i in range(7):
        v=np.array(MODE_TO_F2[i],dtype=np.uint8)
        w=tuple(map(int,(M@v)%2))
        p.append(F2_TO_MODE[w])
    return tuple(p)

def perm_matrix7(p):
    Q=np.zeros((7,7),dtype=int)
    for i,j in enumerate(p): Q[j,i]=1
    return Q

def cycle_orbit(seed,perms,directed=False):
    if directed:
        canon=lambda e:tuple(e)
    else:
        canon=lambda e:tuple(sorted(e))
    seen={canon(seed)}
    q=deque([canon(seed)])
    while q:
        e=q.popleft()
        for p in perms:
            z=canon((p[e[0]],p[e[1]]))
            if z not in seen:
                seen.add(z);q.append(z)
    return seen

def main():
    std=[tuple(t) for t in standard_fano_heptad()]
    comp=[tuple(t) for t in complementary_fano_heptad()]
    assert len(std)==len(comp)==7

    # Every cyclic standard Fano line is exactly a+b+c=0 in F2^3.
    for L in std:
        a,b,c=(MODE_TO_F2[i] for i in L)
        assert xor(xor(a,b),c)==(0,0,0)

    edges=list(itertools.combinations(range(7),2))
    assert len(edges)==21
    completion={}
    by_completion=Counter()
    for i,j in edges:
        k=F2_TO_MODE[xor(MODE_TO_F2[i],MODE_TO_F2[j])]
        assert k not in (i,j)
        completion[(i,j)]=k
        by_completion[k]+=1
    assert set(by_completion.values())=={3}
    mats=gl32()
    perms={mode_perm(M) for M in mats}
    assert len(perms)==168
    assert len(cycle_orbit((0,1),perms))==21
    assert len(cycle_orbit((0,1),perms,directed=True))==42

    J=symplectic_form()
    for p in perms:
        Q=perm_matrix7(p)
        S=np.block([[Q,np.zeros((7,7),dtype=int)],
                    [np.zeros((7,7),dtype=int),Q]])%P3
        assert np.array_equal((S.T@J@S)%P3,J%P3)
        # Primitive conjugation checks on a representative local and pair gate.
        Sinv=S.T
        assert np.array_equal((S@fourier(0)@Sinv)%3,fourier(p[0]))
        assert np.array_equal((S@phase(0)@Sinv)%3,phase(p[0]))
        assert np.array_equal((S@cz(0,1)@Sinv)%3,cz(p[0],p[1]))

    vm=json.loads(
        (ROOT/"data/w33_pass10941_qutrit_universal_instruction_bridge.json").read_text()
    )
    rows=vm["seven_qutrit_clifford_lowering"]["lowerings"]
    pair_support=set()
    for row in rows:
        for op in row["clifford_macro"]:
            if op.startswith("CZ"):
                body=op.split("Z",1)[1].split("^",1)[0]
                i,j=map(int,body.split(","))
                pair_support.add(tuple(sorted((i,j))))
    assert pair_support=={(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)}
    # The current VM therefore uses a Hamiltonian path in the full K7 fabric.
    assert len(pair_support)==6
    assert set(sum(([a,b] for a,b in pair_support),[]))==set(range(7))

    # Symmetry completion of any one pair gives all 21 pair couplers.
    orbit_edges=cycle_orbit(next(iter(pair_support)),perms)
    assert orbit_edges==set(edges)

    # The two Fano heptads triangulate K7 on a torus.
    faces=set(std)|set(comp)
    assert len(faces)==14
    edge_mult=Counter()
    for tri in faces:
        for e in itertools.combinations(tri,2):
            edge_mult[tuple(sorted(e))]+=1
    assert len(edge_mult)==21 and set(edge_mult.values())=={2}
    assert 7-21+14==0

    out={
      "schema":"w33.20260924.fano_seven_qutrit_vm_fabric.v1",
      "status":"PASS_SEVEN_QUTRIT_VM_IS_FANO_INDEXED_K7_CSASZAR_FABRIC",
      "mode_codec":{
        "mode_to_nonzero_F2_3":{str(k):list(v) for k,v in MODE_TO_F2.items()},
        "seven_modes":"PG(2,2) points = nonzero F2^3 vectors",
        "standard_Fano_lines":[list(x) for x in std],
        "line_law":"u+v+w=0 over F2^3",
      },
      "coupler_fabric":{
        "undirected_CZ_pairs":21,
        "directed_pair_latches":42,
        "pair_completion_counts":{str(k):v for k,v in sorted(by_completion.items())},
        "all_pairs_are_one_GL3_2_orbit":True,
        "all_directed_pairs_are_one_GL3_2_orbit":True,
        "Csaszar_1_skeleton":"K7",
        "torus_faces":14,
        "Euler_characteristic":0,
        "faces_split":"7 standard Fano + 7 complementary Fano",
      },
      "symmetry":{
        "GL3_2_order":len(perms),
        "identification":"GL(3,2)=PSL(2,7), order 168",
        "embedded_in_Sp14_3_as_mode_permutations":True,
        "conjugates_F_P_CZ_primitives_equivariantly":True,
        "natural_168_address_set":"the 168 Fano collineations themselves",
      },
      "Pass10941_VM":{
        "status":vm["status"],
        "existing_pair_couplers":[list(x) for x in sorted(pair_support)],
        "existing_pair_graph":"Hamiltonian path P7",
        "existing_pair_coupler_count":len(pair_support),
        "full_K7_pair_coupler_count":21,
        "algebraic_closure":vm["seven_qutrit_clifford_lowering"]["target"],
        "reading":(
          "Pass10941 already reaches the full seven-qutrit Clifford target using "
          "only the six P7 pair couplers.  The 21-edge K7/Fano/Csaszar fabric is "
          "therefore a symmetry-completed routing surface, not an algebraic "
          "universality requirement."
        ),
      },
      "BT1349_erratum":{
        "old_claim":"Fano point adjacency by sharing a line is 3-regular",
        "correct_statement":"every pair of Fano points shares one line, so that adjacency is K7 and degree 6",
        "old_script_replay_failed_at_degree_check":True,
        "correct_spectrum":"6^1 + (-1)^6",
      },
      "theorem":(
        "Index the seven qutrit VM registers by the seven nonzero vectors of "
        "F2^3.  The 168 Fano collineations become exact symplectic mode "
        "permutations inside Sp(14,3), acting transitively on all 21 CZ pairs "
        "and all 42 oriented pairs while conjugating F, P and CZ primitives "
        "equivariantly.  The complete pair fabric is K7, the Csaszar torus "
        "1-skeleton, whose 14 faces split into the repo's two Fano heptads.  "
        "The existing Pass10941 compiler needs only a six-edge Hamiltonian path "
        "for full Clifford closure; the remaining edges restore the full Fano "
        "routing symmetry."
      ),
      "boundary":(
        "The 168 group elements provide a mathematically canonical address set, "
        "but this certificate does not claim that the current 168 detector bins "
        "are physically wired one-to-one to those group elements without an "
        "explicit hardware labeling table."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "GL32":len(perms),"CZ_pairs":21,
      "VM_path":sorted(pair_support),
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
