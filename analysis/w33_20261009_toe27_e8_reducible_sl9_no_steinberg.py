"""Round27: exhaustive invariant-block dimension theorem for every
REDUCIBLE nine-dimensional complex carrier V in the E8=A8 3-grading.

For any finite group acting reducibly on V9, the induced E8 restriction
on sl(V9)+Lambda3(V9)+Lambda3(V9)^* has no irreducible constituent
of complex dimension 81. No group character tables assumed.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe27_e8_reducible_sl9_no_steinberg.json'
def partitions(n,ceiling=None):
 ceiling=n if ceiling is None else ceiling
 if n==0:
  yield ()
  return
 for i in range(min(n,ceiling),1-1,-1):
  for rest in partitions(n-i,i):yield (i,)+rest
def wedge_blocks(partition):
 out=[]
 def rec(i,used,dim,chosen):
  if i==len(partition):
   if used==3:out.append((chosen,dim))
   return
  for j in range(min(partition[i],3-used)+1):
   rec(i+1,used+j,dim*math.comb(partition[i],j),chosen+(j,))
 rec(0,0,1,())
 return out
def run():
 allparts=[x for x in partitions(9) if len(x)>1]
 result=[]
 for pp in allparts:
  blocks=wedge_blocks(pp)
  assert sum(dim for _,dim in blocks)==84
  end=[pp[i]*pp[j] for i in range(len(pp)) for j in range(len(pp))]
  assert sum(end)==81
  # The identity matrix is G-invariant; sl9 excludes one singlet.
  # End summands under splitting invariant, and the trace-free
  # sl9 part is a direct sum of traceless diagonal sectors plus
  # offdiagonal Homs and trivial diagonal scalar space.
  slblocks=[x*x-1 for x in pp if x>=2]
  slblocks+=[pp[i]*pp[j] for i in range(len(pp)) for j in range(len(pp)) if i!=j]
  slblocks += [len(pp)-1]
  assert sum(slblocks)==80
  wedge_dims=[dim for _,dim in blocks]
  max_dim=max(slblocks+wedge_dims)
  assert max_dim<81,(pp,max_dim)
  result.append(dict(V9_partition=list(pp),sl9_G_invariant_blocks=slblocks,
   wedge3_G_invariant_blocks=wedge_dims,
   max_G_invariant_block_dimension=max_dim))
 assert max(a['max_G_invariant_block_dimension'] for a in result)==63 # sl8 traceless
 print('E8 reducible V9 partitions',len(result),'max block',
       max(a['max_G_invariant_block_dimension'] for a in result),flush=True)
 rec=dict(status='PASS',E8_adjoint_dimension=248,SL9_carrier_dim=9,
  total_reducible_nine_partitions=len(result),
  maximum_invariant_block_dim_over_ALL_reducible_carriers=63,
  Steinberg81_multiplicity_for_any_reducible_9D_carrier=0,
  theorem='Let G be ANY finite group, and let V9 be any reducible complex 9D G-representation giving a homomorphism into SL9(C). Under the standard E8 subgroup SL9/Z3, the adjoint e8=sl9+Lambda3(V9)+Lambda3(V9)* decomposes into explicit G-invariant blocks of dimension at most63. By complete reducibility, no irreducible G-module of dimension81 can occur inside the restricted e8 adjoint. Thus for the W33 simple G=PSp4(3), the Steinberg81 cannot appear via any reducible 9D carrier in this E8 embedding family.',
  proof='Decompose V9=direct_sum Vi with dimensions a_i>0, at least two parts. sl9 splits as direct sum of Hom(Vi,Vj) for i !=j, sl(Vi) (dims a_i²-1), and a (number_of_parts-1)-dimensional trivial scalar-diagonal space. Lambda3(V9) splits as direct sum over tuples t_i with sum t_i=3 of tensor products Lambda^(t_i)Vi (dims product comb(a_i,t_i)). Their duals have equal dimensions. Enumerating all integer partitions of 9 with >1 part gives maximum block dimension max(8²-1, binom(8,3))=63. All dimensions <81.',
  unresolved='The theorem does not exclude an irreducible complex 9-dimensional representation of PSp4(3), if one exists; nor embeddings into E8 outside SL9; nor matter 81 arising from symmetry breaking or a different finite group. Checking the actual complex character table is an independent next problem.',
  parent_prior='Round26 only analyzed V9=V6+1+1+1 and found no St81. This proves that obstruction for ALL reducible nine-dimensional SL9 carrier representations, a strictly broader result.',
  cases=result)
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
