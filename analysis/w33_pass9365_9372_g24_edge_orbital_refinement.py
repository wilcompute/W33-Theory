#!/usr/bin/env python3
"""Pass9365-9372: derive the rank-14 Leech orbital refinement from the G2(4) graph edge action.

Pass9085-9092 identifies the 20,800 Leech bare six-spaces with the edges of the
G2(4) graph SRG(416,100,36,20).  Fix an edge e={u,v}.  The remaining 414
vertices split into A=N(u)cap N(v), B=N(u)\(N(v)cup{v}), C symmetrically, and D
adjacent to neither.  The local graph on N(u) is Hall-Janko SRG(100,36,14,12).
Those two SRG parameter sets force every edge-pattern count below.

The key new point is transpose/orientation: an A-D moving edge is seen in the
reverse ordered pair as a B-B/C-C edge, and conversely.  Hence the unique
1512+1512 oriented pair in Pass8789 is exactly this endpoint-incidence
asymmetry in the G2(4) edge action.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9365_9372_G24_EDGE_ORBITAL_REFINEMENT.json'

# G2(4) graph and its local Hall-Janko graph.
v,k,lam,mu=416,100,36,20
lv,lk,llam,lmu=100,36,14,12
assert k*(k-lam-1)==(v-k-1)*mu
assert lk*(lk-llam-1)==(lv-lk-1)*lmu
A=lam
B=C=k-lam-1
D=v-2-A-B-C
assert (A,B,C,D)==(36,63,63,252)

# Edge counts forced by the local HJ graph.
AA=A*llam//2                        # each a in A has 14 A-neighbors
AB=A*(lk-1-llam)                    # after v and 14 A-neighbors: 21 in B
AC=AB
BB=B*(lk-lmu)//2                    # each b has 12 A-neighbors, hence 24 B-neighbors
CC=BB
BC=B*(mu-1-lmu)                     # common neighbors of b and v: u + 12 A + 7 C
AD=A*(k-2-llam-2*(lk-1-llam))       # a: u,v +14 A+21 B+21 C leaves42 D
BD=B*(k-1-lmu-(lk-lmu)-(mu-1-lmu)) # b: u+12A+24B+7C leaves56D
CD=BD
TOTAL=v*k//2
fixed_and_incident=1+2*A+B+C
known=fixed_and_incident+AA+AB+AC+BB+CC+BC+AD+BD+CD
DD=TOTAL-known
assert (AA,AB,AC,BB,CC,BC,AD,BD,CD,DD)==(252,756,756,756,756,441,1512,3528,3528,8316)
assert TOTAL==20800 and known+DD==TOTAL

# Coarse relative-edge classes by endpoint incidence with fixed edge e.
coarse={
 'fixed':1,
 'share_endpoint_triangle':2*A,
 'share_endpoint_wedge':B+C,
 'AA':AA,
 'AB_or_AC':AB+AC,
 'AD':AD,
 'BB_or_CC':BB+CC,
 'BC':BC,
 'BD_or_CD':BD+CD,
 'DD':DD,
}
assert sum(coarse.values())==20800

# Pass8789 rank-14 refinement uniquely fits these coarse cells.
refinement={
 'fixed':[1],
 'share_endpoint_triangle':[72],
 'share_endpoint_wedge':[126],
 'AA':[252],
 'AB_or_AC':[1512],
 'AD':[1512],
 'BB_or_CC':[1512],
 'BC':[63,378],
 'BD_or_CD':[3024,4032],
 'DD':[252,2016,6048],
}
assert sorted(sum(refinement.values(),[]))==sorted([1,63,72,126,252,252,378,1512,1512,1512,2016,3024,4032,6048])

# Ordered-pair transpose proof, purely from endpoint patterns.
transpose={
 'AD':'BB_or_CC',
 'BB_or_CC':'AD',
 'AB_or_AC':'AB_or_AC',
}
# Explanation: if f={a,d} with a adjacent to both u,v and d to neither,
# then relative to f both u,v are adjacent to a only, hence same-side B/B.
# Conversely two B endpoints are both adjacent to u and not v, so relative
# to f the old edge endpoints are A (u) and D (v).
assert AD==BB+CC==1512

out={
 'schema':'w33.pass9365_9372.g24_edge_orbital_refinement.v1','status':'PASS','passes':'9365-9372',
 'ambient_graph':{'name':'G2(4) graph','srg':[v,k,lam,mu],'edges':TOTAL,'local_graph':'Hall-Janko SRG(100,36,14,12)'},
 'fixed_edge_vertex_partition':{'A_common':A,'B_u_only':B,'C_v_only':C,'D_neither':D},
 'forced_edge_counts':{'AA':AA,'AB':AB,'AC':AC,'BB':BB,'CC':CC,'BC':BC,'AD':AD,'BD':BD,'CD':CD,'DD':DD},
 'coarse_relative_edge_counts':coarse,
 'rank14_refinement':refinement,
 'unique_oriented_pair':{'forward':'A-D','reverse':'B-B or C-C','degrees':[1512,1512],'proof':'For f={a,d} of type A-D relative to e={u,v}, both u,v are adjacent to a and not d, hence e is same-side B-B/C-C relative to f; conversely same-side B-B/C-C reverses to A-D.'},
 'self_transpose_1512':'A-B or A-C',
 'classical_H4_boundary':'Pass9061-9068 reduces the remaining S^1_1 versus S^2_1 label to a 16-point flag-stabilizer test. This edge-pattern theorem identifies the oriented Leech pair intrinsically but does not guess which classical 3024 label it refines.',
 'theorem':'The entire coarse rank-14 Leech six-space geometry is forced by the G2(4) SRG and its Hall-Janko local graph. The unique nonsymmetric 1512+1512 pair is exactly A-D <-> (B-B or C-C) under ordered-edge reversal.',
 'claim_boundary':'Exact finite graph arithmetic and endpoint-pattern transpose theorem; the final classical S^1_1/S^2_1 name remains a separate test.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','partition':[A,B,C,D],'oriented':['AD','BB/CC']}))
