function weightedTransfer(){
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

const ns=40,nt=11,n=51,extend=(v,side)=>side===0?v.concat(Array(nt).fill(0)):Array(ns).fill(0).concat(v),tx=gLogical.map(x=>m(2*x)),tz=gLogical,px=joint,pz=logicalZ;
A(dot(tx,tz)===1,"target logical");let parity=pz.concat(tz.map(x=>m(-x))),schedule=[];
for(let i=0;i<3;i++){schedule.push({kind:"P",type:"Z",v:parity,pid:i});if(i<2)for(let [side,zb] of [[0,basisZ],[1,gZ]])for(let v of zb)schedule.push({kind:"C",type:"Z",v:extend(v,side)})}
for(let [side,xb,zb] of [[0,basisX,basisZ],[1,gX,gZ]])for(let [type,rs] of [["X",xb],["Z",zb]])for(let v of rs)schedule.push({kind:"C",type,v:extend(v,side)});
for(let a of schedule){a.support=a.v.map((x,i)=>x?i:-1).filter(i=>i>=0);a.g=gadget(a.support.length,a.type)}

const sy=(rs,v)=>rs.map(r=>dot(r,v)),enc=v=>v.reduce((s,x,i)=>s+x*3**i,0),add=(a,b,len)=>{let z=0;for(let i=0;i<len;i++){z+=m(a%3+b%3)*3**i;a=Math.floor(a/3);b=Math.floor(b/3)}return z};
function leaders(rs,L,n,radius){let map=new Map(),v=Array(n).fill(0);function visit(i,w){let k=enc(sy(rs,v)),c=dot(L,v);A(!map.has(k)||map.get(k)===c,"decoder ambiguity");map.set(k,c);if(w===radius)return;for(let j=i;j<n;j++)for(let t=1;t<3;t++){v[j]=t;visit(j+1,w+1);v[j]=0}}visit(0,0);return map}
let DS=leaders(basisX,px,ns,1),DX=leaders(gZ,tz,nt,2),DZ=leaders(gX,tx,nt,2),global=new Map(),local=[],loc=0,singles={tested:0,accepted:0,malignant:0,weighted_accepted:0};
function inv(s){return s.replace(/([12])(?=;)/g,x=>x==="1"?"2":"1")}
function feature(x,z,rr){let a=x.slice(ns),b=z.slice(ns),c=z.slice(0,ns);return [enc(sy(basisX,c)),enc(sy(gZ,a)),enc(sy(gX,b)),m(dot(tz,a)+rr),m(dot(tx,b)+dot(px,c))]}
function decode(f){let [s,x,z,a,b]=f;if(!DS.has(s)||!DX.has(x)||!DZ.has(z))return -1;return m(a-DX.get(x))+3*m(b-DZ.get(z)-DS.get(s))}
function combine(a,b){return [add(a[0],b[0],basisX.length),add(a[1],b[1],5),add(a[2],b[2],5),m(a[3]+b[3]),m(a[4]+b[4])]}
let weights=[];function put(G,s,f,id){let q=G.get(s);if(!q){q=new Map();G.set(s,q)}let k=f.join(","),v=q.get(k);if(!v){v={f,n:0,w:0,locs:[]};q.set(k,v)}v.n++;v.w+=weights[id];if(v.locs.length<2&&!v.locs.includes(id))v.locs.push(id)}
function record(start,id,x,z,shift=null,flags=""){let rr=Array(3).fill(0),out=[],flagOffset=2+schedule.length+schedule.slice(0,start).reduce((s,a)=>s+a.support.length-1,0);for(let i=0;i<flags.length;i++)if(flags[i]!=="0")out.push((flagOffset+i)+":"+flags[i]+";");
let check=[];for(let i=start;i<schedule.length;i++){let a=schedule[i],v=0;if(i===start&&shift!==null)v=shift;else{let frame=a.type==="Z"?x:z;for(let j of a.support)v+=a.v[j]*frame[j];if(a.type==="X")v=-v}v=m(v);if(a.kind==="P")rr[a.pid]=v;else if(v)check.push((i+2)+":"+v+";")}
let sig=[m(rr[1]-rr[0]),m(rr[2]-rr[0])].map((v,i)=>v?i+":"+v+";":"").join("")+check.join("")+out.join(""),f=feature(x,z,rr[0]);singles.tested++;if(!sig&&decode(f)>=0){singles.accepted++;singles.weighted_accepted+=weights[id];if(decode(f))singles.malignant++}
put(global,sig,f,id);if(!local[id])local[id]=new Map();put(local[id],sig,f,id)}
let zero=()=>Array(n).fill(0),locations=[];
for(let i=0;i<schedule.length;i++){let a=schedule[i],off=loc;for(let j=0;j<a.g.ops;j++)locations.push({kind:"cat",gadget:i,op:j});loc+=a.g.ops;let counts=Array(a.g.ops).fill(0);for(let f of a.g.faults)counts[f.loc]++;for(let j=0;j<counts.length;j++)weights[off+j]=80/counts[j];for(let f of a.g.faults){let x=zero(),z=zero();for(let k=0;k<a.support.length;k++){let j=a.support[k];x[j]=m(a.v[j]*f.x[k]);z[j]=m(a.v[j]*f.z[k])}record(i,off+f.loc,x,z,f.r,f.f)}}
for(let i=0;i<=schedule.length;i++)for(let j=0;j<n;j++){let id=loc++;locations.push({kind:"idle",stage:i,site:j});weights[id]=10;for(let k=1;k<9;k++){let x=zero(),z=zero();x[j]=k%3;z[j]=Math.floor(k/3);record(i,id,x,z)}}
for(let j=0;j<ns;j++){let id=loc++;locations.push({kind:"readout",site:j});weights[id]=40;for(let k=1;k<=2;k++){let z=zero();z[j]=k;record(schedule.length,id,zero(),z)}}
A(singles.malignant===0,"singles");
let witness=null;function pairs(G,save=false){let pass=0,bad=0,measurementPass=0,weightedPass=0,weightedBad=0;for(let [s,q] of G){let p=G.get(inv(s));if(!p)continue;for(let a of q.values())for(let b of p.values()){let count=a.n*b.n;measurementPass+=count;let f=combine(a.f,b.f),d=decode(f);if(d<0)continue;pass+=count;weightedPass+=a.w*b.w;if(d){bad+=count;weightedBad+=a.w*b.w;if(save&&!witness){for(let i of a.locs)for(let j of b.locs)if(i!==j)witness={locations:[locations[i],locations[j]],measurement_signature:s,features:[a.f,b.f],logical:d}}}}}return [measurementPass,pass,bad,weightedPass,weightedBad]}
let g=pairs(global,true),l=[0,0,0,0,0],sumSq=0;for(let q of local){let r=pairs(q);for(let i=0;i<5;i++)l[i]+=r[i];let n=0;for(let a of q.values())for(let b of a.values())n+=b.n;sumSq+=n*n}
let distinct=(singles.tested**2-sumSq)/2,counts=g.map((x,i)=>(x-l[i])/2);A(counts.every(Number.isSafeInteger),"counts");
A(counts[2]===0&&counts[4]===0,"double safe");
let parityG=schedule.filter(a=>a.kind==="P"),w=parityG[0].support.length;for(let a of parityG)for(let shift of [1,2]){let count=a.g.faults.filter(f=>f.r===shift&&!/[12]/.test(f.f)&&f.x.every(x=>!x)&&f.z.every(x=>!x)&&f.loc>=a.g.ops-w).length;A(count===w,"readout witness")}
let choose2=loc*(loc-1)/2,acc1=singles.weighted_accepted/80,acc2=counts[3]/6400,probabilities=[];
for(let p of [1e-7,1e-6,1e-5,5e-5,1e-4,.001]){let q=1-p,b0=q**loc,b1=acc1*p*q**(loc-1),b2=acc2*p*p*q**(loc-2),base=b0+b1+b2,term=loc*(loc-1)*(loc-2)/6*p**3*q**(loc-3),tail=term;for(let k=4;k<=loc;k++){term*=((loc-k+1)/k)*p/q;tail+=term;if(k>loc*p&&term<tail*1e-18)break}let witness=2*w**3*(p/2)**3*q**(loc-3);probabilities.push({p,acceptance_lower:base,acceptance_upper:Math.min(1,base+tail),conditional_failure_lower:witness/Math.min(1,base+tail),conditional_failure_upper:tail/(base+tail),accepted_0_1_2:[b0,b1,b2],unclassified_tail:tail})}
return {singles,locations:loc,parity_readout_weight:w,accepted_single_location_equivalent:acc1,accepted_pair_location_equivalent:acc2,distinct_location_pairs:choose2,malignant_readout_triples:2*w**3,probabilities,measurement_signature_classes:global.size,distinct_location_pair_labels:distinct,measurement_pass_pairs:counts[0],accepted_pairs:counts[1],malignant_pairs:counts[2],witness,decoder:{source_radius:1,target_component_radius:2},scope:"Independent identical location error probability p; conditional uniform nonidentity Pauli/readout labels per location (8,80,2). Integer weight scale80 per label, 6400 per pair. All zero/one/two-fault accepted branches correct; lower acceptance sum exact through weight2, remaining weight>=3 bounded by positive binomial tail. Explicit triple of same-signed parity cat MX readout flips changes common parity, accepted with no other errors, gives cubic lower bound. Conditional failure upper tail/(base+tail) and lower witness/(base+tail). Clean inputs, ideal terminal decoder, no physical loss, no recovery faults; transfer only, not full factory."}}

console.log(JSON.stringify(weightedTransfer(),null,2));
