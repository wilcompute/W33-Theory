"""Exact Eisenstein coercivity witness and native graph overlap controls."""
from pathlib import Path
import json,sys
from fractions import Fraction
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_pass12377_12381_continuation as old
import w33_pass12383_12386_dualhost_fronts as prior
ROOT=Path(__file__).resolve().parents[1]

def mul(A,B):
 a,b=A;c,d=B
 return a@c-b@d,a@d+b@c-b@d

def dagger(A):
 a,b=A
 return (a-b).T,-b.T

def exact_point():
 a,b,V,faces,loops=old.geometry()
 def rows(boundaries):
  A=np.zeros((len(boundaries),135),dtype=object);B=A.copy()
  for r,face in enumerate(boundaries):
   pos=np.zeros(4,dtype=int)
   for e,sign in face:
    if sign<0:pos-=V[e]
    power=int(pos[0]+pos[1])%3
    ca,cb=[(1,0),(0,1),(-1,-1)][power];A[r,e]+=sign*ca;B[r,e]+=sign*cb
    if sign>0:pos+=V[e]
   assert not pos.any()
  return A,B
 F=rows(faces);L=rows(loops);M=(old.R@L[0],old.R@L[1]);P=(L[0][[0,5]],L[1][[0,5]])
 D0=np.zeros((135,27),dtype=object);D1=D0.copy()
 for e,(i,j) in enumerate(zip(a,b)):
  D0[e,i]=-1;ca,cb=[(1,0),(0,1),(-1,-1)][int(V[e,0]+V[e,1])%3];D0[e,j]=ca;D1[e,j]=cb
 D=(D0,D1);K=np.array([[25,-15,-26],[-15,33,18],[-26,18,28]],dtype=object)
 X=mul(dagger(F),F);Y=mul(dagger(M),(K@M[0],K@M[1]));Z=mul(dagger(P),P);G=mul(D,dagger(D))
 A=4500*(X[0]+G[0])+500*Y[0]+27*Z[0];B=4500*(X[1]+G[1])+500*Y[1]+27*Z[1]
 assert all(v==0 for part in mul((4500*X[0]+500*Y[0]+27*Z[0],4500*X[1]+500*Y[1]+27*Z[1]),D) for v in part.flat)
 numeric=(np.asarray(A,float)+np.asarray(B,float)*np.exp(2j*np.pi/3))/4500
 inv=np.linalg.inv(numeric);q=2**24
 xb=np.rint(2*inv.imag/np.sqrt(3)*q).astype(np.int64).astype(object);xa=np.rint((inv.real+inv.imag/np.sqrt(3))*q).astype(np.int64).astype(object)
 ra,rb=mul((A,B),(xa,xb));ra-=4500*q*np.eye(135,dtype=object)
 residual_num=max(sum(abs(int(x))+abs(int(y)) for x,y in zip(r,s)) for r,s in zip(ra,rb));den=4500*q
 xnorm_num=max(sum(abs(int(x))+abs(int(y)) for x,y in zip(r,s)) for r,s in zip(xa,xb))
 assert residual_num<den
 bound=Fraction(den-residual_num,4500*xnorm_num)
 return {'momentum':'(2pi/3,2pi/3,0,0)','operator':'H_repaired_matched + D D^dag','matrix_denominator':4500,'inverse_denominator':q,'matrix_a':A.tolist(),'matrix_b':B.tolist(),'inverse_a':xa.tolist(),'inverse_b':xb.tolist(),'residual_bound':str(Fraction(residual_num,den)),'inverse_inf_norm_bound':str(Fraction(xnorm_num,q)),'certified_physical_eigenvalue_lower_bound':str(bound),'bound_decimal':float(bound),'proof':'Exact Z[omega] residual r<1 gives ||S^-1||inf<=||X||inf/(1-r). Hermiticity bounds its spectral radius; exact H D=0 separates physical and gauge blocks.','scope':'One exact nonidentity momentum, not a global torus constant.'}

def native_overlap():
 a,b,V,_,_=old.geometry();I=np.eye(2);sx=np.array([[0,1],[1,0]]);sy=np.array([[0,-1j],[1j,0]]);sz=np.diag([1,-1]);gamma=[np.kron(sx,I),np.kron(sy,I),np.kron(sz,sx),np.kron(sz,sy)];g5=np.kron(np.kron(sz,sz),np.eye(27))
 phase=np.random.default_rng(12394).uniform(-.1,.1,135);theta=np.random.default_rng(92).normal(size=27)
 def build(ph):
  T=np.zeros((27,27),complex);T[a,b]=np.exp(1j*ph);T[b,a]=np.exp(-1j*ph)
  W=(10*np.eye(27)-T)/10-np.eye(27);Dw=np.kron(np.eye(4),W)
  for mu in range(4):
   C=np.zeros((27,27),complex);C[a,b]=V[:,mu]*np.exp(1j*ph);C[b,a]=-V[:,mu]*np.exp(-1j*ph)
   Dw+=np.kron(gamma[mu],C/2)
  H=g5@Dw;E,U=np.linalg.eigh(H);assert min(abs(E))>1e-8
  D=np.eye(108)+g5@(U*np.sign(E))@U.conj().T
  return D,float(min(abs(E)))
 D,gap=build(phase);D2,_=build(phase+theta[a]-theta[b]);g=np.kron(np.eye(4),np.diag(np.exp(1j*theta)))
 gw=float(np.max(abs(g5@D+D@g5-D@g5@D)));cov=float(np.max(abs(D2-g@D@g.conj().T)));assert gw<1e-12 and cov<1e-12
 return {'dimension':108,'Wilson_kernel_gap':gap,'GW_residual':gw,'gauge_covariance_residual':cov,'index_trace':float(np.trace(g5@(np.eye(108)-D/2)).real),'scope':'Supplied Wilson graph Laplacian and four voltage-weighted derivatives on27 native sites. Finite gauge-covariant overlap operator; no chiral measure, locality bound, selected action or4D continuum proof.'}

def reciprocity_obstruction():
 d=prior.string_input();B=np.array(d['boundary_basis_13_by64']);rng=np.random.default_rng(12395)
 def sign(u,v):
  a=u@B%2;b=v@B%2;dot=int(a[:20]@b[:20]-a[20:]@b[20:]);assert dot%4==0
  return (dot//4)%2
 for _ in range(10000):
  u,v,w=rng.integers(0,2,(3,13));lhs=sign((u+v)%2,w);rhs=(sign(u,w)+sign(v,w))%2
  if lhs!=rhs:return {'u':u.tolist(),'v':v.tolist(),'w':w.tolist(),'left_exponent':lhs,'right_exponent':rhs,'scope':'The reduced-boundary reciprocity sign is not a bicharacter. It cannot be the commutator of an ordinary scalar group2-cocycle on the additive label group. This diagnoses the missing spin/vacuum conventions, not an inconsistency of the published model.'}
 raise AssertionError('No witness found')

if __name__=='__main__':
 out={}
 for n,f in [('exact_coercivity',exact_point),('native_overlap',native_overlap),('reciprocity_obstruction',reciprocity_obstruction)]:out[n]=f();print(n,'PASS',flush=True)
 (ROOT/'data/w33_pass12392_12396_exact_controls.json').write_text(json.dumps(out,indent=2)+'\n')
