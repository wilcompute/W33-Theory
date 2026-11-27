function thirdMoment(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3;
// One-copy subspace of triples sum=0, quotient uniform shifts. Compute permutation traces on orbit basis.
let orbits=[],seen=new Set();for(let n=0;n<27;n++){let a=[n%3,Math.floor(n/3)%3,Math.floor(n/9)];if(m(a.reduce((s,x)=>s+x,0)))continue;let key=[0,1,2].map(t=>a.map(x=>m(x+t)).join("")).sort()[0];if(!seen.has(key)){seen.add(key);orbits.push(key)}}
A(orbits.length===3,"rank");let perms=[[0,1,2],[1,0,2],[2,1,0],[0,2,1],[1,2,0],[2,0,1]],traces=perms.map(p=>orbits.filter(k=>{let a=p.map(i=>+k[i]);return [0,1,2].map(t=>a.map(x=>m(x+t)).join("")).sort()[0]===k}).length),sign=[1,-1,-1,-1,1,1];
let sym=traces.reduce((s,x)=>s+x*x,0)/6,anti=traces.reduce((s,x,i)=>s+sign[i]*x*x,0)/6;A(sym===5&&anti===4,"Pi");
let spec=[{sector:"symmetric",value:16,multiplicity:sym},{sector:"symmetric",value:7,multiplicity:165-sym},{sector:"antisymmetric",value:10,multiplicity:anti},{sector:"antisymmetric",value:1,multiplicity:84-anti},{sector:"mixed",value:4,multiplicity:480}];
A(spec.reduce((s,x)=>s+x.multiplicity,0)===729&&spec.reduce((s,x)=>s+x.value*x.multiplicity,0)===3240,"trace");
let rows=[];for(let k=1;k<=30;k++){let a=BigInt(2*k),v=5n*16n**a+160n*7n**a-4n*10n**a-80n-480n*4n**a;A(v>0,"even coefficient");rows.push(v.toString())}
return {one_copy_orbits:orbits,permutation_traces:traces,Pi_symmetric:sym,Pi_antisymmetric:anti,spectrum:spec,worst_case_even_coefficients:rows,scope:"M3=4I+sum three swaps+9Pi, Pi joint Weyl invariant projector rank9. All signs assigned to whole S3 isotypic sectors with symmetric positive yield positive even moments of M3/120, since 160*7^(2k)>480*4^(2k) and 5*16^(2k)>4*10^(2k)+80 for k>=1. Thus signed determinant monotone in rank; no interior optimum for this class. Not an exhaustive higher-connected-moment analysis."}
}
console.log(JSON.stringify(thirdMoment(),null,2));
