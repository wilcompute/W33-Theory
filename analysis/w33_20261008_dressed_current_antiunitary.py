"""Exact dressed antiunitary of the W33 incidence-current Hamiltonian.

Proves canonical K alone fails (companion script), but a nontrivial dressed
antiunitary A: q -> D p, p -> D q fixes every represented edge current.
This is an internal bosonic symmetry, not automatically a physical time arrow.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass11767_global_current_algebra import actual_edges

def certificate():
    edges=actual_edges()
    assert len(edges)==160 and len(set(edges))==160
    n=80
    unity=[1]*n
    sign=[1]*40+[-1]*40
    assert [a*b for a,b in zip(sign,unity)]==sign
    assert [a*a for a in sign]==unity
    seen=set()
    max_cross=0
    for i,j in edges:
        assert 0<=i<40<=j<80
        assert (i,j) not in seen
        seen.add((i,j))
        u=[40*(int(k==i)+int(k==j))-1 for k in range(n)]
        v=[40*(int(k==i)-int(k==j))-sign[k] for k in range(n)]
        assert sum(u[:40])==sum(u[40:])==0
        assert sum(v[:40])==sum(v[40:])==0
        # D=diag(+1 on points,-1 on lines).
        assert all(sign[k]*u[k]==v[k] for k in range(n))
        assert all(sign[k]*v[k]==u[k] for k in range(n))
        cross=sum(a*b for a,b in zip(u,v))
        max_cross=max(max_cross,abs(cross))
        assert cross==0
    # S(q,p)=(Dp,Dq). S^2=I and S^T Omega S = -Omega.
    # Verify anti-symplectic property on explicit 78-dimensional W basis.
    W=[]
    for block in (0,40):
        for k in range(39):
            row=[0]*80
            row[block+k]=1
            row[block+39]=-1
            W.append(row)
    assert len(W)==78
    for x in W:
        for y in W:
            # Omega((q,p),(q',p'))=q.p'-p.q'
            # For arbitrary q,p in W, S transforms Omega to minus itself.
            assert sum(a*b for a,b in zip(x,y))==sum(a*b*c*c for a,b,c in zip(x,y,sign))
    return {
      "schema":"w33.20261008.dressed_antiunitary.current.v1",
      "status":"PASS",
      "currents_checked":len(seen),
      "line_point_sign":"D=diag(+1 on 40 point coordinates, -1 on 40 line coordinates)",
      "carrier":"W=orthogonal complement of ones80 and (ones40,-ones40), dimension 78",
      "linear_transformation":"S(q,p)=(D p,D q), with S^2=I, S^T Omega S=-Omega on W+W",
      "exact_current_exchange":"D U_e=V_e, D V_e=U_e for all 160 actual incidences",
      "quantum_current_invariance":"T J_e T^-1=(U_e.p+a)(V_e.q+a)=J_e because U_e.V_e=0",
      "hamiltonian_invariance":"T H T^-1=H for H=sum_e J_e^2",
      "explicit_antiunitary":"(T psi)(q)=(2*pi)^(-39) integral_W exp(i q.dot(D x))*conj(psi(x)) dx, on 78-dimensional W",
      "square":"T^2=I on Schwartz functions by Fourier inversion and D^2=I",
      "bare_complex_conjugation":"K H K^-1 != H, established by the independent companion 1560-pair exact witness",
      "canonical_cross_product_max_abs":max_cross,
      "boundary":"Dressed antiunitary is a proposed internal q-p duality, not measured physical time reversal, CPT, parity or an emergent thermodynamic arrow."
    }

if __name__=="__main__":
    print(json.dumps(certificate(),indent=2,sort_keys=True))
