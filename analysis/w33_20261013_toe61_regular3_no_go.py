"""TOE61 conditional regular-manifold obstruction retaining all 1382 embedded octagons.

3 formal zero-chain commutator cells are not regular embedded faces.
A closed regular 3-manifold needs 1302 volumes by Euler but face
incidences permit at most 921 if each volume has >=3 distinct faces.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,v,lk,octs,comm,*_=prep()
P=np.rint(np.asarray([cycle_row(x,ed,v,lk,np.zeros(3)).real for x in octs+comm])).astype(int)
Fdeclared,N1=P.shape
assert (Fdeclared,N1)==(1385,160)
# Three formal commutator 2-cells have algebraic zero boundary at
# Bloch k=0; their attaching walks backtrack and are not regular
# embedded polygonal faces. Retain the 1382 genuinely simple octagons.
lengths=np.count_nonzero(P,axis=1)
regular=P[lengths==8]
F=len(regular)
assert F==1382 and sum(lengths==0)==3
sigs=[]
for row in regular:
 pos=tuple((int(i),int(x)) for i,x in enumerate(row) if x)
 neg=tuple((i,-x) for i,x in pos)
 sigs.append(min(pos,neg))
counts={}
for sig in sigs:counts[sig]=counts.get(sig,0)+1
duplicates=[n for n in counts.values() if n>1]
lens={int(x):int(np.count_nonzero(np.count_nonzero(P,axis=1)==x)) for x in np.unique(np.count_nonzero(P,axis=1))}
print('F',F,'nnz',lens,'unique boundary',len(counts),'duplicate',duplicates,flush=True)
assert len(counts)==F
V=80;E=160
chi2=V-E+F
# Homology T3 has χ=0. Keeping this 2-skeleton, no additional
# cells above3, requires exactly C3=χ2 for finite closed 3-manifold.
required=chi2
# For regular finite CW complex closed orientable 3 manifold:
# count each distinct polygonal 2-face incident to 2 distinct 3-cell
# boundary incidences. No regular 3-ball can have only one face;
# two distinct 2-faces would be hemispheres with identical boundary
# 1-skeleton and identical signed oriented 1-chain -> ruled out by sig uniqueness.
# Hence each 3-ball has >=3 distinct 2-faces.
maxcells=(2*F)//3
assert required>maxcells
shortfall=3*required-2*F
# General fixed (V,E) face-count ceiling: C3=V-E+F=F-80,
# and 3*C3<=2*F imply F<=3*(E-V)=240.
face_ceiling=3*(E-V)
assert face_ceiling==240 and F-face_ceiling==1142
out={'status':'PASS_TOE61_NO_REGULAR_3_MANIFOLD_COMPLETION_FIXED_2_SKELETON',
'actual_cell_counts':{'vertices':V,'edges':E,'regular_octagon_faces':F,'formal_zero_boundary_commutator_faces_excluded':Fdeclared-F,'two_skeleton_Euler':chi2,
'unique_signed_face_boundaries_up_to_orientation':len(counts),'all_declared_face_length_counts':lens, 'two_skeleton_rational_betti':[1,3,1304,0]},
'conditional_manifold_target':{'required_3cells_if_closed_3manifold_no_higher_cells':required,
'required_3boundary_rank_for_T3_homology':1301,
'closed_regular_3manifold_face_coincidence':2,
'minimum_distinct_2_faces_per_3_ball':3,'max_3cells_by_double_counting':maxcells,
'boundary_face_incidence_shortfall':shortfall,
'max_faces_if_pruning_only_2faces_with_fixed_80_vertices_160_edges':face_ceiling,
'minimum_octagon_faces_to_discard_under_these_conditions':F-face_ceiling},
'proof':"A closed orientable 3-manifold has Euler characteristic0. Given C0=80,C1=160,C2=1382 DISTINCT regular octagon faces and no cells above3, it MUST have C3=1302. The original three extra commutator 2-cells have zero boundary and are not regular polygon faces. Every 2-face of a regular closed 3-manifold has exactly two incident 3-ball sides, so total boundary-face incidences is 2*1382=2764. Every closed regular 3-ball needs at least three distinct 2-faces: a two-face sphere would have two disks with the SAME 1-skeleton boundary, but all 1382 embedded simple octagon boundaries are pairwise distinct up to orientation, established exactly from P. Therefore 3*C3<=2*F, i.e. C3<=921; contradiction with required C3=1302.",
'minimal_pruning_bound':"For any closed regular 3-manifold cellulation with these fixed V=80,E=160 and pairwise distinct embedded 2-face boundaries, chi=0 forces C3=F-80. Each volume uses at least3 distinct boundary faces and every face has two sides, hence 3(F-80)<=2F, i.e. F<=240. Retaining all1382 requires removal of at least1142 faces if only deleting faces (no new 0/1/2 cells); even removing that many is far from sufficient to build a manifold.",
'limitations':"Conditional no-go ONLY for a closed REGULAR manifold cellulation keeping ALL 1382 existing distinct native embedded OCTAGON faces as physical 2-faces (and excluding three nonregular formal commutator cells) and only adding 3-cells. It does NOT prohibit a nonregular CW model, removing redundant 2-faces, subdivisions that introduce 0/1/2 cells, thickening of a graph, higher-dimensional embeddings or an emergent continuum. It does NOT prove W33 cannot encode gravity or 4D spacetime in a different construction.",
'prior':"Extends TOE60 Betti/Euler necessary 1305 count with native signed-face uniqueness and incidence double-counting. Uses standard regular-cell-manifold combinatorics; no claim of original general topology theorem."}
(R/'data/w33_20261013_toe61_regular3_no_go.json').write_text(json.dumps(out,indent=2)+'\n')
