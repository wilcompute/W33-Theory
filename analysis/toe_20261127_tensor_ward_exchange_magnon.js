function tensorWard(){
const A=(v,s)=>{if(!v)throw Error(s)},I=[[1,0,0],[0,1,0],[0,0,1]],z=()=>I.map(r=>r.map(()=>0)),add=(a,b,s=1)=>a.map((r,i)=>r.map((x,j)=>x+s*b[i][j])),scale=(a,s)=>a.map(r=>r.map(x=>x*s)),tr=a=>a[0][0]+a[1][1]+a[2][2],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),mv=(a,k)=>a.map(r=>dot(r,k)),mul=(a,b)=>a.map(r=>b[0].map((_,i)=>r.reduce((s,x,j)=>s+x*b[j][i],0))),T=a=>a[0].map((_,i)=>a.map(r=>r[i])),outer=(a,b)=>a.map(x=>b.map(y=>x*y)),norm=a=>Math.max(...a.flat().map(Math.abs)),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],D=p=>add(p,I,-tr(p)/2),R=(h,k)=>dot(k,k)*tr(h)-dot(k,mv(h,k)),B=(h,k)=>{let [x,y,w]=k,K=[[0,-w,y],[w,0,-x],[-y,x,0]];return mul(mul(K,h),T(K))};
let basis=[];for(let i=0;i<3;i++)for(let j=i;j<3;j++){let a=z();a[i][j]=a[j][i]=1;basis.push(a)}
let max=0,checks=0;for(let a=-3;a<=3;a++)for(let b=-3;b<=3;b++)for(let c=-3;c<=3;c++){let k=[a,b,c];if(!dot(k,k))continue;for(let h of basis){max=Math.max(max,Math.abs(R(D(h),k)+dot(k,mv(h,k))),...mv(B(h,k),k).map(Math.abs));checks+=2}for(let q of I){let G=add(outer(k,q),outer(q,k));max=Math.max(max,norm(B(G,k)),Math.abs(R(G,k)));checks+=2}
let v=Math.abs(a)+Math.abs(b)?[b,-a,0]:[1,0,0];v=v.map(x=>x/Math.sqrt(dot(v,v)));let u=cross(k,v);u=u.map(x=>x/Math.sqrt(dot(u,u)));for(let h of [add(outer(v,v),outer(u,u),-1),add(outer(v,u),outer(u,v))]){max=Math.max(max,norm(add(B(h,k),h,dot(k,k))),Math.abs(R(h,k)),...mv(h,k).map(Math.abs));checks+=3}}
A(max<1e-10,'Ward identities');
let dispersion=[];for(let [Akin,Bpot] of [[1,1],[1,4],[.5,3]])for(let p of [.4,.2,.1,.05]){let k=2*Math.sin(p/2),dt=.1,w=Math.sqrt(Akin*Bpot)*k,om=2*Math.asin(dt*w/2)/dt;dispersion.push({Akin,Bpot,p,continuous_time_lattice_frequency:w,split_step_frequency:om,phase_speed:om/p,target_speed:Math.sqrt(Akin*Bpot)})}
return {ward_checks:checks,max_residual:max,dispersion,scope:"Real linearized first-class tensor Hamiltonian, supplied DeWitt kinetic and double-curl bilinear; exact momentum-symbol constraints, not finite ternary microscopic derivation or matched light cone."}
}
function exchangeMagnon(){
let P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},G=P.map((v,i)=>P.map((w,j)=>+(i!==j&&!m(v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1]))));
for(let i=0;i<40;i++)for(let j=0;j<40;j++){let v=G[i].reduce((s,x,k)=>s+x*G[k][j],0);A(v===(i===j?12:G[i][j]?2:4),'SRG')}
let rows=[8,16,32,64,128].map(n=>({n,k:2*Math.PI/n,one_magnon_gap:2-2*Math.cos(2*Math.PI/n),ratio_gap_to_k2:(2-2*Math.cos(2*Math.PI/n))/(2*Math.PI/n)**2}));
return {W33_adjacency:[[12,1],[2,24],[-4,15]],W33_one_magnon:[[0,1],[10,24],[16,15]],chain:rows,scope:"For supplied exchange Hamiltonian J sum(I-S), one differing local state gives graph Laplacian exactly. The shared-tick two-register effective action has positive ferromagnetic J; extending to graph as sum of pair terms is assumed. Magnon z=2, not a relativistic mode."}
}
console.log(JSON.stringify({tensor:tensorWard(),magnon:exchangeMagnon()},null,2));
