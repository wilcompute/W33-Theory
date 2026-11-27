function centerLift(){
const m=(x,n=9)=>(x%n+n)%n,A=(v,s)=>{if(!v)throw Error(s)},G=Array.from({length:729},(_,i)=>[i%9,Math.floor(i/9)%9,Math.floor(i/81)]),mul=(a,b)=>[m(a[0]+b[0]),m(a[1]+b[1]),m(a[2]+b[2]+a[0]*b[1])],inv=a=>[m(-a[0]),m(-a[1]),m(-a[2]+a[0]*a[1])],eq=(a,b)=>a.every((x,i)=>x===b[i]),id=[0,0,0],comm=(a,b)=>mul(mul(mul(a,b),inv(a)),inv(b));
let centers=G.filter(a=>G.every(b=>eq(mul(a,b),mul(b,a)))),derived=new Set(),orders={},fiber={};
for(let a of G){let p=id,k=0;do{p=mul(p,a);k++}while(!eq(p,id));orders[k]=(orders[k]||0)+1;for(let b of G){let c=comm(a,b);A(eq(c,[0,0,m(a[0]*b[1]-a[1]*b[0])]),'comm');derived.add(c.join())}if(!m(a[0],3)&&!m(a[1],3)&&m(a[2],3)){fiber[k]=(fiber[k]||0)+1;A(k===9,'center lifts')}}
A(centers.length===9&&derived.size===9,'center');
// check primitive rep law on generator pairs, full commutator checks above
let rep=(g,q)=>[m(q+g[0]),m(g[2]-g[1]*(q+g[0]))],repChecks=0;for(let a of G)for(let b of [[1,0,0],[0,1,0],[0,0,1]])for(let q=0;q<9;q++){let [j,p]=rep(b,q),[k,r]=rep(a,j),[l,s]=rep(mul(a,b),q);A(k===l&&m(p+r)===s,'representation');repChecks++}
let anomaly=(n,N,k)=>[m((n*n+3*n+2)*N*k**3,6*n),m(2*N*k,n)];
A(anomaly(3,48,1).some(Boolean)&&anomaly(9,48,3).every(x=>!x),'anomaly');
return {order:729,center:centers,derived_size:derived.size,orders,nontrivial_center_fiber_orders:fiber,commutator_checks:G.length**2,repChecks,central_anomaly_before:anomaly(3,48,1),central_anomaly_after:anomaly(9,48,3),scope:"H(Z9) -> H(F3) reduction. Kernel order27, preimage of center C3² × C9. Minimal order729 among class-two 3-groups with an order9 commutator [a,b]: a,b independent mod center to order9 by commuting with b,a, center >=9. No proof of full anomaly extension or E6 embedding; 48 uniform-charge fields only representation of center, not of H27."}
}
function golayLocal(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
let W=new Map([['000000000000',Array(12).fill(0)]]);for(let r of C)for(let v of [...W.values()])for(let t=1;t<3;t++){let w=v.map((x,i)=>m(x+t*r[i]));W.set(w.join(''),w)}
let full=[...W.values()].find(v=>v.every(Boolean));let words=[...W.values()].map(v=>v.map((x,i)=>m(x*full[i]))),checks=words.filter(v=>v.filter(Boolean).length===6&&v.find(Boolean)===1);
function basis(rows){let R=[],p=[];for(let v of rows){let w=v.slice();for(let i=0;i<R.length;i++){let a=w[p[i]];w=w.map((x,j)=>m(x-a*R[i][j]))}let i=w.findIndex(Boolean);if(i>=0){R.push(w.map(x=>m(x*w[i])));p.push(i)}}return R}
let B=basis(checks);A(checks.length===132&&B.length===6,'weight6 spans');let supports=new Set(checks.map(v=>v.reduce((s,x,i)=>s+(x?1<<i:0),0)));A(supports.size===132,'support');
let code= v=>v.reduce((s,x,i)=>s+x*3**i,0),sy=Array.from({length:729},(_,i)=>B.map((_,j)=>Math.floor(i/3**j)%3)),col=Array.from({length:12},(_,i)=>B.map(v=>v[i])),coeff=checks.map(v=>sy.find(s=>v.every((x,i)=>m(s.reduce((a,b,j)=>a+b*B[j][i],0))===x)));
let adj=sy.map(s=>{let dest=new Map();for(let j=0;j<checks.length;j++){let v=checks[j],mismatch=dot(coeff[j],s);if(!mismatch)continue;for(let i=0;i<12;i++)if(v[i]){let t=code(s.map((x,k)=>m(x-mismatch*v[i]*col[i][k])));dest.set(t,(dest.get(t)||0)+1)}}return dest});
let reached=new Set([0]),levels=[1];for(let k=0;k<10&&reached.size<729;k++){let n=[];for(let i=0;i<729;i++)if(!reached.has(i)&&[...adj[i].keys()].some(t=>reached.has(t)))n.push(i);n.forEach(i=>reached.add(i));levels.push(n.length)}A(reached.size===729,'absorbing');
let survive=Array(729).fill(1);survive[0]=0;let rows=[];for(let n=1;n<=500;n++){survive=survive.map((x,i)=>i===0?0:x+[...adj[i]].reduce((s,[j,w])=>s+w*(survive[j]-x)/792,0));if([1,5,10,20,50,100,200,500].includes(n))rows.push({n,worst_survival:Math.max(...survive)})}
return {weight6_directions:checks.length,rank:B.length,supports:supports.size,full_rank_six_subsets:924-supports.size,reverse_reachability_levels:levels,rows,scope:"Constructive code-specific six-site syndrome pumping with uniform choice of check and one of six sites. Correct nonzero syndrome by local Pauli. Exact absorbing graph for each CSS syndrome sector; four independent sectors for two copies. No supplied stabilizer-free universal selector: permutation-invariant dynamics dark on all Golay states cannot have nontrivial jumps <=6 because some code has full-rank marginal on each given support."}
}
console.log(JSON.stringify({center:centerLift(),golay:golayLocal()},null,2));
