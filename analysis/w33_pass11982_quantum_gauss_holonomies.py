"""Actual Gauss-rotor control and64-flat-coordinate harmonic gauge dynamics.

The full native Born-Oppenheimer construction is approximate; the ring
Gauss-law/unitary equivalence test is an exact finite-cutoff matrix identity.
The135edge tritangent input is prior construction, including
analysis/PASS11980_DISCRETE_HEISENBERG_HOLONOMIES.md;
analysis/BT816_cubic_surface_flags_reconstructed.md owns classical135flags.
See analysis/2026-10-14_toe80_native_octagon_e6_weyl_root_system.md.
Also analysis/PASS4992_4999_EXECUTED_OUTCOMES.md.
"""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from w33_pass11980_heisenberg_fixed_holonomies import build_module,DIRECTIONS
from w33_20261015_toe82_native_H27_h1_character import mul

ROOT=Path(__file__).resolve().parents[1]


def ring(phi,L=3,g=.7,kappa=1.,V=.4):
    occupations=[o for o in itertools.product((0,1),repeat=4) if sum(o)==2]
    states=[(o,m) for o in occupations for m in range(-L,L+1)];ix={s:i for i,s in enumerate(states)}
    H=np.zeros((len(states),len(states)),complex);background=np.array([1,0,1,0])
    for col,(o,m) in enumerate(states):
        electric=m+np.cumsum(np.array(o)-background)
        assert electric[-1]==m
        assert all(electric[(i-1)%4]-electric[i]+o[i]-background[i]==0 for i in range(4))
        H[col,col]=.5*g*g*(electric@electric)+V*sum((o[i]-.5)*(o[(i+1)%4]-.5) for i in range(4))
        for i in range(4):
            j=(i+1)%4
            if o[i] and not o[j]:
                out=list(o);out[i]=0;out[j]=1
                shifted=m-(1 if i==3 else 0)
                target=(tuple(out),shifted)
                if target not in ix:continue
                outgoing=shifted+np.cumsum(np.array(out)-background)
                required=np.zeros(4,dtype=int);required[i]=-1
                assert np.array_equal(outgoing-electric,required)
                # c_j^dag c_i with canonical ascending Fock order.
                sign=(-1)**sum(o[min(i,j)+1:max(i,j)])
                amp=-kappa*sign*np.exp(1j*(phi if i==3 else 0))
                row=ix[target];H[row,col]+=amp;H[col,row]+=amp.conjugate()
    assert np.max(abs(H-H.conj().T))<1e-12
    return H,np.array([m for o,m in states])


def payload():
    controls=[]
    for L in (2,3,4):
        H0,m=ring(0,L);Hp,_=ring(2*np.pi/9,L)
        U=np.diag(np.exp(-2j*np.pi*m/9))
        error=float(np.max(abs(Hp-U@H0@U.conj().T)))
        assert error<1e-12
        ev=np.linalg.eigvalsh(Hp)
        controls.append(dict(cutoff=L,dimension=len(m),unitary_equivalence_error=error,ground=float(ev[0]),same_N_gap=float(ev[1]-ev[0])))
    # Native27 complex: Coulomb-project the actual integer flat cochains.
    _,_,C=build_module();G=list(itertools.product(range(3),repeat=3));ix={g:i for i,g in enumerate(G)}
    faces=sorted({tuple(sorted(ix[mul(g,t)] for t in ((0,0,0),d,mul(d,d)))) for g in G for d in DIRECTIONS})
    edges=sorted({e for f in faces for e in itertools.combinations(f,2)})
    B=np.zeros((27,135))
    for j,(a,b) in enumerate(edges):B[a,j]=-1;B[b,j]=1
    P=np.eye(135)-B.T@np.linalg.pinv(B@B.T)@B
    metric=C@P@C.T;mu,muvec=eigh(metric)
    assert min(mu)>0
    invroot=(muvec/np.sqrt(mu))@muvec.T
    old=json.loads((ROOT/'data/w33_pass11980_heisenberg_fixed_holonomies.json').read_text())
    probe=old['explicit_holonomies_and_matter_probe'];row=probe['uniform_hopping_finite_free_fermion_fillings']['18']['continuous_flat_torus_audit']
    coefficients=np.array(row['selected_coefficients']);phase=coefficients@np.array(probe['character_generators_mod9'])%9
    links=phase@C%9;H=np.zeros((27,27),complex);derivatives=np.zeros((64,27,27),complex)
    for j,(a,b) in enumerate(edges):
        H[a,b]=-np.exp(2j*np.pi*links[j]/9);H[b,a]=H[a,b].conjugate()
        derivatives[:,a,b]=1j*C[:,j]*H[a,b];derivatives[:,b,a]=derivatives[:,a,b].conjugate()
    e,u=eigh(H);occupied=u[:,:18];projector=occupied@occupied.conj().T
    K=np.zeros((64,64))
    for j,(a,b) in enumerate(edges):K-=2*np.real(projector[b,a]*H[a,b])*np.outer(C[:,j],C[:,j])
    transition=np.einsum('ai,jab,bk->jik',occupied.conj(),derivatives,u[:,18:])
    K+=2*np.einsum('jia,kia,ia->jk',transition,transition.conj(),1/(e[:18,None]-e[None,18:])).real
    w2,v=eigh(invroot@K@invroot);assert min(w2)>0
    rows=[]
    for g in (.001,.003,.01):
        frequencies=g*np.sqrt(w2)
        covariance=g/2*invroot@(v/np.sqrt(w2))@v.T@invroot
        rms=np.sqrt(np.maximum(np.diag(C.T@covariance@C),0))
        rows.append(dict(g=g,frequency_min=float(min(frequencies)),frequency_max=float(max(frequencies)),
                         frequency_over_fermi_gap=float(max(frequencies)/(e[18]-e[17])),maximum_link_phase_RMS=float(max(rms)),zero_point_energy=float(sum(frequencies)/2)))
    # Gauge representative dependence is removed by P, not assumed away.
    rng=np.random.default_rng(11982);gauge=rng.normal(size=(27,64));C2=C+gauge.T@B
    covariance_error=float(np.max(abs(C2@P@C2.T-metric)));assert covariance_error<1e-10
    return dict(status='PASS',exact_Gauss_rotor_controls=controls,
        background_parameter_equivalence='For fully dynamical compact links, a specified flat external connection can be shifted into the rotor variables. Electric terms, Gauss constraints and flat-face magnetic terms are preserved under the change of variable. H_external(phi)=U_phi H_external(0) U_phi^dag; this is not a symmetry H0 commuting with Uphi and does NOT say the Born-Oppenheimer holonomy potential is constant.',
        native_flat_gauge_metric='M=C [I-B^T(BB^T)^+B] C^T for actual27vertex/135edge tritangent complex, after imposing the45flat triangle constraints. H_BO=(g^2/2) p^T M^-1 p+E18(theta).',
        native_metric_smallest_eigenvalue=float(min(mu)),gauge_representative_metric_error=covariance_error,
        harmonic_quantization=rows,normal_frequency_squared_per_g_squared=w2.tolist(),
        first_order_nearest_neighbor_interaction_energy=float(sum(projector[a,a].real*projector[b,b].real-abs(projector[a,b])**2 for a,b in edges)),
        scope='Ring: full finiteFock/Gauss electricrotor with actualdensityinteraction. Native64coordinate calculation: scalar quadratic Born-Oppenheimer/strong-triangle-flatness approximation, omitting Berry/Born-Huang corrections and nonflat magnetic modes; not full135link interacting spectrum, global tunneling proof, thermodynamic gap or a physical mass.',
        prior=['11969 full nativeGauss compiler','11974/11979 actualtwo-loop patches','11980 stableflat-sector freefermion Hessian'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11982_quantum_gauss_holonomies.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['harmonic_quantization'])
