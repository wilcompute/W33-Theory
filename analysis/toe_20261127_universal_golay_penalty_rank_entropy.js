function selector(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0));
let B=Array.from({length:4},(_,i)=>Array.from({length:12},(_,j)=>+(Math.floor(j/3)===i)));for(let r of [[1,0,1,1],[0,1,1,2]])B.push(r.flatMap(x=>[x,m(-x),0]));
let C=[Array(12).fill(0)];for(let r of B)C=C.flatMap(v=>[0,1,2].map(t=>v.map((x,i)=>m(x+t*r[i]))));
let D=[];for(let i=0;i<3**7;i++){let v=Array.from({length:7},(_,j)=>Math.floor(i/3**j)%3);if(v.filter(Boolean).length===6&&v.find(Boolean)===1&&!m(v.reduce((s,x)=>s+x,0)))D.push(v)}
let Q=Array.from({length:729},(_,i)=>Array.from({length:7},(_,j)=>Math.floor(i/3**j)%3)),mask=Q.map(q=>D.reduce((s,v,i)=>dot(v,q)?s:s|(1n<<BigInt(i)),0n)),pairs=[];
for(let i=0;i<729;i++)for(let j=0;j<729;j++)if(!(mask[i]&mask[j]))pairs.push([Q[i],Q[j]]);
let counts={},total=0,nonzero=0;for(let s=0;s<4096;s++){let S=Array.from({length:12},(_,i)=>i).filter(i=>s>>i&1);if(S.length!==7)continue;let short=C.filter(v=>v.every((x,i)=>!x||S.includes(i))).map(v=>S.map(i=>v[i]));let dim=Math.round(Math.log(short.length)/Math.log(3));let k=pairs.filter(([a,b])=>short.every(v=>!dot(v,a)&&!dot(v,b))).length;let prob=k/3**(2*(6-dim));total+=prob;nonzero+=+(k>0);let key=dim+":"+k;counts[key]=(counts[key]||0)+1}
return {universal_diagonal_rank:pairs.length*9,competitor_subset_census:counts,positive_subsets:nonzero,total_penalty_expectation:total,scope:"Diagonal projector onto computational basis pairs with no orthogonal weight-six projective line; includes independent global translations in each copy. Annihilates all Golay states. Exact expectation for competitor, not proof entire complement selected or unique steady state."}
}
function dimension(){
let rows=[];for(let p of [11,31,101,1009,10007]){let a=Array.from({length:6},(_,i)=>Math.log((p**(i+1)-1)/(p-1))),r=[];for(let tau of [.5,1,1.5,2]){let log=a.map((x,i)=>x-tau*i*Math.log(p)),max=Math.max(...log),z=log.reduce((s,x)=>s+Math.exp(x-max),0);r.push({tau,prob:log.map(x=>Math.exp(x-max)/z)})}rows.push({p,r})}
return {rows,scope:"Connected prime covers, ranks1..6, common labeled count factor cancels, supplied direction cost tau log p per extra generator. Fixed O(1) cost loses to largest dimension. tau<1 maximizes rank, tau>1 minimizes, tau=1 asymptotically uniform. No interior dimension selected by linear log-volume penalty. Curvature or matter terms not derived."}
}
console.log(JSON.stringify({selector:selector(),dimension:dimension()},null,2));
