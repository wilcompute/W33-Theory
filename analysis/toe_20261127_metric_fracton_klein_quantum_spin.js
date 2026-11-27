"use strict";
function run(){
const A=(b,m)=>{if(!b)throw Error(m)},arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),mat=(n,m,f)=>arr(n,i=>arr(m,j=>f(i,j))),mul=(a,b)=>mat(a.length,b[0].length,(i,j)=>sum(a[i].map((x,k)=>x*b[k][j]))),mod=(x,p)=>(x%p+p)%p,eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),tr=a=>sum(a.map((r,i)=>r[i])),hist=a=>{let h={};for(let x of a)h[x]=(h[x]||0)+1;return h},pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
function moduli(){
 let shapes=[{name:"cubic",B:[[1,0,0],[0,1,0],[0,0,1]]},{name:"FCC",B:[[0,1,1],[1,0,1],[1,1,0]].map(r=>r.map(x=>x/Math.cbrt(2)))},{name:"BCC",B:[[-1,1,1],[1,-1,1],[1,1,-1]].map(r=>r.map(x=>x/Math.cbrt(4)))}];
 for(let s of [.8,.6,.4,.25])shapes.push({name:"rectangular_"+s,B:[[s,0,0],[0,1/Math.sqrt(s),0],[0,0,1/Math.sqrt(s)]]});
 let rows=[];for(let {name,B} of shapes){let m=2,vals=[],short=Infinity,twists=Array(8).fill(0),doubleMass=0;for(let N of [12,24,48]){let t=0;for(let i=-N;i<=N;i++)for(let j=-N;j<=N;j++)for(let k=-N;k<=N;k++){if(!(i||j||k))continue;let r=Math.hypot(...arr(3,l=>i*B[0][l]+j*B[1][l]+k*B[2][l]));short=Math.min(short,r);let v=Math.exp(-m*r)*(1+m*r)/(2*Math.PI*r**3);t+=v;if(N===48){for(let a=0;a<8;a++)twists[a]+=(-1)**mod((a&1)*i+((a>>1)&1)*j+((a>>2)&1)*k,2)*v; if(Math.max(Math.abs(i),Math.abs(j),Math.abs(k))<=24)doubleMass+=Math.exp(-2*m*r)*(1+2*m*r)/(2*Math.PI*r**3)} }vals.push(t)}A(vals[2]>=vals[1]-1e-10,"positive winding");let cusp=Math.exp(-m*short)*(1+m*short)/(Math.PI*short**3);A(vals[2]>=cusp-1e-10,"cusp lower");A(Math.abs(sum(twists)/8-doubleMass/8)<1e-9,"spin average identity");rows.push({name,shortest:short,negative_logdet_shape:vals[2],truncation_values:vals,shortest_pair_lower:cusp,twisted_shape_costs:twists,mean_twisted_cost:sum(twists)/8,double_mass_cost_over_8:doubleMass/8})}return rows
}
function fracton(){
 let rows=[];for(let n=1;n<=7;n++){let L=2**n,sy=new Set(),support=new Set(),max=0,steps=0,enc=(x,y,z)=>mod(x,L)+L*(mod(y,L)+L*mod(z,L)),toggle=(s,k)=>{if(s.has(k))s.delete(k);else s.add(k)},apply=(x,y,z)=>{let k=enc(x,y,z);A(!support.has(k),"duplicate");support.add(k);for(let [a,b,c] of [[0,0,0],[1,0,0],[0,1,0],[0,0,1]])toggle(sy,enc(x+a,y+b,z+c));max=Math.max(max,sy.size);steps++};
 function rec(k,x,y,z){if(!k){apply(x,y,z);return}let s=2**(k-1);rec(k-1,x,y,z);rec(k-1,x+s,y,z);rec(k-1,x,y+s,z);rec(k-1,x,y,z+s)}
 rec(n,0,0,0);A(sy.size===0&&steps===4**n&&max<=4+12*n,"fracton construction");let proj=new Set();for(let v of support)toggle(proj,v%L);A(proj.size===L,"nontrivial specialization");
 rows.push({L,physical_qubits:2*L**3,weight:steps,maximum_defects:max,final_defects:sy.size,projection_weight:proj.size,recursive_bound:4+12*n})
 }return rows
}
function representation(){
 let vectors=arr(81,i=>arr(4,j=>Math.floor(i/3**j)%3)),canon=v=>{let f=v.find(x=>x!==0);return f?v.map(x=>mod(x*f,3)).join(""):""},pts=[...new Set(vectors.map(canon).filter(Boolean))].map(x=>x.split("").map(Number)),sym=(a,b)=>mod(a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2],3),N=mat(40,40,(i,j)=>+(sym(pts[i],pts[j])===0)),Adj=N.map((r,i)=>r.map((x,j)=>x-+(i===j))),T=mat(40,40,(i,j)=>4*N[i][j]-1),I=mat(40,40,(i,j)=>+(i===j));
 A(eq(mul(T,T),I.map(r=>r.map(x=>144*x))),"involution");
 A(eq(mul(Adj,Adj),mat(40,40,(i,j)=>8*I[i][j]-2*Adj[i][j]+4)),"SRG");
 const pl=(a,b)=>[[0,1],[2,3],[0,2],[1,3],[0,3],[1,2]].map(([i,j],k)=>mod((a[i]*b[j]-a[j]*b[i])*(k===3?-1:1),3)),lines=new Map();
 for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){let key=canon(pl(pts[i],pts[j]));if(!lines.has(key)){let members=new Set();for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a||b)members.add(canon(pts[i].map((x,k)=>mod(a*x+b*pts[j][k],3))));lines.set(key,{i,j,members})}}
 A(lines.size===130,"Klein count");
 let keys=[...lines.keys()],idx=new Map(pts.map((v,i)=>[v.join(""),i])),bsets=arr(80,i=>new Set(keys.filter(k=>{let l=lines.get(k);return i<40?l.members.has(pts[i].join("")):sym(pts[i-40],pts[l.i])===0&&sym(pts[i-40],pts[l.j])===0})));
 A(bsets.every(s=>s.size===13),"boundaries");let checks=0,perms=[];
 for(let u of pts){let act=v=>v.map((x,k)=>mod(x+sym(v,u)*u[k],3)),perm=pts.map(v=>idx.get(canon(act(v)))),linePerm=new Map(keys.map(k=>{let l=lines.get(k);return [k,canon(pl(act(pts[l.i]),act(pts[l.j])))]}));
 A(new Set(perm).size===40&&new Set(linePerm.values()).size===130,"permutation");
 for(let i=0;i<80;i++){let target=perm[i%40]+(i<40?0:40);A([...bsets[i]].every(k=>bsets[target].has(linePerm.get(k))),"equivariance");checks++}
 perms.push(perm);
 }
 let orbitSizes=[],seen=new Set();for(let i=0;i<1600;i++)if(!seen.has(i)){let queue=[i];seen.add(i);for(let j=0;j<queue.length;j++){let v=queue[j];for(let p of perms){let w=40*p[Math.floor(v/40)]+p[v%40];if(!seen.has(w)){seen.add(w);queue.push(w)}}}orbitSizes.push(queue.length)}
 A(eq(orbitSizes.sort((a,b)=>a-b),[40,480,1080]),"rank3");
 A(tr(T)===120,"trace");
 return {generators:40,lines:130,equivariant_boundary_checks:checks,ordered_pair_orbits:orbitSizes,irreducible_dimensions:[1,15,24],orthogonal_transition_eigenvalues:{"+1":25,"-1":15},trace:tr(T)/12,scope:"Exact Sp4(3) action via projective symplectic polarity and exterior square. Not a Witting ray intertwiner."}
}
function response(){
 let rows=[];for(let type of ["rook","shrikhande"]){let adj=mat(16,16,(i,j)=>{let a=Math.floor(i/4),b=i%4,c=Math.floor(j/4),d=j%4;return +(type==="rook"?i!==j&&(a===c||b===d):["1,0","3,0","0,1","0,3","1,1","3,3"].includes([mod(a-c,4),mod(b-d,4)].join(",")))}),edges=[];for(let i=0;i<16;i++)for(let j=i+1;j<16;j++)if(adj[i][j])edges.push([i,j]);
 let P=mat(16,16,(i,j)=>(adj[i][j]+2*+(i===j)-.5)/4),Q=mat(16,16,(i,j)=>+(i===j)-1/16-P[i][j]);A(eq(mul(P,P),P)&&eq(mul(Q,Q),Q),"spectral projectors");
 const transfer=(P,e,f)=>{let [a,b]=e,[c,d]=f;return P[a][c]-P[a][d]-P[b][c]+P[b][d]},F=mat(48,48,(i,j)=>{let t=[transfer(P,edges[i],edges[j]),transfer(Q,edges[i],edges[j])],w=[Math.sqrt(5),3];return sum(arr(2,a=>sum(arr(2,b=>t[a]*t[b]/(2*w[a]*w[b]*(w[a]+w[b])**2)))))});
 rows.push({type,mass_squared:1,trace:tr(F),trace_square:tr(mul(F,F)),diagonal:F[0][0]})}
 A(Math.abs(rows[0].trace-rows[1].trace)<1e-12&&Math.abs(rows[0].trace_square-rows[1].trace_square)>1e-8,"QFI separation");
 let N=200000,avg=0;for(let i=0;i<N;i++){let z=1-2*(i+.5)/N,p=i*Math.PI*(3-Math.sqrt(5)),r=Math.sqrt(1-z*z);avg+=r**4*Math.cos(p)**2*Math.sin(p)**2/N}A(Math.abs(avg-1/15)<1e-6,"angular average");
 return {rows,TT_angular_average:avg,TT_expected:1/15,scope:"Massive graph harmonic ground state QFI; separate 4D free scalar shear two-particle continuum rho(s) proportional s², not graviton pole."}
}
function spin(){
 let even=arr(32,i=>i).filter(i=>pop(i)%2===0),odd=arr(32,i=>i).filter(i=>pop(i)%2===1),gamma=(i,s)=>{let j=i>>1,b=(s>>j)&1;return [s^(1<<j),mod(2*pop(s&((1<<j)-1))+(i%2?1+2*b:0),4)]},C=s=>{let phase=0;for(let j=4;j>=0;j--){let [t,k]=gamma(2*j,s);s=t;phase=mod(phase+k,4)}return [s,phase]},B=(i,s)=>{let [t,k]=gamma(i,s),[v,l]=C(t);return [v,mod(k+l,4)]};
 let checks=0;for(let i=0;i<10;i++)for(let s of even){let [t,k]=B(i,s);A(even.includes(t)&&eq(B(i,t),[s,k]),"symmetric mass");for(let j=0;j<10;j++){let [a,b]=B(j,s),[u,v]=B(i,a),[c,d]=B(i,s),[w,x]=B(j,c);A(u===w&&mod(b-v-d+x,4)===(i===j?0:2),"Clifford mass");checks++}}
 let charges=even.map(s=>sum(arr(5,i=>((s>>i)&1)*(i<3?-2:3)))),weights=even.map(s=>arr(5,i=>1-2*((s>>i)&1)));let cubic=0;for(let i=0;i<5;i++)for(let j=0;j<5;j++)for(let k=0;k<5;k++)cubic+=Math.abs(sum(weights.map(v=>v[i]*v[j]*v[k])));A(cubic===0&&sum(charges)===0&&sum(charges.map(x=>x**3))===0,"anomaly");
 A(weights.every(v=>!weights.some(w=>v.every((x,i)=>x===-w[i]))),"no singlet bilinear");
 return {even_states:even.length,odd_states:odd.length,charges_in_sixY:hist(charges),mass_matrices:10,exact_clifford_checks:checks,cubic_cartan_residual:cubic,trace_Y6:sum(charges),trace_Y6_cubed:sum(charges.map(x=>x**3)),SU3_cubic:2-1-1,SU3_squared_Y6:2-4+2,SU2_squared_Y6:3-3,SU2_doublets:4,mass_target:"S9",scope:"Fixed real vector mass full rank, Spin(10) covariant Clifford construction; no proof fluctuating vector creates symmetric gapped phase or QCA."}
}
return {status:"PASS",moduli:moduli(),fracton:fracton(),representation:representation(),quantum_response:response(),spin10:spin()}
}
console.log(JSON.stringify(run(),null,2));
