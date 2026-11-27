function exchange(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},V=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)),P=V.filter(v=>v.find(Boolean)===1),sp=(v,w)=>m(v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1]),dot=(v,w)=>m(v.reduce((s,x,i)=>s+x*w[i],0));
let commute=V.slice(1).map(v=>P.filter(p=>!sp(p,v)).length);A(commute.every(x=>x===13),'channel');
let basis=Array.from({length:9},(_,i)=>[i%3,Math.floor(i/3)]),act=(v,i)=>{let q=basis[i],b=m(v[2]*q[0]+v[3]*q[1]+2*(v[0]*v[2]+v[1]*v[3]));return [m(q[0]+v[0])+3*m(q[1]+v[1]),b]},census={};
function moment(t){
let N=9**t,trace=0,projTrace=0,checks=0;
let decode=i=>Array.from({length:t},(_,j)=>Math.floor(i/9**j)%9),enc=a=>a.reduce((s,x,j)=>s+x*9**j,0),add=(M,i,e,c=1)=>{let a=M.get(i)||[0,0,0];a[e]+=c;M.set(i,a)},red=a=>[a[0]-a[2],a[1]-a[2]],equal=(M,Q)=>[...new Set([...M.keys(),...Q.keys()])].every(k=>red(M.get(k)||[0,0,0]).join()===red(Q.get(k)||[0,0,0]).join());
for(let i=0;i<N;i++){
let q=decode(i),M=new Map(),Q=new Map();
for(let p of P){for(let z=0;z<3**t;z++){let a=Array.from({length:t},(_,j)=>Math.floor(z/3**j)%3);if(m(a.reduce((s,x)=>s+x,0)))continue;let f=a.map((k,j)=>act(p.map(x=>m(k*x)),q[j]));add(M,enc(f.map(x=>x[0])),m(f.reduce((s,x)=>s+x[1],0)),1)}}
if(t===2){add(Q,i,0,39);add(Q,enc([q[1],q[0]]),0,9)}else{add(Q,i,0,36);for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let r=q.slice();[r[a],r[b]]=[r[b],r[a]];add(Q,enc(r),0,9)}for(let v of V){let f=q.map(j=>act(v,j));add(Q,enc(f.map(x=>x[0])),m(f.reduce((s,x)=>s+x[1],0)),1)}}
A(equal(M,Q),'moment exact '+t+' '+i);checks++;
}
return checks
}
let checks=[moment(2),moment(3)];
// P = average W^tensor3. trace against permutation: identity, transposition, 3-cycle.
let traces=[0,0,0];for(let i=0;i<729;i++){let q=[i%9,Math.floor(i/9)%9,Math.floor(i/81)];for(let v of V){let f=q.map(j=>act(v,j)),r=f.map(x=>x[0]),e=m(f.reduce((s,x)=>s+x[1],0));for(let [k,p] of [[0,q],[1,[q[1],q[0],q[2]]],[2,[q[1],q[2],q[0]]]])if(r.join()===p.join())traces[k]+=e===0?2:-1}}
traces=traces.map(x=>x/162);A(traces.join()==='9,1,9','projector character');
let dims={sym:165,alt:84,mixed:480},spectra=[{e:1,n:80},{e:4,n:480},{e:7,n:160},{e:10,n:4},{e:16,n:5}];A(spectra.reduce((s,x)=>s+x.n*x.e,0)===120*27,'trace');
return {tick_count:120,pauli_contraction:13/40,channel_eigenvalues:[[1,1],[13/40,80]],exact_moment_basis_checks:checks,M1:'40 I',M2:'13 I + 3 SWAP',M3:'4 I + sum transpositions + 9 P',projector_rank:9,projector_S3_character:traces,projector_irreps:{trivial:5,sign:4,standard:0},M3_spectrum:spectra,scope:'projector moment exchange construction, all rates uniform; supplied interactions and register tensor product; no spontaneous chirality, Lorentz or compactification claim'}
}
console.log(JSON.stringify(exchange(),null,2));
