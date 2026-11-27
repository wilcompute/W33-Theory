function golayInterfaces(first){
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
let aX=first==="memory"?memX:Q,aZ=first==="memory"?memZ:procZ,as=first==="memory"?ms:ps,na=first==="memory"?240:40,N=na+11,embed=(v,off)=>Array.from({length:N},(_,i)=>v[i-off]||0),X=aX.map(v=>embed(v,0)).concat(gX.map(v=>embed(v,na))),Z=aZ.map(v=>embed(v,0)).concat(gZ.map(v=>embed(v,na))),joint=Array(N).fill(0);as.forEach((v,i)=>joint[v]=first==="memory"?sg[i]:1);gs.forEach(v=>joint[v+na]=m(-gLogical[v]));
let dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0));A(X.every(x=>Z.every(z=>!dot(x,z)))&&X.every(x=>!dot(x,joint)),'CSS');
let select=(rows,support,n)=>{let sorted=rows.slice().sort((a,b)=>a.filter(Boolean).length-b.filter(Boolean).length),out=[];for(let r of sorted){if(echelon(out.concat([r]).map(x=>support.map(i=>x[i]))).R.length>out.length)out.push(r);if(out.length===n)break}A(out.length===n,'rank');return out};
let checks=[...select(aX,as,3).map(v=>({type:"X",v:embed(v,0)})),...select(aZ,as,4).map(v=>({type:"Z",v:embed(v,0)})),...select(gX,gs,4).map(v=>({type:"X",v:embed(v,na)})),...select(gZ,gs,4).map(v=>({type:"Z",v:embed(v,na)}))];
let basisX=echelon(X).R,basisZ=echelon(Z).R,ex=echelon(X),ez=echelon(Z.concat([joint]));
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
let schedule=[];for(let i=0;i<3;i++){schedule.push({type:"Z",v:joint,parity:i});for(let c of checks)schedule.push({...c,parity:-1})}
for(let a of schedule){a.support=a.v.map((x,i)=>x?i:-1).filter(i=>i>=0);a.g=gadget(a.support.length,a.type)}
let map=new Map(),single=0,bad1=0,pairs=0,badPairs=0,num=0,locOffset=0,totalPairs=0,prevFaults=0;
let neg=s=>s.replace(/[12]/g,x=>x==="1"?"2":"1"),plus=(v,w,c)=>{if(c)for(let i=0;i<v.length;i++)v[i]=m(v[i]+c*w[i])};
for(let j=0;j<schedule.length;j++){let a=schedule[j],g=a.g,byLoc={};for(let f of g.faults){num++;byLoc[f.loc]=(byLoc[f.loc]||0)+1;let x=[],z=[];for(let i=0;i<a.support.length;i++){let k=a.support[i],c=a.v[k];if(f.x[i])x.push([k,m(c*f.x[i])]);if(f.z[i])z.push([k,m(c*f.z[i])])}
let syx=Array(basisZ.length).fill(0),syz=Array(basisX.length).fill(0),lx=Array(N).fill(0),lz=Array(N).fill(0);
for(let [i,c] of x){plus(syx,sx[i],c);plus(lx,rx[i],c)}for(let [i,c] of z){plus(syz,sz[i],c);plus(lz,rz[i],c)}
let hist=Array(schedule.length).fill(0);hist[j]=f.r;for(let k=j+1;k<schedule.length;k++){let b=schedule[k];hist[k]=m((b.type==="Z"?x:z).reduce((s,[i,c])=>s+(b.type==="Z"?1:-1)*c*b.v[i],0))}
let p=hist.filter((_,i)=>schedule[i].parity>=0),h=hist.filter((_,i)=>schedule[i].parity<0),sig=h.concat([m(p[1]-p[0]),m(p[2]-p[0])],syx,syz).join(""),logical=[p[0]].concat(lx,lz).join(""),flag=/[12]/.test(f.f)?j+":"+f.f:"",key=flag+"|"+sig,opp=(flag?j+":"+neg(f.f):"")+"|"+neg(sig);
if(!flag&&!/[12]/.test(sig)){single++;if(/[12]/.test(logical))bad1++}
for(let old of map.get(opp)||[]){if(old.loc===locOffset+f.loc)continue;pairs++;if(old.logical!==neg(logical))badPairs++}
let arr=map.get(key)||[];arr.push({loc:locOffset+f.loc,logical});map.set(key,arr)}
let n=g.faults.length;totalPairs+=prevFaults*n+n*(n-1)/2-Object.values(byLoc).reduce((s,x)=>s+x*(x-1)/2,0);prevFaults+=n;locOffset+=g.ops}
let ambiguous=0;for(let a of map.values())if(new Set(a.map(x=>x.logical)).size>1)ambiguous++;
return {first,physical_sites:N,logical_supports:[as,gs],checks:checks.map(a=>({type:a.type,weight:a.v.filter(Boolean).length})),terminal_rank:{X:basisX.length,Z:basisZ.length},gadgets:schedule.length,locations:locOffset,single_faults:num,accepted_single:single,malignant_single:bad1,total_pairs:totalPairs,accepted_pairs:pairs,malignant_pairs:badPairs,ambiguous_signatures:ambiguous,scope:"Actual 15 chosen full-support CSS stabilizers, verified cat circuits with Pauli faults at every listed operation, three parity rounds. Ideal terminal full CSS syndrome; no data idles outside gates or loss. Quotient by full stabilizer spaces plus measured joint Z. No full T roundtrip; Golay logical X and Z share the selected weight-five support."}
}
console.log(JSON.stringify([golayInterfaces('processor'),golayInterfaces('memory')],null,2));
