"""Four qutrit MUB analyzers and conservative optical insertion-loss
firewall for the EVENT-READY trusted entanglement witness.

Construct the four 3-dimensional MUB from eigenstates of
Z, X, X Z, X Z^2 (omega=e^(2pi*i/3)).
Compile the projective analyzers U_b^dagger to at most 3 adjacent
two-mode Givens rotations plus diagonal phases (unitary QR).
This is an exact abstract spatial-three-rail compilation, not a
fabricated time-bin optical circuit; temporal-to-spatial conversion,
active setting randomness and setting leakage require independent proof.

For 2 memories each eta=.902, path=.95, 2 detectors eta=.9,
source q=.82499, perfect routing: gross p_max=.5165.
At 3 lossy couplers per qutrit analyzer, 2 analyzers -> 6 stages.
Coupler eta=.995 alone lowers gross p below .51. With f_router=.995,
required EACH coupler efficiency >.9995 in worst-case three-stage
scenario. This severe requirement is conditional on the selected
gross-heralded binary witness and losses as modeled.
"""
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_memory_2026_real_reference_qutrit import q
OUT=ROOT/"data"/"toe_20261117_qutrit_four_MUB_analyzer_stage_loss.json"
def basis():
    om=np.exp(2j*np.pi/3)
    X=np.roll(np.eye(3,dtype=complex),1,axis=0)
    Z=np.diag([1,om,om**2])
    matrices={"Z_computational":np.eye(3,dtype=complex)}
    for b in (0,1,2):
        U=X@np.linalg.matrix_power(Z,b)
        eig,vec=np.linalg.eig(U)
        # deterministic stable ordering by complex phase
        order=np.argsort(np.angle(eig))
        V=vec[:,order]
        for j in range(3):
            V[:,j]/=np.linalg.norm(V[:,j])
            # gauge-fix column phase for stable JSON
            ix=int(np.argmax(np.abs(V[:,j])))
            V[:,j]*=np.exp(-1j*np.angle(V[ix,j]))
        matrices["X_Zpower_"+str(b)]=V
    assert len(matrices)==4
    for k,V in matrices.items():
        assert np.allclose(V.conj().T@V,np.eye(3),atol=1e-13)
    for i,(k,V) in enumerate(matrices.items()):
        for j,(l,W) in enumerate(matrices.items()):
            if i>=j:continue
            Xp=np.abs(V.conj().T@W)**2
            assert np.allclose(Xp,np.ones((3,3))/3,atol=1e-13), (k,l,Xp)
    return matrices
def givens_compile(U):
    W=U.copy()
    n=W.shape[0]
    Gs=[]
    for j in range(n):
        for i in range(n-1,j,-1):
            a=W[i-1,j];b=W[i,j]
            norm=np.sqrt(abs(a)**2+abs(b)**2)
            if norm<1e-12:continue
            g=np.eye(n,dtype=complex)
            g[i-1,i-1]=np.conj(a)/norm
            g[i-1,i]=np.conj(b)/norm
            g[i,i-1]=-b/norm
            g[i,i]=a/norm
            W=g@W
            if abs(b)>1e-12:Gs.append({"G":g,"rails":[i-1,i]})
    assert np.max(np.abs(W-np.diag(np.diag(W))))<1e-12
    D=np.diag(np.diag(W))
    reconstruct=D.copy()
    for gg in reversed(Gs):reconstruct=gg["G"].conj().T@reconstruct
    assert np.allclose(reconstruct,U,atol=1e-12)
    assert len(Gs)<=3
    return {"stages":len(Gs),"rail_pairs":[g["rails"] for g in Gs],
            "maximum_reconstruction_error":float(np.max(np.abs(reconstruct-U))),
            "output_diagonal_phase_modulo_2pi":[float(np.angle(D[i,i])) for i in range(n)]}
def loss():
    base=.9**2 * (.902**2)*.95*q()
    p0=.51
    threshold=(p0/base)**(1/6)
    at_router995=(p0/(base*.995**2))**(1/6)
    assert .997< threshold<.999
    assert .999<at_router995<1.
    grid=[]
    for memcount in (1,2):
      for router in (.95,.99,.995,1.):
       maxp=.9**2*.902**memcount*.95*q()*router**2
       need=(p0/maxp)**(1/6)
       for each_c in (.99,.995,.999,.9995,.9998,1.):
        pmatch=maxp*each_c**6
        grid.append({"memory_arms":memcount,"router_each":router,
          "coupler_stage_throughput":each_c,"total_six_stage_throughput":each_c**6,
          "gross_match":pmatch,"trusted_witness_crosses_p0":pmatch>p0,
          "minimum_equal_coupler_stage_throughput_to_violate":need})
    assert not next(z for z in grid if z["memory_arms"]==2 and z["router_each"]==1. and z["coupler_stage_throughput"]==.995)["trusted_witness_crosses_p0"]
    assert not next(z for z in grid if z["memory_arms"]==2 and z["router_each"]==.995 and z["coupler_stage_throughput"]==.999)["trusted_witness_crosses_p0"]
    assert next(z for z in grid if z["memory_arms"]==2 and z["router_each"]==.995 and z["coupler_stage_throughput"]==.9998)["trusted_witness_crosses_p0"]
    return {"detector_each":.9,"memory_each_reference":.902,
       "no_more_than_3_mixers_per_qutrit_analyzer":True,
       "assumed_total_coupler_stages_two_analyzers":6,
       "two_memories_perfect_router_base":base,
       "minimum_each_coupler_with_perfect_router":threshold,
       "minimum_each_coupler_at_router_99p5_percent":at_router995,
       "samples":grid,"no_go_specific_to_witness":"For this gross event-ready four-MUB binary match witness, symmetric 2-memory 90.2% scenario and path .95, two 3-stage qutrit analyzers at 99.5% throughput per stage make p<=.51 even with 100% temporal routers. Not a quantum-entanglement no-go, not a general optical-hardware law."}
def verify():
    a=basis()
    compiler={k:givens_compile(U.conj().T) for k,U in a.items()}
    assert compiler["Z_computational"]["stages"]==0
    assert all(p["stages"]<=3 for p in compiler.values())
    v=loss()
    return {"status":"PASS_EXPLICIT_FOUR_MUB_QUTRIT_ANALYZERS_AND_SIX_STAGE_LOSS_FIREWALL",
      "MUBs":"Computational Z and eigenbases of XZ^b b=0,1,2; 3x3 Fourier/quadratic chirp equivalents",
      "analyzer_compilation":"Each requested projective measurement U^dagger reconstructed from at most 3 adjacent two-rail Givens rotations and diagonal phase shifts; this is a unitary decomposition not a fabricated time-bin experiment.",
      "basis_pairs_unbiased_verified":6,
      "per_basis_compilers":compiler,"event_ready_loss":v,
      "hardware_caveats":"Must establish deterministic coherent conversion of 3 time bins to spatial rails, setting selection after trusted herald, loss and leakage calibrated by setting, and memory qutrit preservation. Qubit memory efficiency reported in 2026 is merely a hypothetical efficiency anchor."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["event_ready_loss"]["minimum_each_coupler_at_router_99p5_percent"],
          [x["stages"] for x in z["per_basis_compilers"].values()])
