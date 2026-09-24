from pathlib import Path
import importlib.util, json
ROOT=Path(__file__).resolve().parents[1]
# load diagonal closure machinery
sp=importlib.util.spec_from_file_location("dw",ROOT/"analysis/w33_diagonal_weld_e8_lie_generation.py");dw=importlib.util.module_from_spec(sp);sp.loader.exec_module(dw)
# load split involution helpers
si=importlib.util.spec_from_file_location("ri",ROOT/"analysis/w33_e8_split_real_form_involution.py");ri=importlib.util.module_from_spec(si);si.loader.exec_module(ri)
compiler,bridge,table=dw.load_inputs(); amps=dw.backgrounds(bridge); vectors=dw.source_generators(compiler,amps)
sc=json.loads((ROOT/"artifacts/e8_structure_constants_w33_discrete.json").read_text())
roots=[tuple(map(int,r)) for r in sc["basis"]["roots"]]; rmap={r:8+i for i,r in enumerate(roots)}
neg={8+i:rmap[tuple(-x for x in r)] for i,r in enumerate(roots)}
# Compact conjugation sigma_c(h)=-h, sigma_c(e_a)=c_a e_-a, c_a=-sign K(a,-a)
c={}
for a in range(8,248):
 k=ri.killing(sc,a,neg[a]); assert k in (-60,60)
 c[a]=-1 if k>0 else 1
assert all(c[a]==c[neg[a]] for a in c)
# Verify full linear phase map underlying anti-linear compact conjugation.
def sigvec(v):
 out={}
 for k,x in v.items():
  if k<8:out[k]=out.get(k,0)-x
  else:out[neg[k]]=out.get(neg[k],0)+c[k]*x
 return {k:v for k,v in out.items() if v}
checked=0
for a in range(247):
 for b in range(a+1,248):
  lhs=sigvec(ri.bracket_vec(sc,{a:1},{b:1}))
  rhs=ri.bracket_vec(sc,sigvec({a:1}),sigvec({b:1}))
  assert lhs==rhs,(a,b,lhs,rhs);checked+=1
print("compact bracket checks",checked)
# involution and Killing negativity certificate
assert all(c[a]*c[neg[a]]==1 for a in c)
# fixed root planes have K=2*c*k=-120; fixed Cartan ih has negative of positive Kh.
print("root_fixed_K_values",sorted({2*c[a]*ri.killing(sc,a,neg[a]) for a in c if a<neg[a]}))
# Build compact partner of structured real grade1 vector.
def compact_partner(v):
 y=[0]*248
 for a,x in enumerate(v):
  if not x: continue
  if a<8:y[a]-=x
  else:y[neg[a]]+=c[a]*x
 return y
for name in ("plus","minus","center","external"):
 x=vectors[(1,name)]; y=compact_partner(x)
 print(name,"partner support",sum(z!=0 for z in y),"grade2",sum(y[i]!=0 for i in compiler["coordinate_maps"]["grade2_source_indices"]))
 for p in (103,109):
  basis,ev=dw.closure((x,y),table,dw.ModularBasis(p),p)
  print(name,"p",p,"dim",len(basis.rows),"grade",dw.grade_counts(sorted(basis.rows),compiler),"depth",max(basis.depths))

# Freeze compactness and exact-generation witnesses.
import sympy as sp
Kcart=sp.Matrix([[ri.killing(sc,i,j) for j in range(8)] for i in range(8)])
cartan_minors=[int(Kcart[:i,:i].det()) for i in range(1,9)]
assert all(x>0 for x in cartan_minors)
root_fixed_values=sorted({2*c[a]*ri.killing(sc,a,neg[a]) for a in c if a<neg[a]})
assert root_fixed_values==[-120]

modular={}
exact={}
for name in ("plus","minus"):
 x=vectors[(1,name)]; y=compact_partner(x)
 modular[name]={}
 for p0 in (103,109):
  b,_=dw.closure((x,y),table,dw.ModularBasis(p0),p0)
  modular[name][str(p0)]={"dimension":len(b.rows),
      "grading":dw.grade_counts(sorted(b.rows),compiler),"depth":max(b.depths)}
  assert len(b.rows)==248
 b,ev=dw.closure((x,y),table,dw.RationalBasis())
 exact[name]={"dimension":len(b.rows),"grading":dw.grade_counts(sorted(b.rows),compiler),
              "depth":max(b.depths),"events":ev}
 assert len(b.rows)==248

out={"schema":"w33.20260923.compact_e8_two_control.v1",
 "status":"PASS_TWO_FIXED_COMPACT_CONTROLS_GENERATE_E8_MINUS248",
 "bracket_automorphism_checks":checked,
 "root_plane_fixed_killing_values":root_fixed_values,
 "split_cartan_killing_principal_minors":cartan_minors,
 "fixed_cartan_killing_principal_minors":[-x if i%2==1 else x for i,x in enumerate(cartan_minors,1)],
 "modular":modular,"exact_Q":exact,
 "controls":"A=x+sigma_c(x), B=i(x-sigma_c(x)); both are fixed by the anti-linear compact conjugation.",
 "proof":"The fixed real form has negative-definite Killing form. The complexification of Lie_R<A,B> contains x and sigma_c(x), whose exact rational closure is E8(C); hence the fixed real algebra has dimension 248 and is the compact real form E8(-248).",
 "boundary":"Finite Chevalley-algebra controllability; no pulse-energy, drift, bandwidth, stability, or laboratory normalization is inferred."}
(ROOT/"data/w33_20260923_compact_e8_two_control.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS_COMPACT_E8_FROZEN",exact)
