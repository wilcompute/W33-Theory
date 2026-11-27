"use strict";
function build(){
  const A=(x,s)=>{if(!x)throw Error(s)}, sum=a=>a.reduce((s,x)=>s+x,0);
  function normals(p,d){
    const out=[];
    for(let j=0;j<d;j++)for(let n=0;n<p**(d-j-1);n++){
      const a=Array(d).fill(0);a[j]=1;let k=n;
      for(let i=j+1;i<d;i++){a[i]=k%p;k=Math.floor(k/p)}
      out.push(a)
    }return out
  }
  function spectra(p,d,alpha,beta){
    const a=normals(p,d), lambda=Array.from({length:p},(_,k)=>2-2*Math.cos(2*Math.PI*k/p));
    const t=alpha*p**(2/d),s=beta*p**(2/d), f=lambda.map(x=>Math.exp(-t*x)),g=lambda.map(x=>Math.exp(-s*x));
    let x=[],y=[];
    for(const n of a){let u=1,v=1;for(let k=1;k<p;k++){let z=1,w=1;for(const l of n){z*=f[k*l%p];w*=g[k*l%p]}u+=z;v+=w}x.push(u);y.push(v)}
    let N=a.length,m=sum(x)/N,n=sum(y)/N,variance=sum(x.map(z=>(z-m)**2))/N,cov=sum(x.map((z,i)=>(z-m)*(y[i]-n)))/N;
    A(N===(p**d-1)/(p-1),"normal count");
    A(Math.abs(m-(1+(sum(f)**d-1)/N))<1e-10,"mean");
    return {p,d,alpha,beta,N,mean:m,variance,covariance:cov,median:x.slice().sort((u,v)=>u-v)[Math.floor(N/2)],max:x.reduce((u,v)=>Math.max(u,v),0)}
  }
  function independent(p,d,alpha,beta){
    const a=normals(p,d),N=a.length,theta=(p**(d-1)-1)/(p**d-1),eta=(p**(d-2)-1)/(p**d-1);
    const vecs=Array.from({length:p**d},(_,n)=>{let a=[];for(let i=0;i<d;i++){a.push(n%p);n=Math.floor(n/p)}return a});
    const lap=k=>2-2*Math.cos(2*Math.PI*k/p);
    function primal(t){
      const h=Array.from({length:p},(_,r)=>sum(Array.from({length:p},(_,k)=>Math.exp(-t*lap(k))*Math.cos(2*Math.PI*r*k/p)))/p);
      return vecs.map(v=>p*v.reduce((z,k)=>z*h[k],1))
    }
    const u=primal(alpha*p**(2/d)),v=primal(beta*p**(2/d));
    let U=0,V=0,C=0;for(const n of a){
      let x=0,y=0;for(let i=0;i<vecs.length;i++)if(sum(vecs[i].map((r,j)=>r*n[j]))%p===0){x+=u[i];y+=v[i]}U+=x/N;V+=y/N;C+=x*y/N
    }
    let B=0;for(const n of a){let x=0,y=0;for(let k=1;k<p;k++){let i=sum(n.map((r,j)=>(k*r%p)*p**j));x+=u[i];y+=v[i]}B+=x*y}
    const pred=(theta-eta)*B+(eta-theta**2)*(p-u[0])*(p-v[0]);
    const spec=spectra(p,d,alpha,beta);
    A(Math.abs(C-U*V-pred)<2e-10,"projective covariance");
    A(Math.abs(pred-spec.covariance)<2e-10,"dual spectral covariance");
    A(Math.abs(U-spec.mean)<2e-10,"primal Fourier");
    return {p,d,alpha,beta,projective_covariance:pred,primal_covariance:C-U*V,spectral_covariance:spec.covariance}
  }
  const rows=[];
  for(const [d,ps] of [[2,[31,127,509,2039]],[3,[11,31,61,127,251]],[4,[5,11,23,43]]])for(const p of ps)rows.push(spectra(p,d,.5,1));
  const controls=[];for(const p of [3,5,7])for(const d of [2,3,4])for(const [a,b] of [[.13,.7],[.5,.5],[.5,1]])controls.push(independent(p,d,a,b));
  return {status:"PASS",scope:"Uniform index-p covers; rank and flatness imposed. Numerical spectral sums, exact covariance identity proved separately.",controls,rows}
}
console.log(JSON.stringify(build(),null,2));
