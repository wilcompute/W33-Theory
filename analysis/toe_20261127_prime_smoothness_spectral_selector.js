function selectors(){
const A=(x,s)=>{if(!x)throw Error(s)},m=(x,p)=>(x%p+p)%p;
let higher=[];
for(let p of [2,3,5,7,11,13,17,19]){
 if(p===2){higher.push({p,complex_dimension:1,smooth:false,witness:'x=y=(1,i,0)'});continue}
 if(p===3){higher.push({p,complex_dimension:3,smooth:true,reason:'positive d_i^3 cannot sum to zero on nonempty common support'});continue}
 let q=p-2,D=p*q,ex=Array.from({length:q},(_,j)=>j),y=ex.map(j=>m((p-1)*j,D));
 A(ex.every((j,i)=>m(p*j,D)===m(p*y[i],D)&&m((p-1)*y[i]-j,D)===0),'singular gradients');
 let sum=ex.reduce((s,j)=>[s[0]+Math.cos(2*Math.PI*j/q),s[1]+Math.sin(2*Math.PI*j/q)],[0,0]);A(Math.hypot(...sum)<1e-12,'roots sum');
 higher.push({p,complex_dimension:2*p-3,smooth:false,singular_support:q,root_order:D,x_exponents:ex,y_exponents:y,exact_sum:'sum all (p-2) roots of unity = 0',numerical_sum_residual:Math.hypot(...sum)})
}
let high=[6,3-Math.sqrt(3),3+Math.sqrt(3)].flatMap(x=>[x,x]),spectra={axis:[[0,3,3],[3,6,6],[3,6,6]].map(x=>x.concat(high)),diagonal:[[0,6,6],[3,3,6],[3,3,6]].map(x=>x.concat(high))};
let rows=[];
for(let mass of [.1,.5,1,2,5,10])for(let [k,ss] of Object.entries(spectra)){
 let det=ss.map(s=>s.reduce((a,x)=>a+Math.log(x+mass**2),0)/9),avg=det.reduce((a,b)=>a+b,0)/3;
 A(det[0]<avg&&det[1]>avg&&det[1]===det[2],'det sign');
 rows.push({mass,quotient:k,logdet_density:det,cover_density:avg,trivial_difference:det[0]-avg,nontrivial_difference:det[1]-avg})
}
let W=[{kind:'identity',w27:[27,0,0],adj0:78},{kind:'central_1',w27:[0,27,0],adj0:78},{kind:'central_2',w27:[0,0,27],adj0:78},{kind:'A5_neutral15',w27:[15,6,6],adj0:36},{kind:'A5_neutral6_a',w27:[6,15,6],adj0:36},{kind:'A5_neutral6_b',w27:[6,6,15],adj0:36},{kind:'A2^3',w27:[9,9,9],adj0:24},{kind:'D4',w27:[9,9,9],adj0:30}].map(x=>({...x,scalar_27_coefficient:(3*x.w27[0]-27)/2,scalar_78_coefficient:(3*x.adj0-78)/2}));
 // invariant cubics and pairing for full monomial group: diagonal requires each exponent multiple 3; permutations transitive.
 let mon=[];for(let a=0;a<=3;a++)for(let b=0;b<=3-a;b++)for(let c=0;c<=3-a-b;c++)mon.push([a,b,c,3-a-b-c]);
 let pure=mon.filter(x=>x.every(t=>t%3===0));A(pure.length===4,'pure');
 let lines=[];for(let p of [[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]])for(let a=0;a<3;a++)for(let b=0;b<3;b++)lines.push({pairs:p,phases:[a,b]});
 // diagonal phases shift each line phase independently, S4 acts transitively on pair partitions.
 return {higher_prime_symmetry_family:higher,twisted_determinants:rows,Wilson_scalar_coefficients:W,symmetric_moduli:{degree3_invariants:1,pairing_invariants:1,coordinate_endomorphism_invariants:1,polynomial_deformation_invariants:1+1+1-1-1-1,cubic_surface_lines:lines.length,line_orbits:1,cover_invariant_Kahler_rank:2}}
}
console.log(JSON.stringify(selectors(),null,2));
