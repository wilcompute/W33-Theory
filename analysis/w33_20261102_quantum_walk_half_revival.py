#!/usr/bin/env python3
"""Exact half-revival of W(3,q) nearest-neighbour quantum walks, odd q=3,5,7."""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from even_line_sets_gf import build
import w33_20261102_route_216_cubic_tomography as G
def verify(q):
    pts,lines,N=build(q)
    v=(q+1)*(q*q+1);assert N.shape==(v,v)
    I=np.eye(v,dtype=np.int64);J=np.ones((v,v),dtype=np.int64)
    A=N@N.T-(q+1)*I
    k=q*(q+1)
    assert np.array_equal(A@A,(q*q-1)*I-2*A+(q+1)*J)
    assert np.array_equal(A@J,k*J)
    f=q*(q+1)**2//2
    d=2*q*(q*q+1)
    D=(q*q+1)*(A+(q+1)*I)-(q+1)*J
    assert np.array_equal(D@D,d*D)
    assert int(np.trace(D))==d*f
    Rnum=d*I-2*D
    assert np.array_equal(Rnum@Rnum,d*d*I)
    rr=Rnum.astype(float)/d
    p_near=((q-1)/(q*q+1))**2
    p_far=((q+1)/(q*(q*q+1)))**2
    assert abs((k+1)*p_near+(v-k-1)*p_far-1)<1e-12
    for a in (0,v//3,v-1):
        v2=rr[a]**2
        assert abs(v2[a]-p_near)<1e-12
        assert np.max(abs(v2[np.flatnonzero(A[a])]-p_near))<1e-12
        assert np.max(abs(v2[np.flatnonzero((A[a]==0)&(np.arange(v)!=a))]-p_far))<1e-12
    assert int(np.max(abs(np.diag(Rnum))))>0
    if q==3:
        pts3,ls3,N3,ix,norm,sp=G.geometry()
        assert np.array_equal(N,N3)
        old=ROOT/"data/w33_20261102_route_216_cubic_tomography.json"
        assert old.exists()
        # Reconstruct the sign-frame projector from its exact integer graph formula.
        ZtZ=240*I+60*A-24*J
        assert np.array_equal(d*(180*I-ZtZ),180*Rnum)
        # The half-revival reflection is literally I-ZtZ/180, not just same rank.
    return {"q":q,"points":v,"valency":k,"positive_projector_rank":f,
      "projector_integer_scale":d,
      "nontrivial_quantum_walk_period":"pi / coupling J, for odd q",
      "half_period_time":"pi/(2*J)",
      "half_period_matrix":"global_sign * (I - 2 E_+)",
      "global_sign":(-1)**((q+1)//2),
      "return_and_adjacent_probability":p_near,
      "nonadjacent_probability":p_far,
      "multiplicity_return_and_adjacent":k+1,
      "multiplicity_nonadjacent":v-k-1,
      "matrix_unitarity_exact":True,
      "bare_laplacian_normalised_gap":1-(q-1)/k}
def main():
    rows=[verify(q) for q in (3,5,7)]
    result={"status":"PASS_W3Q_HALFWALK_REFLECTION_POVM_BRIDGE",
      "q3_exact_povm_reflection":"U(pi/2) = I - Z.T Z / 180 (for adjacency Hamiltonian A, units J=1)",
      "unitary_period_for_odd_q":"pi / J",
      "cases":rows,
      "scope":"Single-particle continuous-time quantum walk with assumed uniform adjacency couplings J; no derived J, gravity, continuum, photon hardware or TOE."}
    p=ROOT/"data/w33_20261102_quantum_walk_half_revival.json"
    p.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(result["status"],[(r["q"],r["return_and_adjacent_probability"],r["nonadjacent_probability"]) for r in rows])
    return result
if __name__=="__main__":main()
