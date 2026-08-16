#!/usr/bin/env python3
"""Pass5678: spectral decomposition and bottleneck of the connected Levi voltage tower.

For a graph G with a Z2 signature sigma, the adjacency matrix of its 2-lift is
unitarily equivalent to

    A(G) direct-sum A_sigma,

where A_sigma is the signed adjacency matrix.  Thus every lift retains all old
eigenvalues and adds the signed spectrum.  This is the standard 2-lift decomposition.

Pass5677 constructed an infinite connected tower by putting the fresh voltage on one
non-tree chord at each level.  That proves connectedness, but this pass shows why the
*single-chord* choice is not a satisfactory isotropic continuum: the two sheets are
joined by only two cross-sheet edges.  For a 4-regular base with N vertices, the
sheet cut has conductance at most

    Phi <= 2/(4N)=1/(2N),

so Cheeger's easy direction gives a normalized-Laplacian gap <=2 Phi and hence a
combinatorial-Laplacian gap <=4/N.  The gap therefore collapses along this deterministic
tower.  A useful continuum search needs balanced/nonlocal voltage classes, not merely
nontrivial ones.

The verifier also computes the first five spectra.  Distinct adjacency eigenvalues
proliferate 5,13,29,61,125 while the gap collapses.  The finite count pattern is
reported as a verified observation, not extrapolated as an all-level theorem.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import w33_pass5677_connected_levi_voltage_tower as tower

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5678_VOLTAGE_TOWER_SPECTRUM_BOTTLENECK.json'


def dense(adj, signed_chord=None):
    n=len(adj); A=np.zeros((n,n),float)
    for u,v in tower.edges(adj):
        z=-1.0 if signed_chord is not None and (u,v)==signed_chord else 1.0
        A[u,v]=A[v,u]=z
    return A


def distinct(vals,tol=1e-7):
    ans=[]
    for x in np.sort(vals):
        if not ans or abs(x-ans[-1])>tol: ans.append(float(x))
    return ans


def lift_from_chord(adj,chord):
    n=len(adj); out=[set() for _ in range(2*n)]
    for u,v in tower.edges(adj):
        s=1 if (u,v)==chord else 0
        for b in (0,1):
            a=u+b*n; c=v+(b^s)*n
            out[a].add(c);out[c].add(a)
    return out


def main():
    current=tower.levi_graph(); rows=[]
    expected_distinct=[5,13,29,61,125]
    for depth in range(5):
        A=dense(current); ev=np.linalg.eigvalsh(A); ds=distinct(ev)
        gap=float(4.0-ev[-2])
        assert len(ds)==expected_distinct[depth]
        row={"depth":depth,"vertices":len(current),"distinct_adjacency_eigenvalues":len(ds),
             "combinatorial_laplacian_gap":gap}
        if depth<4:
            T=tower.spanning_tree(current)
            chord=next(e for e in tower.edges(current) if e not in T)
            As=dense(current,chord)
            sev=np.linalg.eigvalsh(As)
            lifted=lift_from_chord(current,chord)
            Lev=np.linalg.eigvalsh(dense(lifted))
            union=np.sort(np.r_[ev,sev])
            assert np.allclose(Lev,union,atol=1e-8)
            N=len(current)
            cut_edges=2
            conductance_bound=cut_edges/(4*N)
            comb_gap_bound=8*conductance_bound # d*(2 Phi), d=4
            next_gap=float(4.0-Lev[-2])
            assert next_gap <= comb_gap_bound + 1e-9
            row["next_lift"]={
                "signed_chord":list(chord),
                "cross_sheet_edges":2,
                "sheet_conductance_upper_bound":conductance_bound,
                "next_combinatorial_gap":next_gap,
                "cheeger_easy_upper_bound":comb_gap_bound,
                "spectrum_identity":"spec(2-lift)=spec(A) union spec(A_sigma)"
            }
            current=lifted
        rows.append(row)

    out={
      "pass":5678,
      "status":"CONNECTED_SINGLE_CHORD_TOWER_HAS_EXACT_2LIFT_SPECTRAL_SPLIT_BUT_A_VANISHING_BOTTLENECK",
      "spectral_theorem":"For each Z2 lift, sheet-parity diagonalization gives A_lift ~= A_base direct-sum A_signed.",
      "verified_distinct_counts":{"depth_0_to_4":expected_distinct,"note":"finite verified pattern only; no all-level closed form is claimed"},
      "levels":rows,
      "bottleneck_theorem":"A single negative chord produces exactly two cross-sheet edges. For a 4-regular N-vertex base, Phi <=1/(2N) and the next combinatorial Laplacian gap <=4/N.",
      "physics_consequence":"Fresh cohomology repairs connectivity but a sparse one-chord voltage class produces hierarchical near-disconnection, not an isotropic continuum. A viable refinement needs balanced voltage signatures with controlled new spectrum.",
      "external_prior_art":"Bilu-Linial 2-lifts study exactly the old-spectrum plus new signed-spectrum decomposition and signatures with controlled new eigenvalues (arXiv:math/0312022).",
      "physics_boundary":"Gap collapse in this particular deterministic tower is a graph bottleneck effect. It is not a measured spacetime spectral dimension and does not rule out other balanced cover towers."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
