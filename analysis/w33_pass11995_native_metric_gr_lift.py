"""Ten native edge weights are local coordinates for a full acoustic metric.

11956 owns weighted-harmonic matching on a different 3D cover. Here the
actual11991 four-cover admits all10 metric variations, including offdiagonal
Gowdy polarizations. Einstein dynamics is pulled back as an input, not derived.
"""
import json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from w33_pass11991_native_four_period_cover import native_geometry
ROOT=Path(__file__).resolve().parents[1]
PAIRS=list(itertools.combinations_with_replacement(range(4),2))


def inputs():
    d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    _,edges,B,*_=native_geometry()
    return np.array(B.T[:,1:],float),np.array(d['primitive_integer_edge_voltages'],float),s.Matrix(d['harmonic_voltages_Q']),s.Matrix(d['exact_acoustic_metric'])


def homogenize(w,b,v):
    L=b.T@(w[:,None]*b)
    h=v-b@np.linalg.solve(L,b.T@(w[:,None]*v))
    return h.T@(w[:,None]*h)/27,h


def pack(g):return np.array([g[i,j] for i,j in PAIRS])


def lift(target,b,v,selected):
    w=np.ones(135);history=[]
    for iteration in range(15):
        g,h=homogenize(w,b,v);err=pack(g-target);history.append(float(max(abs(err))))
        if max(abs(err))<2e-14:break
        jac=np.array([[h[e,i]*h[e,j]/27 for e in selected] for i,j in PAIRS])
        delta=np.linalg.solve(jac,-err);scale=1.
        while True:
            trial=w.copy();trial[selected]+=scale*delta
            if min(trial)>.1 and max(abs(pack(homogenize(trial,b,v)[0]-target)))<max(abs(err)):break
            scale/=2;assert scale>1e-9
        w=trial
    assert history[-1]<2e-13
    return w,history


def payload():
    b,v,C,G=inputs()
    derivative=s.Matrix([[C[e,i]*C[e,j]/27 for e in range(135)] for i,j in PAIRS])
    selected=list(derivative.rref()[1]);assert len(selected)==10
    det=s.factor(derivative[:,selected].det());assert det!=0
    assert derivative.rank()==10
    base,h=homogenize(np.ones(135),b,v);assert max(abs(pack(base-np.array(G,float))))<1e-13
    rng=np.random.default_rng(11995);dw=rng.normal(size=135);step=1e-5
    fd=(homogenize(1+step*dw,b,v)[0]-homogenize(1-step*dw,b,v)[0])/(2*step)
    analytic=np.array(derivative,float)@dw
    fd_error=float(max(abs(pack(fd)-analytic)));assert fd_error<1e-8
    # Baseline orthonormal drawing. G is the inverse/acoustic metric here.
    R=np.linalg.cholesky(np.array(G,float))
    clock=json.loads((ROOT/'data/w33_pass11994_native_clock_order.json').read_text())['vacua'][0]
    u=np.array(list(map(float,clock['clock_primitive'])))
    direction=R.T@u/np.sqrt(u@np.array(G,float)@u);e=np.eye(4)[:,0]
    difference=e-direction
    O=np.eye(4) if np.linalg.norm(difference)<1e-12 else np.eye(4)-2*np.outer(difference,difference)/np.dot(difference,difference)
    R=R@O
    assert np.max(abs(R.T@u/np.sqrt(2)-e))<1e-12
    baseline_K=np.array(G,float)-np.outer(np.array(G,float)@u,np.array(G,float)@u)
    assert np.max(abs(baseline_K-2*np.array(s.Matrix(clock['metric_Q']),float)))<1e-12
    rows=[]
    for t,P,Q,lam in [(1,0,0,0),(1.001,.002,.003,.001),(.999,-.002,-.003,-.001),(1.004,.001,-.002,.002)]:
        a=np.exp(lam/2)/np.sqrt(t)
        lorentz=np.zeros((4,4));lorentz[0,0]=-a;lorentz[1,1]=a
        lorentz[2:,2:]=t*np.array([[np.exp(P),np.exp(P)*Q],[np.exp(P)*Q,np.exp(-P)+np.exp(P)*Q*Q]])
        euclidean=lorentz.copy();euclidean[0,0]*=-1
        target=R@np.linalg.inv(euclidean)@R.T
        w,history=lift(target,b,v,selected);metric,_=homogenize(w,b,v)
        A=np.linalg.solve(R,metric)@np.linalg.inv(R.T)
        K=A-2*np.outer(A@e,A@e)/(e@A@e);restored=np.linalg.inv(K)
        error=float(np.max(abs(restored-lorentz)));assert error<1e-11
        rows.append(dict(t=t,P=P,Q=Q,lambda_value=lam,selected_weights=w[selected].tolist(),minimum_weight=float(min(w)),Newton_residual_history=history,Lorentz_metric_error=error))
    return dict(status='PASS',native_edges=135,metric_components=10,
        exact_metric_jacobian_rank=10,selected_edge_indices=selected,selected_jacobian_determinant=str(det),
        envelope_derivative='dG_ij/dw_e = h_ei h_ej/27, with h=V-b(b^T W b)^-1 b^T W V; the corrector is recomputed at EVERY weight change.',
        exact_jacobian_Q=[[str(x) for x in row] for row in derivative[:,selected].tolist()],
        implicit_function_theorem='Nonzero rational10x10 Jacobian proves an open neighborhood of the baseline metric is realized by positive native weights, fixing the other125weights. This local existence statement is exact; displayed finite Newton lifts are numerical witnesses.',
        derivative_finite_difference_error=fd_error,Gowdy_metric_lifts=rows,
        clock_primitive_coordinates=u.tolist(),clock_aligned_frame_R=R.tolist(),baseline_clock_symbol_equals_twice11994_eta=True,
        conditional_GR_action='Align R R^T=G0 so R^T u/sqrt2=e0 for actual11994clock u, which is a clock covector in the acoustic symbol. Define A=R^-1 G(w) R^-T and g=[A-2 A e0 e0^T A/(e0^T A e0)]^-1. The reflection is involutive between positive inversemetrics and Lorentz inversemetrics with e0 timelike, so all10components remain. On this10weight chart, S[w]=S_EH[g(w)] is an invertible field redefinition of supplied continuum Einstein gravity, with lapse/shift constraints and2 propagating modes inherited. No claim that a sum of native graph terms generates this action. The inverse map is cellwise, while continuum derivatives/limit are extra inputs.',
        redundant_edge_weight_kernel_dimension=125,
        gravity_boundary='Kinematic ability to encode all10 metric components and the offdiagonal nonlinear Gowdy metric, not W33-derived Einstein equations, refoliation symmetry or Newton/Lambda selection. Adding generic kinetic terms for135weights would introduce extra modes, not2gravitons.',
        prior=['11956 exact 3D weighted Gauss-reduced metric matching and contraction proof','11991 actual4period cover and acousticG','11992 imported full nonlinear Gowdy Einstein benchmark','11976 finite pointwise constraint failure'],
        primary=['https://doi.org/10.1090/S0002-9947-00-02632-5','https://arxiv.org/abs/gr-qc/9710102','https://arxiv.org/abs/gr-qc/0402005'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11995_native_metric_gr_lift.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['selected_jacobian_determinant'])
