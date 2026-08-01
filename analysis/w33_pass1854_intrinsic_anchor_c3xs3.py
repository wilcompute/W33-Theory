import sys,json,hashlib,itertools,collections,argparse,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass1841_1845_five_executions as w
S,labels,OP,outer,actions,geo,idx=w.build_signature_action()
W=np.array(json.loads((ROOT/'data'/'w33_pass1841_signature_solution_orbit_frontier.json').read_text())['certified_binary_distinct_orbits'][0]['canonical_support'],dtype=int)
pos={int(x):i for i,x in enumerate(W)}
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 r=[0]*len(p)
 for i,j in enumerate(p):r[j]=i
 return tuple(r)
def order(p):
 e=tuple(range(len(p)));x=e
 for n in range(1,100):
  x=comp(p,x)
  if x==e:return n
 raise ValueError
inner=[]
for p in OP:
 im=[idx[bytes(S[i][p].astype(np.int8))] for i in W]
 if set(im)==set(W):inner.append(tuple(pos[x] for x in im))
outercos=[]
for p in OP:
 im=[int(outer[idx[bytes(S[i][p].astype(np.int8))]]) for i in W]
 if set(im)==set(W):outercos.append(tuple(pos[x] for x in im))
inner=sorted(set(inner));outercos=sorted(set(outercos));assert len(inner)==len(outercos)==9
unused=set(range(9));orbits=[]
while unused:
 a=min(unused);O={p[a] for p in inner};orbits.append(sorted(O));unused-=O
assert orbits==[[0,1,2],[3,4,5],[6,7,8]]
def exp(p):return tuple((p[b]-b)%3 for b in (0,3,6))
E=sorted(exp(p) for p in inner);expected=sorted((a,b,c) for a in range(3) for b in range(3) for c in range(3) if (a-b+c)%3==0);assert E==expected
q=min(p for p in outercos if order(p)==2);qi=inv(q)
conj={exp(p):exp(comp(comp(q,p),qi)) for p in inner};assert all(conj[e]==(e[1],e[0],(-e[2])%3) for e in E)
z=(1,1,0);r=(1,2,1);assert conj[z]==z and conj[r]==tuple((-x)%3 for x in r)
G=set(inner);changed=True
while changed:
 changed=False
 for a in list(G):
  for b in list(G|{q}):
   c=comp(a,b)
   if c not in G:G.add(c);changed=True
   c=comp(b,a)
   if c not in G:G.add(c);changed=True
assert len(G)==18
anchors=(W//16).tolist();octets=geo[-1];A=np.zeros((45,45),dtype=np.int8)
for i in range(45):
 si=set(octets[i][0])|set(octets[i][1])
 for j in range(i+1,45):
  sj=set(octets[j][0])|set(octets[j][1])
  if len(si&sj)==2:A[i,j]=A[j,i]=1
assert np.all(A[np.ix_(anchors,anchors)]==1-np.eye(9,dtype=np.int8))
perms=sorted(set(itertools.permutations((0,2,4))));cyclic=[0,3,4];mods=(W%16).tolist();phase={m:i for i,m in enumerate(cyclic)};phase_rows=[]
for O in orbits[:2]:
 assert all(labels[W[i]]=='T128' for i in O);ps=[phase[mods[i]] for i in O];phase_rows.append(ps)
assert phase_rows==[[0,1,2],[2,0,1]] and all(labels[W[i]]=='T96' for i in orbits[2])
out={'schema':'w33.pass1854.intrinsic_anchor_c3xs3.v1','status':'PASS','canonical_witness_indices':W.tolist(),'anchors':anchors,'anchor_induced_graph':'K9 in the dense octet graph','signature_triangles':{'X_T128':orbits[0],'Y_T128':orbits[1],'Z_T96':orbits[2]},'K444_cell_colorings':{'ordered_cell_values':list(map(list,perms)),'cyclic_T128_indices':cyclic,'X_phases':phase_rows[0],'Y_phases':phase_rows[1],'T96_cell_pattern':[2,2,2]},'inner_rotation_coordinates':{'elements':[list(e) for e in E],'linear_relation':'a-b+c=0 mod 3','group':'C3 x C3'},'outer_involution_on_nine_signatures':list(q),'outer_action_on_rotation_coordinates':'(a,b,c) -> (b,a,-c)','direct_product_decomposition':{'central_C3_generator':list(z),'S3_rotation_generator':list(r),'S3_reflection_generator':list(q),'relations':['z^3=r^3=q^2=1','[z,r]=[z,q]=1','q r q = r^-1'],'group':'C3 x S3'},'extended_element_order_histogram':{str(k):v for k,v in sorted(collections.Counter(order(p) for p in G).items())},'checks':{'anchor_K9':True,'three_signature_triangles':True,'local_K444_cyclic_phases':True,'inner_plane_relation':True,'outer_coordinate_formula':True,'central_plus_dihedral_split':True,'extended_order_18':True},'boundary':'This derives the extended stabilizer intrinsically for the certified 6T128+3T96 orbit. It does not classify stabilizers of other signature-resolution orbits.'}
out['certificate_sha256']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest();ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n';print(text,end='')
if args.output:Path(args.output).write_text(text)
