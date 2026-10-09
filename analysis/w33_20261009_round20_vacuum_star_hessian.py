"""Local Gaussian stability at *all eighty* native W33 classical-zero
star directions for the superior complex 78D 11769 covariance.
Finite exhaustive Hessian + several displacement-ray growth witnesses.
Not a spectral enclosure for the infinite-dimensional operator.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
from w33_20261009_round18_classical_star_squeezed_trial import anchor

def main():
 g=H.geometry();u,v=g['u'],g['v'];t=H.exact_trial()
 C0,C0i=H.spectral_covariance(g)
 U=np.rint(u*40).astype(np.int64);V=np.rint(v*40).astype(np.int64)
 a=1/math.sqrt(20);C=t['t']*C0;Ci=C0i/t['t'];P=t['f']*np.diag(g['s'])
 sx=np.einsum('ei,ei->e',v@C,v)/2
 sy=np.einsum('ei,ei->e',u@(Ci+P@C@P),u)/2
 cross=np.einsum('ei,ei->e',v@C@P,u)/2
 base=np.sum((a*a+sx)*(a*a+sy)+4*a*a*cross+2*cross**2)
 assert abs(base-t['energy'])<1e-10
 samples=[]
 for star in range(80):
  q0,p0=anchor(star,U,V)
  x=v@q0;y=u@p0
  # quartic polynomial E(q_scale,p_scale) = base +
  # C_20 q² + C_02 p² + C_11 qp + C_22 q²p².
  # Odd coefficients could occur; compute and verify exact cancellations
  coeff={
   'linear_q':float(np.sum(2*a*x*(a*a+sy+2*cross))),
   'linear_p':float(np.sum(2*a*y*(a*a+sx+2*cross))),
   'qq':float(np.sum(x*x*(a*a+sy))),
   'pp':float(np.sum(y*y*(a*a+sx))),
   'qp':float(np.sum(x*y*(4*a*a+4*cross))),
   'qqp':float(np.sum(2*a*x*x*y)),
   'qpp':float(np.sum(2*a*x*y*y)),
   'qqpp':float(np.sum(x*x*y*y))
  }
  assert abs(coeff['linear_q'])<1e-10 and abs(coeff['linear_p'])<1e-10
  # Genuine cubic q²p and qp² terms survive at star centers.
  # They must enter the GLOBAL coherent-displacement positivity check.
  h=np.array([[2*coeff['qq'],coeff['qp']],[coeff['qp'],2*coeff['pp']]])
  eigen=np.linalg.eigvalsh(h)
  assert eigen[0]>0
  # For q=s, E(s,p)-E0=A*s² + alpha(s)*p² + s*(qp+qqp*s)*p.
  # alpha(s)=pp+qpp*s+qqpp*s². If alpha(s)>0 for all s and
  # D(s)=4*A*alpha(s)-(qp+qqp*s)²>0 for all s, complete the p square.
  A,B,T,W,Z,R=(coeff[k] for k in ('qq','pp','qp','qqp','qpp','qqpp'))
  alpha_disc=Z*Z-4*B*R
  D0=4*A*B-T*T;D1=4*A*Z-2*T*W;D2=4*A*R-W*W
  discr_D=D1*D1-4*D0*D2
  assert A>0 and B>0 and R>0 and alpha_disc<0
  assert D0>0 and D2>0 and discr_D<0,(D0,D1,D2,discr_D)
  disc=D0
  samples.append(dict(star=star,eigenvalues=eigen.tolist(),energy_coefficients=coeff,
      hessian_determinant=disc,alpha_discriminant=alpha_disc,
      completed_square_discriminant=discr_D,completed_square_quadratic=[D0,D1,D2],
      displacement_global_polynomial_minimum=float(base)))
 tiny=[x['eigenvalues'][0] for x in samples]
 out=dict(status='PASS',n_stars=80,centered_complex_Gaussian_energy=float(base),
   minimum_hessian_eigenvalue=float(min(tiny)),maximum_hessian_eigenvalue=float(max(tiny)),
   all_hessian_positive=True,all_global_restricted_displacement_minima_centered=True,
   star_samples=samples,
   exact_nonnegative_polynomial_argument='For every star E(s,r)=E0+A*s²+B*r²+T*s*r+W*s²*r+Z*s*r²+R*s²*r². Linear coefficients vanish, but cubic terms do NOT. Set alpha(s)=B+Z*s+R*s² and D(s)=4A*alpha(s)-(T+W*s)². If both alpha(s)>0,D(s)>0 for all real s (positive leading terms, negative discriminants), completing the r-square proves E(s,r)>=E0 for all real s,r, at fixed covariance/phase. The displayed coefficient signs are numerical unless interval-certified.',
   scope='Finite native W33 graph exhaustive numerical inequalities, with generous positive margins but not exact interval-certified signs. It is a *global* two-parameter coherent-displacement result for each of 80 stars at FIXED covariance, not lower spectral bound or vacuum uniqueness.')
 (ROOT/'data/w33_20261009_round20_vacuum_star_hessian.json').write_text(json.dumps(out,indent=2)+'\n')
 print('VACUUM all80 global-displacement min',base,'min eigen',min(tiny),'max eigen',max(tiny),'min discriminant',min(x['hessian_determinant'] for x in samples),flush=True)
if __name__=='__main__':main()
