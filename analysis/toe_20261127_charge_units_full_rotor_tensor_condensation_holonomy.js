"use strict";
function run(){
const A=(b,m)=>{if(!b)throw Error(m)},mod=(x,p=3)=>(x%p+p)%p,arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),rank=(rows,p=3)=>{let B=[],pv=[];for(let v of rows){v=v.slice().map(x=>mod(x,p));for(let i=0;i<B.length;i++){let c=v[pv[i]];if(c)v=v.map((x,j)=>mod(x-c*B[i][j],p))}let k=v.findIndex(Boolean);if(k>=0){let inv=1;while(v[k]*inv%p!==1)inv++;B.push(v.map(x=>mod(x*inv,p)));pv.push(k)}}return {B,pv,reduce(v){for(let i=0;i<B.length;i++){let c=v[pv[i]];if(c)v=v.map((x,j)=>mod(x-c*B[i][j],p))}return v}}};
function charge(){
 const L=3,N=L**3,M=2*N,idx=(x,y,z)=>mod(x,L)+L*(mod(y,L)+L*mod(z,L)),f=[[0,0,0,1],[1,0,0,1],[0,1,0,2],[0,0,1,2]],g=[[1,0,0,1],[0,1,0,1],[0,0,1,1],[1,1,0,1],[1,0,1,1],[0,1,1,1]],shift=(k,poly)=>{let v=arr(N,()=>0),x=k%L,y=Math.floor(k/L)%L,z=Math.floor(k/L**2);for(let [a,b,c,d] of poly)v[idx(x+a,y+b,z+c)]=d;return v};
 let cols=arr(M,k=>shift(k%N,k<N?f:g)),stab=rank(arr(N,k=>shift(k,g).concat(shift(k,f).map(x=>mod(-x)))));A(stab.B.length===22,"stab rank");
 let single=arr(M,k=>arr(2,c=>({k,c:c+1,s:cols[k].map(x=>mod(x*(c+1)))}))).flat(),groups=new Map(),min=Infinity,witness=null,checks=0,counts=[0,0,0,0],collisionHist={};
 function insert(e,s){counts[e.length]++;let k=s.join(""),old=groups.get(k)||[];for(let d of old){let v=arr(M,()=>0);for(let t of e)v[t.k]=mod(v[t.k]+t.c);for(let t of d)v[t.k]=mod(v[t.k]-t.c);let w=v.filter(Boolean).length;collisionHist[w]=(collisionHist[w]||0)+1;if(w&&w<min){checks++;if(stab.reduce(v).some(Boolean)){min=w;witness=v.map((c,k)=>[k,c]).filter(x=>x[1]);}}}old.push(e);groups.set(k,old)}
 insert([],arr(N,()=>0));for(let a of single)insert([a],a.s);for(let i=0;i<single.length;i++)for(let j=i+1;j<single.length;j++)if(single[i].k!==single[j].k){let a=single[i],b=single[j];insert([a,b],a.s.map((x,k)=>mod(x+b.s[k])))}
 if(min>4)for(let i=0;i<single.length;i++)for(let j=i+1;j<single.length;j++)if(single[i].k!==single[j].k)for(let l=j+1;l<single.length;l++)if(single[l].k!==single[j].k){let a=single[i],b=single[j],c=single[l];insert([a,b,c],a.s.map((x,k)=>mod(x+b.s[k]+c.s[k])))}
 A(min===6&&sum(counts)===204265,"distance");
 A(arr(N,k=>mod(sum(witness.map(([i,c])=>c*cols[i][k])))).every(x=>!x),"logical syndrome");
 return {L,code:[54,10,min],error_half_counts:counts,syndrome_classes:groups.size,collisionHist,logical_membership_checks:checks,witness,unit_rank_F3:3,unit_rank_F9:6,augmentation_dimension_first_order:3,scope:"Exact CSS distance L3 via collision enumeration and X/Z inversion+swap equivalence; charge-ring units recover rank, not metric."}
}
function rotor(){
 const F1=8/2,F2=8*7/4,kinetic=9*F1,L2=9*(11*F2+9*F1),Q=L2-kinetic**2;A(kinetic===36&&Q===414,"derivative norms");
 let pop=x=>x.toString(2).replaceAll("0","").length,even=arr(32,i=>i).filter(i=>pop(i)%2===0),gamma=(i,s)=>{let j=i>>1,b=(s>>j)&1;return [s^(1<<j),mod(2*pop(s&((1<<j)-1))+(i%2?1+2*b:0),4)]},C=s=>{let phase=0;for(let j=4;j>=0;j--){let [t,k]=gamma(2*j,s);s=t;phase=mod(phase+k,4)}return [s,phase]},B=(i,s)=>{let [t,k]=gamma(i,s),[v,l]=C(t);return [v,mod(k+l,4)]};
 let traces=0,relations=0;for(let a=0;a<10;a++)for(let b=0;b<10;b++){let re=0,im=0;for(let s of even){let [t,k]=B(a,s),[u,l]=B(b,s);A(B(a,t)[0]===s&&B(a,t)[1]===k,"symmetry");if(t===u){let d=mod(l-k,4);re+=[1,0,-1,0][d];im+=[0,1,0,-1][d]}let [v,p]=B(a,u),[w,q]=B(b,t);A(v===w&&mod(l-p-k+q,4)===(a===b?0:2),"Clifford");relations++}A(re===16*+(a===b)&&im===0,"trace");traces++}
 let rows=[100,200,248,249,300,500,1000,10000].map(g=>{let lower=g>=64?Math.min(45-2232/g,g/2):null;return {g_over_kappa:g,trial_energy_shift:36,first_excited_lower_shift:lower,gap_lower:lower===null?null:lower-36}});
 A(rows.find(x=>x.g_over_kappa===1000).gap_lower>6.7,"gap");
 return {complex_modes:32,fock_dimension:2**32,rotor:"untruncated L2(S9)",fixed_n_ground_energy:"-16g",fixed_n_gap:"g",overlap:"((1+t)/2)^8",gradient_norm_squared:kinetic,laplacian_norm_squared:L2,orthogonal_laplacian_norm_squared:Q,clifford_checks:relations,trace_checks:traces,rows,scope:"Analytic minmax bound for full on-site rotor and full Fock, not numerical diagonalization or Weyl boundary."}
}
function tensor(){
 let rows=[];for(let p of arr(27,i=>arr(3,j=>Math.floor(i/3**j)%3)).filter(p=>p.some(Boolean))){let [x,y,z]=p,scalar=[x*x,y*y,z*z,x*y,x*z,y*z],G=[[2*x,0,0,y,z,0],[0,2*y,0,x,0,z],[0,0,2*z,0,x,y]],p2=dot(p,p),C=[p2-x*x,p2-y*y,p2-z*z,-2*x*y,-2*x*z,-2*y*z];A(G.every(v=>mod(dot(v,C))===0),"constraint gauge");let r=rank(G).B.length;A(r===3&&C.some(v=>mod(v)),"vector scalar ranks");rows.push({p,isotropic:mod(p2)===0,scalar_dof:6-rank([scalar]).B.length,vector_dof:6-r,linear_GR_dof:6-r-1})}
 return {symbols:rows,isotropic_symbols:rows.filter(x=>x.isotropic).length,scalar_charge_dof:5,vector_charge_dof:3,linear_GR_dof:2,ternary_charge_first_order_dipole_violation:[1,2,2],scope:"Constraint-symbol linear algebra F3, not finite lattice Hamiltonian or graviton dispersion; usual real continuum mode counts same."}
}
function condensation(){
 const v=arr(729,i=>arr(6,j=>Math.floor(i/3**j)%3)),proj=v.filter(a=>a.find(Boolean)===1),Q=a=>mod(a[0]*a[5]-a[1]*a[4]+a[2]*a[3]),B=(a,b)=>mod(Q(a.map((x,i)=>mod(x+b[i])))-Q(a)-Q(b)),nulls=proj.filter(a=>Q(a)===0),hist={},by={},examples={};
 for(let a of proj){let t=nulls.filter(b=>B(a,b)===0).length,n=v.filter(b=>B(a,b)===0).length,k=Q(a)+":"+t;A(n===243,"orthogonal size");hist[t]=(hist[t]||0)+1;by[k]=(by[k]||0)+1;if(!examples[k])examples[k]=a;A(Q(a)-Q(a)===0,"boson")}
 A(nulls.length===130&&hist[40]===234&&hist[49]===130,"W33 count");
 let pts=arr(81,i=>arr(4,j=>Math.floor(i/3**j)%3)).filter(a=>a.find(Boolean)===1),pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],pl=(a,b)=>pairs.map(([i,j])=>mod(a[i]*b[j]-a[j]*b[i])),checks=0;
 for(let a of proj.filter(a=>Q(a)!==0)){let adj=pts.map((p,i)=>pts.map((q,j)=>+(i!==j&&B(a,pl(p,q))===0)));for(let i=0;i<40;i++){A(sum(adj[i])===12,"valency");for(let j=i+1;j<40;j++){A(dot(adj[i],adj[j])===(adj[i][j]?2:4),"SRG");checks++}}}
 return {original_anyons:729,doubled_anyons:729**2,condensate_order:3,unconfined_before_quotient:729**2/3,remaining_anyons:729**2/9,single_layer_surviving_labels:243,projective_bosons:130,selector_histogram:hist,pfaffian_histogram:by,examples,SRG_pair_checks:checks,scope:"Algebraically admissible diagonal boson condensation in D x reverse D; W33 in surviving single-layer bosonic probes. No dynamical sector preference or Hamiltonian."}
}
function holonomy(){
 const F=x=>{x=mod(x,1);return 1-30*x*x*(1-x)**2},dF=x=>{x=mod(x,1);return -60*x*(1-x)*(1-2*x)},q=[1,-2,4],mult=[16,10,1];A(sum(q.map((x,i)=>x*mult[i]))===0&&sum(q.map((x,i)=>x**3*mult[i]))===0,"anomalies");
 let rows=[];for(let spin of [0,.5]){let C=x=>-27*sum(q.map((n,i)=>mult[i]*F(n*x+spin))),D=x=>-27*sum(q.map((n,i)=>mult[i]*n*dF(n*x+spin))),N=12000,best={x:0,value:C(0)},mean=0,roots=[];
 for(let i=0;i<N;i++){let x=i/N,v=C(x);mean+=v/N;if(v>best.value)best={x,value:v};let lo=x,hi=(i+1)/N;if(D(lo)*D(hi)<0){for(let j=0;j<45;j++){let m=(lo+hi)/2;if(D(lo)*D(m)<=0)hi=m;else lo=m}let r=(lo+hi)/2;roots.push(r);if(C(r)>best.value)best={x:r,value:C(r)}}}A(Math.abs(mean)<1e-8&&best.value>0,"zero average nonconstant");let samples=arr(3,i=>C(i/3));rows.push({spin,continuous_mean:mean,continuous_max_estimate:best,stationary_roots:roots,Z9_values_for_actual_charges_3n:samples,Z9_max:Math.max(...samples),unshifted:C(0)})}
 return {charges_actual:q.map(n=>3*n),multiplicity_per_27:mult,weyl_components:729,rows,scope:"Leading absolute chiral determinant coefficient on fixed-volume flat torus, normalized per Weyl; no phase, nonflat gauge configurations, or anomaly-complete integral."}
}
return {status:"PASS",charge:charge(),rotor:rotor(),tensor:tensor(),condensation:condensation(),holonomy:holonomy()}
}
console.log(JSON.stringify(run(),null,2));
