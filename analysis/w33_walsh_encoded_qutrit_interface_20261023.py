#!/usr/bin/env python3
"""Exact 3D Walsh-encoded qutrit invariant inside four XOR line-bus modes.

Contrasts the 3-of-4 naive physical-port subspace (leaks under nonzero XOR)
with a 3-of-4 Fourier-character superposition encoding (never leaks).
This gives a lossless abstract routing/encoding INTERFACE, not a universal
qutrit gate; all XOR logical qutrit actions commute.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pic_xor_walsh_pareto_20261023 import H4
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix

def certificate():
    W=H4().astype(complex)
    V=W[:,1:4]                # 3 logical qutrit Walsh characters
    aux=W[:,0]               # 1 orthogonal auxiliary character
    assert np.linalg.norm(V.conj().T@V-np.eye(3))<1e-13
    F=np.array([[np.exp(2j*np.pi*i*j/3) for j in range(3)]
                for i in range(3)],complex)/np.sqrt(3)
    ops=[]
    for mask in range(4):
        P=permutation_matrix(mask).astype(complex)
        A=V.conj().T@P@V
        signs=np.array([(-1)**((s&mask).bit_count()) for s in (1,2,3)])
        target=np.diag(signs)
        assert np.linalg.norm(A-target)<1e-12
        assert np.linalg.norm((np.eye(4)-V@V.conj().T)@P@V)<1e-12
        ops.append({'mask':mask,'logical_signs':signs.tolist(),
                    'encoded_leakage_frobenius':float(np.linalg.norm((np.eye(4)-V@V.conj().T)@P@V)),
                    'logical_residual':float(np.linalg.norm(A-target))})
    encoded_F3=V@F@V.conj().T+np.outer(aux,aux.conj())
    assert np.linalg.norm(encoded_F3.conj().T@encoded_F3-np.eye(4))<1e-12
    assert np.linalg.norm(encoded_F3@aux-aux)<1e-12
    assert np.linalg.norm(V.conj().T@encoded_F3@V-F)<1e-12
    noncomm=np.linalg.norm(F@np.diag(ops[1]['logical_signs'])-np.diag(ops[1]['logical_signs'])@F)
    assert noncomm>1
    o={'schema':'w33.holonet.walsh_qutrit_encoding.v1',
      'encoding':'3D span of nontrivial Fourier characters of (Z2)^2 in four physical optical modes',
      'V_real':V.real.tolist(),
      'auxiliary_character_real':aux.real.tolist(),
      'switch_logical_characters':ops,
      'embedded_F3_real':encoded_F3.real.tolist(),
      'embedded_F3_imag':encoded_F3.imag.tolist(),
      'encoded_F3_unitarity_residual':float(np.linalg.norm(encoded_F3.conj().T@encoded_F3-np.eye(4))),
      'F3_noncommutation_with_XOR_logical_phase':float(noncomm),
      'physical_requirements':['prepare coherent four-mode Walsh-character superpositions',
         'preserve interferometric phases during bus switching',
         'encode and decode using real H4 optical transform',
         'separate noncommuting 3-mode F3 processing tile',
         'account for loss, auxiliary contamination and mode distinguishability'],
      'scope':'Exact abstract 4-mode unitary geometry, no PDK/fabrication/quantum fidelity data. XOR alone never generates full qutrit unitary group.'}
    raw=json.dumps(o,sort_keys=True,separators=(',',':'))
    o['sha256']=hashlib.sha256(raw.encode()).hexdigest()
    return o
if __name__=='__main__':
    o=certificate()
    p=ROOT/'data/w33_walsh_encoded_qutrit_interface_20261023.json'
    p.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
    print('PASS 3D Walsh qutrit, masks',len(o['switch_logical_characters']),
         'F3 residual',o['encoded_F3_unitarity_residual'],
         'noncomm',o['F3_noncommutation_with_XOR_logical_phase'])
