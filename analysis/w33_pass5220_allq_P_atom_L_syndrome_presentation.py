#!/usr/bin/env python3
"""Pass5220 (bonkers): all-q P-atom presentation and exact L-syndrome rank.

Pass5177/5188 identify every P component with
C_q=Cut(K_{q+1}) tensor Cut(K_{q+1}), dimension q^2.  Pass5179 classifies its
(q+1)^2 minimum atoms as simple tensors of the q+1 factor star cuts.  Since the
factor star cuts span Cut(K_{q+1}), the minimum atoms span C_q.  Thus each
component has exactly (q+1)^2-q^2=2q+1 atom-generator relations.

There are q^2(q^2+1)/2 P components, so the full P-triangle solution space has
 dimension q^4(q^2+1)/2.  The full apartment code is the simultaneous P- and
L-theta kernel and has dimension q^4 (Pass5066/5117).  Therefore, restricted to
the P-side solution space, the independent L-syndrome rank is exactly
q^4(q^2-1)/2.  This yields an all-q finite presentation of the apartment code
by P minimum atoms plus connected-L compatibility equations.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5220_ALLQ_P_ATOM_L_SYNDROME_PRESENTATION.json'

def row(q):
    comps=q*q*(q*q+1)//2;atoms_comp=(q+1)**2;atom_vars=comps*atoms_comp
    rel_comp=2*q+1;internal=comps*rel_comp;pdim=comps*q*q
    full=q**4;lrank=pdim-full;composite_kernel=internal+full
    assert atom_vars-internal==pdim and pdim-lrank==full and atom_vars-composite_kernel==lrank
    return {'q':q,'P_components':comps,'atoms_per_component':atoms_comp,
      'atom_generator_variables':atom_vars,'relations_per_component':rel_comp,
      'internal_atom_relation_dimension':internal,'P_side_solution_dimension':pdim,
      'independent_L_syndrome_rank_on_P_side':lrank,'apartment_code_dimension':full,
      'atom_coefficient_kernel_dimension':composite_kernel}

def main():
    A={str(q):row(q) for q in (2,3,4,5,6,7)}
    assert A['5']=={'q':5,'P_components':325,'atoms_per_component':36,
      'atom_generator_variables':11700,'relations_per_component':11,
      'internal_atom_relation_dimension':3575,'P_side_solution_dimension':8125,
      'independent_L_syndrome_rank_on_P_side':7500,'apartment_code_dimension':625,
      'atom_coefficient_kernel_dimension':4200}
    out={'pass':5220,'status':'THEOREM_ALL_Q_P_ATOM_PRESENTATION_AND_L_SYNDROME_RANK',
      'component':'C_q=Cut(K_{q+1}) tensor Cut(K_{q+1}) has dimension q^2 and is spanned by its (q+1)^2 minimum simple-tensor atoms.',
      'component_atom_relation_dimension':'(q+1)^2-q^2=2q+1',
      'P_components':'q^2(q^2+1)/2',
      'atom_variables':'q^2(q^2+1)(q+1)^2/2',
      'P_side_dimension':'q^4(q^2+1)/2',
      'L_syndrome_rank_on_P_side':'q^4(q^2-1)/2',
      'full_code_kernel_dimension':'q^4',
      'proof':'Minimum factor star cuts span Cut(K_{q+1}); their simple tensors span each P component. P components are coordinate-disjoint. The complete apartment code is the intersection of the P- and L-theta kernels and has dimension q^4, so rank-nullity gives the displayed independent L rank.',
      'anchors':A,
      'q5_interpretation':'11700 atom coefficients modulo 3575 component-internal relations give an 8125-dimensional P-side space. The connected L syndrome imposes exactly 7500 independent conditions, leaving the 625-dimensional q5 apartment code.',
      'connection':'Pass5214 is a nonlinear minimum-shell slice of this linear presentation: its 25 atom groups live inside the 8125-dimensional P-side presentation, while the connected L compatibility operator is the global rank-7500 glue.',
      'boundary':'This is a presentation/dimension theorem. It does not assert that arbitrary sparse atom coefficient vectors represent minimum-weight codewords, nor does it replace the odd-q P/L asymmetry by a tensor symmetry.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
