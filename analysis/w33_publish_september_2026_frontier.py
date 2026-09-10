#!/usr/bin/env python3
"""Publish the September 2026 Heawood/Schubert/observer frontier into docs/index.html.

The main page is intentionally large and is awkward to edit through remote contents APIs.
This script makes the publication step reproducible inside GitHub Actions: it reads the
frozen exact JSON certificates, renders one bounded section, and replaces/inserts that
section between stable marker comments. Running twice is idempotent.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
BEGIN = "<!-- W33-SEPT-2026-FRONTIER:BEGIN -->"
END = "<!-- W33-SEPT-2026-FRONTIER:END -->"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def render_section() -> str:
    outer = load("data/w33_heawood_outer_involution_fixed_census.json")
    group = load("data/w33_heawood_stabilizer96_presentation_lattice.json")
    schubert = load("data/w33_marcelis_trace_schubert_general.json")
    observer = load("data/w33_marcelis_observer_quotient_dynamics.json")
    cube = load("data/w33_outer_cube_observer_bridge.json")
    cover = load("data/w33_stabilizer96_cube_central_cover.json")
    horizon = load("data/w33_affine_fano_information_horizon.json")

    assert all(x["status"] == "PASS" for x in (outer, group, schubert, observer, cube, cover, horizon))
    fixed_modes = outer["fixed_objects"]["fixed_pair_modes"]
    lattice_n = group["normal_subgroup_lattice"]["normal_subgroup_count"]
    model = observer["n3_one_step_model"]
    q = cube["spread_orbit_quotient"]
    cocycle = cover["extension_cocycle"]
    h3 = horizon["n3_information_horizon"]

    links = {
        "outer": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_heawood_outer_involution_fixed_census.json",
        "group": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_heawood_stabilizer96_presentation_lattice.json",
        "schubert": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_marcelis_trace_schubert_general.json",
        "observer": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_marcelis_observer_quotient_dynamics.json",
        "cube": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_outer_cube_observer_bridge.json",
        "cover": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_stabilizer96_cube_central_cover.json",
        "horizon": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_affine_fano_information_horizon.json",
        "note": "https://github.com/wilcompute/W33-Theory/blob/master/analysis/W33_OBSERVER_RELATIVE_RANDOMNESS.md",
    }

    body = f"""
{BEGIN}
<section id="heawood-schubert-observer-20260910" aria-labelledby="heawood-schubert-observer-title">
  <h2 id="heawood-schubert-observer-title">September 2026: outer involution, Schubert trace law, and observer cube</h2>
  <p><strong>Exact certificate frontier.</strong> The multiplier-two outer involution on the 270 Heawood C6 components has cycle structure <code>12 + 129×2</code>. Under the equivariant spread dictionary the 12 fixed objects split exactly <code>{fixed_modes['both_spreads_fixed']} + {fixed_modes['spreads_exchanged']}</code>: six pairs of individually fixed spreads and six pairs whose spreads are exchanged.</p>
  <p>The order-96 C6 stabilizer is the split fiber product <code>D8 ×_C2 S4 ≅ V4 ⋊ S4</code>, with center <code>C2</code>, derived subgroup <code>C2 × A4</code>, abelianization <code>C2 × C2</code>, and a complete <strong>{lattice_n}-node</strong> normal-subgroup lattice.</p>
  <p>The omega-normalized Marcelis trace map obeys an all-n flag law: for <code>b ∈ F_j \\ F_(j+1)</code>, point fibres have size <code>2^(n-j)</code>; incidence-preserving binary lines in the same stratum have <code>2^(n-1-j)</code> GF(4) lifts. At n=3 this recovers the 1/2/4/8 point staircase and the 4/2/1 line staircase.</p>
  <p>A deterministic cyclic coordinate update on <code>PG(3,4)</code> becomes stochastic after the many-to-one observer quotient to <code>PG(3,2)</code>: <strong>{model['observer_kernel']['stochastic_macro_states']}</strong> macrostates are stochastic and <strong>{model['observer_kernel']['deterministic_macro_states']}</strong> are deterministic, with <code>H(B′|B)={html.escape(model['observer_kernel']['H_Bprime_given_B_bits_exact'])}</code> bits, while retaining the fibre key restores <code>H(B′|B,K)=0</code>.</p>
  <p><strong>New cubical bridge.</strong> The complement of W33 collinearity on the eight outer-fixed points is exactly <code>Q3</code>. The stochastic Schubert chart <code>x0=1</code> is <code>AG(3,2) ≅ F2^3</code>, giving a second explicit Q3, and appending one frozen bit embeds it as a facet of the already-certified Q4 temporal router. On the spread side the four fixed spreads form a K4; the quotient of the 270 four-intersection edges has {q['four_intersection_edge_orbits']} edge orbits, with six fixed ordinary edges and six fixed loops recording exchanged spread pairs.</p>
  <p><strong>Central-cover phase obstruction.</strong> The same order-96 Heawood stabilizer is a <em>non-split central double cover</em> of cube symmetry: <code>1 → C2 → H → Aut(Q3) → 1</code> with <code>Aut(Q3) ≅ C2 × S4</code>. The extension is represented by the explicit normalized cocycle <code>α((b,σ),(d,τ)) = d·sgn(σ) mod 2</code>, checked on all <strong>{cocycle['cocycle_triples_checked']}</strong> quotient triples. A commuting quotient pair has asymmetric cocycle values 1 and 0, so its lifts differ by the hidden central <code>z</code>; the certificate treats this only as a finite-group/controller phase obstruction, not yet a Spin/Pin or physical quantum phase.</p>
  <p><strong>Affine/Fano information horizon.</strong> The same observer split is exactly <code>PG(3,2)=AG(3,2) ⊔ PG(2,2)</code>: 8 stochastic affine macrostates over 64 GF(4) microstates versus a 7-state deterministic Fano plane at infinity over 21 microstates. Under one cyclic update the microstate-weighted coarse kernel is <code>[[3/4,1/4],[16/21,5/21]]</code>, with stationary weights <code>64/85,21/85</code>. Its only nonstationary eigenvalue is <strong>{html.escape(h3['nontrivial_eigenvalue'])}</strong>, so sector imbalance alternates sign and collapses by a factor 84 per step. The denominator identity <code>84=4·|PG(2,4)|=4·21</code> exactly matches the independently certified 84 Császár and 84 Szilassi flags; this is recorded as a bridge target, not yet a canonical identification.</p>
  <p><a href="{links['cube']}">Cube/observer bridge JSON</a> · <a href="{links['cover']}">central-cover cocycle</a> · <a href="{links['horizon']}">affine/Fano horizon</a> · <a href="{links['outer']}">outer fixed census</a> · <a href="{links['group']}">order-96 presentation/lattice</a> · <a href="{links['schubert']}">all-n Schubert law</a> · <a href="{links['observer']}">observer quotient dynamics</a> · <a href="{links['note']}">randomness/decryptability note</a></p>
  <p><em>Boundary:</em> the exact finite-geometry and information-theory statements above are certified. The cross-model Q3 identification is an explicit coordinate/gauge bridge, the central cocycle is an abstract group-extension invariant, and the toroidal 84 match is presently arithmetic; none of these statements reduces quantum randomness to hidden classical variables.</p>
</section>
{END}
""".strip()
    return body


def patch(text: str, section: str) -> str:
    if BEGIN in text or END in text:
        assert BEGIN in text and END in text, "publication markers must occur as a pair"
        assert text.count(BEGIN) == text.count(END) == 1
        i = text.index(BEGIN)
        j = text.index(END, i) + len(END)
        return text[:i] + section + text[j:]

    anchor = "</main>" if "</main>" in text else "</body>"
    assert anchor in text, "docs/index.html must contain </main> or </body>"
    pos = text.rfind(anchor)
    return text[:pos] + "\n\n" + section + "\n\n" + text[pos:]


def main() -> int:
    original = INDEX.read_text(encoding="utf-8")
    section = render_section()
    updated = patch(original, section)
    INDEX.write_text(updated, encoding="utf-8")
    second = patch(updated, section)
    assert second == updated, "publication patch must be idempotent"
    print(json.dumps({
        "status": "PASS",
        "changed": updated != original,
        "marker_count": updated.count(BEGIN),
        "section_id_present": 'id="heawood-schubert-observer-20260910"' in updated,
        "central_cover_present": "non-split central double cover" in updated,
        "minus_one_over_84_present": "-1/84" in updated,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
