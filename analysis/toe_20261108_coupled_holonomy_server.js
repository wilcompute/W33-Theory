function coupledHolonomyServer(){
 function simpson(a,b,nu,n=65536){
  function f(i){
   if(i===0||i===n)return 0;
   const t=Math.tan(Math.PI*(i/n-.5));
   return (1+t*t)/(2*(t*t+a*a)*((t+nu)**2+b*b));
  }
  let sum=0;for(let i=1;i<n;i++)sum+=(i%2?4:2)*f(i);return sum/(3*n);
 }
 const bubbles=[0,.4,1.2].map(nu=>({a:1.3,b:2.7,nu,integral:simpson(1.3,2.7,nu),
  closed:(1.3+2.7)/(2*1.3*2.7*((1.3+2.7)**2+nu**2))}));
 const G=[[2,.2],[.2,1.5]],K=[[.8,.1],[.1,.6]],p=[2,3,4],W=[[.2,.3,-.1],[.1,-.2,.25]];
 const D=K.map((r,i)=>r.map((x,j)=>x+p.reduce((s,v,k)=>s+W[i][k]*W[j][k]/v**2,0)));
 function F(s){return D.map((r,i)=>r.map((x,j)=>x-s*G[i][j]-p.reduce((t,v,k)=>t+W[i][k]*W[j][k]/(v*v-s),0)))}
 function eigs(A){const t=(A[0][0]+A[1][1])/2,rad=Math.hypot((A[0][0]-A[1][1])/2,A[0][1]);return[t-rad,t+rad]}
 const poles=[0,1].map(i=>{
  let lo=0,hi=2;for(let j=0;j<90;j++){const s=(lo+hi)/2;if(eigs(F(s))[i]>0)lo=s;else hi=s}
  const s=(lo+hi)/2,A=F(s),v=[-A[0][1],A[0][0]];
  const B=G.map((r,i)=>r.map((x,j)=>x+p.reduce((t,u,k)=>t+W[i][k]*W[j][k]/(u*u-s)**2,0)));
  const norm=v.reduce((t,x,i)=>t+x*v.reduce((q,y,j)=>q+B[i][j]*y,0),0);
  return {s,second_coordinate_residue:v[1]**2/norm};
 }).sort((a,b)=>a.s-b.s);
 return {runtime:"Actual functions.exec V8",bubbles,bath:{G,K,D,p,W,poles},
  scope:"Independent compactified-frequency integral and generic positive two-channel oscillator-bath Schur check. Native27band spectrum remains the independent Python/RDC computation."};
}
