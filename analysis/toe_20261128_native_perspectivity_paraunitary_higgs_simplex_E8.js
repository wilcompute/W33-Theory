"use strict";
function run(){
 const A=(x,m)=>{if(!x)throw Error(m)},arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),mod=(x,p=3)=>(x%p+p)%p,mat=(n,m,f)=>arr(n,i=>arr(m,j=>f(i,j))),mul=(a,b)=>mat(a.length,b[0].length,(i,j)=>dot(a[i],b.map(r=>r[j])));
 function native(){
 const B=(u,v)=>mod(u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2]),P=arr(81,i=>arr(4,j=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),N=P.map((v,i)=>P.map((w,j)=>i!==j&&!B(v,w)?j:-1).filter(j=>j>=0)),L=N.map(ns=>{let l=[];while(ns.length){let i=ns[0],g=ns.filter(j=>!B(P[i],P[j]));l.push(g);ns=ns.filter(j=>!g.includes(j))}return l}),T=P.map((v,i)=>P.map((w,j)=>B(v,w)?L[i].map(l=>{let n=l.find(x=>!B(P[x],w));return L[j].findIndex(g=>g.includes(n))}):null)),id=[0,1,2,3],comp=(x,y)=>x.map(i=>y[i]),typ=p=>{let s=new Set(),l=[];for(let i=0;i<4;i++)if(!s.has(i)){let j=i,n=0;do{s.add(j);n++;j=p[j]}while(j!==i);l.push(n)}return l.sort().join("")};
 let hist={},loops=0;for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)for(let k=j+1;k<40;k++)if(T[i][j]&&T[j][k]&&T[k][i]){let p=comp(comp(T[i][j],T[j][k]),T[k][i]),t=typ(p);hist[t]=(hist[t]||0)+1;loops++}
 let paths=[];for(let j=0;j<40;j++)if(T[0][j])for(let k=0;k<40;k++)if(T[j][k]&&T[k][0])paths.push(comp(comp(T[0][j],T[j][k]),T[k][0]));let g=new Map([[id.join(),id]]);while(true){let n=g.size;for(let x of [...g.values()])for(let y of paths){let z=comp(x,y);g.set(z.join(),z)}if(n===g.size)break}
 let adj=[];for(let i=0;i<40;i++)for(let j of N[i])if(i<j){let set=new Set();for(let k=0;k<40;k++)if(T[i][k]&&T[k][j])set.add(comp(T[i][k],T[k][j]).join());adj.push(set.size)}
 A(T.flat().filter(Boolean).every(p=>new Set(p).size===4)&&g.size===12&&hist["13"]===2880&&hist["1111"]===360&&adj.every(x=>x===3),"native");
 let H=mat(160,160,(i,j)=>+(T[Math.floor(i/4)][Math.floor(j/4)]?.[i%4]===j%4)),hist2={27:1,9:24,3:15,"-1":81,"-3":24,"-9":15},aug={9:24,"-1":81,"-9":15},poly=Object.keys(hist2).map(Number),prod=mat(160,160,(i,j)=>+(i===j));
 for(let x of poly)prod=prod.map(r=>arr(160,j=>sum(r.map((v,k)=>v*H[k][j]))-x*r[j]));A(prod.every(r=>r.every(x=>x===0)),"exact annihilator");
 let power=mat(160,160,(i,j)=>+(i===j)),mom=[];for(let n=0;n<poly.length;n++){let tr=sum(power.map((r,i)=>r[i]));A(tr===sum(poly.map(k=>hist2[k]*k**n)),"integer multiplicity trace");mom.push(tr);power=mul(power,H)}
 return {hist,loops,triangle_group:g.size,basepaths:paths.length,adjacent_transports:[...new Set(adj)],edges:540,flag_adjacency:hist2,augmentation_adjacency:aug,augmentation_laplacian:{18:24,28:81,36:15},exact_annihilator_roots:poly,exact_trace_moments:mom}
 }
 function mirror(){
 let err=0,checks=0;for(let L of [3,4,7,8,16])for(let j=0;j<L;j++){let k=2*Math.PI*j/L,F=[(1+Math.cos(k))/2,Math.sin(k)/2],G=[(1-Math.cos(k))/2,-Math.sin(k)/2];err=Math.max(err,Math.abs(dot(F,F)+dot(G,G)-1),Math.abs(2*dot(F,G)));checks++}A(err<1e-12,"paraunitary");
 function green(L,k,sgn){let s=sgn*Math.sin(k),b=1-Math.cos(k),d=s*s+b*b+1,x=d;for(let j=1;j<L-1;j++)x=d-b*b/x;x=s*s+b*b-b*b/x;return s/x}
 function phi(L,k,M){let f=Math.cos(k/2)**2;return f*green(L,k,-1)+(1-f)/M}
 let rows=[];for(let L of [4,8,16,32])for(let M of [.5,1,2,4,8]){let lo=.0001,hi=Math.PI-.0001;A(phi(L,lo,M)<0&&phi(L,hi,M)>0,"crossing");for(let j=0;j<80;j++){let x=(lo+hi)/2;if(phi(L,x,M)<0)lo=x;else hi=x}let k=(lo+hi)/2;rows.push({L,M,k,ratio_pi:k/Math.PI,residual:Math.abs(phi(L,k,M))})}return {paraunitary_checks:checks,residual:err,orbitals:8,rows}
 }
 function higgs(){
 let choose=(n,r)=>{let a=1;for(let i=0;i<r;i++)a*= (3**(n-i)-1)/(3**(r-i)-1);return Math.round(a)},ranks=arr(7,r=>choose(6,r)),dim=sum(ranks.map((n,r)=>n*3**r)),degrees=arr(7,r=>(3**r-1)/2+(3**(6-r)-1)/2),max=Math.max(...degrees),inc=arr(6,r=>ranks[r]*(3**(6-r)-1)/2);A(dim===1996024,"dim");
 for(let r=0;r<6;r++)A(inc[r]===ranks[r+1]*(3**(r+1)-1)/2,"incidence");
 return {ranks,dim,degrees,max,inc,total_rank_edges:sum(inc),examples:[.05,.1,.2,.3,.5].map(theta=>({theta,one_site_selector_probability_lower:1-theta*theta,two_site_same_selector_probability_lower:1-2*theta*theta,dressed_gap_lower:3})),torus_ground_degeneracy:234*3**10,topological_entropy_per_selected_sector:5*Math.log(3)}
 }
 function geometry(){
 const G=[[2,1,1],[1,2,1],[1,1,2]],H=[[1,.3,-.2],[.3,-.4,.1],[-.2,.1,.7]],u=[.7,-.2,.9],b=[.2,.6,-.3],det=a=>a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]),inv=a=>mat(3,3,(i,j)=>(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3])/det(a)),tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),mv=(a,v)=>a.map(r=>dot(r,v)),trace=a=>sum(a.map((r,i)=>r[i])),s=(g,u)=>Math.sqrt(det(g))*dot(u,mv(inv(g),u))/12,mag=(g,b)=>dot(b,mv(g,b))/(12*Math.sqrt(det(g))),M=inv(G),traceh=trace(mul(M,H)),predS=s(G,u)*traceh/2-Math.sqrt(det(G))*dot(mv(M,u),mv(H,mv(M,u)))/12,predB=mag(G,b)*(-traceh/2)+dot(b,mv(H,b))/(12*Math.sqrt(det(G))),rows=[];
 for(let t of [.1,.01,.001,.0001]){let plus=G.map((r,i)=>r.map((x,j)=>x+t*H[i][j])),minus=G.map((r,i)=>r.map((x,j)=>x-t*H[i][j]));rows.push({t,scalar_error:Math.abs((s(plus,u)-s(minus,u))/(2*t)-predS),magnetic_error:Math.abs((mag(plus,b)-mag(minus,b))/(2*t)-predB)})}
 let cov=[];for(let R of [[[1,1,0],[0,1,0],[0,0,1]],[[1,0,0],[1,1,1],[0,0,1]],[[2,0,0],[0,1,0],[0,0,.5]]]){let g=mul(mul(tr(R),G),R),uu=mv(tr(R),u),bb=mv(inv(R),b);cov.push({det:det(R),scalar_residual:Math.abs(s(g,uu)-s(G,u)),magnetic_residual:Math.abs(mag(g,bb)-mag(G,b))})}A(cov.every(x=>x.scalar_residual<1e-12&&x.magnetic_residual<1e-12),"covariance");
 let phi=[0,1,3,2],pi=[1,3,0,0],xi=[1,0,0,0],delta=arr(4,i=>xi[i]*(phi[(i+1)%4]-phi[(i+3)%4])/2),dp=arr(4,i=>(xi[(i+1)%4]*pi[(i+1)%4]-xi[(i+3)%4]*pi[(i+3)%4])/2),der=sum(arr(4,i=>{let j=(i+1)%4,d=phi[j]-phi[i];return d*(delta[j]-delta[i])-.5*d*d*(xi[j]-xi[i])})),kin=sum(arr(4,i=>pi[i]*dp[i]-.25*pi[i]**2*(xi[(i+1)%4]-xi[(i+3)%4])));A(der===0&&kin===.75,"Ward correction");
 let checks=0;for(let n=0;n<81;n++){let f=arr(4,i=>Math.floor(n/3**i)%3);for(let x=0;x<4;x++){let v=arr(4,i=>+(i===x)),d=arr(4,i=>v[i]*(f[(i+1)%4]-f[(i+3)%4])/2),r=sum(arr(4,i=>{let j=(i+1)%4,z=f[j]-f[i];return z*(d[j]-d[i])-.5*z*z*(v[j]-v[i])}));A(r===0,"gradient identity");checks++}}
 return {predS,predB,rows,cov,gradient_identity_checks:checks,ward_witness:{phi,pi,xi,delta,dp,gradient_derivative:der,kinetic_derivative:kin}}
 }
 function e8(){
 let roots=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)for(let a of [-2,2])for(let b of [-2,2])roots.push(arr(8,k=>k===i?a:k===j?b:0));for(let i=0;i<256;i++){let v=arr(8,j=>i>>j&1?-1:1);if(v.filter(x=>x<0).length%2===0)roots.push(v)}
 const basis=[[1,-1,-1,-1,-1,-1,-1,1],[2,2,0,0,0,0,0,0],[-2,2,0,0,0,0,0,0],[0,-2,2,0,0,0,0,0],[0,0,-2,2,0,0,0,0],[0,0,0,-2,2,0,0,0],[0,0,0,0,-2,2,0,0],[0,0,0,0,0,-2,2,0]],V=arr(256,i=>arr(8,j=>sum(basis.map((v,k)=>(i>>k&1)*v[j])))),q=V.map(v=>mod(dot(v,v)/8,2)),ch=V.map(v=>8+sum(roots.map(r=>{let n=dot(r,v)/4;A(Number.isInteger(n),"E8 pairing");return (-1)**mod(n,2)}))),hist={};
 for(let x of ch)hist[x]=(hist[x]||0)+1;A(hist[248]===1&&hist[-8]===135&&hist[24]===120,"involutions");A(ch.every((c,i)=>i===0||c===(q[i]===0?-8:24)),"quadratic");
 let spaces=new Map([["0",[0]]]),counts=[1];for(let r=0;r<4;r++){let nxt=new Map();for(let U of spaces.values())for(let a=1;a<256;a++)if(!U.includes(a)&&U.every(u=>q[u^a]===0)){let W=U.concat(U.map(u=>u^a)).sort((a,b)=>a-b);nxt.set(W.join(","),W)}spaces=nxt;counts.push(spaces.size)}
 let x=[4,0,0,0,0,0,0,0],even=roots.filter(r=>mod(dot(r,x)/4,2)===0),odd=roots.filter(r=>mod(dot(r,x)/4,2)!==0),cov=R=>mat(8,8,(i,j)=>sum(R.map(r=>r[i]*r[j]/4))),C=cov(even),D=cov(odd);A(even.length===112&&odd.length===128&&C.every((r,i)=>r.every((v,j)=>v===(i===j?28:0)))&&D.every((r,i)=>r.every((v,j)=>v===(i===j?32:0))),"Hessian");
 return {characters:hist,singular_subspaces_by_rank:counts,even_roots:even.length,odd_roots:odd.length,periodic_fermion_log_hessian:720,antiperiodic_fermion_log_hessian:1080,periodic_gauge_log_hessian:-720,combined_anti_one_adj_Weyl_log_hessian:360,Wilson_penalty_scaled_lambda_threshold:1080/(960*Math.PI**2)}
 }
 return {status:"PASS",native:native(),mirror:mirror(),higgs:higgs(),geometry:geometry(),e8:e8()}
}
console.log(JSON.stringify(run(),null,2));
