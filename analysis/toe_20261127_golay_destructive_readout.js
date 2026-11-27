function readout(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),words=new Map([['000000000000',Array(12).fill(0)]]);
for(let r of C)for(let v of [...words.values()])for(let t=1;t<=2;t++){let z=v.map((x,i)=>m(x+t*r[i]));words.set(z.join(''),z)}
function basis(rows){let B=[],p=[];for(let r of rows){let v=r.slice();for(let i=0;i<B.length;i++){let f=v[p[i]];v=v.map((x,j)=>m(x-f*B[i][j]))}let j=v.findIndex(Boolean);if(j>=0){B.push(v.map(x=>m(x*v[j])));p.push(j)}}return B}
let H=basis([...words.values()].filter(x=>!x[0]).map(x=>x.slice(1))),logical=[...words.values()].find(x=>x[0]===1).slice(1),syn=v=>H.map(r=>m(r.reduce((s,x,i)=>s+x*v[i],0))).join(''),phase=v=>m(logical.reduce((s,x,i)=>s+x*v[i],0)),lookup=new Map(),errors=[];
function add(v){let key=syn(v);A(!lookup.has(key),'perfect syndrome');lookup.set(key,v);errors.push(v)}
add(Array(11).fill(0));for(let i=0;i<11;i++)for(let a=1;a<3;a++){let v=Array(11).fill(0);v[i]=a;add(v);for(let j=i+1;j<11;j++)for(let b=1;b<3;b++){let w=v.slice();w[j]=b;add(w)}}A(lookup.size===243,'perfect');
let pop=x=>{let n=0;for(;x;x&=x-1)n++;return n},supports=new Set([...words.values()].filter(x=>x[0]).map(v=>v.slice(1).reduce((s,x,i)=>s+(x?1<<i:0),0))),fail=Array(12).fill(0),total=Array(12).fill(0);
for(let s=0;s<2048;s++){total[pop(s)]++;if([...supports].some(t=>(s&t)===t))fail[pop(s)]++}A(fail[5]===66,'Witt design');
let byWeight=Array.from({length:12},()=>[0,0,0]),N=3**11;for(let i=0;i<N;i++){let v=Array.from({length:11},(_,j)=>Math.floor(i/3**j)%3),r=lookup.get(syn(v)),l=phase(v.map((x,j)=>m(x-r[j])));byWeight[v.filter(Boolean).length][l]++}
let rows=[];for(let p of [.001,.01,.05,.1]){let err=byWeight.reduce((s,r,w)=>s+(r[1]+r[2])*(p/2)**w*(1-p)**(11-w),0),loss=fail.reduce((s,r,w)=>s+r*p**w*(1-p)**(11-w),0);rows.push({p,destructive_readout_error:err,erasure_failure:loss})}
return {syndrome_classes:lookup.size,weight_le2_correctable:errors.length,enumerated_errors:N,logical_error_weight_census:byWeight,located_erasure_patterns:2048,erasure_failure_by_weight:fail,erasure_total_by_weight:total,rows,scope:"Punctured Golay [[11,1,5]] CSS ideal destructive X or Z measurement, symmetric independent trit readout errors and independent located erasures on data. Separate error models, not circuit-level teleportation. No state prep or postselection overhead."}
}
console.log(JSON.stringify(readout(),null,2));
