# Exact cyclotomic odd-Weil construction and fixed-space census.
# Published representation theory is distinguished from the executed checks.
# Companion: analysis/2026-11-18_Klein_Weil_ADE_and_real_Spin7.md.
z:=E(11);;
gauss:=Sum([0..10],j->z^(j*j));;
if gauss^2<>-11 then Error("Gauss identity"); fi;
js:=[1,3,2,5,4];; signs:=[1,1,-1,1,1];;
weights:=[1,9,4,3,5];;
sm:=List([1..5],i->List([1..5],j->signs[i]*signs[j]*
     (z^(js[i]*js[j])-z^(-js[i]*js[j]))/gauss));;
dm:=DiagonalMat(List(weights,a->z^a));;
one:=IdentityMat(5,Cyclotomics);;
if sm^2<>one or dm^11<>one or TraceMat(sm)<>1 or DeterminantMat(sm)<>1 then
 Error("Weil generators"); fi;
g:=Group(sm,dm);;
if Size(g)<>660 or Size(Centre(g))<>1 then Error("Group closure"); fi;
centralizer_size:=Size(Centralizer(g,sm));;
if centralizer_size<>12 then Error("Involution centralizer"); fi;
pr:=PolynomialRing(Cyclotomics,["x0","x1","x2","x3","x4"]);;
xs:=IndeterminatesOfPolynomialRing(pr);;
f:=Sum([1..5],i->xs[i]^2*xs[(i mod 5)+1]);;
act:=m->List(m,row->Sum([1..5],j->row[j]*xs[j]));;
if Value(f,xs,act(sm))<>f or Value(f,xs,act(dm))<>f then
 Error("Cubic invariance"); fi;
classes:=ConjugacyClasses(g);;
rows:=List(classes,c->rec(order:=Order(Representative(c)),size:=Size(c),
 fixed:=Length(NullspaceMat(TransposedMat(Representative(c)-one)))));;
for rr in rows do
 if rr.order=2 and rr.fixed<>3 then Error("Involution type"); fi;
 if rr.order>2 and rr.fixed>1 then Error("Unexpected noninvolution fixed space"); fi;
od;
plus:=NullspaceMat(TransposedMat(sm-one));;
minus:=NullspaceMat(TransposedMat(sm+one));;
if Length(plus)<>3 or Length(minus)<>2 then Error("Eigenspaces"); fi;
fp:=Value(f,xs,List([1..5],i->Sum([1..3],j->xs[j]*plus[j][i])));;
fm:=Value(f,xs,List([1..5],i->Sum([1..2],j->xs[j]*minus[j][i])));;
if fp=Zero(pr) or fm<>Zero(pr) then Error("Fixed cubic restrictions"); fi;
v4:=SylowSubgroup(g,2);;
if Size(v4)<>4 or not IsElementaryAbelian(v4) then Error("Sylow type"); fi;
vg:=GeneratorsOfGroup(v4);;
joint:=NullspaceMat(TransposedMat(Concatenation(vg[1]-one,vg[2]-one)));;
if Length(joint)<>2 then Error("V4 fixed space"); fi;
# Interpolate f(joint[1]+t joint[2]) exactly and test projective discriminant.
ts:=[0,1,-1,2];;
vand:=List(ts,t->List([0..3],j->t^j));;
values:=List(ts,t->Value(f,xs,joint[1]+t*joint[2]));;
coeff:=values*TransposedMat(Inverse(vand));;
d:=coeff[1];;c:=coeff[2];;b:=coeff[3];;a:=coeff[4];;
disc:=b^2*c^2-4*a*c^3-4*b^3*d-27*a^2*d^2+18*a*b*c*d;;
if disc=0 then Error("V4 fixed binary cubic not reduced"); fi;
# Encode the exact generator with integer cyclotomic numerators over11.
sc:=List(sm,row->List(row,u->CoeffsCyc(11*u,11)));;
if not ForAll(Flat(sc),IsInt) then Error("Generator denominator"); fi;
out:="C:/Repos/Theory of Everything/data/toe_20261118_klein_odd_Weil_fixed_strata.json";;
PrintTo(out,"{\n  \"status\": \"PASS\",\n  \"group_order\":660,\n",
 "  \"generator_S_cyclotomic_denominator\":11,\n",
 "  \"generator_S_cyclotomic_numerators\":",sc,",\n",
 "  \"D_weights\":",weights,",\n  \"class_census\":[");
for i in [1..Length(rows)] do
 rr:=rows[i];
 AppendTo(out,"{\"order\":",rr.order,",\"class_size\":",rr.size,
   ",\"ambient_fixed_complex_dimension\":",rr.fixed,"}");
 if i<Length(rows) then AppendTo(out,","); fi;
od;
AppendTo(out,"],\n  \"involution_centralizer_order\":12,\n",
 "  \"invariant_cubic\":\"sum_i x_i^2*x_(i+1)\",\n",
 "  \"involution_fixed_plus_dimension\":3,\n",
 "  \"involution_fixed_minus_dimension\":2,\n",
 "  \"plus_cubic_nonzero\":true,\n  \"minus_plane_contained_in_cubic\":true,\n",
 "  \"V4_common_fixed_dimension\":2,\n  \"V4_binary_discriminant_nonzero\":true,\n",
 "  \"scope\":\"Exact arithmetic; interpretation in companion report.\"\n}\n");
Print("PASS odd Weil660, cubic invariant, fixed-space census=",rows,
      "; V4 binary cubic discriminant nonzero\n");
QUIT;
