import hashlib,json,pathlib,numpy as np,sympy as sp
R=pathlib.Path(__file__).resolve().parents[1]
paths=['data/w33_pass11991_native_four_period_cover.json','data/toe_20261108_coupled_holonomy_response.json']
old=json.loads((R/paths[0]).read_text());d=json.loads((R/paths[1]).read_text())
row=d['rows'][0];K=np.array(row['static_Hessian']);G=sp.Matrix(row['tree_electric_metric_g1']);Z=np.array(row['loop_kinetic_Z0'])
assert row['sizes']==[2,2,2,2] and row['mass']==.8
# Reconstruct exact native metric from its rational acoustic certificate.
G=sp.Matrix([[sp.Rational(x) for x in r] for r in old['exact_acoustic_metric']])*sp.Rational(27,2)
actions=[(r['h'],sp.Matrix(r['matrix'])) for r in old['exact_deck_actions']]
assert all(r==sp.eye(4) for h,r in actions if h[0]==h[1]==0)
P=[]
for a,b in [(1,0),(0,1)]:
 p=sum(((2 if (a*h[0]+b*h[1])%3==0 else -1)*r for h,r in actions),sp.zeros(4))/27
 assert p*p==p and p.trace()==2 and p.T*G==G*p
 P.append(p)
assert P[0]+P[1]==sp.eye(4) and P[0]*P[1]==sp.zeros(4)
weights=[sp.factor((p*G.inv())[3,3]/G.inv()[3,3]) for p in P]
rates=[np.trace(np.array(p,float)@np.array(G.inv(),float)@K)/2 for p in P]
Gn=np.array(G,float)
assert np.max(abs(Gn-np.array(row['tree_electric_metric_g1'])))<1e-14
res=dict(K=max(np.linalg.norm(np.array(r,float).T@K@np.array(r,float)-K) for h,r in actions),
 G=max(np.linalg.norm(np.array(r,float).T@Gn@np.array(r,float)-Gn) for h,r in actions),
 Z0=max(np.linalg.norm(np.array(r,float).T@Z@np.array(r,float)-Z) for h,r in actions))
reconstruction=Gn@sum((v*np.array(p,float) for v,p in zip(rates,P)),np.zeros((4,4)))
assert res['K']<1e-12 and res['G']<1e-12 and res['Z0']<1e-12 and np.linalg.norm(K-reconstruction)<1e-12
out=dict(status='N2_EQUAL_TORUS_NATIVE_H27_STATIC_DOUBLET_SYMMETRY_AND_EXACT_OBSERVABLE_WEIGHTS',
 exact_projectors=[[[str(x) for x in r] for r in p.tolist()] for p in P],
 real_character_planes=[[1,0],[0,1]],exact_theta4_plane_weights=list(map(str,weights)),
 squared_frequencies_over_g2=list(map(float,rates)),numeric_invariance_residuals=res,
 reconstruction_residual=float(np.linalg.norm(K-reconstruction)),
 proof='Prior native H27 action has two inequivalent real2D C3 character planes. On the equal-period finite torus the invariant symmetric Hessian and electric metric restrict to scalars relative to one another on each plane. Thus static frequencies are doublets; projection of the physical fourth holonomy through exact G gives the displayed rational weights. These are representation-sector weights, not generations or particle spins.',
 prior_owner='Pass11991 exact native character-plane/deck action and invariant metric dimension2. This is an application to the new finite holonomy response, not new group classification.',
 input_raw_sha256={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},source_raw_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
print(json.dumps(out,indent=2))
(R/'data/toe_20261108_coupled_holonomy_symmetry.json').write_text(json.dumps(out,indent=2)+'\n')
