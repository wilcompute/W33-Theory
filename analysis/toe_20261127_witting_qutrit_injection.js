function witting(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},patterns=[[0,1,-1,1],[1,0,-1,-1],[1,-1,0,1],[1,1,1,0]],roots=[[1,0],[-.5,Math.sqrt(3)/2],[-.5,-Math.sqrt(3)/2]];
let rayTypes={},wigner={};for(let s of patterns){let a=s.filter(Boolean),min=Math.min(a.filter(x=>x<0).length,a.filter(x=>x>0).length);rayTypes[min]=(rayTypes[min]||0)+9;let W=[];for(let u=0;u<3;u++)for(let v=0;v<3;v++){let z=0;for(let x=0;x<3;x++)z+=a[m(u+2*x)]*a[m(u-2*x)]*roots[m(-v*x)][0];W.push(Math.round(2*z))}A(W.reduce((s,x)=>s+x,0)===18,'Wigner');wigner[min]={numerators_over18:W.sort((a,b)=>a-b),l1:W.reduce((s,x)=>s+Math.abs(x),0)/18}}
let states=[0,1,2,3],trans=states.map(a=>[1,2,3].map(b=>a^b)),target=1,E=[3,0,3,3];A(E.every((x,i)=>i===target?x===0:Math.abs(x-1-trans[i].reduce((s,j)=>s+E[j],0)/3)<1e-10),'hitting');
let survival=Array.from({length:9},(_,n)=>({n,probability_not_yet_hit:(2/3)**n}));
let P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),Q=P.map(v=>v.flatMap((x,i)=>v.slice(i).map(y=>m(x*y)))),parity=[new Set(),new Set(),new Set()];
for(let i=0;i<59049;i++){let c=Array.from({length:10},(_,j)=>Math.floor(i/3**j)%3),v=Q.map(x=>m(x.reduce((s,z,j)=>s+z*c[j],0)));for(let a=0;a<3;a++)parity[a].add(v.reduce((s,x)=>s+(m(x+a)===1),0)%2)}
return {original_two_qubit_magic_rays:36,qutrit_magic_after_known_support_relabel:rayTypes[1],qutrit_stabilizer_after_relabel:rayTypes[0],wigner,reflection_injection:{branch_count:3,branch_probability:1/3,projective_group:'C2 x C2',transition:trans,expected_raw_resources:3,survival},projective40_uniform_reflection_parity_by_logical_coset:parity.map(x=>[...x]),scope:'known support, ideal optical mode relabeling and qutrit diagonal Clifford; not a free conversion in two-qubit resource theory, no protected raw ray preparation or logical reflection implementation'}
}
console.log(JSON.stringify(witting(),null,2));
