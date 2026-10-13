"""TOE58 front 2: exact static native overlap pairing under Wilson mass shifts.

This is the existing Pass11977 overlap kernel, re-tested for wider
Wilson mass range, nonzero gauge fields and time corners. The theorem
forbids static 4D index generation, NOT time-dependent 4D topology.
"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11977_native_overlap import kernel,clifford
gamma,g5=clifford()
Rmat=np.kron(1j*gamma[3]@g5,np.eye(80))
assert np.max(abs(Rmat@Rmat-np.eye(320)))<1e-13
rng=np.random.default_rng(58002)
phases=rng.uniform(-.28,.28,size=160)
records=[]
for m0 in (.3,.5,1.5,3.,7.):
 for omega in (0.,np.pi):
  Q,G5=kernel([.16,-.11,.21],omega,phases=phases,m0=m0)
  pair=float(np.max(abs(Rmat@Q+Q@Rmat)))
  ev=np.linalg.eigvalsh(Q);gap=float(np.min(abs(ev)))
  assert pair<1e-11 and gap>1e-6,(m0,omega,pair,gap)
  assert abs(np.sum(np.sign(ev)))<1e-9
  records.append(dict(m0=m0,time_corner=float(omega),gap=gap,
    anticommutator=pair,index=int(round(-.5*sum(np.sign(ev))))))
# A changed m0 can move a phase boundary; this sweep avoids zero gaps.
# At static time0, the exact unitary R anticommutes with Q independent
# of phases and k. This is NOT a universal4D index theorem.
out={"status":"PASS_TOE58_STATIC_NATIVE_OVERLAP_NO_CHIRAL_INDEX",
"index_zero_cases":records,"basis":320,
"exact_symmetry":"For static link phases and omega=0 or pi, R=i gamma_time gamma5 tensor I_80 anticommutes with the Hermitian Q=gamma5 DW regardless of Wilson m0 and spatial phases. Where Q is invertible its spectrum is ± paired and overlap index -Tr signQ /2=0.",
"physics_boundary":"No time-dependent 4D link topology, nonzero instanton background, Weyl chiral measure, three generations or gauge anomaly cancellation. No inference that all 4D overlap operators have index0. Wilson masses chosen were externally supplied, not derived by W33."}
(R/"data/w33_20261013_toe58_overlap_index.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE58 overlap",[(q["m0"],q["time_corner"],q["gap"]) for q in records])
