"""The ratio-selected Newton polytope coarsens the full pezzotope fan."""

from collections import Counter
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def test_selected_newton_face_lattice():
    path = ROOT / 'data/toe_20261109_pezzotope_canonical_partner.json'
    certificate = json.loads(path.read_text(encoding='utf-8'))
    scattering = certificate['ratio_selected_scattering_potential']
    vertices = scattering['newton_vertices']
    normals = [
        [(-1)**i * value for i, value in enumerate(row)]
        for row in certificate['facet_residue_contractions']
    ]
    supports = [
        frozenset(i for i, vertex in enumerate(vertices)
                  if sum(a*b for a, b in zip(normal, vertex)) == minimum)
        for normal, minimum in zip(normals, scattering['newton_facet_minimums'])
    ]

    def dimension(face):
        first, *other = sorted(face)
        return sp.Matrix([[a-b for a, b in zip(vertices[i], vertices[first])]
                          for i in other]).rank()

    assert [dimension(face) for face in supports] == [3]*10 + [2, 1, 2, 1, 1]
    # The 15 original normals refine the selected fan, so all its facet
    # rays occur among these normals. Intersect the ten facet vertex sets.
    faces = {frozenset(range(len(vertices)))}
    for facet in supports[:10]:
        faces |= {face & facet for face in faces if face & facet}
    assert Counter(dimension(face) for face in faces) == {0: 19, 1: 41, 2: 32, 3: 10, 4: 1}
    assert scattering['unit_weighted_schwinger_integral'] == 25
