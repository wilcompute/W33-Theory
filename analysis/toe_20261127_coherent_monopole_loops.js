function signed(){
 const m=x=>(x%3+3)%3,sg=x=>m(x)===2?-1:m(x),A=(v,s)=>{if(!v)throw Error(s)};
 const V=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**j)%3)).map(v=>v.concat(m(-v.reduce((s,x)=>s+x,0))));
 // Weyl commutator X Z X^-1 Z^-1 gives omega^-1. Check all states and exponents.
 let comm=0;for(let a of [1,2])for(let b of [1,2])for(let q=0;q<3;q++){let x=q,e=0;x=m(x-a);e=m(e-b*x);x=m(x+a);e=m(e+b*(x-a)); // alternative explicit application below
 let p=q,phase=0;phase=m(phase-b*p);p=m(p-a);phase=m(phase+b*p);p=m(p+a);A(p===q&&phase===m(-a*b),'commutator');comm++}
 let rows=[];
 for(let t of [.01,.1,.35,.7]){
  let L=k=>Math.log(1-2*t*Math.cos(2*Math.PI*m(k)/3)+t*t),C=2*(L(1)-L(0))/3,mu=27*C/2;
  let max=0,shift=null;
  for(let f of V){let j=f.reduce((s,x)=>s+sg(x),0)/3;
   let H=f.reduce((s,x)=>s+L(x),0);
   for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)H+=2*(L(f[a]+f[b])+L(f[a]-f[b]+1)+L(f[a]-f[b]-1));
   let z=H-mu*j*j;if(shift===null)shift=z;max=Math.max(max,Math.abs(z-shift));
  }
  A(max<1e-10,'exact penalty');
  rows.push({loop_amplitude:t,cos_coefficient:-C,mu,constant:shift,max_residual:max})
 }
 return {commutator_checks:comm,flux_assignments:243,loops_per_cube:{untwisted_single_faces:6,untwisted_sum_pairs:30,twisted_difference_pairs:60,total:96},rows,scope:"Exact engineered auxiliary oriented-loop determinant identity. Pair of central twists implemented by Weyl commutators; loop inventory, auxiliaries and amplitude supplied, not selected by tick dynamics."}
}
console.log(JSON.stringify(signed(),null,2));
