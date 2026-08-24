#!/usr/bin/env python3
"""Pass10129-10136: repair the proposed OAM implementation of the C2 detector.

The parallel circuit made three unsupported identifications:
  Bargmann chirality = sign/even-odd parity of one OAM index l;
  F9 norm parity = |l| mod 3;
  abstract decoder acceptance/error = optical contrast/efficiency.
None follows from the certified detector.

A faithful finite-mode encoding is instead immediate from F9=F3[i].  Encode
z=a+i b with TWO qutrit coordinates, e.g. a in a 3-level OAM register and b in
a 3-level time-bin register.  Then

  N(z)=z zbar=a^2+b^2 in F3,

and the nine basis symbols split exactly 1|4|4 into norm classes 0|1|2.
The norm cannot be read from OAM alone: symbols (1,0) and (1,1) have the same
OAM coordinate but norms 1 and 2.

The Bargmann bit is a different observable:
  B=<psi0|psi1><psi1|psi2><psi2|psi0>.
It requires three state rays / three complex pairwise overlaps (or an equivalent
three-path interferometric measurement).  It is not the sign of l.

A physically honest architecture is therefore:
  (A) joint OAM-qutrit x time-bin-qutrit mode sorting for the F9 norm class;
  (B) a separate three-state interferometric Bargmann-loop readout;
  (C) agree-or-erase logic combining their C2 bits.
No throughput/fidelity is assigned until a device-level loss/crosstalk model is
specified.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10129_10136_OAM_F9_ORIENTATION_READOUT_REPAIR.json'
P=3

def norm(a,b): return (a*a+b*b)%P

def main():
    symbols=[(a,b) for a in range(P) for b in range(P)]
    classes=defaultdict(list)
    for z in symbols: classes[norm(*z)].append(z)
    counts={k:len(v) for k,v in classes.items()}
    assert counts=={0:1,1:4,2:4}
    assert classes[0]==[(0,0)]
    # OAM-only coordinate a cannot determine the norm.
    ambiguity={}
    for a in range(P):
        ns=sorted({norm(a,b) for b in range(P)})
        ambiguity[str(a)]=ns
    assert ambiguity['1']==[1,2] and ambiguity['2']==[1,2]

    # Norm-one are axes; norm-two are diagonals in F3^2.
    assert set(classes[1])=={(0,1),(0,2),(1,0),(2,0)}
    assert set(classes[2])=={(1,1),(1,2),(2,1),(2,2)}

    out={
      'schema':'w33.pass10129_10136.oam_f9_orientation_readout_repair.v1','status':'PASS','passes':'10129-10136',
      'exact_F9_encoding':{
        'symbol':'z=a+i b, a,b in F3','registers':'a = OAM qutrit; b = time-bin qutrit (one possible hardware encoding)','norm':'N(z)=a^2+b^2 mod 3',
        'norm_classes':{str(k):v for k,v in sorted(classes.items())},'class_sizes':'1 | 4 | 4'},
      'oam_only_no_go':{'norm_sets_by_OAM_coordinate':ambiguity,'witness':'(a,b)=(1,0) has norm1 while (1,1) has norm2; same OAM coordinate a=1','conclusion':'No function of the OAM index alone can implement the F9 norm class in this encoding.'},
      'Bargmann_channel':{'observable':'B=<psi0|psi1><psi1|psi2><psi2|psi0>','bit':'sign(Im B)','requires':'three rays / three complex overlap factors or an equivalent closed-loop interferometer','not_equal_to':'sign(l) or even/odd parity under l -> -l'},
      'repaired_architecture':['joint 3x3 OAM x time-bin sorter/projector for F9 norm class','independent three-state Bargmann-loop interferometric readout','classical or coherent agree-or-erase fusion of the two decoded C2 bits'],
      'removed_parallel_claims':['96.81% abstract acceptance is not optical contrast','99% SLM, 92% sorter and 89.4% total efficiency are not certified for this detector','resource/footprint/cycle-time estimates are not derived from the Holonet model'],
      'theorem':'The exact finite-mode implementation of the F9 norm channel requires two ternary coordinates, naturally an OAM-qutrit x time-bin-qutrit 3x3 register with norm-class partition 1|4|4. The Bargmann chirality is a separate three-ray loop observable. The earlier OAM-sign/mod-3 identification is therefore invalid, but a corrected dual-channel photonic architecture remains feasible in principle.',
      'boundary':'The 1|4|4 finite-field routing is exact. OAM sorting is established optical technology, but this pass gives no measured device loss, crosstalk, fidelity, timing or footprint for the proposed joint detector.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','norm_counts':counts,'oam_only':False}))
    return 0
if __name__=='__main__': raise SystemExit(main())
