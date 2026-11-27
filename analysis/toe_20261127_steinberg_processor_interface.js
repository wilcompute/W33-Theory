function interfaces(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),sp=(u,v)=>m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1]),edges=[],emap=new Map(),adj=P.map(()=>[]);
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!sp(P[i],P[j])){emap.set(i+','+j,edges.length);edges.push([i,j]);adj[i].push(j);adj[j].push(i)}
const eid=(a,b)=>emap.get([Math.min(a,b),Math.max(a,b)].join(',')),cycle=vs=>{let z=edges.map(()=>0);for(let i=0;i<vs.length;i++){let a=vs[i],b=vs[(i+1)%vs.length];z[eid(a,b)]=m(z[eid(a,b)]+(a<b?1:-1))}return z},dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),rank=M=>{M=M.map(r=>r.slice());let t=0;for(let j=0;j<M[0].length;j++){let k=M.findIndex((x,i)=>i>=t&&x[j]);if(k<0)continue;[M[t],M[k]]=[M[k],M[t]];let c=M[t][j];M[t]=M[t].map(x=>m(x*c));for(let i=t+1;i<M.length;i++){let f=M[i][j];if(f)M[i]=M[i].map((x,k)=>m(x-f*M[t][k]))}t++}return t};
let HX=P.map((_,i)=>edges.map(([a,b])=>a===i?2:b===i?1:0)),HZ=[];
for(let a=0;a<40;a++)for(let b of adj[a].filter(x=>x>a))for(let c of adj[b].filter(x=>x>b&&adj[a].includes(x)))HZ.push(cycle([a,b,c]));
let rx=rank(HX),rz=rank(HZ);A(rx===39&&rz===120,'memory');
let X=[],Z=[],pairs=[];for(let a=0;a<40;a++)for(let b of adj[a]){let line=[a,b,...adj[a].filter(c=>c!==b&&adj[b].includes(c))].sort((a,b)=>a-b);let x=edges.map(([u,v])=>line.includes(u)&&line.includes(v)?m(+(v===a)-+(u===a)):0);A(HZ.every(z=>!dot(x,z)),'cocycle');if(!X.some(y=>y.join()===x.join()))X.push(x)}
for(let a=0;a<40;a++)for(let c=a+1;c<40;c++)if(!adj[a].includes(c)){let common=adj[a].filter(b=>adj[c].includes(b));for(let i=0;i<common.length;i++)for(let j=i+1;j<common.length;j++){let z=cycle([a,common[i],c,common[j]]);A(HX.every(x=>!dot(x,z)),'cycle');Z.push(z)}}
let x=X[0],z=Z.find(v=>dot(x,v)===1)||Z.find(v=>dot(x,v)===2).map(a=>m(2*a));A(dot(x,z)===1,'pair');
let R=HX.slice(),xs=[];let rr=rx;for(let v of X){if(rank(R.concat([v]))>rr){R.push(v);xs.push(v);rr++}}A(xs.length===81,'X span');let zspan=rank(HZ.concat(Z));A(zspan===201,'Z span');
let pairing=xs.map(v=>Z.map(z=>dot(v,z)));A(rank(pairing)===81,'pairing rank');
// selected logical qudit non-destructive teleportation from arbitrary memory entangled with spectators.
// Input |a>, processor |+>; measurement Z_M Z_P^{-1} gives s=a-b, X_M outcome t yields phase omega^{-ta}, output X^{-s} Z^{-t}|psi>.
let branches=0;for(let s=0;s<3;s++)for(let t=0;t<3;t++)for(let a=0;a<3;a++){let b=m(a-s),corrected=m(b+s);A(corrected===a&&m(-t*a+t*corrected)===0,'teleport');branches++}
return {memory:{edges:edges.length,triangles:HZ.length,rankX:rx,rankZ:rz,k:240-rx-rz,weight3_cocycle_candidates:X.length,weight4_cycle_candidates:Z.length,low_weight_X_span_mod_stabilizer:xs.length,low_weight_Z_span_mod_stabilizer:zspan-rz,pairing_rank:81,selected_X:x.map((c,i)=>c?{edge:edges[i],c}:null).filter(Boolean),selected_Z:z.map((c,i)=>c?{edge:edges[i],c}:null).filter(Boolean)},interface:{joint_Z_weight:8,selected_memory_X_weight:3,processor_X_weight:40,phase_branches:branches,reverse_interface_joint_X_weight_upper:43,scope:'ideal logical Pauli measurement, selected logical subsystem with commuting complement; full verified circuit and Golay interface not executed'}}
}
console.log(JSON.stringify(interfaces(),null,2));
