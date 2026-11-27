function adjoint2group(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},G=Array.from({length:9},(_,i)=>[i%3,Math.floor(i/3)]),add=(a,b)=>a.map((x,i)=>m(x+b[i])),c=(a,b)=>m(a[0]*b[1]),carry=(a,b)=>a+b>=3?1:0;
let beta=(a,b,d)=>{let v=c(b,d)-c(add(a,b),d)+c(a,add(b,d))-c(a,b);A(v%3===0,'cocycle');return m(v/3)};
let hist=[0,0,0],checks=0;for(let a of G)for(let b of G)for(let d of G){hist[beta(a,b,d)]++;for(let e of G){A(!m(beta(b,d,e)-beta(add(a,b),d,e)+beta(a,add(b,d),e)-beta(a,b,add(d,e))+beta(a,b,d)),'closed');checks++}}
return {finite_restriction_triples:729,postnikov_census:hist,degree4_checks:checks,scope:"Crossed module Z9 -> E6_sc, central image Z3, pi1 E6_ad and pi2 Z3, nontrivial Bockstein of universal lifting obstruction. Restriction along H27/Z3 gives xy' extension and nonzero Bockstein. E8_sc has H^3(BE8;Z3)=0, so no analogous ordinary finite one-form Postnikov extension over E8 alone. 27 does not descend to E6_ad as ordinary local representation; higher charged defects or other symmetry structure needed. No complete spin-bordism calculation."}
}
function matter(){
let rows=[];
function heat(t,d){let x=t/d,s=1,term=1;for(let k=1;k<200;k++){term*=x*x/(4*k*k);s+=term;if(term<s*1e-16)break}return Math.exp(-t+d*Math.log(s))}
for(let d=1;d<=8;d++){let log=m=>{let n=4000,h=100/n,f=t=>t===0?0:Math.exp(-(1+m)*t)*Math.expm1(t+Math.log(heat(t,d)))/t;let s=f(0)+f(100);for(let j=1;j<n;j++)s+=(j%2?4:2)*f(j*h);return Math.log(1+m)-s*h/3};let a=log(.2),b=log(1);rows.push({d,logdet_mass_point2:a,logdet_mass1:b,log_ratio:a-b})}
if(!rows.slice(1).every((r,i)=>r.log_ratio>rows[i].log_ratio))throw Error("monotonicity");
return {rows,scope:"Infinite Euclidean grid normalized Laplacian 1-average cos(k_i). Convex order of iid sample means decreases with rank (leave-one-out Jensen), so expectation of concave log(m+lambda) increases with rank. For eps<delta log((eps+lambda)/(delta+lambda)) is concave too, so fixed-mass determinant ratio favors maximum rank in bulk. Supplied normalized total hopping rate and flat grid; not arbitrary matter or finite-volume dimension measure."}
}
console.log(JSON.stringify({adjoint:adjoint2group(),matter:matter()},null,2));
