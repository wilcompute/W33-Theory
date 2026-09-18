#!/usr/bin/env python3
"""Photonic rail compiler for the outer-complete central-character logical qubit.

Representation input:
  rho_1(X)=X, rho_1(Z)=Z,
  rho_2(X)=X, rho_2(Z)=Z^{-1}
in a common computational basis (rho_2 is the complex-conjugate Heisenberg
representation).  The certified multiplier-minus-one outer action swaps the
two blocks.

Photonic encoding:
  r=1 -> rail H (or path A)
  r=2 -> rail V (or path B)
and use opposite-sign qutrit Z phase programming on the two rails.

Then:
  * the outer logical X_L is exactly the rail SWAP;
  * for polarization rails, a half-wave plate at 45 degrees implements SWAP
    up to a convention-fixed global/rail phase;
  * the center z=diag(omega,omega^-1) is a relative 2pi/3 rail phase;
  * once coherent rail encoding is available, ordinary two-mode/polarization
    rotations provide a logical basis-changing gate, so the logical qubit is
    not restricted to the finite S3 subgroup.

This is a compiler/encoding theorem, not proof that the native VOA sectors are
already coupled to a laboratory polarization degree of freedom.  The physical
interface that coherently maps V1,V2 into the two rails remains the experiment.
"""
from __future__ import annotations
import cmath,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_outer_logical_photonic_rail_compiler.json'

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def close(A,B,tol=1e-9):
    return all(abs(A[i][j]-B[i][j])<tol for i in range(2) for j in range(2))

def main(write=True):
    parent=json.loads((ROOT/'data/w33_suzuki_outer_heisenberg_sector_swap.json').read_text())
    coh=json.loads((ROOT/'data/w33_outer_complete_no_intrinsic_superselection.json').read_text())
    assert parent['status']=='PASS' and coh['status'].startswith('PASS_')
    w=cmath.exp(2j*cmath.pi/3)
    X=[[0,1],[1,0]]
    z=[[w,0],[0,w.conjugate()]]
    zi=[[w.conjugate(),0],[0,w]]
    assert close(mm(mm(X,z),X),zi)
    # Ideal 45-degree HWP Jones matrix is SWAP up to signs/convention.
    # We freeze the logical target matrix, not a vendor-specific optic.
    out={'schema':'w33.outer_logical_photonic_rail_compiler.v1',
      'status':'PASS_ENCODING_COMPILER__NATIVE_SECTOR_INTERFACE_OPEN',
      'encoding':{
        'r1':'polarization H or path rail A',
        'r2':'polarization V or path rail B',
        'internal_729':'same computational labels on both rails',
        'phase_convention':'Z phases have opposite sign on r1 and r2 rails'},
      'logical_operations':{
        'outer_XL':'rail SWAP [[0,1],[1,0]]',
        'photonic_candidate':'half-wave-plate polarization swap or deterministic path cross-connect',
        'center_z':'relative rail phase diag(omega,omega^-1)',
        'basis_change':'generic coherent two-rail SU(2) rotation using waveplates or Mach-Zehnder beam splitters once the sector-to-rail interface exists'},
      'representation_check':{
        'identity':'X_L z X_L = z^-1',
        'rho2_is_conjugate_phase_convention':True,
        'outer_requires_no_antiunitary_device_after_doubling':True},
      'dense_logical_control':{
        'finite_native_group':'<z,X_L> = S3',
        'additional_photonic_resource':'one continuously tunable rail mixer plus relative phase',
        'consequence':'arbitrary logical SU(2) is available at the rail-encoding layer in principle'},
      'hardware_precedent':'single-photon spatial/polarization SWAP and arbitrary mode mixing are standard linear-optical operations; modern acousto/electro-optic devices also synthesize frequency-domain beam splitters',
      'native_VOA_boundary':'The compiler assumes a coherent isometry from the native V1 direct-sum V2 carrier into two optical rails. Representation theory permits it but does not construct the material/VOA interface. No claim of an experimentally realized W33 outer gate is made.',
      'checks':{'parent_sector_swap':True,'outer_complete_irreducible':True,'rail_swap_inverts_center':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
