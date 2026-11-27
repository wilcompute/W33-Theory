function anomalies(){
const m=(x,n)=>(x%n+n)%n,A=(x,s)=>{if(!x)throw Error(s)};
function anomaly(n,charges){let linear=charges.reduce((s,x)=>s+x,0),cubic=charges.reduce((s,x)=>s+x**3,0),a=m((n*n+3*n+2)*cubic,6*n),b=m(2*linear,n);return {n,linear,cubic,cubic_condition_residue:a,mixed_condition_residue:b,anomaly_free:!a&&!b}}
let rows=[];for(let families=1;families<=9;families++)for(let size of [15,16,27])for(let n of [3,6,9,12,18,27])rows.push({families,size,...anomaly(n,Array(size*families).fill(n/3))});
const find=(f,s,n)=>rows.find(x=>x.families===f&&x.size===s&&x.n===n);
A(!find(3,16,3).anomaly_free&&find(3,16,9).anomaly_free&&find(3,15,3).anomaly_free&&find(1,27,3).anomaly_free,'anomalies');
let minimal=[];for(let size of [15,16,27])for(let families of [1,3]){let n=null;for(let k=1;k<=30;k++)if(anomaly(3*k,Array(size*families).fill(k)).anomaly_free){n=3*k;break}minimal.push({size,families,min_cyclic_extension_in_test:n})}
let e6=[...Array(16).fill(1),...Array(10).fill(-2),4];A(e6.reduce((s,x)=>s+x,0)===0&&e6.reduce((s,x)=>s+x**3,0)===0,'E6 continuous');
return {rows,minimal,E6_charge_decomposition:{sixteen:1,ten:-2,singlet:4,linear:0,cubic:0},scope:"Hsieh untwisted Spin x Z_n condition, all fields LH and assumed common charge1 of E6 center; for cyclic pullback Z_(3k)->Z3 charge k. Pure discrete and mixed gravitational anomaly only; full gauge global form, other anomalies, dynamical topological extension and mirror gapping not derived. Not a derivation of family number."}
}
console.log(JSON.stringify(anomalies(),null,2));
