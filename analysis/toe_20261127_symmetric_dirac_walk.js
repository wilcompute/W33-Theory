function symmetricWalk(){
const beta=.35,m=.7,p=.4,c=Math.cos(beta),target=Math.hypot(m,c*p);
let rows=[];for(let a of [.2,.1,.05,.025,.0125]){let u=beta+a*m/2,v=-beta+a*m/2,C=Math.cos(u)*Math.cos(v),D=Math.sin(u)*Math.sin(v),E=Math.acos(C*Math.cos(a*p)-D),gap=Math.PI-Math.acos(-C-D);if(Math.abs(gap-2*beta)>1e-12)throw Error('pi gap');rows.push({a,energy:E/a,error:Math.abs(E/a-target),pi_gap:gap})}return {beta,m,p,c,target,rows,successive_error_ratios:rows.slice(1).map((x,i)=>x.error/rows[i].error)}
}
console.log(JSON.stringify(symmetricWalk(),null,2));
