"""Integral/modular audit of TOE82's native tritangent H1.

H1 coinvariants, not coinvariant-chain homology, classify symmetry-fixed
flat U(1) gauge classes. No physical vacuum selection is inferred.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from w33_20261015_toe82_native_H27_h1_character import mul

ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 2, 2))


def field_basis(matrix, p):
    """Independent columns over F_p, with exact modular elimination."""
    a = np.asarray(matrix, dtype=np.int64).copy() % p
    pivots, rank = [], 0
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(a[rank:, col])
        if not len(candidates):
            continue
        row = rank + int(candidates[0])
        a[[rank, row]] = a[[row, rank]]
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, p) % p
        factors = a[:, col].copy()
        factors[rank] = 0
        a = (a - factors[:, None] * a[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == a.shape[0]:
            break
    return np.asarray(matrix, dtype=np.int64)[:, pivots] % p


def build_module(root=0):
    group = list(itertools.product(range(3), repeat=3))
    index = {g: i for i, g in enumerate(group)}
    faces = sorted({tuple(sorted(index[mul(g, t)] for t in
                    ((0, 0, 0), d, mul(d, d))))
                    for d in DIRECTIONS for g in group})
    edges = sorted({e for f in faces for e in itertools.combinations(f, 2)})
    ei = {e: i for i, e in enumerate(edges)}
    removed = {(a, b): (a, b, c) for a, b, c in faces}
    kept = [e for e in edges if e not in removed]
    ki = {e: i for i, e in enumerate(kept)}
    # Collapse free [a,b] using boundary [a,b]-[a,c]+[b,c].
    collapse = np.zeros((90, 135), dtype=np.int64)
    for e in kept:
        collapse[ki[e], ei[e]] = 1
    for (a, b), (_, _, c) in removed.items():
        collapse[ki[(a, c)], ei[(a, b)]] = 1
        collapse[ki[(b, c)], ei[(a, b)]] = -1
    boundary1 = np.zeros((27, 135), dtype=np.int64)
    boundary2 = np.zeros((135, 45), dtype=np.int64)
    for j, (a, b) in enumerate(edges):
        boundary1[a, j], boundary1[b, j] = -1, 1
    for j, (a, b, c) in enumerate(faces):
        for e, s in (((a, b), 1), ((a, c), -1), ((b, c), 1)):
            boundary2[ei[e], j] = s
    assert not (boundary1 @ boundary2).any()
    assert not (collapse @ boundary2).any()
    adj = {v: [] for v in range(27)}
    for a, b in kept:
        adj[a].append(b)
        adj[b].append(a)
    parents, queue, tree = {root: None}, deque([root]), set()
    while queue:
        v = queue.popleft()
        for w in sorted(adj[v]):
            if w not in parents:
                parents[w] = v
                queue.append(w)
                tree.add(tuple(sorted((v, w))))
    chords = [e for e in kept if e not in tree]
    assert len(chords) == 64
    coordinates = collapse[[ki[e] for e in chords]]
    basis = np.zeros((135, 64), dtype=np.int64)
    for j, (a, b) in enumerate(chords):
        basis[ei[(a, b)], j] = 1
        # Add b -> root -> a; shared tree segments cancel integrally.
        for v, s in ((b, 1), (a, -1)):
            while parents[v] is not None:
                w = parents[v]
                basis[ei[tuple(sorted((v, w)))], j] += s * (1 if v < w else -1)
                v = w
    assert not (boundary1 @ basis).any()
    assert np.array_equal(coordinates @ basis, np.eye(64, dtype=np.int64))
    actions = {}
    for g in group:
        perm = [index[mul(g, h)] for h in group]
        image = np.zeros_like(basis)
        for j, (a, b) in enumerate(edges):
            u, v = perm[a], perm[b]
            image[ei[tuple(sorted((u, v)))]] += (1 if u < v else -1) * basis[j]
        assert not (boundary1 @ image).any()
        actions[g] = coordinates @ image
    # All multiplication relations, not just generator orders.
    for g in group:
        for h in group:
            assert np.array_equal(actions[g] @ actions[h], actions[mul(g, h)])
    return actions, basis, coordinates


def building_chain_check(actions, basis):
    """Unimodular H1 map to the previously constructed cubic Levi building."""
    group = list(itertools.product(range(3), repeat=3))
    index = {g:i for i,g in enumerate(group)}
    faces = sorted({tuple(sorted(index[mul(g,t)] for t in ((0,0,0),d,mul(d,d))))
                    for g in group for d in DIRECTIONS})
    edges = sorted({e for f in faces for e in itertools.combinations(f,2)})
    incidence = [(v,27+j) for j,f in enumerate(faces) for v in f]
    ii = {e:i for i,e in enumerate(incidence)}
    edge_face = {e:j for j,f in enumerate(faces) for e in itertools.combinations(f,2)}
    chain_map = np.zeros((135,135),dtype=np.int64)
    for j,(a,b) in enumerate(edges):
        f = 27+edge_face[(a,b)]
        chain_map[ii[(a,f)],j],chain_map[ii[(b,f)],j] = 1,-1
    adj = {v:[] for v in range(72)}
    for a,b in incidence:
        adj[a].append(b);adj[b].append(a)
    parents,queue,tree = {0:None},deque([0]),set()
    while queue:
        a = queue.popleft()
        for b in sorted(adj[a]):
            if b not in parents:
                parents[b]=a;queue.append(b);tree.add(tuple(sorted((a,b))))
    chords = [e for e in incidence if e not in tree]
    assert len(parents)==72 and len(chords)==64
    target_basis = np.zeros((135,64),dtype=np.int64)
    for j,(a,b) in enumerate(chords):
        target_basis[ii[(a,b)],j]=1
        for v,s in ((b,1),(a,-1)):
            while parents[v] is not None:
                w=parents[v]
                target_basis[ii[tuple(sorted((v,w)))] ,j] += s*(1 if v<w else -1)
                v=w
    target_coordinates = [ii[e] for e in chords]
    transport = (chain_map @ basis)[target_coordinates]
    determinant = int(sp.Matrix(transport.tolist()).det())
    assert abs(determinant)==1
    for g in ((1,0,0),(0,1,0)):
        pv=[index[mul(g,h)] for h in group]
        fi={f:i for i,f in enumerate(faces)}
        pf=[fi[tuple(sorted(pv[v] for v in f))] for f in faces]
        moved = np.zeros_like(target_basis)
        for j,(v,f) in enumerate(incidence):
            moved[ii[(pv[v],27+pf[f-27])]] += target_basis[j]
        target_action = moved[target_coordinates]
        assert np.array_equal(transport @ actions[g],target_action @ transport)
    return {"target":"prior cubic 27-line/45-tritangent Levi building H1, not the W33 81D building",
            "target_cell_counts":[72,135],"H1_transport_determinant":determinant,
            "integral_H27_equivariance_checked":True,
            "prior_source":"analysis/w33_20260901_building_chain_injections.py"}


def holonomy_probe(actions, coordinates, relations):
    """Construct all fixed characters; solve actual link gauge compensators."""
    dm = DomainMatrix.from_Matrix(sp.Matrix(relations.tolist()))
    diagonal, left, right = smith_normal_decomp(dm)
    assert diagonal == left * dm * right
    d, u = diagonal.to_Matrix(), left.to_Matrix()
    rows = []
    for i in range(64):
        order = abs(int(d[i, i]))
        if order > 1:
            rows.append((order, np.array([int(x) % 9 for x in u[i, :]], dtype=np.int64) * (9 // order) % 9))
    assert [o for o, _ in rows] == [3, 9, 9]
    group = list(itertools.product(range(3), repeat=3))
    gi = {g:i for i,g in enumerate(group)}
    faces = sorted({tuple(sorted(gi[mul(g,t)] for t in ((0,0,0), v, mul(v,v))))
                    for g in group for v in DIRECTIONS})
    edges = sorted({e for f in faces for e in itertools.combinations(f,2)})
    edge_index = {e:i for i,e in enumerate(edges)}
    phases, records = set(), []
    for coefficients in itertools.product(range(3), range(9), range(9)):
        character = sum((k*r for k,(_,r) in zip(coefficients, rows)), np.zeros(64,dtype=np.int64)) % 9
        phases.add(tuple(character))
        for g in ((1,0,0),(0,1,0)):
            assert not (character @ (actions[g]-np.eye(64,dtype=np.int64)) % 9).any()
        links = character @ coordinates % 9
        for a,b,c in faces:
            assert (links[edge_index[(a,b)]] - links[edge_index[(a,c)]] + links[edge_index[(b,c)]]) % 9 == 0
        hamiltonian = np.zeros((27,27),dtype=complex)
        for j,(a,b) in enumerate(edges):
            hamiltonian[a,b] = -np.exp(2j*np.pi*links[j]/9)
            hamiltonian[b,a] = hamiltonian[a,b].conjugate()
        spectrum = np.linalg.eigvalsh(hamiltonian)
        order = 1 if not character.any() else (3 if not (3*character%9).any() else 9)
        records.append({"coefficients": list(coefficients), "holonomy_order": order,
                        "single_particle_spectrum": spectrum.tolist()})
    assert len(phases)==243
    # Explicit order-nine witness; exact gauge compensators in the ring Z/9.
    witness = rows[-1][1]
    links = witness @ coordinates % 9
    compensators = {}
    for g in ((1,0,0),(0,1,0)):
        perm = [gi[mul(g,h)] for h in group]
        delta = np.array([(1 if perm[a]<perm[b] else -1)*links[edge_index[tuple(sorted((perm[a],perm[b])))]]-links[j]
                          for j,(a,b) in enumerate(edges)]) % 9
        potential = {0:0}
        while len(potential)<27:
            old = len(potential)
            for j,(a,b) in enumerate(edges):
                if a in potential: potential.setdefault(b,(potential[a]+int(delta[j]))%9)
                if b in potential: potential.setdefault(a,(potential[b]-int(delta[j]))%9)
            assert len(potential)>old
        assert all((potential[b]-potential[a]-delta[j])%9==0 for j,(a,b) in enumerate(edges))
        compensators[str(g)] = [potential[i] for i in range(27)]
    fillings = {}
    for n in (1,9,13,14,18,26):
        energies = [sum(r["single_particle_spectrum"][:n]) for r in records]
        minimum = min(energies)
        winners = [i for i,e in enumerate(energies) if abs(e-minimum)<1e-9]
        fillings[str(n)] = {"minimum_free_energy_at_zero_temperature":minimum,
                            "minimizer_count":len(winners),
                            "minimizer_holonomy_orders": sorted({records[i]["holonomy_order"] for i in winners}),
                            "trivial_sector_energy":energies[0]}
        # Discrete-sector preference need not be stable in the full 64-torus.
        # Independently evaluate every flat-direction curvature at one winner.
        coefficients = records[winners[0]]["coefficients"]
        character = sum((k*r for k,(_,r) in zip(coefficients,rows)), np.zeros(64,dtype=np.int64)) % 9
        edge_phases = character @ coordinates % 9
        h = np.zeros((27,27),dtype=complex)
        dh = np.zeros((64,27,27),dtype=complex)
        for j,(a,b) in enumerate(edges):
            z = -np.exp(2j*np.pi*edge_phases[j]/9)
            h[a,b],h[b,a] = z,z.conjugate()
            dh[:,a,b] = 1j*coordinates[:,j]*z
            dh[:,b,a] = dh[:,a,b].conjugate()
        values,vectors = np.linalg.eigh(h)
        gap = float(values[n]-values[n-1])
        audit = {"selected_coefficients":coefficients,"fermi_gap":gap}
        if gap>1e-8:
            occupied = vectors[:,:n]
            projector = occupied @ occupied.conj().T
            gradient = np.einsum('ab,jba->j',projector,dh).real
            curvature = np.zeros((64,64))
            for j,(a,b) in enumerate(edges):
                curvature -= 2*np.real(projector[b,a]*h[a,b])*np.outer(coordinates[:,j],coordinates[:,j])
            transitions = np.einsum('ai,jab,bk->jik',occupied.conj(),dh,vectors[:,n:])
            denominators = values[:n,None]-values[None,n:]
            curvature += 2*np.einsum('jia,kia,ia->jk',transitions,transitions.conj(),1/denominators).real
            eig, axes = np.linalg.eigh(curvature)
            directional = []
            for v in (axes[:,0], axes[:,-1]):
                step = 1e-3
                trial = []
                for sign in (-1,1):
                    trial_h = h.copy()
                    change = coordinates.T @ v
                    for j,(a,b) in enumerate(edges):
                        trial_h[a,b] *= np.exp(1j*sign*step*change[j])
                        trial_h[b,a] = trial_h[a,b].conjugate()
                    trial.append(float(np.linalg.eigvalsh(trial_h)[:n].sum()))
                fd = (sum(trial)-2*float(values[:n].sum()))/step**2
                analytic = float(v @ curvature @ v)
                assert abs(fd-analytic)<2e-6
                directional.append({"analytic":analytic,"finite_difference":fd})
            audit.update({"max_gradient":float(np.max(np.abs(gradient))),
                          "full_64_flat_direction_hessian_eigenvalues":eig.tolist(),
                          "negative_curvature_count":int(np.sum(eig < -1e-8)),
                          "independent_extreme_axis_curvature_checks":directional})
        else:
            audit["scope"]="Degenerate Fermi level: no differentiable zero-temperature Hessian asserted."
        fillings[str(n)]["continuous_flat_torus_audit"] = audit
    return {"character_generators_mod9": [r.tolist() for _,r in rows],
            "order9_witness_link_phases_in_units_2pi_over9": links.tolist(),
            "order9_witness_H27_gauge_compensators_mod9":compensators,
            "sector_counts_by_order": {str(o):sum(r["holonomy_order"]==o for r in records) for o in (1,3,9)},
            "ordinary_conjugation_fixed_class_count":1,
            "ordinary_conjugation_nontrivial_pair_count":121,
            "uniform_hopping_finite_free_fermion_fillings":fillings,
            "all_243_sector_spectra":records,
            "physical_boundary":"Restricted symmetry-fixed flat sectors only; no global minimum over U1^64, interaction, dynamical gauge vacuum, or absence of generalized CP is claimed."}


def certificate(root=0, probe=True):
    actions, basis, coordinates = build_module(root)
    eye = np.eye(64, dtype=np.int64)
    generators = [(1, 0, 0), (0, 1, 0)]
    differences = [actions[g] - eye for g in generators]
    relations = np.concatenate(differences, axis=1)
    smith = smith_normal_form(sp.Matrix(relations.tolist()), domain=ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(64)]
    torsion = [d for d in diagonal if d > 1]
    free_rank = diagonal.count(0)
    dims = {}
    for p in (2, 3, 5, 7):
        dims[str(p)] = {
            "homology_invariants": 64 - field_basis(np.concatenate(differences), p).shape[1],
            "homology_coinvariants": 64 - field_basis(relations, p).shape[1],
        }
    # For a p-group, these augmentation-ideal images are the radical series.
    radical = eye.copy()
    layers = [64]
    while radical.shape[1]:
        radical = field_basis(np.concatenate([d @ radical for d in differences], axis=1), 3)
        layers.append(radical.shape[1])
        assert len(layers) < 30
    center = actions[(0, 0, 1)] - eye
    center_ranks = []
    power = eye.copy()
    for _ in range(3):
        power = power @ center % 3
        center_ranks.append(field_basis(power, 3).shape[1])
    assert free_rank == 0
    assert dims["3"]["homology_coinvariants"] == len(torsion)
    result = {
        "status": "PASS_11980_INTEGRAL_HEISENBERG_HOLONOMY_AUDIT",
        "prior_owners": ["TOE81 native tritangent topology", "TOE82 H27 complex character",
                         "Pass11560 distinct translation coinvariant-chain torsion"],
        "basis_root": root,
        "integral_H1_rank": 64,
        "prior_cubic_building_chain_equivalence":building_chain_check(actions,basis),
        "coinvariant_smith_diagonal": diagonal,
        "coinvariant_torsion_invariant_factors": torsion,
        "coinvariant_free_rank": free_rank,
        "symmetry_fixed_U1_flat_gauge_class_count": int(sp.prod(torsion)),
        "finite_field_dimensions": dims,
        "F3_radical_dimensions": layers,
        "F3_radical_layer_dimensions": [a-b for a,b in zip(layers,layers[1:])],
        "F3_center_nilpotent_power_ranks": center_ranks,
        "H27_generator_integral_H1_actions": {str(g): actions[g].tolist() for g in generators},
        "scope": "Fixed gauge-equivalence classes in Hom(H1,U1), not invariant link representatives, vacuum energetics, selected masses, gravity, or a physical TOE. H1 coinvariants are not homology of coinvariant chains."
    }
    if probe:
        result["explicit_holonomies_and_matter_probe"] = holonomy_probe(actions, coordinates, relations)
    return result


if __name__ == "__main__":
    c = certificate()
    (ROOT / "data/w33_pass11980_heisenberg_fixed_holonomies.json").write_text(json.dumps(c, indent=2) + "\n")
    print(json.dumps({k: v for k,v in c.items() if k not in
                     ("H27_generator_integral_H1_actions", "explicit_holonomies_and_matter_probe")}, indent=2))
    print(json.dumps(c["explicit_holonomies_and_matter_probe"]["uniform_hopping_finite_free_fermion_fillings"], indent=2))
