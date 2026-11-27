function interfaceFaults(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),sp=(u,v)=>m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1]),E=[],emap=new Map(),adj=P.map(()=>[]);
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!sp(P[i],P[j])){emap.set(i+','+j,E.length);E.push([i,j]);adj[i].push(j);adj[j].push(i)}
const e=(a,b)=>emap.get([Math.min(a,b),Math.max(a,b)].join(',')),rank=M=>{M=M.map(r=>r.slice());let t=0;for(let j=0;j<M[0].length;j++){let k=M.findIndex((x,i)=>i>=t&&x[j]);if(k<0)continue;[M[t],M[k]]=[M[k],M[t]];M[t]=M[t].map(x=>m(x*M[t][j]));for(let i=t+1;i<M.length;i++){let f=M[i][j];M[i]=M[i].map((x,k)=>m(x-f*M[t][k]))}t++}return t};
let memZ=[];for(let a=0;a<40;a++)for(let b of adj[a].filter(x=>x>a))for(let c of adj[b].filter(x=>x>b&&adj[a].includes(x))){let z=E.map(()=>0);z[e(a,b)]=1;z[e(b,c)]=1;z[e(a,c)]=2;memZ.push(z)}
let memX=P.map((_,i)=>E.map(([a,b])=>a===i?2:b===i?1:0)),memSupport=[e(0,1),e(0,13),e(1,4),e(4,13)],ms=[2,1,2,2];
let Q=P[0].flatMap((_,i)=>P[0].slice(i).map((_,j)=>P.map(v=>m(v[i]*v[i+j])))),ps=P.map((v,i)=>v[2]===0&&v[3]===0?i:-1).filter(i=>i>=0);
let R=[P.map(()=>1),...Q],pr=R.map(r=>r.slice()),piv=[],k=0;
for(let j=0;j<40;j++){let t=pr.findIndex((r,i)=>i>=k&&r[j]);if(t<0)continue;[pr[k],pr[t]]=[pr[t],pr[k]];pr[k]=pr[k].map(x=>m(x*pr[k][j]));for(let i=0;i<pr.length;i++)if(i!==k){let f=pr[i][j];pr[i]=pr[i].map((x,l)=>m(x-f*pr[k][l]))}piv.push(j);k++}
let procZ=[];for(let j=0;j<40;j++)if(!piv.includes(j)){let z=P.map(()=>0);z[j]=1;piv.forEach((p,i)=>z[p]=m(-pr[i][j]));procZ.push(z)}
let restriction={memX:rank(memX.map(r=>memSupport.map(i=>r[i]))),memZ:rank(memZ.map(r=>memSupport.map(i=>r[i]))),procX:rank(Q.map(r=>ps.map(i=>r[i]))),procZ:rank(procZ.map(r=>ps.map(i=>r[i])))};
A(Object.values(restriction).join()==="3,4,3,4",'restricted kernels');A(memX.every(r=>!m(memSupport.reduce((s,i,j)=>s+r[i]*ms[j],0)))&&Q.every(r=>!m(ps.reduce((s,i)=>s+r[i],0))),'logical support');
// Work in local sign-normalized data frame: joint Z all +1; zero CSS syndromes iff X=0 and Z constant separately in each block.
let w=8,ops=[],flags=0,N=w+3*(2*w-1);
for(let r=0;r<3;r++){let cat=w+(2*w-1)*r,ver=cat+w;for(let i=0;i<w;i++)ops.push({kind:'prep',q:[cat+i]});ops.push({kind:'F',q:[cat]});for(let i=1;i<w;i++)ops.push({kind:'SUM',q:[cat,cat+i],a:1});for(let i=1;i<w;i++){let v=ver+i-1;ops.push({kind:'prep',q:[v]},{kind:'SUM',q:[cat+i,v],a:1},{kind:'SUM',q:[cat,v],a:2},{kind:'MZ',q:[v],f:flags++})}for(let i=0;i<w;i++)ops.push({kind:'CZ',q:[cat+i,i],a:1});for(let i=0;i<w;i++)ops.push({kind:'MX',q:[cat+i],r})}
let faults=[];
for(let loc=0;loc<ops.length;loc++){let o=ops[loc],k=o.kind.startsWith('M')?1:o.q.length*2;for(let e=1;e<3**k;e++){let er=Array.from({length:k},(_,j)=>Math.floor(e/3**j)%3),X=Array(N).fill(0),Z=X.slice(),F=Array(flags).fill(0),s=[0,0,0];
for(let i=loc;i<ops.length;i++){let a=ops[i],[u,v]=a.q;if(i!==loc||a.kind.startsWith('M')){if(a.kind==='prep'){X[u]=Z[u]=0}else if(a.kind==='F'){[X[u],Z[u]]=[m(-Z[u]),X[u]]}else if(a.kind==='SUM'){X[v]=m(X[v]+a.a*X[u]);Z[u]=m(Z[u]-a.a*Z[v])}else if(a.kind==='CZ'){Z[u]=m(Z[u]+X[v]);Z[v]=m(Z[v]+X[u])}else if(a.kind==='MZ'){F[a.f]=m(X[u]+(i===loc?er[0]:0));X[u]=Z[u]=0}else if(a.kind==='MX'){s[a.r]=m(s[a.r]+Z[u]+(i===loc?er[0]:0));X[u]=Z[u]=0}}
if(i===loc&&!a.kind.startsWith('M'))a.q.forEach((j,t)=>{X[j]=m(X[j]+er[2*t]);Z[j]=m(Z[j]+er[2*t+1])})}
let sig=F.concat([m(s[1]-s[0]),m(s[2]-s[0])],X.slice(0,w),Z.slice(1,4).map(x=>m(x-Z[0])),Z.slice(5,8).map(x=>m(x-Z[4]))),logical=[s[0],m(Z[0]-Z[4])];faults.push({loc,sig:sig.join(''),neg:sig.map(x=>m(-x)).join(''),logical})}}
let map=new Map(),single=0,bad1=0,pairs=0,bad=0,readout=0,data=0,witness=null;
for(let f of faults){if(!/[12]/.test(f.sig)){single++;if(f.logical.some(Boolean))bad1++}for(let g of map.get(f.neg)||[]){if(f.loc===g.loc)continue;pairs++;let l=f.logical.map((x,i)=>m(x+g.logical[i]));if(l.some(Boolean)){bad++;if(l[0])readout++;if(l[1])data++;if(!witness)witness={locations:[g.loc,f.loc],logical:l}}}let a=map.get(f.sig)||[];a.push(f);map.set(f.sig,a)}
A(bad1===0,'single-fault postselected');let totalPairs=faults.length*(faults.length-1)/2;let by={};for(let f of faults)by[f.loc]=(by[f.loc]||0)+1;totalPairs-=Object.values(by).reduce((s,x)=>s+x*(x-1)/2,0);
return {restriction,locations:ops.length,faults:faults.length,accepted_single:single,bad_single:bad1,total_distinct_location_fault_pairs:totalPairs,accepted_pairs:pairs,bad_accepted_pairs:bad,bad_readout:readout,bad_data:data,witness,scope:"Weight-eight memory-to-processor joint Z measurement only, 3 rounds, postselect zero verifier, unanimous readout and ideal final CSS syndrome. Arbitrary true eigenvalue, not full teleportation or noisy final syndrome. Pair counts unweighted over Pauli labels."}
}
console.log(JSON.stringify(interfaceFaults(),null,2));
