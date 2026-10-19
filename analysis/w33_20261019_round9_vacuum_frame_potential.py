"""Front1: full Clifford orbit yields a tight 1440-projector fusion frame.
Proves no single-vacuum Clifford-invariant quadratic OR quartic potential
can pick one of the 1440 discrete E8(-24) real-form vacua uniquely.
Two-body pair overlaps supply nontrivial invariant interactions.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import numpy as np
from w33_20261019_round8_clifford_vacuum_orbit import basis,contexts
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round9_vacuum_frame_potential.json"
I=np.eye(9)
def run():
    qs=np.array([basis[h,a]+basis[h,b] for h in range(40)
                 for a,b in itertools.combinations(range(9),2)])
    assert qs.shape==(1440,9,9)
    vec=qs.reshape(1440,81)
    frame=vec.conj().T@vec
    eig=np.linalg.eigvalsh(frame)
    centered=qs-(2/9)*I
    cg=np.linalg.eigvalsh(centered.reshape(1440,81).conj().T@
                         centered.reshape(1440,81))
    moments={}
    q=qs[0];c=centered[0]
    for power in range(1,5):
        vals=[float(np.trace(np.linalg.matrix_power(v,power)).real) for v in (q,c)]
        moments[str(power)]={"TrQpower":vals[0],"TrQcenteredpower":vals[1]}
    pair_overlaps=np.einsum("ij,aji->a",q,qs).real
    hist=collections.Counter(str(round(float(v),9)) for v in pair_overlaps)
    small=float(np.linalg.norm(qs.sum(axis=0)-320*I))
    # Analytically the *entire* orbit of 1440 Q are conjugate;
    # any G-invariant onsite scalar, including quartic polynomial,
    # takes the same value for all of them. Even functionals built from
    # the frame tensor cannot pick a unique vacuum (unless symmetry
    # explicitly broken).
    checks={"1440_rank2_vacua":len(qs)==1440,
       "fusion_frame_first_moment_320I":small<1e-10,
       "frame_spec_640_28x80":np.max(abs(np.sort(eig)-np.sort([640]+[28]*80)))<1e-8,
       "centered_frame_spec_0_28x80":np.max(abs(np.sort(cg)-np.sort([0]+[28]*80)))<1e-8,
       "quartic_vacuum_moment_exact":abs(moments["4"]["TrQcenteredpower"]-182/243)<1e-12,
       "quartic_moment_constant_under_orbit":max(abs(float(np.trace(np.linalg.matrix_power(x,4)).real)-2) for x in qs)<1e-10,
       "pairwise_overlap_is_nonconstant":len(hist)>3}
    out={"schema":"w33.round9.clifford_rank2_fusion_frame.v1",
      "theorem":"For all 1440 rank-two Q vacua in one projective 2-qutrit Clifford orbit, sum_Q Q = 320 I9, and the 81-dimensional frame operator on Mat9(C) has eigenvalues 640 (identity) and 28 (80 traceless directions). Hence sum_Q (Q-2I9/9)⊗(Q-2I9/9) is 28 times identity on traceless Hermitian operators. A global Clifford-invariant on-site polynomial potential V(Q), quadratic, quartic or arbitrary degree, MUST be constant on the whole orbit: no unique chosen vacuum without explicit or spontaneous symmetry breaking.",
      "size":len(qs),"sum_Q_vs_320I_residual":small,
      "frame_spectrum_predicted":{"identity":640,"traceless_80":28},
      "frame_spectrum_max_residual":float(np.max(abs(np.sort(eig)-np.sort([640]+[28]*80)))),
      "centered_frame_spectrum_max_residual":float(np.max(abs(np.sort(cg)-np.sort([0]+[28]*80)))),
      "single_Q_moments":moments,
      "fixed_Q_pair_overlap_histogram":dict(sorted(hist.items(),key=lambda kv:float(kv[0]))),
      "two_vacuum_interaction":"K(Q,R)=Tr[(Q-2I9/9)(R-2I9/9)] is Clifford invariant but varies with the relative orbit. Thus interactions can choose pair types, although the group still creates symmetry-equivalent degenerate minima. No physical Q vacuum selected.",
      "novelty":"The 1440 orbit and 2916 stabilizer were established Round8. Tight 80-frame normalization and invariant-potential selection obstruction are new consequences; analogous Clifford designs are established stabilizer mathematics.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"hist":out["fixed_Q_pair_overlap_histogram"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
