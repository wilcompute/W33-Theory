function bridge(){
const m=(x,n=3)=>(x%n+n)%n,A=(v,s)=>{if(!v)throw Error(s)},G=Array.from({length:81},(_,i)=>[i%9,Math.floor(i/9)%3,Math.floor(i/27)]),mul=(a,b)=>[m(a[0]+b[0],9),m(a[1]+b[1]),m(a[2]+b[2]+a[0]*b[1])],eq=(a,b)=>a.join()===b.join(),id=G[0],inv=a=>[-a[0],-a[1],-a[2]+a[0]*a[1]].map((x,i)=>m(x,i===0?9:3)),comm=(a,b)=>mul(mul(mul(a,b),inv(a)),inv(b));
let checks=0,center=G.filter(a=>G.every(b=>eq(mul(a,b),mul(b,a)))),derived=new Set(),order={};for(let a of G){let x=id,k=0;do{x=mul(x,a);k++}while(!eq(x,id));order[k]=(order[k]||0)+1;for(let b of G){derived.add(comm(a,b).join());for(let c of G){A(eq(mul(mul(a,b),c),mul(a,mul(b,c))),'assoc');checks++}}}
A(center.length===9&&derived.size===3,'group');
// 3D monomial rep on basis q: shift by x, phase omega^(z+y*q) with convention W = Z^? use Z^y X^x with negative y.
// Choose phase z-y*(q+x) so X^x Z^(-y') produces +x*y' factor when reordered as Z^-y X^x.
let rep=(a,k,q)=>[m(q+a[0]),m(k*a[0]+3*(a[2]-a[1]*(q+a[0])),9)];
for(let k=0;k<3;k++)for(let a of G)for(let b of G)for(let q=0;q<3;q++){let [j,p]=rep(b,k,q),[l,r]=rep(a,k,j),[u,v]=rep(mul(a,b),k,q);A(l===u&&m(p+r,9)===v,'rep');}
let kernels=[0,1,2].map(k=>G.filter(a=>[0,1,2].every(q=>eq(rep(a,k,q),[q,0]))));
A(kernels[0].length===3&&kernels[1].length===3&&kernels[0].every(a=>!kernels[1].some(b=>eq(a,b))||eq(a,id)),'faithful sum');
let linear=27,nonlinear=6;A(linear+nonlinear*9===81,'degrees');
return {order:81,assoc_checks:checks,center,derived:[...derived],element_order_census:order,projections:{H27_kernel:kernels[0],Z9_kernel:G.filter(g=>!g[0])},representation_kernels:kernels,irreducible_dimensions:{1:linear,3:nonlinear},faithful_direct_sum_dimension:6,scope:"Pullback H27 ×_{Z3} Z9, two independent central factors. Three monomial irreps with positive commutator character verified; conjugates provide other three. Anomaly pulled back from Z9 vanishes by functoriality if representation factors via original common charge. Not dynamical gauging or full mixed anomaly audit."}
}
function postselect(){
let Wg=x=>1+264*x**6+440*x**9+24*x**12,Wb=x=>1+8*x**3+240*x**6+464*x**9+16*x**12,x=-.5,pg=(2/3)**12*Wg(x),pb=(2/3)**12*Wb(x),rows=[];
for(let n=0;n<=20;n++){let p=1/(1+123200/60480*(pb/pg)**n);rows.push({n,posterior_Golay:p,overall_acceptance:(60480*pg**n+123200*pb**n)/183680})}
return {per_trial:{Golay:pg,weight3:pb,likelihood_ratio:pg/pb},rows,scope:"Operational complement-projector postselection: choose uniform tick and accept every site rejecting P_a; probabilities exact via transfer expectation at t=-1. Independent fresh copies of same hidden code needed; not repeat filtering one collapsed state; not a ground-state selector."}
}
console.log(JSON.stringify({bridge:bridge(),filter:postselect()},null,2));
