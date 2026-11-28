function transferAudit(){
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
for(let i=0;i<3;i++)schedule.push({kind:"P",type:"Z",v:parity});
for(let [side,xb,zb] of [[0,basisX,basisZ],[1,gX,gZ]])for(let [type,rs] of [["X",xb],["Z",zb]])for(let v of rs)schedule.push({kind:"C",type,v:extend(v,side)});
for(let a of schedule){a.support=a.v.map((x,i)=>x?i:-1).filter(i=>i>=0);a.g=gadget(a.support.length,a.type)}
function decoder(rs,n){let map=new Map(),sy=v=>rs.map(r=>dot(r,v)).join("");let z=Array(n).fill(0);map.set(sy(z),z);for(let i=0;i<n;i++)for(let c=1;c<=2;c++){let v=z.slice();v[i]=c;let k=sy(v);A(!map.has(k),"unique weight1");map.set(k,v)}return v=>{let u=map.get(sy(v));return u?v.map((x,i)=>m(x-u[i])):null}}
let decS=decoder(basisX,ns),decTX=decoder(gZ,nt),decTZ=decoder(gX,nt);
let census={},example=null;function test(start,loc,x,z,shift=0,flags=false){let count=census[loc]??={tested:0,rejected:0,accepted:0,malignant:0};count.tested++;if(flags){count.rejected++;return}let rr=Array.from({length:Math.min(start,3)},()=>0);
for(let i=start;i<schedule.length;i++){let a=schedule[i],v=0;if(i===start&&loc==="cat")v=shift;else{let frame=a.type==="Z"?x:z;for(let j of a.support)v+=a.v[j]*frame[j];if(a.type==="X")v=-v}v=m(v);if(a.kind==="P")rr.push(v);else if(v){count.rejected++;return}}
if(rr.some(r=>r!==rr[0])){count.rejected++;return}
let s=decS(z.slice(0,ns)),u=decTX(x.slice(ns)),v=decTZ(z.slice(ns));if(!s||!u||!v){count.rejected++;return}
let logical=[m(dot(tz,u)+(rr[0]||0)),m(dot(tx,v)+dot(px,s))];count.accepted++;if(logical.some(Boolean)){count.malignant++;if(!example)example={start,loc,x,z,shift,rr,logical}}}
let zero=()=>Array(n).fill(0);
test(0,"clean",zero(),zero());
for(let i=0;i<schedule.length;i++){let a=schedule[i];for(let f of a.g.faults){let x=zero(),z=zero();for(let k=0;k<a.support.length;k++){let j=a.support[k];x[j]=m(a.v[j]*f.x[k]);z[j]=m(a.v[j]*f.z[k])}test(i,"cat",x,z,f.r,/[12]/.test(f.f))}}
for(let i=0;i<=schedule.length;i++)for(let j=0;j<n;j++)for(let k=1;k<9;k++){let x=zero(),z=zero();x[j]=k%3;z[j]=Math.floor(k/3);test(i,"idle",x,z)}
for(let j=0;j<ns;j++)for(let k=1;k<=2;k++){let z=zero();z[j]=k;test(schedule.length,"source_readout",zero(),z)}
A(Object.values(census).every(x=>!x.malignant),JSON.stringify(example));
function shortenedLogical(rs,L,missing){let rr=rs.map(v=>missing.map(j=>v[j])),aug=rr.map((v,i)=>v.concat(Array.from({length:rs.length},(_,j)=>+(i===j)))),r=echelon(aug);let v=L.slice();for(let i=0;i<r.R.length;i++){let j=r.p[i];if(j>=missing.length)continue;let t=m(-v[missing[j]]);if(t)for(let k=0;k<rs.length;k++)for(let l=0;l<v.length;l++)v[l]=m(v[l]+t*r.R[i][missing.length+k]*rs[k][l])}return missing.every(j=>v[j]===0)?v:null}
let erasures={source:[],target:[]};
for(let [name,N,rs,L,max] of [["source",ns,basisX,px,3],["target",nt,gX,tx,4]])for(let k=1;k<=max;k++){let count=0;function rec(start,missing){if(missing.length===k){A(shortenedLogical(rs,L,missing),"erasure logical");count++;return}for(let i=start;i<N;i++)rec(i+1,missing.concat(i))}rec(0,[]);erasures[name].push({k,count})}
// For source readout, erase one known trit and correct one unknown nonzero trit shift using shortened checks.
let mixed=0;for(let e=0;e<ns;e++){let pivot=basisX.find(v=>v[e]);A(pivot,"pivot");let checks=basisX.filter(v=>v!==pivot).map(v=>v.map((x,i)=>m(x-v[e]*pivot[e]*pivot[i]))),l=shortenedLogical(basisX,px,[e]),map=new Map();for(let j=0;j<ns;j++)if(j!==e)for(let c=1;c<=2;c++){let sy=checks.map(v=>m(c*v[j])).join(""),logical=m(c*l[j]);if(map.has(sy))A(map.get(sy)===logical,"mixed ambiguity");else map.set(sy,logical);A(/[12]/.test(sy)||!logical,"zero syndrome");mixed++}}
let total=Object.values(census).reduce((a,b)=>a+b.tested,0);
return {n,checks:schedule.length,cat_locations:schedule.reduce((s,a)=>s+a.g.ops,0),census,total,erasures,mixed_source_one_erasure_one_flip:mixed,scope:"Exact single-location Pauli signatures for three joint Z_source Z_target^-1 cats, full independent source/target CSS postselection, inter-gadget idles, source MX readout flips. Source initially arbitrary clean logical state, target clean |+_L>; parity label s=a-b and source Fourier label t imply correction X^s Z^t in time order (Z^t X^s operator). Decoder uses ideal target terminal syndromes and source destructive classical syndrome; final correction noiseless. Erasure combinatorics certifies source X-logical readout on up to3 erased positions and target X logical outside up to4 erased positions (target full recovery also needs Z; gX=gZ and logicals proportional). Not noisy encoding or active recovery, combined faults or full factory threshold."}
}

console.log(JSON.stringify(transferAudit(),null,2));
