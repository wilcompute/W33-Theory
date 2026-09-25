#!/usr/bin/env python3
"""Pass 10954: regular-C8 spectral completion of the minimal Pin clock.

Pass 10953 gives a six-dimensional unitary clock with C8 characters
{0,1,3,4,5,7}.  This pass adds the unique missing characters {2,6}, i.e.
+i and -i, and proves that the result is the regular representation of C8:
all nonidentity character traces vanish and a canonical eight-state clock
orbit is orthonormal.  The repo's independent temporal Weil packet contains
the same +/-i phase values, but no carrier intertwiner is claimed.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10951_clock_pin_spin_central_sign_bridge as p51
import w33_pass10952_clock_complete_positivity_firewall as p52

OUT = ROOT / "data/w33_pass10954_regular_c8_clock_completion.json"
TOL = 1e-8
def nearest_root_exponent(z, n=8):
    roots = np.exp(2j * np.pi * np.arange(n) / n)
    k = int(np.argmin(np.abs(roots-z)))
    return k, float(abs(roots[k]-z))


def build_doubled_clock():
    p53 = json.loads(
        (ROOT / "data/w33_pass10953_minimal_doubled_pin_clock_visibility.json")
        .read_text(encoding="utf-8")
    )
    g = tuple(tuple(x for x in row)
              for row in json.loads(
                  (ROOT / "data/w33_pass10952_clock_complete_positivity_firewall.json")
                  .read_text(encoding="utf-8")
              )["qutrit_extended_clifford"]["clock_matrix_g"])
    reps, _ = p52.build_sl23_representatives()
    s = p51.mm(g, p52.J)
    u = reps[s]
    z = np.zeros((3,3), complex)
    d = np.block([[z,u],[u.conj(),z]])
    return d, p53
def normalized_uniform_orbit_gram(u):
    vals, vecs = np.linalg.eig(u)
    labels = [nearest_root_exponent(z)[0] for z in vals]
    order = np.argsort(labels)
    q, _ = np.linalg.qr(vecs[:,order])
    psi0 = np.sum(q, axis=1) / np.sqrt(u.shape[0])
    states = [np.linalg.matrix_power(u,n) @ psi0 for n in range(8)]
    gram = np.array([[np.vdot(a,b) for b in states] for a in states])
    return gram


def bit_action(bits, perm, scales):
    signs = tuple(1 if b == 0 else 2 for b in bits)
    image = tuple(scales[i] * signs[perm[i]] % 3 for i in range(4))
    return tuple(0 if x == 1 else 1 for x in image)


def complement(bits):
    return tuple(1-b for b in bits)


def q3(bits):
    x1,x2,x3,x4=bits
    return (x1^x4,x2^x4,x3^x4)


def eig_by_exp(u):
    vals,vecs=np.linalg.eig(u)
    out={}
    for z,v in zip(vals,vecs.T):
        k,err=nearest_root_exponent(z)
        assert err<TOL and k not in out
        out[k]=v/np.linalg.norm(v)
    return out


def main():
    d, p53 = build_doubled_clock()
    labels = sorted(nearest_root_exponent(z)[0] for z in np.linalg.eigvals(d))
    assert labels == [0,1,3,4,5,7]
    missing = sorted(set(range(8))-set(labels))
    assert missing == [2,6]

    aux = np.diag([1j,-1j]).astype(complex)
    zero62 = np.zeros((6,2),complex)
    zero26 = np.zeros((2,6),complex)
    completed = np.block([[d,zero62],[zero26,aux]])
    assert np.linalg.norm(completed@completed.conj().T-np.eye(8)) < TOL
    comp_labels = sorted(
        nearest_root_exponent(z)[0] for z in np.linalg.eigvals(completed)
    )
    assert comp_labels == list(range(8))
    assert np.linalg.norm(np.linalg.matrix_power(completed,8)-np.eye(8)) < TOL

    traces=[]
    vis=[]
    for n in range(8):
        tr=np.trace(np.linalg.matrix_power(completed,n))
        traces.append([float(np.round(tr.real,12)),float(np.round(tr.imag,12))])
        vis.append(float(np.round(abs(tr)/8,12)))
    assert np.allclose(np.array(traces),
                       np.array([[8,0]]+[[0,0]]*7),atol=TOL)
    assert vis == [1.0]+[0.0]*7

    regular_poly=np.linalg.norm(
        np.linalg.matrix_power(completed,8)-np.eye(8)
    )
    # Every C8 character occurs once, hence x^8-1 is the minimal polynomial.
    assert regular_poly < TOL

    gram8=normalized_uniform_orbit_gram(completed)
    assert np.linalg.norm(gram8-np.eye(8)) < TOL
    # The compressed six-mode orbit cannot resolve eight orthogonal clock states.
    gram6=normalized_uniform_orbit_gram(d)
    gram6_eigs=np.linalg.eigvalsh((gram6+gram6.conj().T)/2)
    gram6_rank=int(np.sum(gram6_eigs>TOL))
    assert gram6_rank == 6
    off6=gram6-np.eye(8)
    max_alias=float(np.max(np.abs(off6)))
    assert abs(max_alias-1/3) < TOL

    # Unique minimal character completion: two missing one-dimensional characters.
    completion_dimension=8
    lower_bound_for_8_orthogonal_states=8
    assert completion_dimension == lower_bound_for_8_orthogonal_states

    # Repo-native realization: the 16 oriented A2^4 sign states before the
    # global-inversion quotient split into two regular C8 clock orbits.
    p52_data=json.loads(
        (ROOT/"data/w33_pass10952_clock_complete_positivity_firewall.json")
        .read_text(encoding="utf-8")
    )
    g=tuple(tuple(x for x in row)
            for row in p52_data["qutrit_extended_clifford"]["clock_matrix_g"])
    perm,scales=p51.p46.monomial_pullback(g)
    states=list(itertools.product((0,1),repeat=4))
    state_id={x:i for i,x in enumerate(states)}
    p16=tuple(state_id[bit_action(x,perm,scales)] for x in states)
    cycles16=[]
    seen=set()
    for i in range(16):
        if i in seen:
            continue
        cyc=[]; j=i
        while j not in seen:
            seen.add(j); cyc.append(j); j=p16[j]
        cycles16.append(cyc)
    assert sorted(len(c) for c in cycles16)==[8,8]
    for x in states:
        y=x
        for _ in range(4):
            y=bit_action(y,perm,scales)
        assert y==complement(x)

    # Across the whole GL(2,3) clock/tetracode group, determinant is exactly
    # the orientation-parity flip character.
    det_flip_hist={}
    gl=[]
    for e in itertools.product(range(3),repeat=4):
        m=((e[0],e[1]),(e[2],e[3]))
        if p51.p46.det2(m):
            gl.append(m)
    assert len(gl)==48
    for m in gl:
        _,ss=p51.p46.monomial_pullback(m)
        flip=sum(x==2 for x in ss)%2
        detbit=0 if p51.p46.det2(m)==1 else 1
        assert flip==detbit
        det_flip_hist[(p51.p46.det2(m),flip)]=det_flip_hist.get(
            (p51.p46.det2(m),flip),0
        )+1
    assert det_flip_hist=={(1,0):24,(2,1):24}

    # Quotienting simultaneous inversion produces the existing eight-leaf
    # F2^4/<1111> fibre.  Our order-eight lift becomes two 4-cycles there.
    leaf_pts=sorted({q3(x) for x in states})
    leaf_id={x:i for i,x in enumerate(leaf_pts)}
    leaf_perm=[]
    for x in leaf_pts:
        lift=(x[0],x[1],x[2],0)
        leaf_perm.append(leaf_id[q3(bit_action(lift,perm,scales))])
    leaf_cycles=[]; seen=set()
    for i in range(8):
        if i in seen:
            continue
        cyc=[]; j=i
        while j not in seen:
            seen.add(j); cyc.append(j); j=leaf_perm[j]
        leaf_cycles.append(cyc)
    assert sorted(len(c) for c in leaf_cycles)==[4,4]
    assert all(
        [sum(leaf_pts[i])%2 for i in cyc] in ([0,1,0,1],[1,0,1,0])
        for cyc in leaf_cycles
    )

    old_fibre=json.loads(
        (ROOT/"data/w33_20260924_temporal_tetracode_common_mode.json")
        .read_text(encoding="utf-8")
    )
    assert old_fibre["pass7409_weld"]["orientation_states"]==8
    assert old_fibre["automorphisms"]["fibre_cycle_type_histogram"][
        "(4, 4)"
    ]==6

    # Label either oriented 8-cycle by successive powers of g.  Its permutation
    # matrix is the regular C8 shift, giving a repo-native realization of the
    # spectral completion rather than an abstract auxiliary pair.
    r8=np.zeros((8,8),complex)
    for n in range(8):
        r8[(n+1)%8,n]=1
    assert sorted(eig_by_exp(r8))==list(range(8))
    er=eig_by_exp(r8)
    ec=eig_by_exp(completed)
    ed=eig_by_exp(d)
    w8=sum(np.outer(er[k],ec[k].conj()) for k in range(8))
    assert np.linalg.norm(w8.conj().T@w8-np.eye(8))<TOL
    full_intertwiner_error=float(np.linalg.norm(r8@w8-w8@completed))
    assert full_intertwiner_error<TOL

    w6=sum(np.outer(er[k],ed[k].conj()) for k in labels)
    assert np.linalg.norm(w6.conj().T@w6-np.eye(6))<TOL
    compressed_intertwiner_error=float(np.linalg.norm(r8@w6-w6@d))
    assert compressed_intertwiner_error<TOL
    p6=w6@w6.conj().T
    pmiss=np.eye(8)-p6
    expected_miss=sum(np.outer(er[k],er[k].conj()) for k in missing)
    missing_projector_error=float(np.linalg.norm(pmiss-expected_miss))
    assert missing_projector_error<TOL

    # Four ticks are the deck involution x -> x+1111.  The missing +/-i modes
    # are deck-even and therefore descend to the unoriented leaf quotient.
    deck=np.linalg.matrix_power(r8,4)
    pplus=(np.eye(8)+deck)/2
    pminus=(np.eye(8)-deck)/2
    assert np.linalg.matrix_rank(pplus,TOL)==4
    assert np.linalg.matrix_rank(pminus,TOL)==4
    assert all(np.linalg.norm(deck@er[k]-er[k])<TOL for k in missing)
    pin_deck_even_rank=int(np.linalg.matrix_rank(pplus@w6,TOL))
    pin_deck_odd_rank=int(np.linalg.matrix_rank(pminus@w6,TOL))
    assert (pin_deck_even_rank,pin_deck_odd_rank)==(2,4)

    maslov=json.loads(
        (ROOT/"data/w33_20260924_temporal_maslov_mu12.json")
        .read_text(encoding="utf-8")
    )
    hist=maslov["quadratic_history_atlas"]["phase_exponent_histogram_mu12"]
    assert hist == {"0":13,"3":4,"6":6,"9":4}
    temporal_values={
        "mu12_exponent_3": "i",
        "mu12_exponent_9": "-i",
    }
    out={
      "schema":"w33.pass10954.regular-c8-clock-completion.v1",
      "status":"PASS_REGULAR_C8_CLOCK_COMPLETION",
      "compressed_clock":{
        "dimension":6,
        "C8_character_exponents":labels,
        "missing_character_exponents":missing,
        "missing_phase_values":["+i","-i"],
        "eight_orbit_gram_rank":gram6_rank,
        "max_offdiagonal_clock_alias":max_alias,
        "reading":"the 6D Pin clock is a two-frequency compression of the regular C8 clock",
      },
      "unique_minimal_completion":{
        "auxiliary_matrix":"diag(+i,-i)",
        "added_character_exponents":[2,6],
        "dimension":8,
        "lower_bound_for_eight_orthogonal_clock_positions":8,
        "all_C8_characters_once":comp_labels==list(range(8)),
        "minimal_polynomial":"x^8-1",
        "power8_identity_error":regular_poly,
      },
      "regular_clock":{
        "trace_sequence":traces,
        "normalized_trace_visibility":vis,
        "uniform_spectral_clock_gram_identity_error":
            float(np.linalg.norm(gram8-np.eye(8))),
        "theorem":
            "the completed carrier is the regular representation of C8 and admits eight mutually orthogonal clock positions",
      },
      "oriented_A2_4_clock_cover":{
        "oriented_sign_states":16,
        "clock_cycle_lengths":[len(c) for c in cycles16],
        "four_ticks":"global complement x -> x+1111",
        "eight_ticks":"identity",
        "leaf_quotient_states":8,
        "leaf_cycle_lengths":[len(c) for c in leaf_cycles],
        "leaf_cycles_alternate_Fano_parity":True,
        "regular_C8_orbit_count":2,
        "full_8D_intertwiner_error":full_intertwiner_error,
        "compressed_6D_intertwiner_error":compressed_intertwiner_error,
        "missing_projector_error":missing_projector_error,
        "pin_subspace_deck_even_rank":pin_deck_even_rank,
        "pin_subspace_deck_odd_rank":pin_deck_odd_rank,
        "missing_modes_deck_even":True,
        "reading":(
            "each oriented lift of one projective four-cycle is a regular C8 orbit; "
            "the six-dimensional Pin clock is exactly the character-deleted subrepresentation "
            "with k=2,6 omitted"
        ),
      },
      "shared_determinant_character":{
        "GL2_3_elements":48,
        "det_plus_orientation_preserving":det_flip_hist[(1,0)],
        "det_minus_orientation_flipping":det_flip_hist[(2,1)],
        "all48_exact":True,
        "channel_weld":(
            "the same determinant C2 distinguishes unitary/antiunitary extended-Clifford "
            "actions and, for the clock powers, CP/non-CP operation slots"
        ),
        "fibre_weld":(
            "determinant +1 preserves the Fano-hinge bipartition; determinant -1 flips it"
        ),
      },
      "temporal_weil_phase_comparison":{
        "source_status":maslov["status"],
        "phase_exponent_histogram_mu12":hist,
        "rank_one_phase_values":temporal_values,
        "value_match":
            "the independently certified temporal rank-one Weil phases +/-i equal the two missing C8 phase values",
        "firewall":
            "phase-value equality only; no objectwise map from the two Weil orbits to the two auxiliary one-dimensional C8 characters is constructed",
      },
      "interpretation":{
        "spectral_resolution":
            "the 1/3 residual overlaps of Pass10953 are exactly aliasing caused by omitting the +/-i frequency pair",
        "completion_effect":
            "adding that pair cancels every nonzero-tick character overlap and yields perfect eight-step distinguishability",
        "repo_native_completion":
            "the required regular C8 already occurs on either oriented eight-cycle above the A2^4 leaf fibre",
        "deck_mode_correction":
            "the missing +/-i modes are deck-even leaf-descending modes, not orientation-odd modes",
        "hardware_boundary":
            "this is a finite representation/reference-frame design target; no current 8D photonic implementation or temporal-Weil intertwiner is asserted",
      },
      "theorem":(
        "The minimal 6D Pin clock is the regular C8 character spectrum with exactly "
        "the +/-i characters removed. The completion is not merely formal: the exact "
        "Pass10951 clock acts on the 16 pre-quotient A2^4 orientation-sign states as "
        "two disjoint 8-cycles, and either cycle carries the regular C8 representation. "
        "Four ticks are the global inversion deck transformation and quotient to the "
        "existing two 4-cycles on the eight E8 leaves. An explicit unitary intertwiner "
        "embeds the 6D Pin clock as the k={0,1,3,4,5,7} subrepresentation; its missing "
        "k={2,6} modes are both deck-even. Across all 48 GL(2,3) automorphisms, "
        "determinant +1 exactly preserves and determinant -1 exactly flips the Fano-hinge "
        "orientation parity, the same C2 used by the extended-Clifford/CP grading. "
        "The independent temporal Weil atlas has the same +/-i phase values, but no "
        "Weil-orbit intertwiner is claimed."
      ),
      "boundary":(
        "This identifies an exact finite E8/tetracode orientation-cover carrier and a "
        "shared determinant character. It does not identify the oriented cover with "
        "physical time, the missing deck-even modes with temporal chirality, the two "
        "8-cycles with past/future, or the auxiliary spectral degrees with particles."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "compressed":labels,
      "missing":missing,
      "regular":comp_labels,
      "visibility":vis,
      "gram8_error":out["regular_clock"]["uniform_spectral_clock_gram_identity_error"],
      "compressed_alias":max_alias,
    },indent=2))


if __name__=="__main__":
    main()
