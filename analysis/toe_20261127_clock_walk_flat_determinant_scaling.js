function clockDynamics(){
const A=(x,s)=>{if(!x)throw Error(s)},rows=[];
for(let q of [3,9,27,81,243]){
let theta=2*Math.PI/q,h=1-Math.cos(theta),r=2*(1+Math.cos(theta)),tau=1/h;
let p=Array.from({length:q},(_,k)=>Array.from({length:q},(_,l)=>Math.exp(-tau*(1-Math.cos(l*theta)))*Math.cos(k*l*theta)/q).reduce((s,x)=>s+x,0));
A(Math.min(...p)>-1e-12&&Math.abs(p.reduce((s,x)=>s+x,0)-1)<1e-10,'heat kernel');
let amp=[0,1,2].map(j=>p.reduce((s,x,k)=>s+x*Math.cos(k*j*theta),0));A(Math.abs(-Math.log(amp[2])-r)<1e-8,'ratio');
let K=(t,j)=>Array.from({length:q},(_,k)=>Math.cos(2*t*(Math.cos(k*theta)-Math.cos((k+j)*theta)))).reduce((s,x)=>s+x,0)/q;
let cross=null;
if(q>3){let prev=.0001,lo=prev,hi=null;for(let step=1;step<=20000;step++){let t=step/(q===243?100:1000);if(K(t,1)<=0||K(t,2)<=0)break;if(K(t,2)-K(t,1)**4<0){lo=prev;hi=t;break}prev=t}if(hi!==null){for(let k=0;k<60;k++){let mid=(lo+hi)/2;if(K(mid,2)-K(mid,1)**4>0)lo=mid;else hi=mid}let t=(lo+hi)/2,mu=-Math.log(K(t,1)),dist=Array.from({length:q},(_,k)=>{let re=0,im=0;for(let l=0;l<q;l++){let phase=k*l*theta-2*t*Math.cos(l*theta);re+=Math.cos(phase)/q;im+=Math.sin(phase)/q}return re*re+im*im});A(Math.abs(K(t,2)-Math.exp(-4*mu))<1e-10,'matching');A([0,1,2].every(j=>Math.abs(dist.reduce((s,x,k)=>s+x*Math.cos(j*k*theta),0)-K(t,j))<1e-10),'unitary DFT');cross={time:t,mu,K1:K(t,1),K2:K(t,2),p: q===9?dist:undefined}}}
rows.push({q,tau,charge2_action:-Math.log(amp[2]),relative_error:1-r/4,unitary_matching:cross})}
return {rows,scope:"Markov nearest-neighbor jumps produce exact cosine action, no positive symmetric generator reaches quadratic ratio4 at finite q. Closed clock quantum walk H=S+S†, initial |0>, produces probability by unitary evolution; its character expectation crosses exact Gaussian ratio at selected time. Conditional coherent amplitude, not unconditional gauge action; interaction and matching stopping time supplied."}
}
function determinantScale(){
const A=(v,s)=>{if(!v)throw Error(s)},gcd=(a,b)=>b?gcd(b,a%b):a,rows=[];
for(let d of [2,3,4]){
let N=d===4?32:d===3?80:160,g=Array(N+1).fill(1);g[0]=0;for(let j=1;j<d;j++){let h=Array(N+1).fill(0);for(let k=1;k<=N;k++)for(let l=1;k*l<=N;l++)h[k*l]+=k**j*g[l];g=h}
let sum=Array(N+1).fill(0);
for(let k=2;k<=N;k++){let c=Array.from({length:k},(_,j)=>2*(1-Math.cos(2*Math.PI*j/k)));for(let n=1;n<k**d;n++){let x=n,u=k,lam=0;for(let j=0;j<d;j++){let a=x%k;x=Math.floor(x/k);u=gcd(u,a);lam+=c[a]}if(u===1)sum[k]+=1/lam}}
for(let n of [8,13,16,23,24,31,32,48,61,64,79,97,127,128,157].filter(x=>x<=N)){let tr=0;for(let k=2;k<=n;k++)if(!(n%k))tr+=g[n/k]/g[n]*sum[k];rows.push({d,n,mean_trace_pseudoinverse:tr,mean_per_site:tr/n})}
 // brute projective generators for prime 5,7; compare character order formula
for(let p of [5,7]){let tr=0,ct=0;for(let lead=0;lead<d;lead++)for(let n=0;n<p**(d-lead-1);n++){let a=Array(d).fill(0);a[lead]=1;for(let j=lead+1;j<d;j++)a[j]=Math.floor(n/p**(j-lead-1))%p;for(let k=1;k<p;k++)tr+=1/a.reduce((s,x)=>s+2*(1-Math.cos(2*Math.PI*k*x/p)),0);ct++}A(Math.abs(tr/ct-sum[p]/g[p])<1e-9,'prime trace')}
}
return {rows,scope:"Uniform connected flat Z^d covers of arbitrary finite index. Character order k inclusion probability g_d(n/k)/g_d(n). For d>=3 primitive character sum O(k^d), yielding expected Tr L+ O(n sum_{l|n}1/l) <= O(n log n), d2 O(n log² n). Conditional on orbit sizes independent uniform covers, same bound O(N log N) across assembly. Thus determinant realization of parallel component fugacity converges in TV for delta=o(1/(N log N)) in d>=3, versus graph-uniform o(N^-2). Supplied flatness and neutral auxiliaries; does not select dimension."}
}
console.log(JSON.stringify({clock:clockDynamics(),geometry:determinantScale()},null,2));
