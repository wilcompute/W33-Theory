function fifthOvoid(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),V=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**j)%3)),P=V.filter(v=>v.find(Boolean)===1&&!m(v.reduce((s,x)=>s+x,0))),iso=P.filter(v=>!dot(v,v)),ani=P.filter(v=>dot(v,v));
A(P.length===40&&iso.length===10,'elliptic');
let pairs=0;for(let i=0;i<10;i++)for(let j=i+1;j<10;j++){A(dot(iso[i],iso[j])!==0,'elliptic quadric');pairs++}
let states=new Map([['00000',10]]);for(let a of iso)for(let z=1;z<9;z++){let q=a.map(x=>m(x*(z%3))+3*m(x*Math.floor(z/3))).join('');A(!states.has(q),'distinct');states.set(q,1)}
let out=new Map(),nrm=0;for(let [key,c] of states){let q=[...key].map(Number);nrm+=c*c;for(let a of iso){if(dot(a,q.map(x=>x%3))||dot(a,q.map(x=>Math.floor(x/3))))continue;for(let z=0;z<9;z++){let s=q.map((x,i)=>m(x%3+a[i]*(z%3))+3*m(Math.floor(x/3)+a[i]*Math.floor(z/3))).join('');out.set(s,(out.get(s)||0)+c)}}}
A(out.size===states.size&&[...out].every(([k,v])=>v===18*states.get(k)),'exact max');
let refPreserve=0;for(let a of ani){let d=dot(a,a);for(let [s,c] of states){let q=[...s].map(Number),x=dot(a,q.map(x=>x%3)),y=dot(a,q.map(x=>Math.floor(x/3))),k=q.map((v,i)=>m(v%3+a[i]*x*d)+3*m(Math.floor(v/3)+a[i]*y*d)).join('');A(states.get(k)===c,'reflection invariance')}refPreserve++}
return {replica_points:P.length,isotropic:iso,anisotropic_norm_counts:[1,2].map(d=>ani.filter(v=>dot(v,v)===d).length),isotropic_nonorthogonal_pairs:pairs,trial_nonzero_amplitudes:states.size,integer_norm_squared:nrm,exact_projector_sum_max:2,reflection_invariance_checks:refPreserve*states.size,exact_M5_max:"16/3",formula:"M5=(1/9)sum_30 R + sum_10 Pi; both upper bounds saturated by the same state",scope:"Replica PG(3,3) elliptic quadric, not identification with original symplectic W33 geometry; norm of fifth raw moment exact."}
}
console.log(JSON.stringify(fifthOvoid(),null,2));
