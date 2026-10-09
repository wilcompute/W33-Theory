"""Exact local principal-symbol Hessian at the known classical
zero of H_cl = sum_e[(Ve.q+a)(Ue.p+a)]².

A positive quantum gap (from CCR/subellipticity) cannot be concluded
from harmonic small oscillations about this zero if the classical
Hessian has a kernel. This is a *semiclassical obstruction*, not proof
that the quantum H has zero gap.
"""
from pathlib import Path
import sys,json
import numpy as np
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
def certificate():
    geo=V.geometry()
    U=np.rint(40*geo['u']).astype('int64');W=np.rint(40*geo['v']).astype('int64')
    # q0=a*[39,-1^39,0^40]; p0=(a/39)*[-39,1^39,0^40].
    # For each current:  x/a = (W.qint+40)/40,
    # y/a = (U.pint+1560)/1560, and x*y=0 identically.
    qi=np.array([39]+[-1]*39+[0]*40,'int64')
    pi=np.array([-39]+[1]*39+[0]*40,'int64')
    X=W@qi+40;Y=U@pi+1560
    assert not np.any(X*Y)
    assert np.count_nonzero(X)==4
    # Scale derivative row by positive 62400, so every entry integral:
    # x=a X/40, y=a Y/1560, dJ= y*(W/40)dq + x*(U/40)dp,
    # 62400/a*dJ = Y W + 39 X U  (a cancels common scale).
    rows=np.concatenate((Y[:,None]*W,39*X[:,None]*U),axis=1)
    # Integer-matrix rank LOWER certificate: an invertible minor over F_p
    # lifts to an invertible integer/rational minor. Analytic UPPER bound:
    # q-gradients belong to 78D augmentation, and at most four p rows
    # survive because exactly four X factors are nonzero.
    def rank_mod(matrix, prime=32003):
        arr=np.array(matrix,dtype='int64')%prime
        r=0
        for c in range(arr.shape[1]):
            nz=np.flatnonzero(arr[r:,c])
            if not len(nz):continue
            pivot=r+int(nz[0])
            arr[[r,pivot]]=arr[[pivot,r]]
            arr[r]=(arr[r]*pow(int(arr[r,c]),-1,prime))%prime
            if r+1<len(arr):
                factor=arr[r+1:,c].copy()
                arr[r+1:]=(arr[r+1:]-factor[:,None]*arr[r])%prime
            r+=1
            if r==len(arr):break
        return r
    rank_q=rank_mod(Y[:,None]*W)
    rank_p=rank_mod(39*X[:,None]*U)
    rank=rank_mod(rows)
    assert rank==rank_q+rank_p
    assert rank_q==78 and rank_p==4 and rank==82
    return dict(status='PASS',classical_zero='q0=a*(39,-1x39,0x40), p0=a/39*(-39,1x39,0x40), a=1/sqrt20',
        currents=160,nonzero_q_factor=int(np.count_nonzero(X)),nonzero_p_factor=int(np.count_nonzero(Y)),
        gradient_jacobian_rank=int(rank),q_gradient_rank=int(rank_q),
        p_gradient_rank=int(rank_p),tangent_phase_dimension=156,
        Hessian_rank=int(rank),Hessian_nullity=int(156-rank),
        theorem='At a common classical zero of each quartic current square, Hessian(Hcl) = 2 J_gradient.T J_gradient. Its nullity is nonzero, so the purely quadratic harmonic approximation is noncoercive; higher-order terms and quantum commutator estimates are necessary for the physical gap.',
        scope='Classical principal-symbol only. Quantum gap does not follow from Hessian degeneracy; overall Hessian scale omitted.')
if __name__=='__main__':
    x=certificate();(ROOT/'data/w33_20261009_classical_zero_hessian_rank.json').write_text(json.dumps(x,indent=2)+'\n')
    print('HESSIAN',x['Hessian_rank'],x['Hessian_nullity'],x['q_gradient_rank'],x['p_gradient_rank'])
