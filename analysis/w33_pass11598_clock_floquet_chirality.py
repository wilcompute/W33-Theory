#!/usr/bin/env python3
import runpy,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
ns=runpy.run_path(str(ROOT/'analysis/w33_pass11583_clock_chirality_quaternion.py'))
GA=ns['GA'];Ci=ns['Ci'];g=ns['g']
I=np.eye(32,dtype=complex);gamma10=np.array(g[9].evalf(),complex)
G2=np.linalg.matrix_power(GA,2);G4=np.linalg.matrix_power(GA,4);G8=np.linalg.matrix_power(GA,8)
err2=np.linalg.norm(G2-1j*gamma10);err4=np.linalg.norm(G4+I);err8=np.linalg.norm(G8-I)
comm4=np.linalg.norm(G4@Ci-Ci@G4)
assert max(err2,err4,err8,comm4)<1e-10
out={'status':'PASS_CLOCK_FLOQUET_FOUR_TICK_RETURN_IS_SCALAR_NO_SELECTOR',
     'G2_equals_i_gamma10_error':float(err2),'G4_equals_minus_identity_error':float(err4),
     'G8_equals_identity_error':float(err8),'G4_chirality_commutator_error':float(comm4),
     'theorem':'Two clock ticks are i*Gamma_10 and exchange Spin(10) Weyl chirality; four ticks return to the same chirality but the Floquet operator is only -I; eight ticks are I.',
     'no_go':'The pure order-eight clock therefore has no nontrivial chirality-preserving four-tick Floquet dynamics that could select one Weyl sector. A selector requires an additional clock-odd order parameter or explicit symmetry reduction.'}
(ROOT/'data/PART_W33_PASS11598_CLOCK_FLOQUET_CHIRALITY.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
