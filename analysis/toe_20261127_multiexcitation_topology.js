function multiExchange(){
const A=(v,s)=>{if(!v)throw Error(s)},results=[];
for(let n of [1,2,3])for(let kind of ["rook","shrikhande"]){
let edges=[];for(let i=0;i<16;i++)for(let j=i+1;j<16;j++){let x=(j%4-i%4+4)%4,y=(Math.floor(j/4)-Math.floor(i/4)+4)%4;if(kind==="rook"?(x===0||y===0):[[1,0],[3,0],[0,1],[0,3],[1,1],[3,3]].some(([a,b])=>a===x&&b===y))edges.push([i,j])}
let masks=[];for(let a=0;a<65536;a++){let x=a,k=0;while(x){x&=x-1;k++}if(k===n)masks.push(a)}let D=masks.length,idx=new Map(masks.map((x,i)=>[x,i])),neighbors=masks.map(v=>edges.filter(([a,b])=>((v>>a)&1)!==((v>>b)&1)).map(([a,b])=>idx.get(v^(1<<a)^(1<<b))));
let M=Array.from({length:D},(_,i)=>{let v=new Float64Array(D);v[i]=1;return v}),traces=[D],max=0;
for(let k=1;k<=9;k++){let R=Array.from({length:D},()=>new Float64Array(D));for(let i=0;i<D;i++){let row=R[i],q=M[i],adj=neighbors[i];for(let j=0;j<D;j++)row[j]=adj.length*q[j];for(let a of adj){let s=M[a];for(let j=0;j<D;j++)row[j]-=s[j]}}
let tr=R.reduce((s,r,i)=>s+r[i],0);A(Number.isSafeInteger(tr),'exact trace');traces.push(tr);M=R}
results.push({n,kind,dimension:D,traces})
}
let comparisons=[1,2,3].map(n=>{let [a,b]=results.filter(r=>r.n===n),diff=a.traces.map((x,i)=>x-b.traces[i]),first=diff.findIndex(Boolean);return {n,first_difference:first,trace_differences:diff,leading_partition_preference:first<0?"undetermined":((-1)**first*diff[first]>0?"rook":"shrikhande")}})
return {results,comparisons,scope:"Exact integer trace moments for identical hard-core excitations of the same swap Hamiltonian. First nonzero trace difference determines sufficiently high-temperature restricted partition preference, not full Gibbs graph ensemble or unique topology."}
}
console.log(JSON.stringify(multiExchange(),null,2));
