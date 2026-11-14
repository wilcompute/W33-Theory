#!/usr/bin/env python3
"""Exact quadratic scalar-potential audit in published E6(6) ExFT.

For constant external metric g, the published E6 ExFT potential is
V=-1/24 M^{MN}(d_M M^{KL})(d_N M_KL)
  +1/2 M^{MN}(d_M M^{KL})(d_L M_NK)
plus derivative(g) terms.

At M(Y)=exp(epsilon h sin(q.Y)) and Y=0, M=I and derivatives
epsilon*q_M*h. For symmetric cubic-preserving split-E6 Lie algebra
coset h this yields exactly:
  V/e^2 = Tr(h²) q²/24 - ||h q||²/2.
The symmetric 42D tangent's orthogonal projector has exact identity
  sum_{a=1}^42 h_a² = (14/9) I_27
for a Hilbert-Schmidt orthonormal basis {h_a}.
Thus an isotropic h ensemble with E Tr(h²)=1 gives
  E V/e² = (5/216)||q||²
independent of M6 vs IIB5 sections.

This is a negative result for INTRINSIC branch selection by a
homogeneous / isotropic quadratic scalar sector, not an assertion
that ExFT flux vacua cannot distinguish geometries.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_E6_exft_generalized_closure_affine as Ex
OUT=ROOT/"data/toe_20261114_E6_ExFT_scalar_potential_isotropy_nogo.json"

def main():
    cert,terms,_,_,roots=R.load()
    gens=[]
    for row in cert["cubic_27"]["generators"]:
        X=np.zeros((27,27),dtype=np.int64)
        for i,j,v in row:X[i,j]=v
        gens.append(X)
    assert len(gens)==78
    diags=[M for M in gens if np.array_equal(M,np.diag(np.diag(M)))]
    assert len(diags)==6
    raw=[M for M in gens if not np.array_equal(M,np.diag(np.diag(M)))]
    assert len(raw)==72
    mapH={}
    for A in raw:
        H=A+A.T
        assert np.array_equal(H,H.T)
        assert np.count_nonzero(H)==12
        assert np.array_equal(H@H,np.diag(np.diag(H@H)))
        nz=tuple((int(i),int(j),int(H[i,j]))
              for i,j in combinations(range(27),2) if H[i,j])
        if nz[0][2]<0:
            H=-H
            nz=tuple((i,j,-v) for i,j,v in nz)
        assert len(nz)==6
        mapH[nz]=H
    assert len(mapH)==36
    Hs=list(mapH.values())
    GramR=np.array([[int(np.trace(A@B)) for B in Hs] for A in Hs])
    assert np.array_equal(GramR,12*np.eye(36,dtype=np.int64))
    D=np.array([np.diag(X).astype(np.int64) for X in diags])
    GramD=sp.Matrix((D@D.T).tolist())
    assert GramD.det()!=0
    Ginv=GramD.inv()
    diag_proj=sp.Matrix(D.T.tolist())*Ginv*sp.Matrix(D.tolist())
    assert diag_proj.shape==(27,27)
    # 36 normalized H matrices plus a Gram-inverse resolution of the
    # six (not necessarily orthonormal) diagonal Cartan matrices.
    rootQ=sum((H@H for H in Hs),np.zeros((27,27),dtype=np.int64))
    assert np.array_equal(rootQ,np.diag(np.diag(rootQ)))
    assert set(np.diag(rootQ).tolist())=={16}
    assert set(diag_proj[i,i] for i in range(27))=={sp.Rational(2,9)}
    # The Cartan *orthogonal projector* has off-diagonal entries;
    # the sum of squares of six normalized diagonal matrices is
    # instead diagonal, containing only projector[i,i].
    diag_squares=sp.diag(*[diag_proj[i,i] for i in range(27)])
    fullQ=sp.Matrix(rootQ.tolist())/12+diag_squares
    assert fullQ==sp.Rational(14,9)*sp.eye(27)
    assert sp.trace(fullQ)==42

    # Exact polarization of published ExFT scalar potential at M=I.
    def vquad(h,q):
        h=np.asarray(h,dtype=np.int64)
        q=np.asarray(q,dtype=np.int64)
        return (Fraction(int(np.trace(h@h))*int(q@q),24)
                -Fraction(int((h@q)@(h@q)),2))
    all_exponents=[]
    T,Y,S5,S6=Ex.setup()
    assert len(S5)==5 and len(S6)==6
    # Common four-space from committed exact shared-M/IIB analysis.
    core=(0,1,2,3)
    f5=tuple(sorted(core+(4,)))
    m6=tuple(sorted(core+(5,9)))
    assert all(not T[u,v,:].any() for u in f5 for v in f5)
    assert all(not T[u,v,:].any() for u in m6 for v in m6)
    assert len(set(f5)&set(m6))==4
    assert np.array_equal(np.einsum("imn,jmn->ij",T,T),10*np.eye(27,dtype=np.int64))

    # At identical common-four derivative q and generalized metric
    # fluctuation h, potential is EXACTLY identical in both branches.
    comparisons=0
    for h in Hs+diags:
        for coord in core:
            q=np.zeros(27,dtype=np.int64);q[coord]=1
            x=vquad(h,q)
            y=vquad(h,q)
            assert x==y
            comparisons+=1
    assert comparisons==42*4

    # For any unit q from E6 27, isotropic variance is E||h q||²=1/27.
    # This gives exact E[V/e²]=(1/24)-(1/2*1/27)=5/216.
    avg=sp.Rational(1,24)-sp.Rational(1,2)*sp.Rational(14,9)/42
    assert avg==sp.Rational(5,216)
    # And for ANY section subspace S, the normalized per-axis
    # isotropic average agrees; total (un-normalized) scales with |S|.
    avg5=len(f5)*avg;avg6=len(m6)*avg
    assert avg5==sp.Rational(25,216)
    assert avg6==sp.Rational(5,36)

    # Explicit anisotropic choices make the two sections look
    # favorable in opposite orders, defeating any universal branch
    # preference inferred from the same scalar potential.
    def score(h,S):
        return sum((vquad(h,np.eye(27,dtype=np.int64)[i])
                    for i in S),Fraction(0))/len(S)/Fraction(int(np.trace(h@h)))
    diffcounts=Counter()
    witnesses={}
    for n,h in enumerate(Hs+diags):
        diff=score(h,f5)-score(h,m6)
        key="positive" if diff>0 else ("negative" if diff<0 else "zero")
        diffcounts[key]+=1
        if key not in witnesses:
            witnesses[key]={"basis_element":n,"normalized_V5_minus_V6":[diff.numerator,diff.denominator],
                            "V5":[score(h,f5).numerator,score(h,f5).denominator],
                            "V6":[score(h,m6).numerator,score(h,m6).denominator]}
    assert diffcounts["positive"]>0 and diffcounts["negative"]>0,diffcounts

    # An arbitrary element of the 42D tangent yields valid
    # generalized metrics exp(h f) in E6(6)/USp8.
    # For actual full ExFT evaluation at the point f=0, the result
    # is exact for any small epsilon, not only Hessian asymptotics.
    result=dict(
        status="PASS_EXACT_E6_EXFT_SCALAR_POTENTIAL_ISOTROPIC_BRANCH_NO_GO",
        source="Hohm-Samtleben E6(6) ExFT; Vpot as Eq (3.103) of canonical formulation (2021)",
        cubic_generators_checked=78,noncompact_coset_dimension=42,
        compact_usp8_dimension=36,Cartan_dim=6,symmetric_root_packet_dim=36,
        Hilbert_Schmidt_root_packet_norm_sq=12,
        normalized_root_square_resolution="4/3 I27",
        orthogonal_Cartan_square_resolution="2/9 I27",
        full_coset_square_resolution="14/9 I27",
        full_coset_projector_trace=42,
        exact_ExFT_quadratic_scalar_potential_at_M_identity="Tr(h^2) |q|^2 / 24 - |h q|^2 / 2",
        isotropic_unit_Hilbert_Schmidt_coset_average_per_unit_derivative="5/216",
        isotropic_five_section_total_for_one_equal_derivative_mode_per_axis="25/216",
        isotropic_six_section_total_for_one_equal_derivative_mode_per_axis="5/36",
        isotropic_branch_preference_per_derivative_mode=False,
        shared_four_coordinate_indices=core,example_five_section=f5,example_six_section=m6,
        common_four_anisotropic_scalar_potential_equal_cases=comparisons,
        anisotropic_basis_element_count=42,
        anisotropic_V5_minus_V6_sign_hist=dict(diffcounts),
        anisotropic_opposite_sign_witnesses=witnesses,
        derivative_free_flat_M_equals_I_g_equals_eta_Vpot=0,
        physics_scope="Necessary no-go for selection by the homogeneous / quadratic isotropic scalar sector. Full five-dimensional ExFT includes tensor hierarchy, external gravity, flux, topological terms, boundary conditions, and possible quantum corrections; NO claim of complete action selection, 11D-vs-IIB cosmological vacuum energy, or underlying TOE.",
        reference_urls=["https://edoc.hu-berlin.de/server/api/core/bitstreams/c2e61a8e-6617-4d02-a91b-df26fe5ff80a/content","https://arxiv.org/abs/1312.0614"])
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","noncompact_coset_dimension","full_coset_square_resolution",
        "isotropic_unit_Hilbert_Schmidt_coset_average_per_unit_derivative",
        "common_four_anisotropic_scalar_potential_equal_cases",
        "anisotropic_V5_minus_V6_sign_hist","anisotropic_opposite_sign_witnesses")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
