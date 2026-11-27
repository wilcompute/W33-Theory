"use strict";
function build(){
 const A=(b,m)=>{if(!b)throw Error(m)},arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),mod=(x,p)=>(x%p+p)%p,gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a);
 function normals(p,d){let a=[];for(let j=0;j<d;j++)for(let n=0;n<p**(d-j-1);n++){let v=Array(d).fill(0);v[j]=1;let k=n;for(let i=j+1;i<d;i++){v[i]=k%p;k=Math.floor(k/p)}a.push(v)}return a}
 function directions(p,d,R){let primitive=0,lines=new Map();function visit(v,r){if(v.length===d){if(v.find(x=>x!==0)>0&&v.reduce((s,x)=>gcd(s,x),0)===1){primitive++;let lead=v.find(x=>mod(x,p)!==0),inv=arr(p,i=>i).find(i=>mod(i*lead,p)===1),w=v.map(x=>mod(inv*x,p));lines.set(w.join(","),w)}return}for(let i=-r;i<=r;i++)visit([...v,i],r-Math.abs(i))}visit([],R);if(R*R<p)A(primitive===lines.size,"minor injectivity");return {primitive,lines:[...lines.values()]}}
 function one(p,d){
 const ns=normals(p,d),N=ns.length,theta=(p**(d-1)-1)/(p**d-1),eta=(p**(d-2)-1)/(p**d-1),alpha=.5,t=alpha*p**(2/d),f=arr(p,k=>Math.exp(-t*(2-2*Math.cos(2*Math.PI*k/p)))),h=arr(p,v=>sum(f.map((x,k)=>x*Math.cos(2*Math.PI*k*v/p)))/p),Y=ns.map(a=>sum(arr(p,k=>a.reduce((s,x)=>s*f[k*x%p],1))));
 let rows=[];
 for(let R of [...new Set([.25,.5,.75,1,1.25,1.5].map(a=>Math.max(1,Math.floor(a*p**(1/d)))))]){const {primitive,lines}=directions(p,d,R),M=lines.length;
 let count=0,first=0,second=0,minY=Infinity,maxNoHit=-Infinity;
 const lineHeat=lines.map(v=>p*sum(arr(p,k=>v.reduce((s,x)=>s*h[k*x%p],1)))),minLine=Math.min(...lineHeat);
 for(let i=0;i<N;i++){let m=0;for(const v of lines)if(dot(ns[i],v)%p===0)m++;first+=m;second+=m*(m-1);if(m){count++;minY=Math.min(minY,Y[i]);A(Y[i]>=minLine-1e-9,"heat lower bound")}else maxNoHit=Math.max(maxNoHit,Y[i])}
 A(first===M*(p**(d-1)-1)/(p-1),"exact first moment");A(second===M*(M-1)*(p**(d-2)-1)/(p-1),"exact second moment");
 const mu=M*theta,fac=M*(M-1)*eta,lower=mu*mu/(mu+fac),bonf=mu-fac/2,upper=Math.min(1,mu),prob=count/N;
 A(prob>=Math.max(lower,bonf)-1e-12&&prob<=upper+1e-12,"prob bounds");
 if(d===2)A(count===M,"rank2 exact");
 rows.push({R,normalized_radius:R/p**(1/d),primitive,distinct_projective_lines:M,hyperplanes:N,exact_failures:count,probability:prob,mean:mu,factorial_second_moment:fac,lower:Math.max(lower,bonf),upper,min_line_heat:minLine,min_failed_heat:Number.isFinite(minY)?minY:null,max_passing_heat:Number.isFinite(maxNoHit)?maxNoHit:null})
 }
 return {p,d,alpha,rows}
 }
 const rows=[];for(const [d,ps] of [[2,[127,509]],[3,[31,127]],[4,[11,23]]])for(const p of ps)rows.push(one(p,d));
 return {status:"PASS",ensembles:rows,scope:"Uniform connected prime covers, exact projective counting and finite heat lower bound (floating Fourier). Failure means dZ <= prescribed radius, not decoding failure under stochastic noise."}
}
console.log(JSON.stringify(build(),null,2));
