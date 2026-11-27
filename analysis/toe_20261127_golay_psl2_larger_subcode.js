function largerSubcode(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
function basis(rows,p=3){let R=[],piv=[];for(let a of rows){let v=a.slice();for(let i=0;i<R.length;i++){let f=v[piv[i]];if(f)v=v.map((x,j)=>(x-f*R[i][j]+p*p)%p)}let k=v.findIndex(Boolean);if(k>=0){let inv=1;while(inv*v[k]%p!==1)inv++;R.push(v.map(x=>x*inv%p));piv.push(k)}}return R}
let B=basis(C),words=[Array(12).fill(0)];for(let r of B)words=words.flatMap(v=>[0,1,2].map(t=>v.map((x,i)=>m(x+t*r[i]))));let ones=words.find(v=>v.every(Boolean));B=B.map(v=>v.map((x,i)=>m(x*ones[i])));A(B.length===6&&words.filter(v=>v.some(Boolean)).every(v=>v.filter(Boolean).length>=6),"Golay");
const mod=x=>(x%11+11)%11,inv=x=>Array.from({length:10},(_,i)=>i+1).find(y=>mod(x*y)===1),G=new Map();
for(let a=0;a<11;a++)for(let b=0;b<11;b++)for(let c=0;c<11;c++)for(let d=0;d<11;d++)if(mod(a*d-b*c)===1){let p=Array.from({length:12},(_,x)=>{let u=x===11?a:mod(a*x+b),v=x===11?c:mod(c*x+d);return v?mod(u*inv(v)):11});G.set(p.join(","),p)}
let P=[...G.values()];A(P.length===660,"group");A(new Set(P.map(p=>p[0]+","+p[1])).size===132,"2transitive");
let seed=193,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},permute=(B,p)=>B.map(v=>p.map(i=>v[i])),samples=[];
for(let i=0;i<32;i++){let p=Array.from({length:12},(_,j)=>j);for(let j=11;j>0;j--){let k=Math.floor(rng()*(j+1));[p[j],p[k]]=[p[k],p[j]]}samples.push(permute(B,p))}
let dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),orbits=samples.map(b=>P.map(p=>permute(b,p))),gram=samples.map((b,i)=>samples.map((_,j)=>orbits[j].reduce((s,c)=>{let r=basis(b.map(v=>c.map(w=>dot(v,w)))).length;return s+3**(10-2*r)},0)));
A(gram.every((r,i)=>r.every((v,j)=>v===gram[j][i])),"symmetric");
let rank=basis(gram.map(r=>r.map(x=>x%101)),101).length;
A(rank>=12,"independent");
return {group_size:P.length,ordered_pair_orbit:132,sample_bases:samples,gram_numerators:gram,gram_denominator:660*59049,rank_mod101:rank,guaranteed_subcode_dimension:Math.floor(rank/2),scope:"Larger deterministic sample. Orbit averages invariant under PSL2(11) on 12 coordinates. Every |C>^2 fixed by common transversal two-qutrit Clifford up to common phase (global Weyl, Fourier, quadratic phase, linear mixing; selfdual C containing ones). Thus all nontrivial weight2 balanced Pauli compressions on invariant space equivalent to one Hermitian operator, by 2-transitivity and Sp4(3) transitivity. Others vanish under global Weyl. Higher-rank numerical range of Hermitian compression contains scalar compression of dimension floor(rank/2), via pairing eigenvectors around median. Proves distance at least3 subcode exists in Golay span, not explicit eigenvectors or recovery circuit."}
}
console.log(JSON.stringify(largerSubcode(),null,2));
