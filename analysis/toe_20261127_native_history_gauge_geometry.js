function nativeHistory(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},V=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)),idx=v=>v.reduce((s,x,j)=>s+m(x)*3**j,0),sp=(a,b)=>m(a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1]),rows=[];
for(let exclude of [false,true]){
let f=Array(243).fill(0n);f[0]=1n;for(let n=1;n<=10;n++){let g=Array(243).fill(0n);for(let a=0;a<81;a++)for(let z=0;z<3;z++)if(f[3*a+z])for(let b=exclude?1:0;b<81;b++){let c=idx(V[a].map((x,i)=>x+V[b][i])),q=m(z+2*sp(V[a],V[b]));g[3*c+q]+=f[3*a+z]}f=g;
A(f[1]===f[2],'conjugate symmetry');let D=exclude?80n:81n;
let pred=(D**BigInt(n)+80n*((exclude?-1n:0n)**BigInt(n)))/81n;A(f[0]+f[1]+f[2]===pred,'closed count');let signed=f[0]-f[1],expected=exclude?((8n**BigInt(n)+(-10n)**BigInt(n))*0n):0n;
// sum of all W(v)=9 parity; for excluded identity eigenvalues 8 (5), -10 (4).
let s=(5n*(exclude?8n:9n)**BigInt(n)+4n*(exclude?-10n:-9n)**BigInt(n))/9n;A(signed===s,'signed count trace');
rows.push({exclude_identity:exclude,n,central_counts:f.slice(0,3).map(String),signed_closed_sum:String(signed),sign:signed>0n?1:signed<0n?-1:0})
}}
return {rows,scope:"Uniform Weyl increments, not the full 120 Clifford tick family; trace sum over histories returning to zero displacement. All even lengths positive, odd length >=3 negative for nonidentity-only increments. On a bipartite graph independent Weyl increment sums do not give needed positive action Fourier coefficients by themselves."}
}
function gaugeGeometry(){
const A=(v,s)=>{if(!v)throw Error(s)},sg=x=>x===2?-1:x,counts={};
for(let a=0;a<27;a++){let v=[a%3,Math.floor(a/3)%3,Math.floor(a/9)],w=(3-v.reduce((s,x)=>s+x,0)%3)%3;v.push(w);let n=v.filter(Boolean).length,j=v.reduce((s,x)=>s+sg(x),0)/3,key=n+','+j*j;counts[key]=(counts[key]||0)+1}
A(Object.values(counts).reduce((s,x)=>s+x,0)===27,'tetra');
function z(b,mu){let a=Math.exp(-1.5*b),single=Object.entries(counts).reduce((s,[k,c])=>{let [n,j]=k.split(',').map(Number);return s+c*a**n*Math.exp(-mu*j)},0)/27;let tor=((1+2*a)**32+2*(1-a)**32)/3**32;return {log_rook:8*Math.log(single),log_torus:Math.log(tor),log_ratio:Math.log(tor)-8*Math.log(single)}}
let rows=[];for(let b of [0,.1,.265,.37,.512,.75,1,2]){let lo=0,hi=40;let threshold=null;if(z(b,0).log_ratio>=-1e-12)threshold=0;else if(z(b,hi).log_ratio>0){for(let i=0;i<80;i++){let mid=(lo+hi)/2;if(z(b,mid).log_ratio>0)hi=mid;else lo=mid}threshold=(hi+lo)/2}rows.push({beta:b,mu_crossover:threshold,...z(b,1),max_suppression_log_ratio:z(b,40).log_ratio})}
return {tetra_flux_census:counts,rows,scope:"Exact normalized link-gauge partition for rook clique complex (eight edge-disjoint tetrahedra) and oriented Shrikhande torus (one face relation), with principal-lift monopole penalty on each 3-simplex. Extends cubic penalty to tetrahedra, supplied rule; different cell dimensions, not a four-dimensional spacetime selector."}
}
console.log(JSON.stringify({history:nativeHistory(),geometry:gaugeGeometry()},null,2));
