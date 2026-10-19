"""Round6 front2: Exhaustive heptad outcome spectral families, exact
F3^4 Pauli-translation quotient, and transitivity under concrete Clifford
generators on ALL 2880 noncommuting heptads.
"""
from __future__ import annotations
import itertools,json,collections
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,pauli,symp,build_projectors
from w33_20261019_tick_commutator_extremum import maximal_cliques
from w33_20261019_nextfive_optics_su9 import GENERATORS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round6_heptad_symmetry.json"
pts=points();P=build_projectors(pts).reshape(40,3,9,9); ptindex={x:i for i,x in enumerate(pts)}
adj=[sum(int(i!=j and symp(pts[i],pts[j])!=0)<<j for j in range(40)) for i in range(40)]
cliques=maximal_cliques(adj)
all7=[tuple(sorted(q)) for q in cliques if len(q)==7]
assert len(all7)==2880
H=all7[0]
def canon(v):
    v=tuple(int(k)%3 for k in v)
    t=next(x for x in v if x)
    return tuple((x*t)%3 for x in v)
def vact(U,v):
    M=U@pauli(v)@U.conj().T
    for q in itertools.product(range(3),repeat=4):
        if not any(q):continue
        D=pauli(q)
        if abs(abs(np.trace(M@D.conj().T))-9)<1e-8:
            return canon(q)
    raise ValueError("not Clifford")
def mapgenerator(U):
    qbasis=[vact(U,p) for p in pts]
    return tuple(ptindex[q] for q in qbasis)
def action(G,h):
    return tuple(sorted(G[x] for x in h))
G={k:mapgenerator(V) for k,V in GENERATORS.items()}
reached={H}
queue=collections.deque([H])
while queue:
    h=queue.popleft()
    for g in G.values():
        b=action(g,h)
        if b not in reached:reached.add(b);queue.append(b)
def spectrum(k):
    Q=sum(P[p,j] for p,j in zip(H,k))/7
    return tuple(np.round(np.linalg.eigvalsh(Q),10).tolist())
classes=collections.defaultdict(list)
for k in itertools.product(range(3),repeat=7):
    classes[spectrum(k)].append(k)
# Pauli D_t sends P_p,k to P_p,k+f(t,p). We calculate shifts from
# conjugated projectors directly; the action on all 7 labels is affine.
Tshifts=set()
for t in itertools.product(range(3),repeat=4):
    D=pauli(t)
    sh=[]
    for p in H:
        X=D@P[p,0]@D.conj().T
        shifts=[np.linalg.norm(X-P[p,j]) for j in range(3)]
        sh.append(int(np.argmin(shifts)))
        assert min(shifts)<1e-10
    Tshifts.add(tuple(sh))
assert len(Tshifts)==81
allout=set(itertools.product(range(3),repeat=7))
def plus(v,s):return tuple((a+b)%3 for a,b in zip(v,s))
torbits=[]
while allout:
    seed=min(allout)
    orbit={plus(seed,s) for s in Tshifts}
    assert orbit.issubset(allout)
    allout-=orbit
    torbits.append(orbit)
translation_invariants=all(len({spectrum(k) for k in orb})==1 for orb in torbits)
family=[]
for sp,labels in sorted(classes.items(),key=lambda x:len(x[1])):
    family.append({"size":len(labels),"translation_cosets":len(labels)//81,
        "spectrum_9_eigenvalues_round_10_decimals":list(sp),
        "sample_outcome_labels":list(labels[0]),
        "F_at_T_0_5":float(-.5*np.log(np.exp((np.array(sp)-1)/.5).sum()))})
checks={"2880_max_heptads":len(all7)==2880,
    "five_spectral_types":len(classes)==5,
    "all_2880_reached_by_five_Clifford_generators":len(reached)==2880,
    "81_distinct_translations":len(Tshifts)==81,
    "27_translation_orbits_81_each":len(torbits)==27 and all(len(x)==81 for x in torbits),
    "Pauli_translation_preserves_spectra":translation_invariants,
    "family_sizes_81_162_486_486_972":sorted(len(v) for v in classes.values())==[81,162,486,486,972]}
out={"schema":"w33.round6.heptad_translation_orbits.v1","sample_heptad":list(H),
"Clifford_generator_permutations":{k:list(v) for k,v in G.items()},
"orbit_heptads":len(reached),"all_heptads":len(all7),
"Pauli_translation_group_image_order":len(Tshifts),
"number_translation_cosets":len(torbits),
"five_spectral_families":family,
"global_note":"All 2880 maximal noncommuting 7-sets are related by concrete two-qutrit Clifford generators, and their quantum spectra therefore have identical 5-family, 2187 assignment distributions up to relabelling. This is a statement at EQUAL seven weights, not a solution of the global 40-mass variational problem.",
"algebraic_scope":"The 81 translations and five Clifford generators produce verified finite permutations; eigenvalues computed numerically to 10 decimals. The five eigenvalue algebraic formulas are not yet exact symbolic certificates.",
"checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"checks":out["checks"],"heptads":len(reached),"family_counts":[(f["size"],f["translation_cosets"]) for f in family]},indent=2))
assert out["all_checks_pass"]
