function exceptional(){
const m=(x,n)=>(x%n+n)%n,A=(v,s)=>{if(!v)throw Error(s)},gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a),lcm=(a,b)=>a*b/gcd(a,b),rows=[];
for(let n=1;n<=5;n++){let q=3**n,G=Array.from({length:9*q},(_,i)=>[i%q,Math.floor(i/q)%3,Math.floor(i/(3*q))]),kernel=[],scalar27=[],fail=0,restricted={};
for(let [x,y,z] of G){let six=[1,-1].flatMap(k=>Array.from({length:3},(_,a)=>m(k*x+q/3*(x%3?a:z-y*(a+x)),q)));A(m(six.reduce((s,x)=>s+x,0),q)===0,'det1');if(six.every(x=>!x))kernel.push([x,y,z]);let e27=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)e27.push(m(six[i]+six[j],q));for(let k=0;k<2;k++)e27.push(...six.map(x=>m(-x,q)));if(e27.every(x=>x===e27[0]))scalar27.push({g:[x,y,z],phase_exponent:e27[0]});
let ord=lcm(q/gcd(q,x),y||z?3:1);if(ord>1){A(e27.every(v=>v%(q/ord)===0),'charge');let ch=e27.map(v=>v/(q/ord)),s1=ch.reduce((s,x)=>s+x,0),s3=ch.reduce((s,x)=>s+x**3,0);if(m((ord*ord+3*ord+2)*s3,6*ord)||m(2*s1,ord))fail++;restricted[ord]=(restricted[ord]||0)+1}}
A(kernel.length===1&&scalar27.length===3&&scalar27.every(x=>x.g[0]===0&&x.g[1]===0)&&fail===0,'embedding');
rows.push({n,q,kernel,scalar27,cyclic_anomaly_failures:fail,restricted})
}
return {rows,scope:"Faithful monomial SU6 representation rho_(+1,+) direct sum rho_(-1,+). Standard compact simply connected E6 embedding of SU6 with 27 = wedge²6 + 2 conjugate6. All cyclic restrictions on 27 pass. E6 center pulls back precisely to commutator Z3, which has an actual order3 subgroup; 48 uniformly center charged fermions remain anomalous there. Distinct from previous anomaly-free abelianization charge pullback; no physical E6 breaking or full nonabelian global anomaly proof."}
}
console.log(JSON.stringify(exceptional(),null,2));
