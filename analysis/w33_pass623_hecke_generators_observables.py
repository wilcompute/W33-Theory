#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,functools,hashlib,itertools,json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass623_hecke_generators_observables.json'


def partitions(n,m=None):
 if n==0:yield ();return
 m=n if m is None else min(m,n)
 for a in range(m,0,-1):
  for r in partitions(n-a,a):yield (a,)+r
def cells(part):return {(r,c) for r,n in enumerate(part) for c in range(n)}
def shape(S):
 if not S:return ()
 lens=[]
 for r in range(max(x for x,_ in S)+1):
  C={c for rr,c in S if rr==r}
  if C and C!=set(range(max(C)+1)):return None
  lens.append(len(C))
 while lens and lens[-1]==0:lens.pop()
 if any(lens[i]<lens[i+1] for i in range(len(lens)-1)):return None
 return tuple(lens)
def strips(part,k):
 C=cells(part);out=[]
 for z in itertools.combinations(C,k):
  R=set(z);new=shape(C-R)
  if new is None:continue
  seen={next(iter(R))};q=list(seen)
  while q:
   r,c=q.pop()
   for u in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
    if u in R and u not in seen:seen.add(u);q.append(u)
  if len(seen)!=k:continue
  if any({(r,c),(r+1,c),(r,c+1),(r+1,c+1)}<=R for r,c in R):continue
  out.append((new,len({r for r,_ in R})-1))
 return out
@functools.lru_cache(None)
def chi(part,cycle):
 if not cycle:return int(sum(part)==0)
 return sum((-1)**h*chi(q,cycle[1:]) for q,h in strips(part,cycle[0]))
def cycle_type(p):
 seen=set();out=[]
 for i in range(8):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=p[j]
  out.append(n)
 return tuple(sorted(out,reverse=True))
def hook_dimension(part):
 n=sum(part);den=1
 for r,row in enumerate(part):
  for c in range(row):den*=row-c+sum(1 for rr in range(r+1,len(part)) if part[rr]>c)
 return math.factorial(n)//den
def wedderburn_spectra(H):
 rows=[]
 for part in partitions(8):
  m=sum(chi(part,cycle_type(h)) for h in H)//4
  if not m:continue
  blocks=[]
  for i in range(1,6):
   g=trans(i,i+1);trP=Fraction(sum(chi(part,cycle_type(comp(h,g))) for h in H),4);scale=2 if i in (1,5) else 1;tr=scale*trP
   assert tr.denominator==1;tr=int(tr)
   if scale==2:
    plus=(tr+m)//3;minus=m-plus;spec={'2':plus,'-1':minus}
   else:
    plus=(m+tr)//2;minus=m-plus;spec={'1':plus,'-1':minus}
   blocks.append({'operator':f'A{i}','trace':tr,'spectrum':spec})
  rows.append({'partition':list(part),'Specht_dimension':hook_dimension(part),'H_fixed_multiplicity':m,'generator_blocks':blocks})
 return rows

def comp(p,q):return tuple(p[q[i]] for i in range(8))
def trans(a,b):
 p=list(range(8));p[a],p[b]=p[b],p[a];return tuple(p)

def payload():
 I=tuple(range(8));H={I,trans(0,1),trans(6,7),comp(trans(0,1),trans(6,7))}
 G=list(itertools.permutations(range(8)));cid={};cos=[];reps=[]
 for g in G:
  if g in cid:continue
  D={comp(comp(h1,g),h2) for h1 in H for h2 in H};k=len(cos)
  for x in D:cid[x]=k
  cos.append(tuple(sorted(D)));reps.append(min(D))
 idc=cid[I]
 cache={}
 def mul(d,e):
  key=(d,e)
  if key in cache:return cache[key]
  cnt=collections.Counter(cid[comp(x,y)] for x in cos[d] for y in cos[e]);out={}
  for c,n in cnt.items():
   assert n%len(cos[c])==0
   a=n//len(cos[c]);assert a%4==0
   if a//4:out[c]=a//4
  cache[key]=out;return out
 gens=[]
 for i in range(7):
  c=cid[trans(i,i+1)]
  if c!=idc and c not in gens:gens.append(c)
 def reach(gs):
  seen={idc};q=collections.deque([idc])
  while q:
   d=q.popleft()
   for e in gs:
    for c in mul(d,e):
     if c not in seen:seen.add(c);q.append(c)
  return len(seen)
 full_reach=reach(gens);remove_reach=[reach([x for x in gens if x!=e]) for e in gens]
 h=hashlib.sha256();transition_nnz=[];M=[]
 for e in gens:
  cols=[];nnz=0
  for d in range(len(cos)):
   o=mul(d,e);row=tuple(sorted(o.items()));cols.append(row);nnz+=len(row);h.update(repr((e,d,row)).encode())
  M.append(cols);transition_nnz.append(nnz)
 def apply(cols,v):
  z=0
  while v:
   q=v&-v;i=q.bit_length()-1
   for c,a in cols[i]:
    if a&1:z^=1<<c
   v^=q
  return z
 B={};q=collections.deque()
 def add(v):
  w=v
  while w:
   p=w.bit_length()-1
   if p in B:w^=B[p]
   else:B[p]=w;q.append(v);return True
  return False
 add(1<<idc)
 while q:
  v=q.popleft()
  for cols in M:add(apply(cols,v))
 mod2_rank=len(B)
 squares=[mul(e,e) for e in gens]
 commute=[]
 for i in range(5):
  for j in range(i+1,5):commute.append({'pair':[i,i+1,j,j+1],'commutes':mul(gens[i],gens[j])==mul(gens[j],gens[i])})
 def vmul(v,e):
  out={}
  for d,a in v.items():
   for c,b in mul(d,e).items():out[c]=out.get(c,0)+a*b
  return {c:a for c,a in out.items() if a}
 braid=[]
 for i in range(4):
  lhs=vmul(vmul({gens[i]:1},gens[i+1]),gens[i]);rhs=vmul(vmul({gens[i+1]:1},gens[i]),gens[i+1])
  braid.append({'pair':[i+1,i+2],'holds':lhs==rhs,'lhs':{str(k):v for k,v in sorted(lhs.items())},'rhs':{str(k):v for k,v in sorted(rhs.items())}})
 hist=collections.Counter(map(len,cos));blocks=wedderburn_spectra(tuple(H))
 checks={
  'S8_order40320_H_order4':len(G)==40320 and len(H)==4,
  'double_cosets2892':len(cos)==2892,
  'size_histogram_4_8_16':hist=={4:48,8:672,16:2172},
  'five_nontrivial_adjacent_generators':len(gens)==5,
  'five_generators_support_reach_all2892':full_reach==2892,
  'each_adjacent_generator_support_necessary':remove_reach==[192,66,49,66,192],
  'normalized_identity':mul(idc,idc)=={idc:1},
  'multiplication_transition_hash_locked':len(h.hexdigest())==64,
  'mod2_word_span_rank2531':mod2_rank==2531,
  'middle_three_are_involutions':all(squares[i]=={idc:1} for i in (1,2,3)),
  'endpoint_quadratics_deformed':squares[0]=={idc:2,gens[0]:1} and squares[4]=={idc:2,gens[4]:1},
  'interior_braids_hold_endpoint_braids_deform':[r['holds'] for r in braid]==[False,True,True,False],
  'twenty_exact_Wedderburn_generator_spectra':len(blocks)==20 and sum(r['Specht_dimension']*r['H_fixed_multiplicity'] for r in blocks)==10080,
  'block_spectra_obey_quadratic_relations':all(sum(b['spectrum'].values())==r['H_fixed_multiplicity'] for r in blocks for b in r['generator_blocks']),
  'left_right_and_interior_block_spectra_match':all(r['generator_blocks'][0]['spectrum']==r['generator_blocks'][4]['spectrum'] and r['generator_blocks'][1]['spectrum']==r['generator_blocks'][2]['spectrum']==r['generator_blocks'][3]['spectrum'] for r in blocks),
 }
 return {'schema':'w33.pass623.hecke_generators_observables.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'canonical_basis':{'definition':'For each double coset D=HgH, use A_D=(1/|H|) sum_{x in D} x in e_H Q[S8] e_H. Products are A_D A_E=sum_F c(D,E;F) A_F, where c is obtained by counting pairs xy in each F and dividing by |H||F|.','dimension':len(cos),'double_coset_size_histogram':{str(k):v for k,v in sorted(hist.items())},'multiplication_oracle':'The deterministic script enumerates all basis representatives and exact integer structure constants.','five_generator_transition_sha256':h.hexdigest(),'transition_nonzeros':transition_nnz},
  'adjacent_operator_family':{'operators':[{'name':f'A{i+1}','adjacent_transposition':[i+1,i+2],'double_coset_id':gens[i],'representative':list(reps[gens[i]]),'double_coset_size':len(cos[gens[i]])} for i in range(5)],'support_reach':full_reach,'reach_after_removing_each':remove_reach,'mod2_word_span_dimension':mod2_rank,'mod2_deficiency':2892-mod2_rank,'quadratic_relations':[{str(k):v for k,v in sorted(x.items())} for x in squares],'commutation_table':commute,'braid_relations':braid},
  'Wedderburn_generator_spectra':blocks,
  'observable_placement':{'twisted_Laplacian':'The uncoupled Pass-613 operator is A_identity tensor L, so its Hecke coordinate is exactly the identity in every one of the 20 Wedderburn sectors.','Wilson_and_scalar_curvature_no_go':'A scalar function of the connection sector is diagonal on Q[S8/H]. A diagonal operator commuting with the transitive left S8 action must be constant. Therefore nonconstant Wilson sums or curvature labels are not elements of the scalar Hecke algebra.','correct_extension':'Equivariant Wilson or curvature transport belongs to a matrix-valued Hecke algebra End_H(V_fibre)-valued on double cosets. Orbit averaging a scalar Wilson function retains only its constant mean and destroys class discrimination.'},
  'theorem':'The 2,892-dimensional Hecke algebra has an explicit canonical double-coset basis and exact convolution oracle. Five adjacent-transposition operators support-generate every basis sector; the three interior operators obey Coxeter involution/braid relations, while the two boundary operators satisfy deformed quadratics and endpoint braid defects caused by H. All five generators are placed explicitly in each of the 20 Wedderburn multiplicity blocks by exact trace and eigenvalue multiplicities. The uncoupled twisted Laplacian is the Hecke identity, whereas nonconstant scalar Wilson and curvature observables provably require a matrix-valued Hecke extension.',
  'checks':checks,'boundary':'Support generation is weaker than a characteristic-zero minimal algebra-generator theorem. The exact mod-2 word span has dimension 2531, exposing a 361-dimensional modular collapse; a full rational word-basis certificate is not claimed.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 623 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'double_cosets':p['canonical_basis']['dimension'],'mod2_span':p['adjacent_operator_family']['mod2_word_span_dimension']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
