"""Audit the actual paper/compiler Weyl ordering, not a new commutation geometry."""
import pathlib,itertools,json,sys,collections
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20260924_temporal_su9_e8_compiler as old

def build():
    w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag([1,w,w*w])
    labels=list(itertools.product(range(3),repeat=4));clock=[];shift=[]
    for a,b,c,d in labels:
        P=lambda j,k:np.linalg.matrix_power(Z,j)@np.linalg.matrix_power(X,k)
        Q=lambda j,k:np.linalg.matrix_power(X,j)@np.linalg.matrix_power(Z,k)
        clock.append(np.kron(P(a,b),P(c,d).conj()));shift.append(np.kron(Q(a,b),Q(c,d).conj()))
    errors=[];wrong=[];count=collections.Counter();zeros=0
    for x,A,C in zip(labels,clock,shift):
        for y,B,D in zip(labels,clock,shift):
            k=old.symp(x,y);count[k]+=1
            errors.append(float(np.linalg.norm(A@B-w**k*B@A)))
            wrong.append(float(np.linalg.norm(C@D-w**k*D@C)))
            assert np.linalg.norm(C@D-w**((-k)%3)*D@C)<1e-12
            zeros+=int(k==0)
    assert max(errors)<1e-12 and sum(e>1e-8 for e in wrong)==4320
    for a,b in itertools.product(range(3),repeat=2):
        assert np.linalg.norm(old.qutrit_pauli(a,b)-np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b))<1e-12
    paper=(ROOT/'papers/forty_points/sec03_selfentangle.tex').read_text()
    assert 'P_u=Z^{u_1}X^{u_2}'in paper and 'P_u=X^{u_1}Z^{u_2}'not in paper
    return dict(status='PASS_PAPER_COMPILER_CLOCK_FIRST_PHASE_RECONCILIATION',ordered_label_pairs=81**2,
        exact_phase_histogram=dict(sorted(count.items())),commuting_ordered_pairs=zeros,
        maximum_clock_first_matrix_residual=max(errors),shift_first_pairs_disagreeing_with_displayed_clock_first_phase=4320,
        maximum_wrong_convention_residual=max(wrong),
        corrected_paper_definition='P_u=Z^(u1) X^(u2), matching the cited executable compiler; label coordinates reversed relative to Section2.',
        exact_phase_law='For ZX=omega XZ and P_u=Z^a X^b: P_u P_v=omega^(aB-bA) P_v P_u. For Phi_(u,v)(M)=P_u M P_v^dagger, the exponent is [u,u_prime]-[v,v_prime]. The X-first convention reverses that exponent.',
        vectorization='Paper convention |i><j| maps to |i> tensor |j>, so Phi matrix is P_u tensor conjugate(P_v).',
        boundary='A paper notation correction: the cited compiler already used the correct clock-first convention. No change to old executable mathematics or the zero-pairing W33 graph; a global sign reversal changes oriented phases, not commutation incidence. Exhaustive complex matrix checks are floating-point; the phase-law proof uses exact ZX=omega XZ arithmetic.')

if __name__=='__main__':
    out=build();(ROOT/'data/w33_20261102_two_sided_phase_convention.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['ordered_label_pairs'],out['shift_first_pairs_disagreeing_with_displayed_clock_first_phase'],flush=True)
