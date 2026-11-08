// Actual server V8: independent Simpson/Bessel integral and cyclic quality controls.
const inputMatrix=[[0,1,0,0,0,0],[0,0,2,0,0,0],[0,0,0,1,0,0],[1,0,0,0,0,0],[0,0,0,0,1,1],[0,0,0,0,0,1]];
function simpson(f,a,b,n){let h=(b-a)/n,s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3;}
function scaledK(n,z){let top=Math.acosh(1+45/z);return simpson(u=>Math.exp(-z*(Math.cosh(u)-1))*Math.cosh(n*u),0,top,128);}
function rate(mh,ml,T,panels=512){
 let integ=simpson(v=>{let t=v*v,E=2*mh+T*t,s=E*E;
 return 2*v*(s+2*mh*mh)*(s+2*ml*ml)*Math.sqrt(Math.max(0,(s-4*mh*mh)*(s-4*ml*ml)))*scaledK(1,E/T)*Math.exp(-t);
 },0,Math.sqrt(60),panels);
 return integ/(48*Math.PI*mh**4*scaledK(2,mh/T)**2);
}
function mul(M,v){return M.map(row=>row.reduce((s,x,i)=>s+x*v[i],0)%3);}
function orbit(){for(let n=1;n<729;n++){let v=Array.from({length:6},(_,i)=>Math.floor(n/3**(5-i))%3),w=v.slice(),seen=[];for(let j=0;j<24;j++){seen.push(w.join(""));w=mul(inputMatrix,w);}if(new Set(seen).size===24&&w.join("")===v.join(""))return {seed:v,orbit_length:24};}throw Error("No24orbit");}
function quality(N,r){return Math.log10(2*N*N)+2*Math.log10(2.435e27/1.44667e-33)+(N-2)*Math.log10(r)-N/2*Math.log10(2);}
function build(){
 let b=.053,e=Math.tanh(b*.3/2),r=e/(b*(1+e*e));
 let threshold=Array.from({length:1996},(_,i)=>i+5).find(N=>quality(N,r)<0);
 return {runtime:"Actual functions.exec server V8",rates:[.1,.03,.003].flatMap(T=>[[1.03,.97],[1.,1.]].map(([mh,ml])=>({mh,ml,T,rate:rate(mh,ml,T),refined_rate:rate(mh,ml,T,1024)}))),quality:{r_min:r,log10_Q24:quality(24,r),first_degree:threshold,rmax24:10**(-(Math.log10(2*24*24)+2*Math.log10(2.435e27/1.44667e-33)-12*Math.log10(2))/22)},orbit:orbit(),scope:"Independent integral, algebraic and conditional EFT controls. No independent full population/energy ODE or quantum gravity calculation."};
}
