function noisyInjection(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),sp=(u,v)=>m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1]),E=[],emap=new Map(),adj=P.map(()=>[]);
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!sp(P[i],P[j])){emap.set(i+','+j,E.length);E.push([i,j]);adj[i].push(j);adj[j].push(i)}
let e=(a,b)=>emap.get([Math.min(a,b),Math.max(a,b)].join(',')),memZ=[];for(let a=0;a<40;a++)for(let b of adj[a].filter(x=>x>a))for(let c of adj[b].filter(x=>x>b&&adj[a].includes(x))){let z=E.map(()=>0);z[e(a,b)]=1;z[e(b,c)]=1;z[e(a,c)]=2;memZ.push(z)}
let memX=P.map((_,i)=>E.map(([a,b])=>a===i?2:b===i?1:0)),ms=[e(0,1),e(0,13),e(1,4),e(4,13)],sg=[2,1,2,2],Q=P[0].flatMap((_,i)=>P[0].slice(i).map((_,j)=>P.map(v=>m(v[i]*v[i+j])))),ps=P.map((v,i)=>v[2]===0&&v[3]===0?i:-1).filter(i=>i>=0);
function echelon(M){let R=[],p=[];for(let v of M){let r=v.slice();for(let i=0;i<R.length;i++){let f=r[p[i]];if(f)r=r.map((x,j)=>m(x-f*R[i][j]))}let j=r.findIndex(Boolean);if(j>=0){let f=r[j];R.push(r.map(x=>m(x*f)));p.push(j)}}return {R,p}}
let {R,p}=echelon([P.map(()=>1),...Q]);let procZ=[];for(let j=0;j<40;j++)if(!p.includes(j)){let z=P.map(()=>0);z[j]=1;for(let i=p.length-1;i>=0;i--)z[p[i]]=m(-R[i].reduce((s,x,k)=>s+x*z[k],0));procZ.push(z)}
let leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1;
let C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),words=new Map([['000000000000',Array(12).fill(0)]]);
for(let row of C)for(let v of [...words.values()])for(let t=1;t<=2;t++){let a=v.map((x,i)=>m(x+t*row[i]));words.set(a.join(''),a)}
A(words.size===729,'Golay');let short=[...words.values()].filter(x=>!x[0]).map(v=>v.slice(1)),gX=echelon(short).R,gZ=gX;
let gLogical=[...words.values()].find(x=>x[0]===1&&x.filter(Boolean).length===6).slice(1),gs=gLogical.map((x,i)=>x?i:-1).filter(i=>i>=0);A(gs.length===5&&gX.length===5,'Golay logical');
let dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0));
let first="golay";let X=first==="memory"?memX:first==="processor"?Q:gX,Z=first==="memory"?memZ:first==="processor"?procZ:gZ,N=X[0].length,joint=null,logicalZ=Array(N).fill(0);
if(first==="memory"){
ms.forEach((v,i)=>logicalZ[v]=sg[i]);for(let i=0;i<40&&!joint;i++)for(let j of adj[i]){let line=P.map((v,k)=>k).filter(k=>[0,1,2].some(a=>[0,1,2].some(b=>P[i].every((x,l)=>m(a*x+b*P[j][l])===P[k][l]))));let v=memX[i].map((c,k)=>E[k].every(x=>line.includes(x))?c:0);if(dot(v,logicalZ)&&Z.every(z=>!dot(v,z))){joint=v.map(x=>m(x*dot(v,logicalZ)));break}}
}else if(first==="processor"){
ps.forEach(i=>logicalZ[i]=1);let best=41;for(let c=0;c<3**Q.length;c++){let a=Array.from({length:Q.length},(_,i)=>Math.floor(c/3**i)%3),v=P.map((_,i)=>m(1+Q.reduce((s,r,k)=>s+a[k]*r[i],0))),w=v.filter(Boolean).length;if(w<best){best=w;joint=v}}A(best===13,'processor distance');
}else{logicalZ=gLogical;joint=gLogical.map(x=>m(2*x))}
A(joint&&dot(joint,logicalZ)===1&&Z.every(z=>!dot(z,joint))&&X.every(x=>Z.every(z=>!dot(x,z))),'CSS logical X');
let as=joint.map((v,i)=>v?i:-1).filter(i=>i>=0);
let select=(rows,support,n)=>{let sorted=rows.slice().sort((a,b)=>a.filter(Boolean).length-b.filter(Boolean).length),out=[];for(let r of sorted){if(echelon(out.concat([r]).map(x=>support.map(i=>x[i]))).R.length>out.length)out.push(r);if(out.length===n)break}A(out.length===n,'rank');return out};
let checks=[...select(X,as,echelon(X.map(v=>as.map(i=>v[i]))).R.length).map(v=>({type:"X",v})),...select(Z,as,echelon(Z.map(v=>as.map(i=>v[i]))).R.length).map(v=>({type:"Z",v}))];
let basisX=echelon(X).R,basisZ=echelon(Z).R,ex=echelon(X.concat([joint])),ez=echelon(Z);
function residue(v,b){v=v.slice();for(let i=0;i<b.R.length;i++){let f=v[b.p[i]];if(f)v=v.map((x,j)=>m(x-f*b.R[i][j]))}return v}
let unit=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>+(i===j))),rx=unit.map(v=>residue(v,ex)),rz=unit.map(v=>residue(v,ez)),sx=unit.map((v,i)=>basisZ.map(r=>r[i])),sz=unit.map((v,i)=>basisX.map(r=>r[i]));
// Single-check circuits. Fault propagation includes all cat/verifier/prep/readout gates, and data idles omitted.
let cache=new Map();
function gadget(w,type){let key=w+type;if(cache.has(key))return cache.get(key);let ops=[],n=3*w-1;
for(let i=0;i<w;i++)ops.push({k:"P",q:[w+i]});ops.push({k:"F",q:[w]});for(let i=1;i<w;i++)ops.push({k:"S",q:[w,w+i],a:1});for(let i=1;i<w;i++){let v=2*w+i-1;ops.push({k:"P",q:[v]},{k:"S",q:[w+i,v],a:1},{k:"S",q:[w,v],a:2},{k:"MZ",q:[v],f:i-1})}for(let i=0;i<w;i++)ops.push({k:type==="Z"?"CZ":"S",q:[w+i,i],a:1});for(let i=0;i<w;i++)ops.push({k:"MX",q:[w+i]});
let out=[];for(let loc=0;loc<ops.length;loc++){let o=ops[loc],nvar=o.k.startsWith("M")?1:2*o.q.length;for(let code=1;code<3**nvar;code++){let er=Array.from({length:nvar},(_,i)=>Math.floor(code/3**i)%3),x=Array(n).fill(0),z=x.slice(),f=Array(w-1).fill(0),r=0;
for(let i=loc;i<ops.length;i++){let a=ops[i],[u,v]=a.q;if(i!==loc||a.k.startsWith("M")){if(a.k==="P"){x[u]=z[u]=0}else if(a.k==="F"){[x[u],z[u]]=[m(-z[u]),x[u]]}else if(a.k==="S"){x[v]=m(x[v]+a.a*x[u]);z[u]=m(z[u]-a.a*z[v])}else if(a.k==="CZ"){z[u]=m(z[u]+x[v]);z[v]=m(z[v]+x[u])}else if(a.k==="MZ"){f[a.f]=m(x[u]+(i===loc?er[0]:0));x[u]=z[u]=0}else if(a.k==="MX"){r=m(r+z[u]+(i===loc?er[0]:0));x[u]=z[u]=0}}
if(i===loc&&!a.k.startsWith("M"))a.q.forEach((j,t)=>{x[j]=m(x[j]+er[2*t]);z[j]=m(z[j]+er[2*t+1])})}
out.push({loc,f:f.join(""),r,x:x.slice(0,w),z:z.slice(0,w)})}}
let g={ops:ops.length,faults:out};cache.set(key,g);return g}

let zL=logicalZ,xL=joint,zero=()=>Array(N).fill(0),frame=()=>({x:zero(),z:zero()});
let lookup=new Map();function put(v){let k=basisX.map(r=>dot(r,v)).join("");A(!lookup.has(k),"perfect");lookup.set(k,v)}put(zero());for(let i=0;i<N;i++)for(let a=1;a<3;a++){let v=zero();v[i]=a;put(v);for(let j=i+1;j<N;j++)for(let b=1;b<3;b++){let w=v.slice();w[j]=b;put(w)}}A(lookup.size===243,"lookup");
let cols=[xL,...basisX];for(let v of unit)if(echelon(cols.concat([v])).R.length>cols.length)cols.push(v);A(cols.length===11,"encoder");
let M=unit.map((_,i)=>cols.map(c=>c[i])),ops=[];
for(let i=0;i<N;i++){let j=M.findIndex((r,j)=>j>=i&&r[i]);A(j>=0,"pivot");if(j!==i){[M[i],M[j]]=[M[j],M[i]];ops.push({k:"swap",i,j})}if(M[i][i]===2){M[i]=M[i].map(v=>m(2*v));ops.push({k:"scale",i})}for(let j=0;j<N;j++)if(j!==i&&M[j][i]){let a=m(-M[j][i]);M[j]=M[j].map((v,k)=>m(v+a*M[i][k]));ops.push({k:"sum",i,j,a:m(-a)})}}
ops.reverse();A(M.every((r,i)=>r.every((x,j)=>x===+(i===j))),"identity");
function gate(F,o){let {i,j,a,k}=o;if(k==="swap"){[F.x[i],F.x[j]]=[F.x[j],F.x[i]];[F.z[i],F.z[j]]=[F.z[j],F.z[i]]}else if(k==="scale"){F.x[i]=m(2*F.x[i]);F.z[i]=m(2*F.z[i])}else{F.x[j]=m(F.x[j]+a*F.x[i]);F.z[i]=m(F.z[i]-a*F.z[j])}}
for(let i=0;i<N;i++){let F=frame();F.x[i]=1;ops.forEach(o=>gate(F,o));A(F.x.every((x,j)=>x===cols[i][j]),"encoder column")}
let ck=[...basisX.map(v=>({type:"X",v})),...basisZ.map(v=>({type:"Z",v}))].map(a=>{let support=a.v.map((x,i)=>x?i:-1).filter(i=>i>=0),g=gadget(support.length,a.type),by=Array.from({length:g.ops},()=>[]);for(let f of g.faults)by[f.loc].push(f);return {...a,support,by}});
let seed=5619,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},add=(F,i,x,z)=>{F.x[i]=m(F.x[i]+x);F.z[i]=m(F.z[i]+z)},one=(F,i,p)=>{if(rng()<p){let k=1+Math.floor(rng()*8);add(F,i,k%3,Math.floor(k/3))}},two=(F,i,G,j,p)=>{if(rng()<p){let k=1+Math.floor(rng()*80);add(F,i,k%3,Math.floor(k/3)%3);add(G,j,Math.floor(k/9)%3,Math.floor(k/27))}};
function verify(F,p){for(let round=0;round<2;round++)for(let a of ck){let r=a.type==="Z"?dot(a.v,F.x):m(-dot(a.v,F.z)),flags=Array(a.support.length-1).fill(0);for(let group of a.by)if(rng()<p){let f=group[Math.floor(rng()*group.length)];r=m(r+f.r);for(let i=0;i<flags.length;i++)flags[i]=m(flags[i]+ +f.f[i]);for(let i=0;i<a.support.length;i++){let j=a.support[i],c=a.v[j];add(F,j,c*f.x[i],c*f.z[i])}}if(r||flags.some(Boolean))return false;for(let i=0;i<N;i++)one(F,i,p)}return true}
function decode(v){let r=lookup.get(basisX.map(h=>dot(h,v)).join(""));return v.map((x,i)=>m(x-r[i]))}
let f=a=>m(a)**3,mod9=x=>(x%9+9)%9,correction=c=>{let v=[0,1,2].map(a=>mod9(7*(f(a)-f(a+c)))),r=v.map(x=>mod9(x-v[0])/3),B=m(2*(r[2]-2*r[1])),D=m(r[1]-B);return [B,D]};
let classical=[{v:zero(),c:0},{v:xL,c:1},{v:xL.map(x=>m(2*x)),c:2}];for(let h of basisX)classical=classical.flatMap(({v,c})=>[0,1,2].map(t=>({c,v:v.map((x,i)=>m(x+t*h[i]))})));
function read(v,lost){if(!lost.some(Boolean))return dot(zL,decode(v));let min=N+1,cs=new Set();for(let {v:w,c} of classical){let d=0;for(let i=0;i<N;i++)if(!lost[i]&&v[i]!==w[i])d++;if(d<min){min=d;cs=new Set([c])}else if(d===min)cs.add(c)}return cs.size===1&&2*min+lost.filter(Boolean).length<5?[...cs][0]:null}
function trial(p,loss,force=false){
let F=frame(),G=frame();for(let i=0;i<N;i++)one(G,i,p);if(force)add(G,0,0,1);for(let o of ops){gate(G,o);if(o.k==="scale")one(G,o.i,p);else two(G,o.i,G,o.j,p)}
if(!verify(G,p))return "resource_reject";
for(let i=0;i<N;i++){G.x[i]=m(G.x[i]-F.x[i]);F.z[i]=m(F.z[i]+G.z[i]);two(F,i,G,i,p)}
if(Array.from({length:N},()=>rng()<loss).some(Boolean))return "data_loss_reject";
let c0=Math.floor(rng()*3),v=G.x.slice(),lost=Array.from({length:N},()=>rng()<loss);for(let i=0;i<N;i++)if(rng()<p)v[i]=m(v[i]+1+Math.floor(rng()*2));let shift=read(v,lost);if(shift===null)return "readout_reject";
let c=m(c0+shift);if(!verify(F,p))return "data_check_reject";
let [B,D]=correction(c);for(let i=0;i<N;i++){F.z[i]=m(F.z[i]+4*B*F.x[i]);one(F,i,p)}
let lx=dot(zL,decode(F.x)),lz=dot(xL,decode(F.z)),ph=[0,1,2].map(a=>mod9(7*(f(a+c0)-f(a))+3*(B*a*a+D*a+lz*a)));
return lx||ph.some(x=>x!==ph[0])?"logical_failure":"success"}
A(trial(0,0)==="success","ideal");A(trial(0,0,true)==="logical_failure","bare resource Z");
let rows=[];for(let [p,loss] of [[.0001,0],[.001,0],[.001,.01],[.005,.01]]){let count={};for(let i=0;i<4000;i++){let x=trial(p,loss);count[x]=(count[x]||0)+1}rows.push({p,loss,trials:4000,counts:count})}
return {encoder_gates:ops.length,encoder_gate_census:ops.reduce((s,o)=>(s[o.k]=(s[o.k]||0)+1,s),{}),checks_per_verification:2*ck.length,check_locations_per_verification:2*ck.reduce((s,a)=>s+a.by.length+N,0),rows,forced_bare_magic_Z:"accepted logical failure",scope:"Actual Clifford encoder from bare T^7|+>, independent Pauli faults at preparations and encoder gates; resource postselection with two full noisy verified-cat syndrome rounds and inter-gadget idles. Inverse transversal SUM, magic destructive readout with trit noise and located erasures, data loss rejection, noisy terminal checks and transversal quadratic feedforward. Final logical result evaluated with ideal CSS recovery as diagnostic, not physically executed. Clean encoded input, no initial data errors or within-gadget idles; resource bare non-Clifford fault is undetectable. No projective magic-state factory or complete outer T/CCZ trajectory."}
}

console.log(JSON.stringify(noisyInjection(),null,2));
