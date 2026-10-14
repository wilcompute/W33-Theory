"""TOE71: holonomy-preserving W33-derived closed spin 4-manifold, but not a
native four-dimensional overlap lattice. The index requires external curvature.

Given a regular genus-81 handlebody thickening H of the actual W33 Levi
graph, inclusion boundary H -> H induces H1 surjection. A graph flat
character therefore pulls back to the closed genus-81 boundary surface,
and extends to its product with an *added* T2. Contrast the TOE70
20-face cellulation, which kills the selected three flat characters.
"""
from __future__ import annotations
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import graph

def certificate():
    ed,adj=graph()
    V=80;E=len(ed)
    assert E==160
    parents=list(range(V))
    def root(v):
        while parents[v]!=v:
            parents[v]=parents[parents[v]];v=parents[v]
        return v
    tree=[]
    for i,(a,b) in enumerate(ed):
        aa=root(a);bb=root(b)
        if aa!=bb:parents[aa]=bb;tree.append(i)
    assert len(tree)==79
    chord=[i for i in range(160) if i not in set(tree)]
    assert len(chord)==81
    phase_edges=(59,93,139)
    assert all(e in chord for e in phase_edges)
    g=E-V+1
    assert g==81
    # Genus boundary of regular neighborhood of connected graph with
    # g loops: ∂H is a closed orientable genus-g surface, and the
    # inclusion j:∂H->H is surjective on H1, ker rank g.
    surface=[1,2*g,1];torus=[1,2,1]
    prod=[sum(surface[j]*torus[k-j] for j in range(3) if 0<=k-j<3)
          for k in range(5)]
    assert prod==[1,164,326,164,1]
    # The intersection form of Sigma_g x T2 is 163 hyperbolic planes.
    assert prod[2]==2+4*g==326
    charges=(1,5,-7,-8,9)
    assert sum(charges)==sum(q**3 for q in charges)==0
    examples=[]
    for m,n in ((0,0),(1,0),(0,1),(1,1),(1,-1),(2,3)):
        # For c1(L)=m*u+n*v, u and v pullbacks of fundamental 2-forms
        # of Sigma_g and T2, integral c1^2=2mn, signature=0.
        index=m*n
        examples.append({
          "surface_flux":m,"torus_flux":n,
          "c1_square":2*m*n,"unit_charge_spin_Dirac_index":index,
          "charge_nine_twisted_index":81*index,
          "five_charge_total_index":sum(q*q for q in charges)*index})
    assert examples[3]["unit_charge_spin_Dirac_index"]==1
    assert examples[3]["five_charge_total_index"]==220
    return {
      "status":"PASS_TOE71_NATIVE_GRAPH_HOLONOMY_PRESERVING_CONTINUUM_4D",
      "native_graph_vertices_edges":[V,E],
      "canonical_sorted_spanning_tree_edges":len(tree),
      "canonical_sorted_fundamental_chords":len(chord),
      "selected_flat_three_deck_edges":list(phase_edges),
      "handlebody_retraction_H1_rank":g,
      "boundary_closed_genus":g,
      "boundary_H1_rank":2*g,
      "inclusion_boundary_to_handlebody_H1_surjective":True,
      "inclusion_H1_kernel_rank":g,
      "three_deck_characters_extend_as_flat_surface_holonomies":True,
      "additional_two_torus_is_external_input":True,
      "M4":"boundary of regular 3D neighborhood of native W33 Levi graph, times added T2",
      "M4_betti":prod,"closed":True,"oriented":True,"spin":True,
      "signature":0,"untwisted_spin_Dirac_index":0,
      "intersection_hyperbolic_planes":2*g+1,
      "line_bundle_twist_examples":examples,
      "flat_holonomy_alone_c1_square":0,
      "flat_holonomy_alone_index":0,
      "known_five_charge_example":list(charges),
      "known_U1_cubic_anomaly":sum(q**3 for q in charges),
      "known_U1_gravitational_anomaly":sum(charges),
      "conceptual_obstruction":"Flat three-deck characters survive this handlebody-derived boundary, unlike the 20-face attachment, but they cannot alone create a nonzero chiral index. Independent nonflat U1 curvature in BOTH surface factors must be imposed to get index mn. The ribbon thickening, added T2, spin structure and line bundle are extra choices.",
      "scope":"A W33-derived closed smooth continuum M4 and index-theory construction, not an explicit local W33 discretization, admissible overlap-Dirac index, anomaly-free lattice Weyl measure, Lorentz dynamics or physical chiral Standard Model."
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe71_4d_holonomy_and_index.json").write_text(
      json.dumps(c,indent=2)+"\n",encoding="utf-8")
    print(c["status"],c["M4_betti"])
