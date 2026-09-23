#!/usr/bin/env python3
"""Exact anti-linear real structure of the executable hybrid E8 compiler.

The recent hybrid Chevalley compiler makes it possible to upgrade the earlier
label-level charge-conjugation scaffold to an honest semilinear Lie-algebra
automorphism.

On the committed source Chevalley basis define
    theta(h_i) = -h_i,
    theta(e_alpha) = e_{-alpha}.
The source structure constants are integers.  Direct exhaustive verification
over all C(248,2)=30,628 unordered basis pairs proves theta([x,y]) =
[theta(x),theta(y)].  Composing theta with Eisenstein conjugation
omega <-> omega^2 therefore gives an anti-linear involutive Lie automorphism J.

The fixed Q-real form can be analyzed without introducing numerical
approximations.  Let delta=1+2 omega, so conjugate(delta)=-delta and delta^2=-3.
For each opposite-root pair the J-fixed plane is spanned over Q by
    e_alpha+e_-alpha,
    delta(e_alpha-e_-alpha),
while the Cartan fixed directions are delta h_i.

The exact Killing form computed from the committed structure constants has
Cartan block positive definite, and opposite-root pairings
    +60 on 64 pairs,
    -60 on 56 pairs.
Therefore the J-fixed real form has inertia
    (128 positive, 120 negative),
Killing signature +8.  This is the split real form E8(8).

In hybrid coordinates the true involution is NOT the earlier labelwise scaffold:
all 81 g1 source roots do pair with the exact g2 negative roots, but 39 of the
81 frozen row signs differ.  Thus on the matter block
    J_12 = Bbar^{-1} D Bbar o conjugation,
where D=diag(sign_g1 * sign_g2) has 39 minus signs.
The neutral block also needs h_i -> -h_i and root negation, rather than fixing
its 86 labels pointwise.

No spacetime, gravity, or physical CP claim follows from identifying the split
real form of this finite Lie-algebra compiler.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_split_real_form_involution.json"

def bracket_terms(sc,a,b):
    if a==b:return []
    sign=1 if a<b else -1
    key=f"{min(a,b)},{max(a,b)}"
    return [(int(k),sign*int(c)) for k,c in sc["brackets"].get(key,[])]

def bracket_vec(sc,A,B):
    out={}
    for a,x in A.items():
        for b,y in B.items():
            for k,c in bracket_terms(sc,a,b):
                out[k]=out.get(k,0)+x*y*c
                if out[k]==0:del out[k]
    return out

def theta_vec(v,neg):
    out={}
    for k,c in v.items():
        if k<8:out[k]=out.get(k,0)-c
        else:out[neg[k]]=out.get(neg[k],0)+c
    return {k:v for k,v in out.items() if v}

def gf2_rank_solution(equations,n):
    basis=[None]*n
    rank=0
    for mask,rhs in equations:
        m=int(mask);r=int(rhs)&1
        while m:
            p=m.bit_length()-1
            if basis[p] is None:
                basis[p]=(m,r);rank+=1;break
            m^=basis[p][0];r^=basis[p][1]
        if m==0 and r:
            raise AssertionError("inconsistent sign system")
    sol=[0]*n
    for p in range(n):
        if basis[p] is None:continue
        m,r=basis[p]
        lower=m&((1<<p)-1)
        v=r
        while lower:
            bit=lower&-lower
            j=bit.bit_length()-1
            v^=sol[j]
            lower^=bit
        sol[p]=v
    return rank,sol

def killing(sc,a,b):
    tr=0
    for j in range(248):
        for k,c1 in bracket_terms(sc,b,j):
            for ell,c2 in bracket_terms(sc,a,k):
                if ell==j:tr+=c1*c2
    return tr

def ldl_inertia(A):
    n=len(A)
    L=[[Fraction(0) for _ in range(n)] for _ in range(n)]
    D=[Fraction(0) for _ in range(n)]
    for i in range(n):
        L[i][i]=1
        d=Fraction(A[i][i])
        for k in range(i):d-=L[i][k]*L[i][k]*D[k]
        assert d
        D[i]=d
        for j in range(i+1,n):
            v=Fraction(A[j][i])
            for k in range(i):v-=L[j][k]*L[i][k]*D[k]
            L[j][i]=v/D[i]
    return D,sum(x>0 for x in D),sum(x<0 for x in D)

def main(write=True):
    sc=json.loads((ROOT/"artifacts/e8_structure_constants_w33_discrete.json").read_text())
    comp=json.loads((ROOT/"data/w33_e8_full_hybrid_chevalley_compiler.json").read_text())
    charge=json.loads((ROOT/"data/w33_e8_hybrid_charge_conjugation.json").read_text())
    assert sc["basis"]["n"]==248 and sc["basis"]["cartan_dim"]==8
    roots=[tuple(map(int,r)) for r in sc["basis"]["roots"]]
    rmap={r:8+i for i,r in enumerate(roots)}
    neg={8+i:rmap[tuple(-x for x in r)] for i,r in enumerate(roots)}
    assert all(neg[neg[i]]==i for i in range(8,248))

    # Solve the complete +/- root-phase constraint system.  The source gauge
    # admits the particularly simple all-plus root-negation involution.
    equations=[]
    for a in range(8,248):
        b=neg[a]
        if a<b:
            equations.append(((1<<(a-8))^(1<<(b-8)),0))
    root_brackets=0
    for a in range(8,248):
        for b in range(a+1,248):
            t=bracket_terms(sc,a,b)
            if len(t)==1 and t[0][0]>=8:
                g,N=t[0]
                tn=bracket_terms(sc,neg[a],neg[b])
                assert len(tn)==1 and tn[0][0]==neg[g]
                Nn=tn[0][1]
                ratio=Nn//N
                assert ratio in (-1,1)
                rhs=0 if ratio==1 else 1
                mask=(1<<(a-8))^(1<<(b-8))^(1<<(g-8))
                equations.append((mask,rhs));root_brackets+=1
    rank,sol=gf2_rank_solution(equations,240)
    assert len(equations)==6840 and root_brackets==6720
    assert rank==232 and 240-rank==8
    assert set(sol)=={0}

    # Exhaustive Lie-automorphism check on the full source basis.
    checked=0
    for a in range(247):
        for b in range(a+1,248):
            A={a:1};B={b:1}
            lhs=theta_vec(bracket_vec(sc,A,B),neg)
            rhs=bracket_vec(sc,theta_vec(A,neg),theta_vec(B,neg))
            assert lhs==rhs,(a,b,lhs,rhs)
            checked+=1
    assert checked==30628

    # Exact Killing form and real-form signature.
    Kh=[[killing(sc,i,j) for j in range(8)] for i in range(8)]
    D,hpos,hneg=ldl_inertia(Kh)
    assert (hpos,hneg)==(8,0)
    rootK=[]
    for a in range(8,248):
        if a<neg[a]:rootK.append(killing(sc,a,neg[a]))
    hist={str(v):rootK.count(v) for v in sorted(set(rootK))}
    assert hist=={"-60":56,"60":64}
    # For delta=1+2omega, delta^2=-3.  Fixed Cartan directions delta*h
    # reverse the positive Cartan sign; each fixed root plane retains sign K.
    positive=2*hist["60"]+hneg
    negative=2*hist["-60"]+hpos
    assert (positive,negative)==(128,120)

    # Compare the true transported involution with the earlier label scaffold.
    maps=comp["coordinate_maps"]
    ratios=[]
    for i in range(81):
        assert neg[int(maps["grade1_source_indices"][i])]==int(maps["grade2_source_indices"][i])
        ratios.append(int(maps["grade1_signs"][i])*int(maps["grade2_signs"][i]))
    assert ratios.count(-1)==39 and ratios.count(1)==42
    assert charge["involution"]["grade_action"]=={"g0":"g0","g1":"g2","g2":"g1"}

    g0=maps["neutral_source_indices"]
    assert g0[:8]==list(range(8))
    neutral_roots=g0[8:]
    assert len(neutral_roots)==78
    assert set(neutral_roots)=={neg[i] for i in neutral_roots}

    out={
      "schema":"w33.e8_split_real_form_involution.v1",
      "status":"PASS_TRUE_ANTILINEAR_HYBRID_E8_LIE_INVOLUTION_HAS_SPLIT_REAL_FORM_E8_8",
      "headline":"The executable 248D hybrid compiler now has an exact anti-linear Lie-algebra real structure, upgrading the previous label-level charge-conjugation scaffold. In the committed source Chevalley gauge theta(h_i)=-h_i and theta(e_alpha)=e_-alpha satisfies every one of the 30,628 unordered basis-pair bracket identities. Since the structure constants are integral, J=theta composed with Eisenstein conjugation is anti-linear and involutive. The exact fixed-form Killing inertia is (128 positive,120 negative), hence signature +8 and real form E8(8), the split form. Transport into hybrid coordinates shows why the former pointwise scaffold was incomplete: all 81 matter roots pair with their exact negatives, but 39 row-gauge signs differ, producing a nontrivial Bbar^-1 D Bbar correction, while the neutral block requires Cartan sign reversal and root negation.",
      "source_involution":{
        "cartan_rule":"h_i -> -h_i",
        "root_rule":"e_alpha -> e_-alpha",
        "root_phase_sign_solution":"all +1 in the committed Chevalley gauge",
        "phase_constraint_equations":len(equations),
        "phase_constraint_rank":rank,
        "phase_constraint_nullity":240-rank,
        "unordered_basis_pairs_checked":checked,
        "all_brackets_preserved":True,
        "Eisenstein_semilinear_rule":"J = theta o (omega -> omega^2)",
        "J_squared":1
      },
      "killing_form":{
        "cartan_block":Kh,
        "cartan_LDL_diagonal":[str(x) for x in D],
        "cartan_inertia":{"positive":hpos,"negative":hneg},
        "opposite_root_pairing_histogram":hist,
        "fixed_real_form_inertia":{"positive":positive,"negative":negative,"zero":0},
        "signature_difference":positive-negative,
        "real_form":"E8(8), split real form",
        "fixed_field_basis_note":"delta=1+2omega obeys conjugate(delta)=-delta and delta^2=-3; fixed Cartan directions are delta*h_i"
      },
      "hybrid_transport":{
        "all_81_grade1_roots_pair_with_exact_grade2_negatives":True,
        "row_sign_ratio_plus":ratios.count(1),
        "row_sign_ratio_minus":ratios.count(-1),
        "matter_formula":"J_12(x)=Bbar^{-1} D Bbar conjugate(x), D=diag(sign_g1*sign_g2)",
        "matter_identity_swap_is_exact":False,
        "neutral_formula":"h_i -> -h_i and each of the 78 neutral root vectors -> its opposite root vector",
        "previous_scaffold_status":"correct as a grade-label/coefficient-conjugation scaffold, but not the full transported Lie involution"
      },
      "physics_reading":"The finite E8 compiler carries the split E8(8) real structure exactly. This creates a rigorous algebraic interface to any future dynamics that genuinely uses E8(8), while separating that statement from spacetime, supergravity, vacuum selection, or observed CP physics.",
      "boundary":"Identifying the real form E8(8) is a Lie-algebra statement from the exact Killing signature. It does not derive an E8(8) gauge theory of nature, exceptional field theory, a spacetime signature, gravity, a Hamiltonian, a vacuum, masses, couplings, or CP violation.",
      "parents":[
        "artifacts/e8_structure_constants_w33_discrete.json",
        "data/w33_e8_full_hybrid_chevalley_compiler.json",
        "data/w33_e8_hybrid_charge_conjugation.json"
      ],
      "checks":{
        "root_negation_is_bijection":True,
        "all_plus_phase_solution":True,
        "all_30628_basis_pair_brackets_preserved":True,
        "J_antilinear_involutive":True,
        "killing_signature_128_120":True,
        "split_real_form_E8_8":True,
        "all_81_matter_root_negations_aligned":True,
        "39_hybrid_row_sign_mismatches_expose_nontrivial_correction":True,
        "neutral_block_not_pointwise_fixed":True,
        "physics_not_overclaimed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
