#!/usr/bin/env python3
"""Five W33 photonic fronts: exact GF(2) compiler, nonlocal recursion,
nine-mode qutrit eraser, operational causal-break quantum-memory witness.

Calculations are mathematical/ideal optics only. Lookup logic, controlled
phase optics, photon sources, real reference systems and delays unbuilt.
Prior art includes binary bilinear phase-oracle factorization, quantum
erasers, and process-tensor causal-break tests. W33-specific certificate.
"""
from __future__ import annotations
import json,hashlib,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_port_fabric_20261023 import ADJ

def adjacency():
    a=np.zeros((40,40),dtype=np.uint8)
    for i,neighbor in enumerate(ADJ):
        for j in neighbor:a[i,j]=1
    assert np.array_equal(a,a.T) and not np.trace(a)
    assert (a.sum(1)==12).all()
    return a

def gf2_compiler():
    """GF2 exact low-rank U @ V.T == W33 A, rank optimal for bilinear flags."""
    A=adjacency()
    ints=[sum(int(A[i,j])<<j for j in range(40)) for i in range(40)]
    selected=[];basis={}
    for orig in ints:
        x=orig;representation=0
        while x:
            pivot=x.bit_length()-1
            if pivot in basis:
                x^=basis[pivot][0];representation^=basis[pivot][1]
            else:
                k=len(selected)
                selected.append(orig)
                basis[pivot]=(x,representation^(1<<k))
                break
    r=len(selected)
    U=np.zeros((40,r),dtype=np.uint8)
    V=np.zeros((40,r),dtype=np.uint8)
    for i,orig in enumerate(ints):
        x=orig;representation=0
        while x:
            pivot=x.bit_length()-1
            row,coef=basis[pivot]
            x^=row;representation^=coef
        for k in range(r):U[i,k]=(representation>>k)&1
    for k,orig in enumerate(selected):
        for j in range(40):V[j,k]=(orig>>j)&1
    R=((U.astype(np.int32)@V.T.astype(np.int32))%2).astype(np.uint8)
    assert np.array_equal(R,A) and r==16
    # GF2 rank is a strict minimum under independent binary parity-product
    # cross-register CZ links; it is NOT minimum MZI/optical area.
    phase=1-2*A.astype(np.int8)
    assert np.array_equal(1-2*R.astype(np.int8),phase)
    base=40*40
    return {'gf2_rank':r,'selected_row_coordinates':U.astype(int).tolist(),
      'selected_column_coordinates':V.astype(int).tolist(),
      'adjacency_reconstruction_exact':True,
      'bilinear_phase_links':r,'ordered_address_phase_flips':480,
      'ordered_address_pairs':base,'graph_edges_undirected':240,
      'logical_link_reduction_vs_edge_truth_table':240/r,
      'proof':'A(a,b)=sum_k U[a,k]V[b,k] modulo 2; (-1)^A = product_k CZ(flag_Uk(a),flag_Vk(b)). Rank GF2(A)=16 lower bounds parity-product cross links, within this gate family.',
      'engineering':'Address-dependent reversible lookup and uncompute of 32 parity flags required. No physical 40-mode controlled optical phase network, CZ nonlinearities or cost-optimized S-matrix is implemented.'}

def nine_mode_eraser():
    """Actual 9x9 unitary matrices, plus coherent vs incoherent density matrices."""
    w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/math.sqrt(3)
    C=np.zeros((9,9),complex)
    for a in range(3):
        for t in range(3):C[3*a+(t+a)%3,3*a+t]=1
    assert np.linalg.norm(C.conj().T@C-np.eye(9))<1e-12
    input=np.kron(np.ones(3)/math.sqrt(3),np.array([1,0,0]))
    psi=C@input
    rho=np.outer(psi,psi.conj())
    null=np.diag(np.abs(psi)**2).astype(complex)
    decoder=np.kron(F.conj().T,F.conj().T)
    def joint_p(mu):
        out=decoder@(mu*rho+(1-mu)*null)@decoder.conj().T
        trigger=sum(np.real(out[3*a,3*a]) for a in range(3)) # time Fourier bin 0
        joint=float(out[0,0].real)
        return float(trigger),joint,float(joint/trigger)
    rows=[]
    for mu in (0,.25,.5,.75,1):
        trig,joint,cond=joint_p(mu)
        assert abs(trig-1/3)<1e-12
        assert abs(joint-(1+2*mu)/9)<1e-12
        rows.append({'offdiagonal_coherence':mu,'time_plus_trigger':trig,
          'path_plus_and_time_plus_joint_probability':joint,
          'path_plus_conditioned_on_time_plus':cond})
    # One-photon source characterization is independent of first-order fringe
    return {'controlled_SUM_matrix_9x9_real':C.real.astype(int).tolist(),
      'unbalanced_fourier_decoders':'F3 dagger acting on each qutrit mode factor',
      'rows':rows,'incoherent_diagonal_null_same_occupations':True,
      'note':'Mathematical nine-mode coherent-state interference alone does not exclude classical vector-wave nonseparability or prove single-photon antibunching. g2(0) and a calibrated source must be measured.'}

def phase_recursive_nonlocal():
    """Exact factorized n=4 boundary: one W33 edge => H, two independent
    crossed edges => 2H. Triangle n=3 calculated via 40x40 Gram matrix."""
    A=adjacency().astype(np.int32)
    S=1-2*A
    singular=np.linalg.svd(S/40,compute_uv=False)
    q=singular**2
    H=float(-sum(p*math.log2(p) for p in q if p>1e-14))
    purity=float(np.sum(q*q))
    # n=3 state with edges (0,1), (0,2): Gram rho_{aa'}
    # = sum_{bc} S_ab S_ac S_a'b S_a'c / 40^3
    cross=S@S.T
    gram=(cross*cross).astype(float)/(40**3)
    ev=np.linalg.eigvalsh(gram)
    assert abs(ev.sum()-1)<1e-12 and min(ev)>-1e-12
    triangle_H=float(-sum(x*math.log2(x) for x in ev if x>1e-14))
    # n=4 bipartite (0,2) and (1,3) across cut 01|23:
    # C= kron(S/40,S/40) up to right index swapping.
    # Schmidt probabilities are q_i * q_j; no 1600^3 SVD.
    doubled=np.kron(q,q)
    doubled_H=float(-sum(x*math.log2(x) for x in doubled if x>1e-14))
    assert abs(doubled_H-2*H)<1e-9
    return {'single_cross_edge_entropy_bits':H,'single_cross_edge_purity':purity,
      'depth3_two_spokes_cross_cut_entropy_bits':triangle_H,
      'depth3_two_spokes_spectrum':np.round(ev,13).tolist(),
      'depth4_one_edge_middle_cut':{'edges':[[1,2]],'entropy_bits':H,'schmidt_rank':40},
      'depth4_two_cross_edges_middle_cut':{'edges':[[0,2],[1,3]],'entropy_bits':doubled_H,
          'schmidt_rank':1600,'reduced_purity':purity**2},
      'theorem':'For r disjoint W33 controlled-phase links crossing one partition, independent factors give Schmidt rank 40^r and entropy r*H_W33. Nearest-neighbor chain is the special r=1 area law.',
      'bounds':'Independent physical 40-state register factors needed. No claim for arbitrary overlapping long-range interactions.'}

def _swap_s_e(rho):
    return rho.reshape((3,)*6).transpose(0,2,1,3,5,4).reshape(27,27)
def _trace_s(rho):
    return np.einsum('rseRsE->reRE',rho.reshape((3,)*6))
def _trace_e(rho):
    return np.einsum('rseRSe->rsRS',rho.reshape((3,)*6)).reshape(9,9)
def _negativity(rho):
    rho_pt=rho.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
    return float(-np.minimum(np.linalg.eigvalsh(rho_pt),0).sum())
def _causal_break(initial_rs,reset_environment=False):
    z=np.diag([1,0,0]).astype(complex)
    initial_rse=np.kron(initial_rs,z)
    # S and E SWAP first: previous S state's quantum coherence -> E.
    mid=_swap_s_e(initial_rse)
    rho_re=_trace_s(mid)
    if reset_environment:
        rho_r=np.einsum('reRe->rR',rho_re)
        rho_re=np.kron(rho_r,z).reshape(3,3,3,3)
    # Causal break: trace S and *independently* prepare |0><0|_S
    after_break=np.einsum('reRE,sS->rseRSE',rho_re,z).reshape(27,27)
    after_second=_swap_s_e(after_break)
    return _trace_e(after_second)

def causal_break_witness():
    # R is independent qutrit reference; S system; E memory. Model has
    # forward-time SWAPs and a destructive re-preparation of S mid-process.
    v=np.eye(3).reshape(9)/math.sqrt(3)
    rho_rs=np.outer(v,v.conj())
    preserved=_causal_break(rho_rs)
    lost=_causal_break(rho_rs,reset_environment=True)
    assert np.linalg.norm(preserved-rho_rs)<1e-12
    expected_lost=np.kron(np.eye(3)/3,np.diag([1,0,0]))
    assert np.linalg.norm(lost-expected_lost)<1e-12
    intact_neg=_negativity(preserved)
    null_neg=_negativity(lost)
    assert abs(intact_neg-1)<1e-12 and abs(null_neg)<1e-12
    # For input encoded |+> vs incoherent I/3, tests a coherence transfer.
    plus=np.ones(3,dtype=complex)/math.sqrt(3)
    z=np.diag([1,0,0])
    init_plus=np.kron(z,np.outer(plus,plus.conj()))
    init_mix=np.kron(z,np.eye(3)/3)
    outs=[]
    P=np.outer(plus,plus.conj())
    for name,src in [('coherent',init_plus),('incoherent_same_basis_populations',init_mix)]:
        with_memory=_causal_break(src)
        erased=_causal_break(src,True)
        sys_out=np.einsum('rsrS->sS',with_memory.reshape(3,3,3,3))
        erased_out=np.einsum('rsrS->sS',erased.reshape(3,3,3,3))
        outs.append({'input':name,'post_break_path_plus_with_E_memory':float(np.trace(sys_out@P).real),
          'with_environment_reset':float(np.trace(erased_out@P).real)})
    assert abs(outs[0]['post_break_path_plus_with_E_memory']-1)<1e-12
    assert abs(outs[1]['post_break_path_plus_with_E_memory']-1/3)<1e-12
    return {'three_qutrit_total_dimension':27,'causal_order':'prepare RS; SWAP S,E; replace S by |0> independent of history; SWAP S,E; measure RS',
      'reference_and_system_maximally_entangled_initial':True,
      'final_RS_negativity_environment_retained':intact_neg,
      'final_RS_negativity_environment_erased_at_break':null_neg,
      'coherence_control':outs,
      'operational_result':'Full qutrit coherence of earlier S is retained in E across a causal break and recovered afterwards. A memoryless environment-reset null loses that coherence and the reference entanglement.',
      'interpretation':'Witnesses modeled quantum environmental memory; unlike a channel Choi vector this uses a real separate R in the model and actual intermediate re-preparation. No backward-in-time signaling or fabricated apparatus.',
      'protocol_requirements':['independent reference qutrit R with accessible joint tomography','physical controllable SWAP S,E and environmental quantum storage','true trace-and-reprepare causal break S','environment-reset memoryless control','pre-registered RS entanglement negativity and source/circuit errors']}

def result():
    parts={'nine_mode_optical_eraser':nine_mode_eraser(),
       'W33_GF2_16_channel_phase_compiler':gf2_compiler(),
       'nonlocal_recursion':phase_recursive_nonlocal(),
       'causal_break_reference_test':causal_break_witness()}
    obj={'schema':'w33.photonic_five_fronts_20261023.phase_oracle_and_temporal_memory.v1',
         'parts':parts,'physical_boundary':'Mathematical state/channel/control models only; no calibrated photon source, PDK, nonlinear CZ, physical 40-level lookup, separate reference qudit memory, board PCF or lab data'}
    obj['sha256']=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return obj
if __name__=='__main__':
    obj=result()
    p=ROOT/'data/w33_photonic_five_fronts_GF2_phase_causal_break_20261023.json'
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS W33 GF2 rank',obj['parts']['W33_GF2_16_channel_phase_compiler']['gf2_rank'],
          'nonlocal H2',obj['parts']['nonlocal_recursion']['depth4_two_cross_edges_middle_cut']['entropy_bits'],
          'causal reference negativity',obj['parts']['causal_break_reference_test']['final_RS_negativity_environment_retained'])
