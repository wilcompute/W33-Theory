function higher(){
const m=(x,n=3)=>(x%n+n)%n,A=(v,s)=>{if(!v)throw Error(s)},G=Array.from({length:243},(_,i)=>[i%9,Math.floor(i/9)%9,Math.floor(i/81)]),idx=g=>g[0]+9*g[1]+81*g[2],N=G.length,prod=new Uint16Array(N*N),c=new Uint8Array(N*N);
for(let i=0;i<N;i++)for(let j=0;j<N;j++){let a=G[i],b=G[j],z=a[2]+b[2]+a[0]*b[1];prod[i*N+j]=idx([m(a[0]+b[0],9),m(a[1]+b[1],9),m(z)]);c[i*N+j]=m(Math.floor(z/3))}
let counts=[0,0,0],B=(i,j,k)=>{let v=c[j*N+k]-c[prod[i*N+j]*N+k]+c[i*N+prod[j*N+k]]-c[i*N+j];A(v%3===0,'cocycle');return m(v/3)};
for(let i=0;i<N;i++)for(let j=0;j<N;j++)for(let k=0;k<N;k++)counts[B(i,j,k)]++;
let seed=123;for(let t=0;t<20000;t++){let g=Array.from({length:4},()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%N}),[i,j,k,l]=g;A(!m(B(j,k,l)-B(prod[i*N+j],k,l)+B(i,prod[j*N+k],l)-B(i,j,prod[k*N+l])+B(i,j,k)),'3 cocycle')}
return {group_order:N,cocycle_triples:N**3,postnikov_census:counts,degree4_checks:20000,scope:"Crossed module Z9 -> H(Z9), map u to central z=3u, trivial action. pi1=H(Z9)/<z^3>, pi2=Z3. Postnikov beta(c) for the Z3 central extension; nontrivial by order27 commutator obstruction to lifting c to Z9. Not an E8 2-group or full spin anomaly cancellation."}
}
function golay(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
let W=new Map([['000000000000',Array(12).fill(0)]]);for(let r of C)for(let v of [...W.values()])for(let t=1;t<3;t++){let w=v.map((x,i)=>m(x+t*r[i]));W.set(w.join(''),w)}
let full=[...W.values()].find(v=>v.every(Boolean)),words=[...W.values()].map(v=>v.map((x,i)=>m(x*full[i]))),hist={};for(let v of words.filter(v=>v.filter(Boolean).length===6)){let k=v.filter(x=>x===1).length;hist[k]=(hist[k]||0)+1}
let D=[];for(let i=0;i<3**7;i++){let v=Array.from({length:7},(_,j)=>Math.floor(i/3**j)%3),a=v.filter(x=>x===1).length,b=v.filter(x=>x===2).length;if(a+b===6&&v.find(Boolean)===1&&hist[a])D.push(v)}
// Since all v sum0, use representatives with last trit zero in each copy. Count basis states in common kernel of all marginal projectors via orthogonality.
let Q=Array.from({length:729},(_,i)=>Array.from({length:7},(_,j)=>Math.floor(i/3**j)%3)),dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0));
let mask=Q.map(q=>D.reduce((s,v,i)=>dot(v,q)?s:s|(1n<<BigInt(i)),0n)),counts={},witness=null;
for(let i=0;i<729;i++)for(let j=0;j<729;j++){let bits=mask[i]&mask[j],n=0;while(bits){bits&=bits-1n;n++}counts[n]=(counts[n]||0)+1;if(!n&&!witness)witness=[Q[i],Q[j]]}
return {weight6_sign_census:hist,seven_site_directions:D.length,quotient_basis_pair_count:729**2,number_of_orthogonal_directions_census:counts,common_kernel_computational_witness:witness,scope:"Seven-site reduced support is rank 3^5 per copy, projector onto X(v),Z(v) fixed spaces for one shortened line. Orbit under coordinate permutations realizes all listed sign types. Basis vectors with no compatible line lie in common kernel if present; absence does not prove full span. No universal preparation claimed."}
}
console.log(JSON.stringify({higher:higher(),golay:golay()},null,2));
