#!/usr/bin/env python3
"""Schur no-go for the scalar determinant-phase proposal.

The certified six-qutrit ground register is the irreducible 729-dimensional
Schrodinger representation V_r of H=3^(1+12), with central character r=1 or 2.
The controller invariant det(X) is a scalar in F3.  Therefore any coupling that
preserves the full H action and depends only on det(X) has image in
End_H(V_r)=C I.  In particular omega^(r det X) I is a global phase, not a
non-Clifford register gate.

A genuine gate must break this scalarity by coupling X to noncentral Weyl
operators W_u (or another state-dependent descendant/OPE channel).  This does
not rule out the determinant as a coefficient/invariant; it rules out treating
the bare scalar phase as the missing magic intertwiner.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_det_phase_scalar_no_go.json'

def main(write=True):
    out={
      'schema':'w33.det_phase_scalar_no_go.v1','status':'PASS_NO_GO',
      'register':{'group':'extraspecial 3^(1+12)','dimension':729,'central_characters':[1,2],'irreducible':True},
      'controller':{'module':'sp4(F3) adjoint','dimension':10,'invariant':'det(X) in F3'},
      'theorem':{'commutant':'End_H(V_r)=C I by irreducibility/Schur','bare_candidate':'omega^(r det(X)) I','action':'scalar global phase','nontrivial_register_gate':False},
      'required_escape':'An operator-valued coupling X -> sum_u c_u(X) W_u with some nonzero Weyl label u, or an equivalent noncentral VOA descendant/OPE channel; the scalar invariant may enter coefficients but cannot itself be the gate.',
      'consequence':'The prior quartic determinant result remains a nonlinear controller invariant and fusion-compatible witness, but its interpretation as a magic gate requires a state-dependent operator intertwiner that is still open.',
      'boundary':'Exact representation-theoretic no-go; it does not exclude non-Heisenberg-equivariant or noncentral physical couplings.'}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out
if __name__=='__main__':main(True)
