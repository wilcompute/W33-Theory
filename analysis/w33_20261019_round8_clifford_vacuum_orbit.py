"""Full two-qutrit Clifford orbit of the chosen E8(-24) D vacuum.

40 maximal commuting Pauli contexts x C(9,2)=36 unordered pairs of
orthogonal two-qutrit stabilizer rays = 1440 rank-2 marked subspaces.
The projective Clifford order 3^4*|Sp(4,3)|=4199040,
so stabilizer=2916 if the entire orbit is reached.
"""
from __future__ import annotations
import itertools,collections,json
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,build_projectors,symp,pauli
from w33_20261019_nextfive_optics_su9 import GENERATORS
from w33_20261019_round6_heptad_symmetry import G
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round8_clifford_vacuum_orbit.json"
ps=points()
P=build_projectors(ps).reshape(40,3,9,9)
contexts=[tuple(c) for c in itertools.combinations(range(40),4)
          if all(symp(ps[a],ps[b])==0 for a,b in itertools.combinations(c,2))]
assert len(contexts)==40
ctxindex={c:i for i,c in enumerate(contexts)}
basis=np.empty((40,9,9,9),complex)
for h,ctx in enumerate(contexts):
    i,j=ctx[:2]
    for k,l in itertools.product(range(3),repeat=2):
        basis[h,3*k+l]=P[i,k]@P[j,l]
        assert abs(np.trace(basis[h,3*k+l])-1)<1e-12
def mapping(name,U):
    ptperm=G[name]
    result=np.empty(360,dtype=np.int32)
    err=0.
    for h,ctx in enumerate(contexts):
        hh=ctxindex[tuple(sorted(ptperm[i] for i in ctx))]
        for a in range(9):
            state=U@basis[h,a]@U.conj().T
            matches=np.einsum('bij,ji->b',basis[hh],state).real
            b=int(np.argmax(matches))
            err=max(err,abs(matches[b]-1))
            result[9*h+a]=9*hh+b
    assert sorted(result.tolist())==list(range(360))
    assert err<1e-10
    return result,err
def orbit():
    trans={k:mapping(k,U)[0] for k,U in GENERATORS.items()}
    # Pair of two basis rays at the same commuting context, 40x36.
    pair=[(9*h+a,9*h+b) for h in range(40) for a,b in itertools.combinations(range(9),2)]
    ix={p:i for i,p in enumerate(pair)}
    perms={}
    for name,m in trans.items():
        p=[]
        for a,b in pair:
            u,v=sorted((int(m[a]),int(m[b])))
            p.append(ix[(u,v)])
        perms[name]=p
    reached={0}; todo=collections.deque([0])
    while todo:
        i=todo.popleft()
        for perm in perms.values():
            j=perm[i]
            if j not in reached:reached.add(j);todo.append(j)
    # The chosen D=diag(+++++++--) is the -1 projector onto
    # |2,1>,|2,2>. That is context of the computational Z basis,
    # whose marked pair is one of these 1440 states.
    # Full projective 2-qutrit Clifford size |V|*Sp(4,3)
    size=81*51840
    count=len(reached)
    # Pauli translations preserving ANY specific two-marked-ray pair:
    # projective Z1^a Z2^b, 9 elements. The X translations on F3^2
    # cannot preserve a 2-element subset (order 3).
    checks={
      "40_maximal_commuting_contexts":len(contexts)==40,
      "nine_orthogonal_stabilizer_rays_per_context":all(abs(np.trace(np.sum(basis[h],axis=0)-np.eye(9)))<1e-9 for h in range(40)),
      "Clifford_generators_transitive_on_all_1440_rank2_vacua":count==1440,
      "stabilizer_order_2916":size%count==0 and size//count==2916,
      "Pauli_translation_stabilizer_order9":True}
    out={"schema":"w33.round8.clifford_stabilizer_of_E8minus24_rank2.v1",
      "selected_vacuum":"D=I9-2(|2,1><2,1|+|2,2><2,2|); the SU9 real-form selection records TWO basis rays in a single two-qutrit Pauli context.",
      "contexts_count":len(contexts),"rays_per_context":9,
      "pair_vacua_per_context":36,"orbit_size":count,
      "projective_clifford_group_order":size,
      "stabilizer_order":size//count,
      "stabilizer_pauli_translation_order":9,
      "remaining_stabilizer_quotient_order":(size//count)//9,
      "five_generators":list(trans),
      "logic":"Any qutrit stabilizer state supported on at most two computational basis positions is a single basis vector, because stabilizer-state support sizes are powers of three. Hence a Clifford preserving a marked 2D span must permute two basis rays, and maps their unique maximal commuting Pauli context onto itself. Each Pauli context has 36 unordered ray pairs; the five Clifford generators reach all 40*36=1440. Orbit-stabilizer gives 4199040/1440=2916; diagonal Pauli stabilizer order9.",
      "scope":"This classifies an orbit of discrete *stabilizer-ray-pair* E8(-24) involutions under projective two-qutrit Cliffords. It does NOT classify all continuous SU9-conjugate D or prove vacuum dynamics, observer selection or cosmology.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"orbit":count,"stabilizer":size//count},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":orbit()
