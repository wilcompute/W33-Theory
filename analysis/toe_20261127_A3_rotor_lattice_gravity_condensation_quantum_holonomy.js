"use strict";
function run(){
const A=(v,m)=>{if(!v)throw Error(m)},arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),mod=(x,p=3)=>(x%p+p)%p,mat=(n,m,f)=>arr(n,i=>arr(m,j=>f(i,j))),tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),mul=(a,b)=>mat(a.length,b[0].length,(i,j)=>dot(a[i],b.map(r=>r[j]))),maxabs=a=>Math.max(...a.flat().map(Math.abs)),I=n=>mat(n,n,(i,j)=>+(i===j)),mv=(a,b)=>a.map(r=>dot(r,b));
function eig(a){a=a.map(r=>r.slice());let n=a.length;for(let sweep=0;sweep<80;sweep++){let mx=0;for(let p=0;p<n;p++)for(let q=p+1;q<n;q++){let b=a[p][q];mx=Math.max(mx,Math.abs(b));if(Math.abs(b)<1e-12)continue;let z=(a[q][q]-a[p][p])/(2*b),t=(z>=0?1:-1)/(Math.abs(z)+Math.hypot(1,z)),c=1/Math.hypot(1,t),s=t*c;a[p][p]-=t*b;a[q][q]+=t*b;a[p][q]=a[q][p]=0;for(let k=0;k<n;k++)if(k!==p&&k!==q){let u=a[k][p],v=a[k][q];a[k][p]=a[p][k]=c*u-s*v;a[k][q]=a[q][k]=s*u+c*v}}if(mx<1e-10)return a.map((r,i)=>r[i]).sort((x,y)=>x-y)}throw Error("eigen convergence")}
function geometry(){
 const add=(a,b)=>[mod(a[0]+b[0]),mod(a[1]+b[1])],mul9=(a,b)=>[mod(a[0]*b[0]-a[1]*b[1]),mod(a[0]*b[1]+a[1]*b[0])],conj=a=>[a[0],mod(-a[1])],elts=arr(9,i=>[i%3,Math.floor(i/3)]),punct=[[0,0],[2,0],[0,2],[2,2]],key=a=>a.join(""),set=new Set(punct.map(key)),perms=[];
 for(let sem of [0,1])for(let a of elts.filter(a=>a.some(Boolean)))for(let b of elts){let v=punct.map(x=>add(mul9(a,sem?conj(x):x),b));if(v.every(x=>set.has(key(x))))perms.push({sem,a,b,perm:v.map(x=>punct.findIndex(p=>key(p)===key(x)))})}
 A(perms.length===8,"D4");let counts={},short=[],V=[[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]],G=mul(tr(V),V);
 for(let x=-5;x<=5;x++)for(let y=-5;y<=5;y++)for(let z=-5;z<=5;z++){let v=mv(V,[x,y,z]),n=dot(v,v);if(n<=20){counts[n]=(counts[n]||0)+1;if(n===2)short.push(v)}}
 A(short.length===12&&counts[4]===6&&counts[6]===24,"A3 shells");
 let alt=[1,-1,-1,1];A(perms.every(p=>p.perm.every((j,i)=>alt[j]===alt[i])||p.perm.every((j,i)=>alt[j]===-alt[i])),"D4 axis");
 const covariance=mat(4,4,(i,j)=>sum(short.map(v=>v[i]*v[j]))/12);A(maxabs(covariance.map((r,i)=>r.map((v,j)=>v-((i===j)?1/2:-1/6))))<1e-14,"isotropy");
 let a=[1,-1,0,0].map(x=>x/Math.sqrt(2)),b=[1,1,-1,-1].map(x=>x/2),m4=[a,b].map(p=>sum(short.map(v=>dot(v,p)**4))/12);A(Math.abs(m4[0]-5/6)<1e-12&&Math.abs(m4[1]-2/3)<1e-12,"fourth moment");
 return {punctures:punct,automorphisms:perms,valuation_matrix:V,gram:G,covolume:2,normalized_shortest:Math.SQRT2/Math.cbrt(2),shells:counts,shortest_vectors:short,covariance,extra_invariant:alt,fourth_moments:m4,scope:"Intrinsic equal-puncture valuation metric, not uniquely imposed by D4 or physical dynamics."}
}
function rotor(){
 let gap=6.768,rows=[];for(let N of [2,4,8,16,32])for(let J of [.01,.05,.1])rows.push({N,J,finite_weyl_gap_lower:gap-6*N*J,local_norm_bound:6*J,explicit_projected_interaction_gap_lower:gap-6*J});
 let slab=[];for(let L of [4,8,16,32])for(let k of [0,.2,.5,1,1.5,Math.PI]){let b=.2+1-Math.cos(k),small,upper=null,lower=null;
 if(b<1){let inv=mat(L,L,(i,j)=>j>=i?b**(L-1-j+i):0);small=b**L/Math.sqrt(eig(mul(tr(inv),inv)).at(-1));upper=b**L/Math.sqrt(sum(arr(L,j=>b**(2*j))));lower=(1-b*b)*b**L;A(small>=lower*(1-1e-9)&&small<=upper*(1+1e-9),"stable singular bounds")}
 else{let T=mat(L,L,(i,j)=>b*+(i===j)-+(j===i+1));small=Math.sqrt(Math.max(0,eig(mul(tr(T),T))[0]));}
 slab.push({L,k,b,smallest_singular:small,edge_energy:Math.hypot(Math.sin(k),small),bulk_min:Math.hypot(Math.sin(k),1-b),lower,upper,opposite_wall_trial_probability:b<1?b**(2*(L-1))/sum(arr(L,j=>b**(2*j))):null})}
 return {gap_lower:gap,rows,slab,scope:"Uniform weak product-phase stability via known theorem for bounded rotor interactions; explicit projector-dressed even hopping alternative; free Wilson slab, not interacting selective mirror gapping."}
}
function gravity(){
 const rt=Math.SQRT2,E=[[[1,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,1]],[[0,1/rt,0],[1/rt,0,0],[0,0,0]],[[0,0,1/rt],[0,0,0],[1/rt,0,0]],[[0,0,0],[0,0,1/rt],[0,1/rt,0]]],t=[1,1,1,0,0,0],T=I(6).map((r,i)=>r.map((x,j)=>x-.5*t[i]*t[j]));let checks=0,res=0,samples=[];
 for(let L of [3,4,7,8,16])for(let a=0;a<L;a++)for(let b=0;b<L;b++)for(let c=0;c<L;c++){if(!(a||b||c))continue;let p=[a,b,c].map(x=>2*Math.sin(Math.PI*(x<=L/2?x:x-L)/L)),p2=dot(p,p),D=tr(E.map(e=>mv(e,p))),Dt=tr(D),u=mv(Dt,p),C=t.map((x,i)=>p2*x-u[i]),V=mat(6,6,(i,j)=>p2*+(i===j)-p2*t[i]*t[j]-2*dot(Dt[i],Dt[j])+t[i]*u[j]+u[i]*t[j]);
 let P=I(3).map((r,i)=>r.map((v,j)=>v-p[i]*p[j]/p2)),TT=mat(6,6,(i,j)=>{let q=mul(mul(P,E[j]),P),d=sum(q.map((r,k)=>r[k]));return sum(E[i].map((r,k)=>dot(r,q[k].map((x,l)=>x-.5*d*P[k][l]))))});
 let e=Math.max(maxabs(mul(V,Dt)),maxabs([mv(D,C)]),maxabs([mv(T,C).map((x,i)=>x+u[i])]),maxabs(mul(V,TT).map((r,i)=>r.map((x,j)=>x-p2*TT[i][j]))),maxabs(mul(TT,TT).map((r,i)=>r.map((x,j)=>x-TT[i][j]))),Math.abs(sum(TT.map((r,i)=>r[i]))-2));res=Math.max(res,e);A(e<1e-10,"constraints");
 checks++;if(b===0&&c===0&&a===1)samples.push({L,omega:Math.sqrt(p2),continuum:2*Math.PI/L,ratio:Math.sqrt(p2)/(2*Math.PI/L)})}
 return {checks,max_residual:res,samples,zero_mode:"homogeneous metric moduli separate",scope:"Staggered derivative Fourier quadratic ADM control, exact first-class linear constraints; no nonlinear closure or derived universal coupling."}
}
function condensation(){
 let vals=arr(729,i=>arr(6,j=>Math.floor(i/3**j)%3)),P=vals.filter(v=>v.find(Boolean)===1),Q=v=>mod(v[0]*v[5]-v[1]*v[4]+v[2]*v[3]),B=(a,b)=>mod(Q(a.map((x,i)=>x+b[i]))-Q(a)-Q(b)),N=P.filter(v=>!Q(v)),classes={};
 let e=(k,t)=>Math.min(...arr(3,j=>2*t*Math.cos(2*Math.PI*(j+k/3)/3)));
 for(let a of [Array(6).fill(0),...P]){let h=N.filter(b=>!B(a,b)).length,positive=h*e(0,1)+(130-h)*e(1,1),negative=h*e(0,-1)+(130-h)*e(1,-1),key=a.some(Boolean)?Q(a)?"nonsingular":"singular":"vacuum";if(!classes[key])classes[key]={count:0,orthogonal_probes:h,positive_hopping_energy:positive,negative_hopping_energy:negative};let z=classes[key];A(z.orthogonal_probes===h,"orbit");z.count++}
 A(classes.nonsingular.positive_hopping_energy<classes.singular.positive_hopping_energy&&classes.singular.negative_hopping_energy>classes.vacuum.negative_hopping_energy,"selector");
 return {probe_count:N.length,classes,frustrated_ring_eigen_min:[0,1,2].map(k=>e(k,1)),unfrustrated_ring_eigen_min:[0,1,2].map(k=>e(k,-1)),selector_gap:classes.singular.positive_hopping_energy-classes.nonsingular.positive_hopping_energy,scope:"Exactly solvable annular topological-charge plus local probe ring Hamiltonian; supplied hopping sign, no bulk condensation."}
}
function holonomy(){
 const zeta=Math.PI**4/90,F=x=>{x=mod(x,1);return 1-30*x*x*(1-x)**2},qs=[1,-2,4],m=[16,10,1],C=(x,d)=>-sum(qs.map((q,i)=>m[i]*F(q*x+d)))/27;
 let rows=[];for(let spin of [0,.5])for(let eta of [1,.1,.01,.001,.0001]){let es=[];for(let K of [16,32]){let coeff=d=>d===0?0:sum(qs.map((q,i)=>{let j=Math.abs(d/q);return Number.isInteger(j)?m[i]*Math.cos(2*Math.PI*j*spin)/(54*zeta*j**4):0}));let H=mat(2*K+1,2*K+1,(i,j)=>i===j?4*Math.PI**2*eta*(i-K)**2:coeff(i-j));es.push(eig(H)[0])}rows.push({spin,eta,ground_upper:es[1],truncation_difference:es[0]-es[1],exact_potential_min:spin===0?-13/27:-7/8})}
 A(rows.every(r=>r.ground_upper>=r.exact_potential_min-1e-7&&r.truncation_difference>=-1e-9),"variational");
 let lip=15*sum(qs.map((q,i)=>Math.abs(q)*m[i]))/27,x=1/3,c=C(x,0),eps=c/(2*lip);A(C(x-eps,0)>c/2&&C(x+eps,0)>c/2,"open positive interval");
 for(let i=0;i<=1200;i++){let x=i/2400,P=-27+2160*x*x-9600*x**3+12960*x**4-(x>=.25?120*(4*x-1)**3:0);A(Math.abs(P-27*C(x,0))<1e-10,"polynomial")}
 A(Math.abs(c-13/27)<1e-12,"exact max");
 return {normalized_by:729,rows,periodic_max:13/27,antiperiodic_max:7/8,lipschitz:lip,positive_interval_radius:eps,scope:"Quantized flat gauge zero mode in supplied one-loop potential, variational Fourier truncation. No full nonperturbative gauge theory or chiral determinant phase."}
}
return {status:"PASS",geometry:geometry(),rotor:rotor(),gravity:gravity(),condensation:condensation(),holonomy:holonomy()}
}
console.log(JSON.stringify(run(),null,2));
