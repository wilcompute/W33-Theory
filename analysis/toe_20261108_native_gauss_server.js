function nativeGaussServer(){
 function integral(a,b,nu,power,n=65536){
  const f=i=>{
   if(i===0||i===n)return power===2?2:0;
   const t=Math.tan(Math.PI*(i/n-.5));
   return (1+t*t)*(2*t+nu)**power/(2*(t*t+a*a)*((t+nu)**2+b*b));
  };
  let sum=f(0)+f(n);for(let i=1;i<n;i++)sum+=(i%2?4:2)*f(i);return sum/(3*n);
 }
 const integrals=[];
 for(const nu of [0,.4,1.2]){
  const a=1.3,b=2.7,p=a+b,d=2*a*b*(p*p+nu*nu);
  const exact=[p/d,(b-a)*nu/d,p*(4*a*b+nu*nu)/d];
  integrals.push({a,b,nu,quadrature:[0,1,2].map(q=>integral(a,b,nu,q)),closed:exact,
   density_contact:p/(2*a*b),density_after_contact:p*(a-b)**2/d});
 }
 const transpose=A=>A[0].map((_,j)=>A.map(r=>r[j]));
 const multiply=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,x,k)=>s+x*B[k][j],0)));
 function inverse(A){
  const n=A.length,M=A.map((r,i)=>r.concat(Array.from({length:n},(_,j)=>+(i===j))));
  for(let k=0;k<n;k++){
   let p=k;for(let i=k+1;i<n;i++)if(Math.abs(M[i][k])>Math.abs(M[p][k]))p=i;
   [M[k],M[p]]=[M[p],M[k]];const v=M[k][k];M[k]=M[k].map(x=>x/v);
   for(let i=0;i<n;i++)if(i!==k){const q=M[i][k];M[i]=M[i].map((x,j)=>x-q*M[k][j]);}
  }return M.map(r=>r.slice(n));
 }
 function schur(A,k){
  const a=A.slice(0,k).map(r=>r.slice(0,k)),b=A.slice(0,k).map(r=>r.slice(k)),d=A.slice(k).map(r=>r.slice(k));
  const term=multiply(multiply(b,inverse(d)),transpose(b));
  return a.map((r,i)=>r.map((x,j)=>x-term[i][j]));
 }
 const E=[[2,.1,.2,.4],[.1,1.5,.15,.1],[.2,.15,1.8,-.2],[.4,.1,-.2,2.2]],K=[.4,2,3];
 const S=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[.6,0,0,1]];
 const changed=multiply(multiply(transpose(S),E),S);
 const cases=[.2,.7].map(nu=>{
  const Er=schur(E,3),Er2=schur(changed,3);
  const F=Er.map((r,i)=>r.map((x,j)=>nu*nu*x+(i===j?K[i]:0)));
  return {nu,E_reduced:Er,profile_reduced_error:Math.max(...Er.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-Er2[i][j])))),low_kernel:schur(F,1)[0][0]};
 });
 return {runtime:"Actual functions.exec V8",integrals,toy:{E,K,profile_shift:S,cases},
  scope:"Independent temporal bubble/contact quadratures plus generic nested temporal/optical Schur check. Full native135edge numerical model is separate Python/RDC."};
}
