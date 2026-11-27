function verify(){
const m=x=>(x%3+3)%3,V=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**(n-1-j))%3)),A=(x,s)=>{if(!x)throw Error(s)};
let P=V(2).slice(1),W=(a,b,c)=>P.map(([x,y])=>m(a+b*x+c*y)),f=x=>x===2?-1:x,wt=x=>x.filter(Boolean).length,dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),counts=Array.from({length:3},()=>Array(9).fill(0)),dx=8,dz=8;
for(let [a,b,c] of V(3)){let w=W(a,b,c);A((w.reduce((s,x)=>s+f(x),0)+f(a))%9===0,'T');if(a)dx=Math.min(dx,wt(w))}
for(let e of V(8)){if(dot(e,W(0,1,0))||dot(e,W(0,0,1)))continue;let l=m(e.reduce((s,x)=>s+x,0));counts[l][wt(e)]++;if(l)dz=Math.min(dz,wt(e))}
A(dx===5&&dz===2,'distance');
let prob=p=>{let z=counts.map(row=>row.reduce((s,n,w)=>s+n*(p/2)**w*(1-p)**(8-w),0)),a=z.reduce((a,b)=>a+b,0);return {p,accept:a,output_error:(z[1]+z[2])/a,cost:8/a}};
let lo=.001,hi=.6;for(let j=0;j<60;j++){let p=(lo+hi)/2;if(prob(p).output_error<p)lo=p;else hi=p}
let beta=.35,mass=.7,p=.4,c=Math.cos(beta),walk=[.2,.1,.05,.025,.0125].map(a=>{let t=beta+a*mass,C=Math.cos(t)*c,D=-Math.sin(t)*Math.sin(beta),E=Math.acos(C*Math.cos(a*p)-D),target=Math.hypot(mass,c*p);return {a,E:E/a,target,error:Math.abs(E/a-target),pi_gap:Math.PI-Math.acos(-C-D)}});
let C=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>i===j?0:i===0||j===0?1:[1,4].includes((i-j+5)%5)?1:2));
let G=V(6).map(x=>x.concat(C[0].map((_,j)=>m(x.reduce((s,a,i)=>s+a*C[i][j],0))))),gd=Math.min(...G.filter(x=>x[0]).map(x=>wt(x.slice(1)))),phases=[0,1,2].map(a=>[...new Set(G.filter(x=>x[0]===a).map(x=>(x.slice(1).reduce((s,v)=>s+f(v),0)%9+9)%9))].sort());
return {dx,dz,counts,threshold:(lo+hi)/2,noise:[.001,.01,.05,.1,.2,.3].map(prob),golay:{distance:gd,phases},walk}
}
console.log(JSON.stringify(verify(),null,2));
