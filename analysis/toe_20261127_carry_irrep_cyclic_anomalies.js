function restrictions(){
const m=(x,n)=>(x%n+n)%n,A=(v,s)=>{if(!v)throw Error(s)},gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a),lcm=(a,b)=>a*b/gcd(a,b),rows=[];
for(let n=1;n<=5;n++){let q=3**n,G=Array.from({length:9*q},(_,i)=>[i%q,Math.floor(i/q)%3,Math.floor(i/(3*q))]),rs=[];
for(let k=0;k<q/3;k++)for(let s of [1,2]){let fail=0,min=1,byOrder={};for(let [x,y,z] of G){let ord=lcm(q/gcd(q,x),y||z?3:1);if(ord===1)continue;let ex=Array.from({length:3},(_,a)=>m(k*x+(q/3)*(x%3?a:s*(z-y*(a+x))),q));A(ex.every(e=>!(e%(q/ord))),'charge');let ch=ex.map(e=>e/(q/ord)),linear=ch.reduce((s,x)=>s+x,0),cubic=ch.reduce((s,x)=>s+x**3,0),u=m((ord*ord+3*ord+2)*cubic,6*ord),v=m(2*linear,ord);if(u||v){fail++;byOrder[ord]=(byOrder[ord]||0)+1}min=lcm(min,lcm(6*ord/gcd(u,6*ord),ord/gcd(v,ord)))}
rs.push({k,s,failed_elements:fail,byOrder,min_copies_for_all_cyclic_restrictions:min})}
let census={};for(let a of rs)census[a.min_copies_for_all_cyclic_restrictions]=(census[a.min_copies_for_all_cyclic_restrictions]||0)+1;rows.push({n,q,census,representations:n<=3?rs:undefined})}
return {rows,scope:"Necessary cyclic-subgroup anomaly restrictions for untwisted Spin x G_n. Uses eigencharges of monomial irreps and Hsieh Eq1.2; no sufficiency for full nonabelian spin bordism. Central commutator Z3 acts on each triplet by common nontrivial charge, so no individual triplet passes."}
}
console.log(JSON.stringify(restrictions(),null,2));
