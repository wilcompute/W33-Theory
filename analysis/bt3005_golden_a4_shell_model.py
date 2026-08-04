from itertools import product
import json
def F(v):
 x,y=v;return (y,x^y)
def add(a,b):return (a[0]^b[0],a[1]^b[1])
def compose(g,h):
 v,k=g;w,l=h;z=w
 for _ in range(k):z=F(z)
 return (add(v,z),(k+l)%3)
A=[(v,k) for v in product(range(2),repeat=2) for k in range(3)];assert len({compose(g,h) for g in A for h in A})==12
orders=[];I=((0,0),0)
for g in A:
 x=I
 for n in range(1,13):
  x=compose(g,x)
  if x==I:orders.append(n);break
assert {n:orders.count(n) for n in set(orders)}=={1:1,2:3,3:8}
V=list(product(range(2),repeat=2));perms=[]
for v,k in A:
 p=[]
 for x in V:
  y=x
  for _ in range(k):y=F(y)
  p.append(V.index(add(v,y)))
 perms.append(tuple(p))
assert len(set(perms))==12
acc=0;bits=[]
for _ in range(233):
 acc+=89;bit=int(acc>=233)
 if bit:acc-=233
 bits.append(bit)
assert sum(bits)==89 and acc==0 and all(not(bits[i] and bits[(i+1)%233]) for i in range(233))
md=max(abs(sum(bits[:n])-n*89/233) for n in range(234))
out={'schema':'w33.pass3005.golden_a4_shell.v1','status':'COMPLETE_EXACT_MODEL_AND_SOURCE_RTL','a4_order':12,'a4_element_order_histogram':{'1':1,'2':3,'3':8},'faithful_v4_permutation_count':12,'fibonacci_mod2_action':'F(x,y)=(y,x+y), order 3','scheduler':{'numerator':89,'denominator':233,'pulses_per_period':89,'period':233,'cyclic_no_adjacent_expensive_slots':True,'maximum_prefix_discrepancy':md},'type_barrier':'shell opcodes have no write path into protected D4 registers; core opcodes require core_authorized','boundary':'89/233 is a finite Christoffel hardware approximant to 1/phi^2, not an infinite irrational aperiodic generator.'}
print(json.dumps(out,indent=2,sort_keys=True))
