"""TOE61 Gauss-charged/neutral exact Schur *formulas* and numerical bounds.

Selected 3-loop compact U1 rotor only, edge charge background q.
The charge q is a fixed longitudinal electric string, not dynamical fermions.
"""
from pathlib import Path
import numpy as np,json
from scipy import sparse
from scipy.sparse.linalg import eigsh
R=Path(__file__).resolve().parents[1]
prior=json.loads((R/'data/w33_20261013_toe58_three_octagons.json').read_text())
G=np.array(prior['signed_Gram'],float)
assert G.tolist()==[[8,-4,-4],[-4,8,4],[-4,4,8]]
# q=edge0 from TOE58; its overlaps with selected loops recomputed
import sys;sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,v,lookup,octs,comm,*_=prep()
P=np.rint(np.array([cycle_row(x,ed,v,lookup,np.zeros(3)).real for x in octs+comm])).astype(int)
C=P[[0,186,164]]
q=np.zeros(160);q[0]=1
u=C@q;s=np.linalg.solve(G,u)
perp=float(q@q-u@s)
assert perp>=-1e-10
lmin=float(np.linalg.eigvalsh(G)[0])
assert abs(lmin-4)<1e-10
def eigen(g,N,charge):
 L=2*N+1;m=np.arange(-N,N+1)
 x,y,z=np.meshgrid(m,m,m,indexing='ij')
 M=np.column_stack([x.ravel(),y.ravel(),z.ravel()])
 en=g*g/2*(np.einsum('ai,ij,aj->a',M,G,M)+2*charge*(M@u)+charge*charge*(q@q))
 diagonal=en+3/g**2
 S=sparse.diags(np.ones(L-1),1,shape=(L,L),format='csr');hop=S+S.T;I=sparse.eye(L,format='csr')
 T=sparse.kron(sparse.kron(hop,I),I)+sparse.kron(sparse.kron(I,hop),I)+sparse.kron(sparse.kron(I,I),hop)
 H=sparse.diags(diagonal,format='csr')-T/(2*g*g)
 values,vecs=eigsh(H,k=2,which='SA',tol=2e-11)
 gs=vecs[:,0];E=float(gs@(H@gs));res=float(np.linalg.norm(H@gs-E*gs))
 # for ||m||>=N+1, ||C^T m+q||>=sqrt(lmin)*(N+1)-||q||
 coarse=max(0,np.sqrt(lmin)*(N+1)-charge*np.linalg.norm(q))**2
 # sharper shifted quadratic bound:
 sharper=lmin*max(0,(N+1)-charge*np.linalg.norm(s))**2+charge*perp
 lower_ext=.5*g*g*max(coarse,sharper)
 b2=3/(4*g**4)
 assert lower_ext>E,(g,N,charge,E,lower_ext)
 lower=max(0,E-b2/(lower_ext-E))
 return dict(N=N,states=len(M),charged=bool(charge),ritz_E=E,ritz_gap=float(values[1]-values[0]),
             ground_eigenvector_residual=res,
             outside_electric_bound=lower_ext,
             approximate_Schur_lower=lower,
             width=E-lower)
out=[]
for g in (.7,1.1):
 sector={}
 for charge in (0,1):
  rows=[eigen(g,N,charge) for N in (4,5,6)]
  assert all(x['ground_eigenvector_residual']<1e-8 for x in rows)
  sector['charged' if charge else 'neutral']=rows
 neut=sector['neutral'][-1];chg=sector['charged'][-1]
 gaplow=chg['approximate_Schur_lower']-neut['ritz_E']
 gapup=chg['ritz_E']-neut['approximate_Schur_lower']
 out.append(dict(g=g,neutral=sector['neutral'],charged=sector['charged'],
    charge_excitation_gap_numeric_interval=[gaplow,gapup],
    E_q_minus_E_zero_at_N6=chg['ritz_E']-neut['ritz_E']))
 print('TOE61 charged',g,'gap interval',gaplow,gapup,'Ritz',chg['ritz_E']-neut['ritz_E'],flush=True)
assert all(x['charge_excitation_gap_numeric_interval'][0]>0 for x in out)
doc={'status':'PASS_TOE61_SELECTED_THREE_LOOP_CHARGED_GAP_BOUNDS',
'native_3_loop_Gram':G.astype(int).tolist(),'charged_reference_edge':0,
'charge_overlap_vector':u.astype(int).tolist(),'shifted_quadratic_vector':s.tolist(),
'orthogonal_projection_remainder_norm_sq':perp,'cases':out,
'conditional_theorem':"For any selected 3-loop electric flux E=C.Tm+q with nonzero fixed native edge q, Gauss charge B.T E=B.Tq is constant. Outside |m|_infty>N, use ||C.Tm+q||²=(m+G^-1 Cq).T G(m+G^-1 Cq)+||q||²−(Cq).T G^-1(Cq). Thus C_ext >=g²/2[λmin(G) max(0,N+1-||G^-1Cq||)²+q_perp²]. Compare with triangle inequality ||C.Tm+q||>=sqrt λmin(G)(N+1)−||q||. Wilson magnetic potential is PSD; finite-to-outside hop norm squared 3/(4g⁴); Schur gives lower L=E_N−b²/(C_ext−E_N). Subtract neutral and charged intervals to enclose E_charged−E_neutral. Finite blocks preserve exact Gauss.",
'precision':"Numbers use ordinary float sparse Ritz eigenvalues and residuals, not outward-rounded interval eigenvalues; exact mathematical Schur inequalities apply to exact finite-block eigenvalues. This is NOT a rigorously machine-certified numerical spectral interval.",
'physics_scope':"Only the selected 3 Wilson plaquette shifts with fixed external electric string q; no dynamical fermions, no full 1385 plaquettes, no charge screening/confinement, no physical electric charge or full continuum QED."}
(R/'data/w33_20261013_toe61_charge_gap.json').write_text(json.dumps(doc,indent=2)+'\n')
