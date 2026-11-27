function gramDimension(){
 const A=(v,s)=>{if(!v)throw Error(s)},q=3,d=5,N=183680,br=Array.from({length:6},(_,i)=>(q**d-q**i)/(q-1)),cr=Array.from({length:6},(_,i)=>(q**i-1)/(q-1)),k=[1];for(let i=1;i<=d;i++)k.push(k[i-1]*br[i-1]/cr[i]);A(k.reduce((s,x)=>s+x,0)===N,"size");
 function pol(theta){let a=[1,theta];for(let i=1;i<d;i++)a.push((theta*a[i]-br[i-1]*a[i-1])/cr[i+1]);return a}
 let rows=[];for(let j=0;j<=d;j++){let th=(q**(d-j)-q**j)/(q-1),a=pol(th),mult=N/a.reduce((s,x,i)=>s+x*x/k[i],0),num=a.reduce((s,x,i)=>s+x*q**(2*(d-i)),0);A(Math.abs(mult-Math.round(mult))<1e-8&&Number.isInteger(num),"spectrum");rows.push({j,adjacency_eigenvalue:th,multiplicity:Math.round(mult),gram_eigenvalue_numerator:num,gram_eigenvalue_denominator:q**(2*d)})}
 A(rows.reduce((s,x)=>s+x.multiplicity,0)===N,"multiplicities");
 let nG=60480,distG=k.map((v,i)=>(nG/N)*v+(1-nG/N)*pol(39)[i]); // equitable quotient eigenvalue 39 =66-27
 A(distG.every(x=>Math.abs(x-Math.round(x))<1e-8),"distance counts");
 distG=distG.map(Math.round);let traceSq=nG*distG.reduce((s,x,i)=>s+x*q**(-4*i),0),lower=Math.ceil(nG*nG/traceSq),upper=rows.filter(x=>x.gram_eigenvalue_numerator).reduce((s,x)=>s+x.multiplicity,0);
 return {distance_valencies:k,rows,full_code_state_span_rank:upper,Golay_distance_census_from_Golay:distG,Golay_span_rank_lower:lower,Golay_span_rank_upper:upper,scope:"Uses established split dual polar graph intersection array; exact Gram polynomial and equitable quotient. Rank of all 183680 two-copy states exact. Golay-only span bounded by second moment, not computed exactly. Any Hamiltonian dark on all Golay targets has at least this degeneracy."}
}
function dim(){
 const A=(v,s)=>{if(!v)throw Error(s)},rows=[];
 function heat(t,d){let x=t/d,s=1,term=1;for(let k=1;k<300;k++){term*=x*x/(4*k*k);s+=term;if(term<s*1e-17)break}return Math.exp(-t+d*Math.log(s))}
 function log(d,m,n){let h=160/n,f=t=>t===0?0:Math.exp(-m*t)*(Math.exp(-t)-heat(t,d))/t,s=f(0)+f(160);for(let j=1;j<n;j++)s+=(j%2?4:2)*f(j*h);return Math.log(1+m)+s*h/3}
 for(let d=1;d<=24;d++){let a=log(d,.2,8000),b=log(d,1,8000),a2=log(d,.2,16000),b2=log(d,1,16000);rows.push({d,low:a2,high:b2,weight:3*a2-10*b2,quadrature_difference:Math.max(Math.abs(a-a2),Math.abs(b-b2))})}
 let best=rows.reduce((a,b)=>a.weight>b.weight?a:b);A(best.d===4,"selected");
 let ratios=rows.slice(1).map((r,i)=>(r.low-rows[i].low)/(r.high-rows[i].high));return {rows,increment_ratios:ratios,selected_rank:best.d,adjacent_ratio_interval:[ratios[3],ratios[2]],scope:"Supplied competing determinant weights 3 logdet(lambda+.2)-10 logdet(lambda+1), normalized hopping. Finite candidate ranks1..24, numerical quadrature convergence not certified global. Extensive logweight dominates O(log p) history entropy for fixed rank candidates. Ratios and masses chosen to illustrate interior selection; not physical derivation."}
}
console.log(JSON.stringify({gram:gramDimension(),dimension:dim()},null,2));
