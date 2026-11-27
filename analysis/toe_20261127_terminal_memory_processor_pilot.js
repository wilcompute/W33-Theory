function terminalPilot(first){
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
let X=first==="memory"?memX:first==="processor"?Q:gX,Z=first==="memory"?memZ:first==="processor"?procZ:gZ,N=X[0].length,joint=null,logicalZ=Array(N).fill(0);
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

let independent=rows=>{let out=[];for(let v of rows.slice().sort((a,b)=>a.filter(Boolean).length-b.filter(Boolean).length)){if(echelon(out.concat([v])).R.length>out.length)out.push(v)}return out};
let terminalX=independent(X),terminalZ=independent(Z),schedule=[];
for(let i=0;i<3;i++){schedule.push({type:"X",v:joint,parity:i});for(let c of checks)schedule.push({...c,parity:-1})}
for(let i=0;i<2;i++){for(let v of terminalX)schedule.push({type:"X",v,parity:-1});for(let v of terminalZ)schedule.push({type:"Z",v,parity:-1})}
let ends=[],loc=0;
for(let a of schedule){a.support=a.v.map((x,i)=>x?i:-1).filter(i=>i>=0);a.g=gadget(a.support.length,a.type);a.byLoc=Array.from({length:a.g.ops},()=>[]);for(let f of a.g.faults)a.byLoc[f.loc].push(f);loc+=a.g.ops+N;ends.push(loc)}
let encode=(x,z)=>x.concat(z).join(""),good=new Set([encode(Array(N).fill(0),Array(N).fill(0))]);
for(let i=0;i<N;i++)for(let k=1;k<9;k++)good.add(encode(rx[i].map(x=>m(x*(k%3))),rz[i].map(x=>m(x*Math.floor(k/3)))));
let seed=first==="memory"?1234:9876,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},decode=l=>{let j=ends.findIndex(e=>e>l),a=schedule[j],k=l-(j?ends[j-1]:0);if(k>=a.g.ops){let p=k-a.g.ops,e=1+Math.floor(8*rng());return {j,after:true,x:e%3?[[p,e%3]]:[],z:e>=3?[[p,Math.floor(e/3)]]:[],flag:"",r:0}}
let f=a.byLoc[k][Math.floor(rng()*a.byLoc[k].length)],x=[],z=[];for(let i=0;i<a.support.length;i++){let p=a.support[i],c=a.v[p];if(f.x[i])x.push([p,m(c*f.x[i])]);if(f.z[i])z.push([p,m(c*f.z[i])])}return {j,after:false,x,z,flag:f.f,r:f.r}};
let plus=(v,w,c)=>{for(let i=0;i<v.length;i++)v[i]=m(v[i]+c*w[i])};
function evaluate(F){
let flags=new Map();for(let f of F){let v=flags.get(f.j)||Array(f.flag.length).fill(0);if(f.flag.length){for(let i=0;i<f.flag.length;i++)v[i]=m(v[i]+ +f.flag[i]);flags.set(f.j,v)}}if([...flags.values()].some(v=>v.some(Boolean)))return null;
let parity=[],bad=0;for(let j=0;j<schedule.length;j++){let a=schedule[j],val=0;for(let f of F){if(f.j===j&&!f.after)val+=f.r;else if(f.j<j)val+=(a.type==="Z"?f.x:f.z).reduce((s,[i,c])=>s+(a.type==="Z"?1:-1)*a.v[i]*c,0)}val=m(val);if(a.parity>=0)parity.push(val);else if(val)return null}
if(parity.some(x=>x!==parity[0]))return null;
let x=Array(N).fill(0),z=Array(N).fill(0);for(let f of F){for(let [i,c] of f.x)x[i]=m(x[i]+c);for(let [i,c] of f.z)z[i]=m(z[i]+c)}
let rawWeight=x.filter((v,i)=>v||z[i]).length,key=encode(residue(x,ex),residue(z,ez));return {parity:parity[0],correctableByWeightOne:good.has(key),rawWeight}
}
let rows=[];for(let k of [1,2]){let accept=0,badParity=0,beyond=0,weights={},witness=null;for(let n=0;n<30000;n++){let l=Math.floor(rng()*loc),F=[decode(l)];if(k===2){let r=Math.floor(rng()*(loc-1));if(r>=l)r++;F.push(decode(r))}let v=evaluate(F);if(v){accept++;badParity+=+(v.parity!==0);beyond+=+!v.correctableByWeightOne;weights[v.rawWeight]=(weights[v.rawWeight]||0)+1;if(!v.correctableByWeightOne&&!witness)witness={F,v}}}rows.push({faults:k,trials:30000,accepted:accept,badParity,beyondWeightOne:beyond,rawWeightCensus:weights,witness})}
return {first,physical_sites:N,actual_gadgets:schedule.length,locations:loc,idles:schedule.length*N,terminal_rank:{X:terminalX.length,Z:terminalZ.length},rows,scope:"Sampled independent uniform distinct fault locations and uniform nonidentity label per location, clean input, two full terminal CSS rounds, inter-gadget idles. Acceptance only recorded checks and flags. Weight-one equivalence modulo stabilizers and measured X is conservative diagnostic, not implemented correction or proof of malignant logical error. No within-gadget idles or loss."}
}

console.log(JSON.stringify(['processor','memory'].map(terminalPilot),null,2));
