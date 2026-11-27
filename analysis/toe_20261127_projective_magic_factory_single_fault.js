function projectiveFactory(){
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
let first="processor";let X=first==="memory"?memX:first==="processor"?Q:gX,Z=first==="memory"?memZ:first==="processor"?procZ:gZ,N=X[0].length,joint=null,logicalZ=Array(N).fill(0);
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

let D=echelon(X.concat([joint])).R,cols=D.slice();for(let v of unit)if(echelon(cols.concat([v])).R.length>cols.length)cols.push(v);A(cols.length===40&&D.length===11,"encoder columns");
let M=unit.map((_,i)=>cols.map(c=>c[i])),ops={sum:0,swap:0,scale:0};for(let i=0;i<N;i++){let j=M.findIndex((r,j)=>j>=i&&r[i]);A(j>=0,"pivot");if(j!==i){[M[i],M[j]]=[M[j],M[i]];ops.swap++}if(M[i][i]===2){M[i]=M[i].map(x=>m(2*x));ops.scale++}for(let j=0;j<N;j++)if(j!==i&&M[j][i]){let a=M[j][i];M[j]=M[j].map((x,k)=>m(x-a*M[i][k]));ops.sum++}}A(M.every((r,i)=>r.every((x,j)=>x===+(i===j))),"encoder elimination");
let schedule=[...D.map(v=>({type:"X",v})),...basisZ.map(v=>({type:"Z",v}))],types=new Map(),locationCount=0;
for(let a of schedule){let w=a.v.filter(Boolean).length,key=a.type+w;locationCount+=gadget(w,a.type).ops;if(types.has(key))continue;let g=gadget(w,a.type),accepted=0,max=0,witness=null;for(let f of g.faults)if(!/[12]/.test(f.f)){accepted++;let wt=Math.min(...[0,1,2].map(t=>f.x.filter((x,i)=>m(x-(a.type==="X"?t:0))||m(f.z[i]-(a.type==="Z"?t:0))).length));if(wt>max){max=wt;witness=f}}types.set(key,{type:a.type,w,locations:g.ops,labels:g.faults.length,flagfree:accepted,max_residual_weight_mod_measured_stabilizer:max,witness});}
A([...types.values()].every(x=>x.max_residual_weight_mod_measured_stabilizer<=1),"single-cat fault");
let pairMap=new Map(),sy=v=>basisX.map(x=>dot(x,v)).join(""),wordSet=new Set(),logicals=new Set();for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)for(let a=1;a<3;a++)for(let b=1;b<3;b++){let v=unit[i].map((x,k)=>m(a*x+b*unit[j][k])),key=sy(v);for(let old of pairMap.get(key)||[]){let u=v.map((x,k)=>m(x-old[k])),w=u.filter(Boolean).length;A(w===4,"pair collisions minimum weight");for(let z of [u,u.map(x=>m(-x))]){let k=z.join("");wordSet.add(k);if(dot(joint,z))logicals.add(k)}}let q=pairMap.get(key)||[];q.push(v);pairMap.set(key,q)}
let counts={},support=new Set();for(let s of logicals){let v=Array.from(s,Number);let ix=v.map((x,i)=>x?i:-1).filter(i=>i>=0);support.add(ix.join(","));A(v.filter(Boolean).every(x=>x===v[ix[0]]),"line coefficients");let r=echelon(ix.map(i=>P[i])).R.length;A(r===2,"line");counts[dot(joint,v)]=(counts[dot(joint,v)]||0)+1}
A(logicals.size===260&&support.size===130,"projective lines");
let transfer=0;for(let a=0;a<3;a++)for(let s=0;s<3;s++)for(let t=0;t<3;t++){let b=m(a-s);A(m(b+s)===a&&m(t*a-t*m(b+s))===0,"teleportation");transfer++}
return {encoder_gate_census:ops,full_plus_state_stabilizers:schedule.length,one_round_cat_locations:locationCount,gadget_types:[...types.values()].map(({witness,...x})=>x),phase_fault_pairs:3120,distinct_weight4_closed_Z:wordSet.size,weight4_logical_Z:logicals.size,logical_supports:support.size,logical_phase_census:counts,transfer_basis_outcomes:transfer,scope:"Projective |+_L> preparation includes logical X in full stabilizer-state verification before transversal T. Exact single-fault argument: encoder fault detected or stabilizer-equivalent with ideal verification; any single fault inside one verified-cat gadget leaves at most one data site modulo measured stabilizer when flags clear. Transversal T preserves support even for non-Pauli conjugation. With ideal final CSS recovery, a single fault in preparation/checks/T layer correctable; full physical verification schedule not simulated, random initial stabilizer outcomes assumed zero for encoded state; no faults in transfer or recovery. Ideal joint Z parity and source X readout transfer checked. Exact minimum-weight logical Z census gives leading 260(p/2)^4 under independent symmetric phase errors and ideal code-space postselection after T. No complete fault-tolerant factory."}
}

console.log(JSON.stringify(projectiveFactory(),null,2));
