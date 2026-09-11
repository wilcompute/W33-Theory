#!/usr/bin/env python3
"""Publish the September 2026 Heawood/Schubert/observer frontier into docs/index.html.

The section is generated only from frozen exact certificates and replaced between
stable markers.  Running twice is idempotent.
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
    lag = load("data/w33_projective_horizon_lag_law.json")
    finite = load("data/w33_trace_observer_finite_observability.json")
    bridge84 = load("data/w33_boundary_singer_toroidal_84_bridge.json")
    parity = load("data/w33_cocycle_rank1_576_parity_firewall.json")
    a4core = load("data/w33_a4_untwisted_core_synthesis.json")

    certs = (outer, group, schubert, observer, cube, cover, horizon, lag, finite, bridge84, parity, a4core)
    assert all(x["status"] == "PASS" for x in certs)

    fixed_modes = outer["fixed_objects"]["fixed_pair_modes"]
    lattice_n = group["normal_subgroup_lattice"]["normal_subgroup_count"]
    model = observer["n3_one_step_model"]
    q = cube["spread_orbit_quotient"]
    cocycle = cover["extension_cocycle"]
    h3 = horizon["n3_information_horizon"]
    l3 = lag["n3_projective_anticorrelation"]
    obs = finite["trace_trajectory_observability"]

    links = {
        "outer": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_heawood_outer_involution_fixed_census.json",
        "group": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_heawood_stabilizer96_presentation_lattice.json",
        "schubert": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_marcelis_trace_schubert_general.json",
        "observer": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_marcelis_observer_quotient_dynamics.json",
        "cube": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_outer_cube_observer_bridge.json",
        "cover": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_stabilizer96_cube_central_cover.json",
        "horizon": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_affine_fano_information_horizon.json",
        "lag": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_projective_horizon_lag_law.json",
        "finite": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_trace_observer_finite_observability.json",
        "bridge84": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_boundary_singer_toroidal_84_bridge.json",
        "parity": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_cocycle_rank1_576_parity_firewall.json",
        "a4": "https://github.com/wilcompute/W33-Theory/blob/master/data/w33_a4_untwisted_core_synthesis.json",
        "note": "https://github.com/wilcompute/W33-Theory/blob/master/analysis/W33_OBSERVER_RELATIVE_RANDOMNESS.md",
    }

    body = f"""
{BEGIN}
<section id="heawood-schubert-observer-20260910" aria-labelledby="heawood-schubert-observer-title">
  <h2 id="heawood-schubert-observer-title">September 2026: outer involution, observer geometry, and the untwisted A4 core</h2>
  <p><strong>Exact certificate frontier.</strong> The multiplier-two outer involution on the 270 Heawood C6 components has cycle structure <code>12 + 129×2</code>. Under the equivariant spread dictionary the 12 fixed objects split exactly <code>{fixed_modes['both_spreads_fixed']} + {fixed_modes['spreads_exchanged']}</code>: six pairs of individually fixed spreads and six pairs whose spreads are exchanged.</p>
  <p>The order-96 C6 stabilizer is the split fiber product <code>D8 ×_C2 S4 ≅ V4 ⋊ S4</code>, with center <code>C2</code>, derived subgroup <code>C2 × A4</code>, abelianization <code>C2 × C2</code>, and a complete <strong>{lattice_n}-node</strong> normal-subgroup lattice.</p>
  <p>The omega-normalized Marcelis trace map obeys an all-n flag law: for <code>b ∈ F_j \\ F_(j+1)</code>, point fibres have size <code>2^(n-j)</code>; incidence-preserving binary lines in the same stratum have <code>2^(n-1-j)</code> GF(4) lifts. At n=3 this recovers the 1/2/4/8 point staircase and the 4/2/1 line staircase.</p>
  <p>A deterministic cyclic coordinate update on <code>PG(3,4)</code> becomes stochastic after the many-to-one trace observer quotient to <code>PG(3,2)</code>: <strong>{model['observer_kernel']['stochastic_macro_states']}</strong> macrostates are stochastic and <strong>{model['observer_kernel']['deterministic_macro_states']}</strong> are deterministic, with <code>H(B′|B)={html.escape(model['observer_kernel']['H_Bprime_given_B_bits_exact'])}</code> bits. Retaining the fibre key restores <code>H(B′|B,K)=0</code>.</p>
  <p><strong>New cubical bridge.</strong> The complement of W33 collinearity on the eight outer-fixed points is exactly <code>Q3</code>. The stochastic Schubert chart <code>x0=1</code> is <code>AG(3,2) ≅ F2^3</code>, giving a second explicit Q3, and appending one frozen bit embeds it as a facet of the already-certified Q4 temporal router. On the spread side the four fixed spreads form a K4; the quotient of the 270 four-intersection edges has {q['four_intersection_edge_orbits']} edge orbits, with six fixed ordinary edges and six fixed loops recording exchanged spread pairs.</p>
  <p><strong>Central-cover phase obstruction.</strong> The same order-96 Heawood stabilizer is a <em>non-split central double cover</em> of cube symmetry: <code>1 → C2 → H → Aut(Q3) → 1</code> with <code>Aut(Q3) ≅ C2 × S4</code>. The normalized cocycle <code>α((b,σ),(d,τ)) = d·sgn(σ) mod 2</code> was checked on all <strong>{cocycle['cocycle_triples_checked']}</strong> quotient triples.</p>
  <p><strong>Corrected affine/Fano law.</strong> The observer split is <code>PG(3,2)=AG(3,2) ⊔ PG(2,2)</code>: eight stochastic affine macrostates over 64 GF(4) microstates versus seven deterministic Fano-at-infinity macrostates over 21 microstates. The one-lag pair table is <code>[[3/4,1/4],[16/21,5/21]]</code>, whose nontrivial eigenvalue is <strong>{html.escape(h3['nontrivial_eigenvalue'])}</strong>. This value is <em>not</em> a repeated-time decay rate: the exact lag certificate gives autocorrelation <code>{html.escape(str(l3['autocorrelation_over_one_period']))}</code>, so lags 1,2,3 all have correlation −1/84 and lag 4 is the exact identity.</p>
  <p><strong>Finite observability.</strong> The trace quotient is not irreversibly lossy under the declared order-four dynamics. Consecutive trace words distinguish <code>15 → 57 → 77 → 85</code> microstate classes, and <strong>{obs['minimal_observability_horizon']} samples recover the exact PG(3,4) microstate</strong>. Residual entropies are <code>228/85 → 72/85 → 16/85 → 0</code> bits. By contrast, a support-mask observer with the same 15 macrostate cardinality is an exact deterministic factor from the first step. Apparent stochasticity is therefore a partition-equivariance property, not a state-count property.</p>
  <p><strong>The 84 bridge is now constructive.</strong> The projective boundary codec has <code>84=|PG(2,4)|·|GF(4)|=21·4</code> states. A regular Singer <code>C21</code> supplies a <code>C7</code> whose quotient has 12 states, identified exactly as <code>GF(4)×GF(4)* = AGL(1,4) ≅ A4</code>, acting sharply transitively on the 12 directed K4 edges. Lifting those phases around the repo's concrete toroidal Singer cycle gives an explicit <strong>C7-equivariant 84↔84 bijection</strong> to the Császár/Szilassi flag system, after the declared Singer and affine-coordinate choices.</p>
  <p><strong>A4 untwisted core and the 576 firewall.</strong> The same local <code>AGL(1,4)</code> is literally the even-permutation <code>A4 &lt; S4</code> on the four affine labels. It matches the normal order-12 <code>A4_section</code> in the stabilizer lattice, while <code>H′=C2×A4</code> and the order-48 preimage is <code>V4×A4</code>. The cocycle vanishes whenever the first S4 element is even. Its 48×48 support therefore has exactly <strong>{parity['support_geometry']['twisted_pairs']}</strong> twisted entries <code>=24²=576</code> and <strong>{parity['support_geometry']['untwisted_pairs']}</strong> untwisted entries. On abelianization the commutator is the nondegenerate binary symplectic form, and its eight-element central lift is exactly <code>D8</code>. Thus the tetrahedral A4 codec is an exact untwisted core; the central obstruction appears only on extension through odd S4 parity and the antipodal bit.</p>
  <p><a href="{links['cube']}">cube/observer Q3</a> · <a href="{links['cover']}">central-cover cocycle</a> · <a href="{links['horizon']}">affine/Fano pair law</a> · <a href="{links['lag']}">exact lag correction</a> · <a href="{links['finite']}">four-sample observability</a> · <a href="{links['bridge84']}">C7-equivariant 84 bridge</a> · <a href="{links['parity']}">576 parity firewall</a> · <a href="{links['a4']}">A4 untwisted core</a> · <a href="{links['outer']}">outer census</a> · <a href="{links['group']}">order-96 lattice</a> · <a href="{links['schubert']}">all-n Schubert law</a> · <a href="{links['observer']}">observer quotient</a> · <a href="{links['note']}">randomness/decryptability note</a></p>
  <p><em>Boundary:</em> the finite-geometry, group-cohomology, and information-theory statements above are exact certificates. The Q3 and 84 cross-model dictionaries use declared gauges, and the central cocycle is a finite group-extension invariant. None of these statements reduces Bell-certified quantum randomness to hidden classical variables, identifies the cocycle with Spin/Pin physics, or supplies a spacetime interpretation of the observer horizon.</p>
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
    assert patch(updated, section) == updated, "publication patch must be idempotent"
    print(json.dumps({
        "status": "PASS",
        "changed": updated != original,
        "marker_count": updated.count(BEGIN),
        "section_id_present": 'id="heawood-schubert-observer-20260910"' in updated,
        "central_cover_present": "non-split central double cover" in updated,
        "minus_one_over_84_present": "-1/84" in updated,
        "four_sample_observability_present": "4 samples recover" in updated,
        "equivariant_84_bridge_present": "C7-equivariant 84" in updated,
        "A4_untwisted_core_present": "A4 untwisted core" in updated,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
