"""Explicit geometric implementation of the five11987 gates in two qutrits.

Odd parity supplies four data levels; four even levels supply auxiliaries.
Control Hamiltonians are supplied, not derived from native hopping/hardware.
"""
import itertools
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import schur
from w33_pass11988_spinor_weil_intertwiner import odd_encoding

ROOT=Path(__file__).resolve().parents[1]


def gates():
    rows=json.loads((ROOT/'data/w33_pass11987_atlas_spin_gate_alphabet.json').read_text())['gates']
    return [(r['even_word'],np.array(r['gate_real'])+1j*np.array(r['gate_imag'])) for r in rows]


def spectral_gate(U):
    T,V=schur(U,output='complex');phases=np.angle(np.diag(T))
    assert np.max(abs(U-(V*np.exp(1j*phases))@V.conj().T))<1e-10
    return V,phases


def dark_path(U,t):
    O,E=odd_encoding();V,phases=spectral_gate(U);data=O@V;aux=E[:,:4]
    segment=min(int(t),2);u=min(max(t-segment,0.),1.)
    s=u*u*(3-2*u);ds=6*u*(1-u)
    if segment==0:theta=np.pi*s/2;theta_dot=np.pi*ds/2;psi=np.zeros(4);psi_dot=np.zeros(4)
    elif segment==1:theta=np.pi/2;theta_dot=0.;psi=-2*phases*s;psi_dot=-2*phases*ds
    else:theta=np.pi*(1-s)/2;theta_dot=-np.pi*ds/2;psi=-2*phases;psi_dot=np.zeros(4)
    c=np.cos(theta/2);sine=np.sin(theta/2);phase=np.exp(1j*psi)
    D=c*data+sine*phase*aux
    derivative=-theta_dot*sine*data/2+phase*(theta_dot*c/2+1j*psi_dot*sine)*aux
    P=D@D.conj().T;Pd=derivative@D.conj().T+D@derivative.conj().T
    assert np.max(abs(P@P-P))<1e-12
    return P,Pd


def hamiltonian(U,t,segment_time=1.,gap=2.,counterdiabatic=True):
    P,Pd=dark_path(U,t/segment_time);H=gap*(np.eye(9)-P)
    if counterdiabatic:H=H+1j*(Pd@P-P@Pd)/segment_time
    assert np.max(abs(H-H.conj().T))<1e-12
    return H


def propagate(U,segment_time=1.,counterdiabatic=True):
    O,_=odd_encoding();y=O.astype(complex).ravel();nfev=0
    def rhs(t,y):return (-1j*hamiltonian(U,t,segment_time,counterdiabatic=counterdiabatic)@y.reshape(9,4)).ravel()
    for segment in range(3):
        sol=solve_ivp(rhs,(segment*segment_time,(segment+1)*segment_time),y,method='DOP853',rtol=2e-10,atol=2e-12)
        assert sol.success;y=sol.y[:,-1];nfev+=sol.nfev
    evolved=y.reshape(9,4);effective=O.T@evolved
    return dict(encoded_operator_max_error=float(np.max(abs(effective-U))),
        leakage_operator_norm=float(np.linalg.norm((np.eye(9)-O@O.T)@evolved,2)),
        isometry_max_error=float(np.max(abs(evolved.conj().T@evolved-np.eye(4)))),
        ode_function_evaluations=nfev)


def weyl_coefficients(H):
    omega=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag([1,omega,omega**2]);rows=[]
    reconstructed=np.zeros((9,9),complex)
    for a,b,c,d in itertools.product(range(3),repeat=4):
        D=np.kron(np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b),np.linalg.matrix_power(X,c)@np.linalg.matrix_power(Z,d))
        coefficient=np.trace(D.conj().T@H)/9;reconstructed+=coefficient*D
        if abs(coefficient)>1e-12:rows.append(dict(label=[a,b,c,d],coefficient=[float(coefficient.real),float(coefficient.imag)]))
    assert np.max(abs(reconstructed-H))<1e-11
    return rows,float(np.max(abs(reconstructed-H)))


def peer_optical_mesh(U):
    sys.path.insert(0,str(ROOT))
    from analysis.w33_20261015_toe92_optical_givens_mesh import decompose
    diagonal,steps=decompose(U)
    chronological=[];reconstructed=np.diag(np.diag(diagonal));depth=[0]*4
    for a,b,G in reversed(steps):
        gate=G.conj().T;embedded=np.eye(4,dtype=complex);embedded[np.ix_([a,b],[a,b])]=gate
        reconstructed=embedded@reconstructed
        layer=max(depth[a],depth[b])+1;depth[a]=depth[b]=layer
        chronological.append(dict(rails=[a,b],gate_real=gate.real.tolist(),gate_imag=gate.imag.tolist()))
    error=float(np.max(abs(reconstructed-U)));assert error<1e-10
    return dict(first_operation_diagonal_phase_rad=np.angle(np.diag(diagonal)).tolist(),
        subsequent_operations_in_state_application_order=chronological,Givens_rotations=len(steps),
        maximum_path_mixer_depth=max(depth),reconstruction_max_error=error,
        scope='Alternative four-rail SINGLE-photon ququart realization of the same4x4 matrices using the peerTOE92 generic compiler. A virtual C2 tensor C2 insideonephoton is not a scalable entanglinggate betweenindependently encoded photons, nor a demonstrated two-qutrit hardware interaction.')


def payload():
    O,E=odd_encoding();P0=O@O.T;parity=E@E.T-P0;rows=[]
    for name,U in gates():
        check=propagate(U);assert check['encoded_operator_max_error']<2e-8 and check['leakage_operator_norm']<2e-8
        V,phi=spectral_gate(U)
        assert np.max(abs(dark_path(U,0)[0]-P0))<1e-12 and np.max(abs(dark_path(U,3)[0]-P0))<1e-12
        samples=[hamiltonian(U,t) for t in np.linspace(0,3,61)]
        coefficients,err=weyl_coefficients(hamiltonian(U,1.5))
        assert max(np.max(abs(P0@H@P0)) for H in [hamiltonian(U,0),hamiltonian(U,3)])<1e-11
        rows.append(dict(word=name,**check,eigenphases=phi.tolist(),
            max_sampled_H_norm=float(max(np.linalg.norm(H,2) for H in samples)),
            max_sampled_parity_commutator=float(max(np.linalg.norm(H@parity-parity@H,2) for H in samples)),
            peer_TOE92_optical_compilation=peer_optical_mesh(U),
            midpoint_Weyl_coefficients=coefficients,midpoint_Weyl_reconstruction_error=err))
    U=gates()[0][1];controls=[]
    for duration in (1.,4.,16.):
        controls.append(dict(segment_time=duration,counterdiabatic=False,**propagate(U,duration,False)))
    assert controls[0]['encoded_operator_max_error']>1e-3
    return dict(status='PASS',Hilbert_dimension=9,data_dimension=4,auxiliary_dimension=4,spectator_dimension=1,
        native_encoding='Use11663 odd parity basis O for data; first4 normalized even columns E for ancillas. Fifth even column remains bright spectator.',
        exact_path='For U=V diag(exp(i phi_j)) Vdag, d_j=OV_j, a_j=E_j. D_j=cos(theta/2)d_j+exp(i psi_j)sin(theta/2)a_j. Follow meridian theta0->pi/2, longitude psi0->-2phi, returnmeridian theta->0, with cubic smoothsteps.',
        geometric_phase_identity='gamma_j=-integral sin(theta/2)^2 dpsi_j=phi_j. Both meridians have dpsi=0. Thus parallel transport on data is exactly U.',
        exact_control='P=sum |D_j><D_j|, H0=Delta(I-P), Hcd=i[Pdot,P]. [[Pdot,P],P]=Pdot gives Pdot=-i[Hcd,P]; P Hcd P=0, so no dark-space dynamical phase. Gap Delta=2 and three time units are supplied.',
        gate_checks=rows,no_counterdiabatic_controls=controls,
        implementation_boundary='All five gates now have an explicit finite-time Hamiltonian process and an independently integrated9-level Schrodinger control. Requires coherent independently shaped two-qutrit Weyl couplings, including odd/even parity mixing. No experimental pulses, native available interaction set, preparation/readout, scalability, noise threshold, fault tolerance or physical energy/time scale is derived.',
        prior=['11663 paritybasis','11987 gatealphabet','11988 equivariance obstruction preserved','Pass4261-4268 earlier different counterdiabatic CZ architecture','11539 different U2 E6 orbit holonomy','analysis/w33_20261015_toe92_optical_givens_mesh.py owns the reused generic4mode compiler'],
        primary=['https://arxiv.org/abs/quant-ph/9904011','https://arxiv.org/abs/1905.09524'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11990_odd_even_holonomic_controls.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],max(r['encoded_operator_max_error'] for r in d['gate_checks']))
