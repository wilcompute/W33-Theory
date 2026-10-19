"""Follow-up fronts 3+4: explicit controlled-phase-gate compilation and
lossy synthetic readout; Clifford intertwiner of the projector quotient to
the sl9(A8) component of the standard E8 = sl9+Lambda3+Lambda6 model.

The Clifford/sl9 equivariance is tested for explicit generators. It does
NOT establish identification with the repo's Chevalley basis.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,build_projectors

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_nextfive_optics_su9.json"
w=np.exp(2j*np.pi/3); I9=np.eye(9,dtype=complex); I3=np.eye(3)
P=build_projectors(points())
F=np.array([[w**(j*k) for k in range(3)] for j in range(3)],complex)/np.sqrt(3)
F1=np.kron(F,I3)
S1=np.kron(np.diag([1,1,w]),I3)
CZ=np.diag([w**(a*b) for a in range(3) for b in range(3)])
SUM=np.zeros((9,9),complex)
SWAP=np.zeros((9,9),complex)
for a in range(3):
 for b in range(3):
    SUM[3*a+(a+b)%3,3*a+b]=1
    SWAP[3*b+a,3*a+b]=1
G=CZ@F1
proj0=np.kron(np.diag([1,0,0]),I3)
proj1=G@proj0@G.conj().T
proj_null=np.kron(I3,np.diag([1,0,0]))
GENERATORS={"F1":F1,"S1":S1,"CZ":CZ,"SUM":SUM,"SWAP":SWAP}
BASIS=np.array([P[3*p]-P[3*p+1] if j==0 else P[3*p]-P[3*p+2]
                for p in range(40) for j in range(2)])
assert len(BASIS)==80
# In each Pauli plane, Gram=[[6,3],[3,6]] and inverse=[[2,-1],[-1,2]]/9.
GINV=np.array([[2,-1],[-1,2]])/9
def coeffs(Y):
    overlaps=np.einsum("aij,ji->a",BASIS,Y).real.reshape(40,2)
    return (overlaps@GINV).reshape(80)
def phi(c):
    return np.einsum("a,aij->ij",c,BASIS)
def rep(M):
    # columns give 80D Clifford action on the Pauli-projector contrast basis
    cols=[]
    residual=0.
    for Y in BASIS:
        Z=M@Y@M.conj().T
        c=coeffs(Z)
        residual=max(residual,float(np.linalg.norm(Z-phi(c))))
        cols.append(c)
    return np.array(cols).T,residual

def phase(Pi,t):
    return I9+(np.exp(1j*t)-1)*Pi
def witness(A,B,t):
    Ua=phase(A,t); Ub=phase(B,t)
    W=Ua@Ub@Ua.conj().T@Ub.conj().T
    return float(1-np.trace(W).real/9)
def tracks():
    res={}
    err=max(float(np.linalg.norm(Q@Q-Q)) for Q in (proj0,proj1,proj_null))
    overlap01=float(np.trace(proj0@proj1).real)
    overlap0n=float(np.trace(proj0@proj_null).real)
    comm=lambda A,B:float(np.vdot(A@B-B@A,A@B-B@A).real)
    nr=comm(proj0,proj1)
    cr=comm(proj0,proj_null)
    alpha=np.pi/2
    delta=8/27
    err=max(err,abs(witness(proj0,proj1,alpha)-delta),
            abs(witness(proj0,proj_null,alpha)))
    # Optical compilation: Q=G P0 G^-1 where G=CZ (F3 tensor I).
    # CONTROLLED Q phase = (I_ctrl tensor G) CTRL_PHASE(P0)
    #                        (I_ctrl tensor G^-1).
    # Q loop requires two unconditional G and inverses, P loops local.
    leak=.01; fringe=.95; flip=.01
    visibility=(1-leak)**4*fringe*(1-2*flip)
    predicted=visibility*delta
    N=math.ceil(32*math.log(4/.05)/predicted**2)
    random=np.random.default_rng(20261019)
    trials=4000
    p_comm=(1+visibility)/2
    p_noncomm=(1+visibility*(1-delta))/2
    null_samples=random.binomial(N,p_comm,size=(2,trials))
    noncomm_samples=random.binomial(N,p_noncomm,size=trials)
    signal=(2*null_samples[0]/N-1)-(2*noncomm_samples/N-1)
    negative=(2*null_samples[0]/N-1)-(2*null_samples[1]/N-1)
    threshold=predicted/2
    detection=float(np.mean(signal>threshold))
    false_positive=float(np.mean(negative>threshold))
    res["optics"]={
      "qudit_target_dim":9,
      "local_projector":"|0><0| tensor I3",
      "noncommuting_projector":"G P0 G^dag, G=CZ*(F3 tensor I3)",
      "commuting_null":"I3 tensor |0><0|",
      "projector_error":err,
      "noncommuting_commutator_norm_sq":nr,
      "commuting_commutator_norm_sq":cr,
      "pairwise_overlap_noncommuting":overlap01,
      "pairwise_overlap_commuting":overlap0n,
      "ideal_trace_deficit_theta_pi_2":witness(proj0,proj1,alpha),
      "compiled_gate_route":"Four controlled local phase gates; for Q use unconditional CZ and F3 basis conjugation around controlled |0> phase; inverse loop gates needed; ancilla Hadamard trace test.",
      "synthetic_noise":{"leak_per_gate":leak,"ancilla_visibility":fringe,
          "readout_flip":flip,"effective_visibility":visibility},
      "effective_predicted_contrast":predicted,"shots_per_condition_conservative":N,
      "synthetic_replicates":trials,
      "empirical_synthetic_detection_probability":detection,
      "empirical_synthetic_false_alarm_probability":false_positive,
      "statistical_caveat":"Simulated independent binomial readout with loss represented ONLY as visibility reduction. No actual target photon noise, drift, coherent leakage or device calibration.",
      "pass":err<1e-10 and abs(nr-4/3)<1e-10 and cr<1e-10 and abs(overlap01-overlap0n)<1e-10 and detection>.95 and false_positive<.05}
    group={}
    biggest=0.
    for name,M in GENERATORS.items():
        A,e=rep(M)
        biggest=max(biggest,e)
        # Verify equivariance Phi(rho(g)c)=g Phi(c)g^-1 on random vectors.
        c=random.normal(size=80)
        err_eq=float(np.linalg.norm(phi(A@c)-M@phi(c)@M.conj().T))
        biggest=max(biggest,err_eq)
        group[name]={"intertwiner_residual":err_eq,"operator_image_residual":e,
                     "character_trace":float(np.trace(A)),
                     "orthogonal_with_respect_to_projector_Gram":None}
    # Pauli translation adjoint trace from physical U=Z tensor I
    D=np.kron(np.diag([1,w,w*w]),I3)
    ad,_=rep(D)
    char_D=float(np.trace(ad))
    # Verify representation composition on representative pair.
    A_F,_=rep(F1)
    A_CZ,_=rep(CZ)
    A_combo,_=rep(F1@CZ)
    compose=float(np.linalg.norm(A_combo-A_F@A_CZ))
    # Wedge-three sector (84D). For two unitary generators evaluate the
    # exterior algebra functor and validate composition: wedge^3(UV).
    tri=list(itertools.combinations(range(9),3))
    def wedge3(M):
        return np.array([[np.linalg.det(M[np.ix_(a,b)]) for b in tri] for a in tri])
    Fw=wedge3(F1);Cw=wedge3(CZ)
    wedge_error=float(np.linalg.norm(wedge3(F1@CZ)-Fw@Cw))
    wedge_unitarity=float(max(np.linalg.norm(Fw.conj().T@Fw-np.eye(84)),
                            np.linalg.norm(Cw.conj().T@Cw-np.eye(84))))
    res["su9_clifford_bridge"]={
      "operator_contrast_basis_size":len(BASIS),
      "traceless_module":"40 pairwise orthogonal 2D real Pauli-projector planes = Hermitian traceless C9; complexification equals sl9(C)",
      "constructive_Phi":"Phi(c)=sum_p [c_(p,1)*(P_p0-P_p1)+c_(p,2)*(P_p0-P_p2)]",
      "inverse_on_traceless":"For each p use Gram inverse [[2,-1],[-1,2]]/9 against the two contrast operators",
      "generator_tests":group,"max_equivariance_residual":biggest,
      "Pauli_translation_character":char_D,
      "F_CZ_composition_residual":compose,
      "exterior_cube_dimension":len(tri),
      "exterior_cube_functor_composition_residual":wedge_error,
      "exterior_cube_unitarity_residual":wedge_unitarity,
      "standard_A8_E8_sector_dimensions":[80,84,84],
      "result":"EXPLICIT Clifford-equivariant Phi from 80-dimensional Pauli contrast quotient to sl9 sector of the standard E8 A8 model. Not a Chevalley-coordinate intertwiner to a named repository 248x248 representation.",
      "prior_art":"Repo w33_20260924_temporal_su9_e8_compiler.py and standard sl9+Lambda3+Lambda6 E8 construction: 80/84/84 branching is established, not new.",
      "pass":biggest<1e-9 and compose<1e-9 and abs(char_D+1)<1e-9 and wedge_error<1e-9 and wedge_unitarity<1e-9}
    res["checks"]={k:v["pass"] for k,v in res.items()}
    res["all_checks_pass"]=all(res["checks"].values())
    OUT.write_text(json.dumps(res,indent=2)+"\n")
    print(json.dumps({"checks":res["checks"],"optics":res["optics"],"su9_compact":
      {k:res["su9_clifford_bridge"][k] for k in ("Pauli_translation_character",
      "max_equivariance_residual","F_CZ_composition_residual","exterior_cube_functor_composition_residual")}},indent=2))
    assert res["all_checks_pass"]
    return res
if __name__=="__main__":tracks()
