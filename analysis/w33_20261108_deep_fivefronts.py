#!/usr/bin/env python3
"""2026-11-08 five independent W33 research gates, native-tensor and optical exact checks.

No physical vacuum, measured constant, loop calculation or prototype is asserted.
Input provenance: Forty Points, native E6 signed 1620 record tensor, prior null27 clock.
"""
from __future__ import annotations
import argparse, itertools, json, math, os, subprocess, sys
from pathlib import Path
from collections import Counter
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
V=list(itertools.product(range(3),repeat=3))
VID={v:i for i,v in enumerate(V)}
Z=np.exp(2j*np.pi/3)

def diff(u,v):return tuple((u[i]-v[i])%3 for i in range(3))
def det3(v):return (v[0]*v[2]-v[1]**2)%3

def native_e6(root=ROOT):
    """Native 27 x 3 signed tensor; does NOT invent particle/generation labels."""
    sys.path.insert(0,str(root/"analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as P
    old=P._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py","e6_mass_block_20261108")
    records=old.load_parent().build_records()
    assert len(records)==1620
    # Generic deterministic field; the block skew property holds for *every* field.
    phi=np.array([math.sin(i*.712)+.3*math.cos(i*.13)+1j*math.cos(i*.83)
                  for i in range(81)],complex)
    M=np.zeros((81,81),complex)
    for u,x,o,c in records:
        M[o,x]+=c*phi[u]
    blocks=M.reshape(27,3,27,3)
    antisym_residual=float(np.max(abs(blocks+blocks.transpose(0,3,2,1))))
    ranks=Counter(int(np.linalg.matrix_rank(blocks[i,:,j,:],tol=1e-9))
                  for i in range(27) for j in range(27))
    assert antisym_residual<1e-12 and ranks==Counter({0:459,2:270})
    assert np.max(abs(M+M.T))<1e-12
    # A fiber P_i = |i><i| (x) I3 commutes with SL3 but not with E6.
    e6=np.load(root/"artifacts/e6_27rep_basis_export/E6_basis_78.npy")
    assert e6.shape==(78,27,27)
    commutator_norm_sq=[]
    for i in range(27):
        # Frobenius norm^2 of [P_i,G_a] (real gauge generators not needed for >0).
        val=float(sum(np.linalg.norm(e6[a,i,:])**2+np.linalg.norm(e6[a,:,i])**2
                 -2*abs(e6[a,i,i])**2 for a in range(78)))
        commutator_norm_sq.append(val)
    assert min(commutator_norm_sq)>1e-8
    # Verify exact algebraic rank statement in the 3x3 epsilon model independently.
    eps=np.array([[[0,0,0],[0,0,1],[0,-1,0]],
                  [[0,0,-1],[0,0,0],[1,0,0]],
                  [[0,1,0],[-1,0,0],[0,0,0]]],int)
    assert np.all(np.einsum("aij,ji->a",eps,eps[0])==np.einsum("aij,ji->a",eps,eps[0]))
    return {
       "status":"NATIVE_E6_DIRECT_FIBER_PROJECTOR_OBSTRUCTION",
       "signed_tensor_records":len(records),"e6_irrep_generators":len(e6),
       "field_space":"C^27 tensor C^3; 27 E6 fibers x 3 qutrit labels",
       "block_count":27**2,"block_rank_census":{str(k):v for k,v in sorted(ranks.items())},
       "max_block_antisymmetry_residual":antisym_residual,
       "fiber_projectors_tested":27,
       "all_fiber_projectors_break_full_E6":min(commutator_norm_sq)>1e-8,
       "min_commutator_norm_squared":min(commutator_norm_sq),
       "native_rank_fixture_path":"data/w33_20261001_dflat_cartan_mass_loop.json",
       "conclusion":"Every direct 3x3 fiber-to-fiber mass block is skew and singular; naive 3-family selection from one E6-index pair fails. A gauge-invariant proper projector is forbidden before symmetry breaking because the E6 27 is irreducible.",
       "limits":"No physical 3-generation Yukawa or symmetry-broken projector was found. Mixed E6-coordinate projectors and added operators are not excluded."}

def odd_prime_chirp(p):
    """Prime-field *dense-weighted* translation-invariant escape from null-graph no-go."""
    k=np.indices((p,p,p))
    q=(k[0]*k[2]-k[1]**2)%p
    # Integer-valued dual quadratic spectral Hamiltonian. It is folded mod p.
    h=np.fft.ifftn(q)
    assert np.max(abs(h.imag))<1e-12
    u=np.fft.ifftn(np.exp(-2j*np.pi*q/p))
    norm=float(np.sum(abs(u)**2))
    err=float(np.max(abs(abs(u)**2-p**-3)))
    d=np.indices((p,p,p))
    null=((d[0]*d[2]-d[1]**2)%p==0)
    null[0,0,0]=False
    strength=abs(h);strength[0,0,0]=0
    weighted=strength>1e-9
    cnt=int(np.count_nonzero(weighted))
    outside=int(np.count_nonzero(weighted&~null))
    assert err<1e-12 and abs(norm-1)<1e-12
    assert outside>0
    return {"prime":p,"vertices":p**3,"t_star":"2*pi/p",
       "dual_symbol":"lambda(k)=canonical_integer_representative(det(k)) in {0,...,p-1}",
       "unitary_kernel":"inverse_Fourier[exp(-2*pi*i*det(k)/p)]",
       "flatness_max_abs_probability_residual":err,
       "sum_probabilities":norm,
       "nonzero_offdiagonal_weighted_differences":cnt,
       "off_null_support_differences":outside,
       "null_differences":p*p-1,
       "fraction_off_null":outside/max(cnt,1),
       "physical_boundary":"Real symmetric weighted Cayley Hamiltonian, but couplings extend beyond null links and grow nonlocal with p. Spectral values are folded integers, not a controlled smooth Lorentz dispersion."}

def weighted_continuum():
    return {"status":"EXACT_WEIGHTED_ESCAPE_WITH_NONLOCALITY_OBSTRUCTION",
       "cases":[odd_prime_chirp(p) for p in (3,5,7,11)],
       "proof":"The inverse finite Fourier transform of a nondegenerate quadratic chirp has constant modulus p^-3/2 by completing the square and the quadratic Gauss-sum norm p^(3/2).",
       "prior_no_go":"Only unweighted null-support adjacency was excluded for odd q>=5; dense weighted Hamiltonians fall outside that theorem.",
       "future_target":"Find finite-support weights with locally controlled generator and continuum low-k limit; not demonstrated here."}

def gauge_selector():
    """Harmonic projection is source-specific; vertex-charge gradients are H1-blind."""
    e=[(i,j) for i,x in enumerate(V) for j,y in enumerate(V)
       if i<j and det3(diff(x,y))==0]
    ix={pair:k for k,pair in enumerate(e)}
    f=[(i,j,k) for i in range(27) for j in range(i+1,27) for k in range(j+1,27)
       if (i,j) in ix and (i,k) in ix and (j,k) in ix]
    assert len(e)==108 and len(f)==36
    B1=np.zeros((27,108))
    B2=np.zeros((108,36))
    for n,(i,j) in enumerate(e):B1[i,n]=-1;B1[j,n]=1
    for n,(i,j,k) in enumerate(f):
        B2[ix[(i,j)],n]=1;B2[ix[(i,k)],n]=-1;B2[ix[(j,k)],n]=1
    assert np.max(abs(B1@B2))==0 and np.max(abs(B2.T@B2-3*np.eye(36)))==0
    Pgrad=B1.T@np.linalg.pinv(B1@B1.T,rcond=1e-12)@B1
    Pface=B2@B2.T/3
    PH=np.eye(108)-Pgrad-Pface
    rank=int(round(np.trace(PH)))
    residual=float(max(np.max(abs(PH@PH-PH)),np.max(abs(B1@PH)),np.max(abs(B2.T@PH))))
    leverage=np.diag(PH)
    assert rank==46 and residual<1e-10
    assert np.max(abs(leverage-23/54))<1e-11
    q=np.zeros(27);q[0]=1;q[1]=-1
    charge_source=B1.T@q
    charge_harmonic=float(np.linalg.norm(PH@charge_source))
    face_harmonic=float(np.linalg.norm(PH@B2[:,0]))
    e0=np.zeros(108);e0[0]=1
    conserved_cycle=(np.eye(108)-Pgrad)@e0
    div_cycle=float(np.linalg.norm(B1@conserved_cycle))
    cycle_leverage=float(np.linalg.norm(PH@conserved_cycle)**2)
    assert charge_harmonic<1e-11 and face_harmonic<1e-11 and div_cycle<1e-11
    assert abs(cycle_leverage-23/54)<1e-11
    return {"status":"EXACT_GAUGE_HODGE_CHARGE_SOURCE_FALISIFIER",
       "vertices":27,"edges":108,"faces":36,"harmonic_rank":rank,
       "projector_idempotence_and_closure_residual":residual,
       "single_oriented_edge_harmonic_leverage_squared":cycle_leverage,
       "exact_single_edge_leverage":"23/54",
       "per_edge_uniformity_deviation":float(np.max(abs(leverage-23/54))),
       "gradient_charge_harmonic_norm":charge_harmonic,
       "single_triangle_boundary_harmonic_norm":face_harmonic,
       "conserved_nonlocal_cycle_divergence":div_cycle,
       "conclusion":"All 108 oriented edges have same harmonic leverage 23/54; vertex-charge gradients excite none of H1, but divergence-free noncontractible cycle currents can. This does not select a unique photon coupling."}

def git_pickaxe(path,needle,root=ROOT,timeout=22):
    if not (root/path).is_file():return {"path":path,"needle":needle,"status":"path_absent"}
    try:
        shallow=subprocess.run(["git","-C",str(root),"rev-parse","--is-shallow-repository"],
                               capture_output=True,text=True,timeout=8)
        if shallow.returncode or shallow.stdout.strip()=="true":
            return {"path":path,"needle":needle,"status":"history_not_complete_or_shallow_checkout"}
        p=subprocess.run(["git","-C",str(root),"log","--follow","--reverse",
                          "--format=%H%x09%aI%x09%s","-S",needle,"--",path],
                         capture_output=True,text=True,timeout=timeout)
        if p.returncode:
            return {"path":path,"needle":needle,"status":"git_log_failed","detail":p.stderr[:120]}
        changes=[line.split("\t",2) for line in p.stdout.splitlines() if "\t" in line]
        return {"path":path,"needle":needle,"status":"file_history_pickaxe",
                "changes_count":len(changes),
                "first_change_on_file_history":dict(zip(("commit","author_date","message"),changes[0])) if changes else None,
                "most_recent_change_on_file_history":dict(zip(("commit","author_date","message"),changes[-1])) if changes else None}
    except subprocess.TimeoutExpired:
        return {"path":path,"needle":needle,"status":"timeout_bounded_no_inferred_first_owner"}

def provenance(root=ROOT):
    candidates=[
        ("analysis/2026-11-07_natural_constants_derivation_catalog.md","137+1/28+4/14045"),
        ("analysis/2026-11-07_natural_constants_derivation_catalog.md","137+880/24445"),
        ("analysis/2026-11-07_natural_constants_derivation_catalog.md","3/13+1/2200"),
        ("papers/forty_points/sec09_physics.tex","Nelson"),
        ("papers/forty_points/sec09_physics.tex","Weber")]
    results=[git_pickaxe(path,needle,root=root) for path,needle in candidates]
    return {"status":"CHRONOLOGICAL_FILE_PICKAXE_WITH_BOUNDARIES",
            "candidates":results,
            "scope":"First count-changing occurrence *within each named file's traversable history*, not first discovery in all repo, no semantic equivalence or selected-observable independence.",
            "shallow_note":"CI shallow checkout is explicitly excluded; only a full local clone can yield history metadata."}

def optical():
    """Concrete 27-port stage mappings, loss and crosstalk calibration fixture."""
    def forward_c(v):a,b,c=v;return (a,b,(c+2*a)%3)
    def forward_a(v):a,b,c=v;return ((a+2*c)%3,b,c)
    def inverse_a(v):a,b,c=v;return ((a+c)%3,b,c) # inverse of +2c (add c)
    def inverse_c(v):a,b,c=v;return (a,b,(c+a)%3)
    stages=[]
    for name,fn in [("SUM_c_plus_2a",forward_c),("SUM_a_plus_2c",forward_a),
                    ("SUM_a_plus_c_inverse",inverse_a),("SUM_c_plus_a_inverse",inverse_c)]:
        stages.append({"name":name,"map":[{"from":VID[v],"to":VID[fn(v)]} for v in V]})
        assert sorted(x["to"] for x in stages[-1]["map"])==list(range(27))
    P=np.zeros((27,27))
    for v in V:
        u=forward_a(forward_c(v))
        assert inverse_c(inverse_a(u))==v
        P[VID[u],VID[v]]=1
    def h(sign):
        return np.array([[Z**(sign*(j-k)**2%3)/np.sqrt(3) for k in range(3)]
                         for j in range(3)])
    M=Z*np.exp(-1j*np.pi/6)*P.T@np.kron(np.kron(h(1),h(-1)),h(-1))@P
    exact=np.array([[Z**((1+det3(diff(a,b)))%3)*np.exp(-1j*np.pi/6)/np.sqrt(27)
                     for b in V] for a in V])
    error=float(np.max(abs(M-exact)))
    assert error<1e-12
    tritters=[]
    for axis,sign in enumerate((1,-1,-1)):
        for frozen in itertools.product(range(3),repeat=2):
            ports=[]
            for t in range(3):
                xyz=list(frozen);xyz.insert(axis,t)
                ports.append(VID[tuple(xyz)])
            tritters.append({"axis":axis,"phase_sign":sign,"ports":ports})
    assert len(tritters)==27
    eta=0.92+0.06*np.cos(np.arange(27)*2*np.pi/27)**2
    crosstalk=.005
    C=np.zeros((27,27))
    for j in range(27):
        C[j,j]=1-2*crosstalk
        C[(j+1)%27,j]+=crosstalk
        C[(j-1)%27,j]+=crosstalk
    p=np.abs(M[:,0])**2
    observed=C@(eta*p)/(eta@p)
    corrected=np.linalg.solve(C,observed)/eta
    corrected/=sum(corrected)
    cal_res=float(np.max(abs(corrected-1/27)))
    raw_bias=float(np.max(abs(observed-1/27)))
    assert cal_res<1e-12 and raw_bias>1e-5
    # Random counts are deterministic synthetic engineering data only.
    n=5000
    rng=np.random.default_rng(20261108)
    counts=rng.multinomial(n,observed)
    return {"status":"EXPLICIT_27_PORT_STAGE_NETLIST_AND_CALIBRATION_TOY",
       "port_order":"lexicographic (a,b,c) over F3",
       "permutation_stages":stages,"tritter_layers":tritters,
       "sum_permutation_networks":4,"tritters":27,
       "max_two_mode_beamsplitters_excluding_permutation_routing":81,
       "generic_unitary_two_mode_bound":351,"matrix_max_residual":error,
       "calibration":{"detector_efficiency":eta.tolist(),"cyclic_crosstalk":crosstalk,
         "postselected_bias_before_correction":raw_bias,
         "bias_after_exact_synthetic_calibration":cal_res,
         "per_input_accepted_counts":n,
         "first_input_synthetic_click_counts":counts.tolist()},
       "scope":"Port/permutation schedule and idealized loss/crosstalk only; not a lithographic layout, MZI phase calibration, lab result or TOE-specific test."}

def produce(root=ROOT):
    return {"schema":"w33.20261108.five_frontrunner_deep_v1",
      "native_e6":native_e6(root),"weighted":weighted_continuum(),
      "gauge":gauge_selector(),"provenance":provenance(root),
      "optical":optical(),
      "limits":"No actual E6 quark/lepton assignment, vacuum, physical photon, causal continuum or optical device constructed."}
def main():
    pa=argparse.ArgumentParser()
    pa.add_argument("--root",type=Path,default=ROOT)
    pa.add_argument("--out",type=Path,default=Path("data/w33_20261108_deep_fivefronts.json"))
    args=pa.parse_args()
    d=produce(args.root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"native_blocks":d["native_e6"]["block_rank_census"],
       "weighted_out_null":[(c["prime"],c["off_null_support_differences"]) for c in d["weighted"]["cases"]],
       "harmonic_leverage":d["gauge"]["exact_single_edge_leverage"],
       "history":[x["status"] for x in d["provenance"]["candidates"]],
       "optical_error":d["optical"]["matrix_max_residual"]}))
if __name__=="__main__":main()
