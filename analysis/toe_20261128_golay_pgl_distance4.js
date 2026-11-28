function distance4(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
function basis(rows,p=3){let R=[],piv=[];for(let a of rows){let v=a.slice();for(let i=0;i<R.length;i++){let f=v[piv[i]];if(f)v=v.map((x,j)=>(x-f*R[i][j]+p*p)%p)}let k=v.findIndex(Boolean);if(k>=0){let inv=1;while(inv*v[k]%p!==1)inv++;R.push(v.map(x=>x*inv%p));piv.push(k)}}return R}
let B=basis(C),words=[Array(12).fill(0)];for(let r of B)words=words.flatMap(v=>[0,1,2].map(t=>v.map((x,i)=>m(x+t*r[i]))));let ones=words.find(v=>v.every(Boolean));B=B.map(v=>v.map((x,i)=>m(x*ones[i])));A(B.length===6&&words.filter(v=>v.some(Boolean)).every(v=>v.filter(Boolean).length>=6),"Golay");
const mod=x=>(x%11+11)%11,inv=x=>Array.from({length:10},(_,i)=>i+1).find(y=>mod(x*y)===1),G=new Map();
for(let a=0;a<11;a++)for(let b=0;b<11;b++)for(let c=0;c<11;c++)for(let d=0;d<11;d++)if(mod(a*d-b*c)){let p=Array.from({length:12},(_,x)=>{let u=x===11?a:mod(a*x+b),v=x===11?c:mod(c*x+d);return v?mod(u*inv(v)):11});G.set(p.join(","),p)}
let P=[...G.values()];A(P.length===1320&&new Set(P.map(p=>p.slice(0,3).join(","))).size===1320,"3transitive");
const mask=4095,pack=v=>v.reduce((s,x,i)=>s|((x===1?1:x===2?4096:0)<<i),0),neg=x=>((x&mask)<<12)|(x>>>12);
function add(x,y){let a=x&mask,b=x>>>12,c=y&mask,d=y>>>12;return (((a&~(c|d))|(c&~(a|b))|(b&d))&mask)|((((b&~(c|d))|(d&~(a|b))|(a&c))&mask)<<12)}
function canonical(rows){let r=rows.slice(),n=0;for(let j=0;j<12;j++){let b=1<<j,k=r.findIndex((x,i)=>i>=n&&((x|x>>>12)&b));if(k<0)continue;[r[n],r[k]]=[r[k],r[n]];if(r[n]&(b<<12))r[n]=neg(r[n]);for(let i=0;i<r.length;i++)if(i!==n){if(r[i]&b)r[i]=add(r[i],neg(r[n]));else if(r[i]&(b<<12))r[i]=add(r[i],r[n])}n++}return r.slice(0,n)}
let seed=193,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},permute=(B,p)=>B.map(v=>p.map(i=>v[i])),samples=[],orbits=[],used=new Set(),tries=0;
for(let i=0;i<250&&samples.length<46;i++){tries++;let p=Array.from({length:12},(_,j)=>j);for(let j=11;j>0;j--){let k=Math.floor(rng()*(j+1));[p[j],p[k]]=[p[k],p[j]]}let b=permute(B,p),key=canonical(b.map(pack)).join(",");if(used.has(key))continue;let orbit=new Map();for(let q of P){let r=canonical(permute(b,q).map(pack)),k=r.join(",");orbit.set(k,r);used.add(k)}samples.push(b);orbits.push([...orbit.values()])}
let packed=samples.map(b=>b.map(pack)),gram=packed.map((b,i)=>orbits.map(o=>o.reduce((s,c)=>s+3**(2*(11-canonical(b.concat(c)).length)),0)*(1320/o.length)));
A(gram.every((r,i)=>r.every((v,j)=>v===gram[j][i])),"symmetric");let rank=basis(gram.map(r=>r.map(x=>x%101)),101).length;
let sp=(a,b)=>m(a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1]),v=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).slice(1),hist={};
for(let a of v)for(let b of v){let c=a.map((x,i)=>m(-x-b[i]));if(!c.some(Boolean))continue;let key=a.every((x,i)=>x===b[i])?"rank1":sp(a,b)?"symplectic":"isotropic";hist[key]=(hist[key]||0)+1}
let mops=4,s=Math.ceil(rank/(mops+1)),K=Math.floor((s-1)/(mops+1))+1;
return {group:P.length,tries,orbits:orbits.map(o=>o.length),covered:used.size,rank_mod101:rank,gram,denominator:1320*59049,sample_bases:samples,balanced_triples:hist,hermitian_compressions:mops,orthogonal_points:s,guaranteed_distance4_dimension:K,scope:"PGL2(11) is sharply 3-transitive, common Clifford reduces balanced triples to rank1, independent isotropic and symplectic (opposite sign merged by swapping ordered sites), plus balanced pair. Four Hermitian compressions. Greedily choose ceil(n/5) orthogonal vectors with all cross compressions zero; Tverberg yields floor((s-1)/5)+1 scalar-compression vectors. Exact existence, not explicit basis or optimality."}
}
console.log(JSON.stringify(distance4(),null,2));
