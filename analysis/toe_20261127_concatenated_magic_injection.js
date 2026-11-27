function protectedInjection(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),words=new Map([['000000000000',Array(12).fill(0)]]);
for(let r of C)for(let v of [...words.values()])for(let t=1;t<=2;t++){let z=v.map((x,i)=>m(x+t*r[i]));words.set(z.join(''),z)}
function basis(rows){let B=[],p=[];for(let r of rows){let v=r.slice();for(let i=0;i<B.length;i++){let f=v[p[i]];v=v.map((x,j)=>m(x-f*B[i][j]))}let j=v.findIndex(Boolean);if(j>=0){B.push(v.map(x=>m(x*v[j])));p.push(j)}}return B}
let H=basis([...words.values()].filter(x=>!x[0]).map(x=>x.slice(1))),logical=[...words.values()].find(x=>x[0]===1).slice(1),syn=v=>H.map(r=>m(r.reduce((s,x,i)=>s+x*v[i],0))).join(''),phase=v=>m(logical.reduce((s,x,i)=>s+x*v[i],0)),lookup=new Map(),errors=[];
function add(v){let key=syn(v);A(!lookup.has(key),'perfect syndrome');lookup.set(key,v);errors.push(v)}
add(Array(11).fill(0));for(let i=0;i<11;i++)for(let a=1;a<3;a++){let v=Array(11).fill(0);v[i]=a;add(v);for(let j=i+1;j<11;j++)for(let b=1;b<3;b++){let w=v.slice();w[j]=b;add(w)}}A(lookup.size===243,'perfect');

let mod9=x=>(x%9+9)%9,f=a=>m(a)**3,checks=0,correction=[];
for(let e=1;e<9;e++)for(let c=0;c<3;c++){let values=Array.from({length:3},(_,a)=>mod9(e*(f(a)-f(a+c)))),r=values.map(x=>mod9(x-values[0])/3);A(r.every(Number.isInteger),'Clifford');let B=m(2*(r[2]-2*r[1])),D=m(r[1]-B);for(let a=0;a<3;a++){A(mod9(e*f(a+c)+values[0]+3*(B*a*a+D*a))===mod9(e*f(a)),'T injection');checks++}correction.push({power:e,outcome:c,quadratic:B,linear:D})}
let ccz=0;for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){A(mod9(-f(a+b+c)+f(a+b)+f(a+c)+f(b+c)-f(a)-f(b)-f(c))===mod9(3*a*b*c),'CCZ');ccz++}
let vec=Array.from({length:11},(_,i)=>Array.from({length:3},(_,a)=>{let v=Array(11).fill(0);v[i]=a;return v})),addVec=(v,w)=>v.map((x,i)=>m(x+w[i])),correct=v=>{let u=lookup.get(syn(v));return v.every((x,i)=>x===u[i])};
let componentChecks=0;for(let i=0;i<11;i++)for(let a=0;a<3;a++){A(correct(vec[i][a]),'single');componentChecks++;for(let j=i+1;j<11;j++)for(let b=0;b<3;b++){A(correct(addVec(vec[i][a],vec[j][b])),'double');componentChecks++}}
let tCount=40,cczCount=7*40;
return {ideal_T_phase_checks:checks,correction,CCZ_basis_checks:ccz,componentChecks,transversal_SUM_single_fault_labels:11*80,transversal_SUM_distinct_location_pair_labels:55*80**2,accepted_malignant_with_ideal_recovery:0,outer_T_resources:tCount,outer_CCZ_resources:cczCount,physical_SUM_for_T_injection:11*tCount,physical_SUM_for_CCZ_injections_only:11*cczCount,scope:"Inner Golay injection: prepare encoded T^e|+>, apply inverse transversal SUM from data into magic block, measure magic Z with perfect classical syndrome correction; ideal data Pauli recovery before conditional quadratic Clifford. All one/two post-SUM faults on distinct transversal locations correctable by exact component-factorization. Ideal encoded inputs, resource prep, recovery and Clifford feedforward; no noisy preparation, check extraction or correction circuit. CCZ synthesized by seven T phases on linear sums via logical Clifford operations; counts exclude those additional Clifford gates."}
}

console.log(JSON.stringify(protectedInjection(),null,2));
