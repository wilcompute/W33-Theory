function extras(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},V=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**j)%3));
function factory(){
let P=V(2).slice(1),weights=n=>{let h=Array(9).fill(0);for(let a of V(n)){let w=0;for(let [x,y] of P){let v=Array.from({length:3},(_,i)=>n===6?m(a[2*i]*x+a[2*i+1]*y):m(a[3*i]+a[3*i+1]*x+a[3*i+2]*y));if(v.some(Boolean))w++}h[w]++}return h},S=weights(6),L=weights(9);
let pr=p=>{let z=1-27*p/26,acc=S.reduce((s,n,w)=>s+n*z**w,0)/729,good=L.reduce((s,n,w)=>s+n*z**w,0)/19683;return {p,accept:acc,output:1-good/acc,expected_raw:8/acc}};
let lo=.001,hi=.8;for(let i=0;i<60;i++){let p=(lo+hi)/2;if(pr(p).output<p)lo=p;else hi=p}
let chain=[];for(let p of [.01,.05,.1,.2]){let a=pr(p),b=pr(a.output);chain.push({input:p,first:a,second:b,raw_cost:64/(a.accept*b.accept)})}
return {dual_syndrome_weights:S,dual_with_logical_weights:L,noise:[.001,.01,.05,.1,.2,.3].map(pr),fixed_point:(lo+hi)/2,two_rounds:chain,scope:'8 noisy three-qutrit CCZ resources, independent across sites, correlated uniform nonzero Z triple at each site, ideal Clifford and syndrome'}
}
function meson(){
let rows=[];
for(let n of [6,8,12,16])for(let t2 of [.15,.3,.6]){
let t1=.3,g=3,dim=3*n;
function ground(k){
let adj=Array.from({length:dim},()=>[]),diag=[];
for(let r=0;r<n;r++)for(let e=0;e<3;e++){
let i=3*r+e,E=Array.from({length:n},(_,j)=>m(e+(j<r?1:0)));diag[i]=g*E.filter(Boolean).length;
for(let particle of [0,1])for(let s of [-1,1]){
let u=particle?r:0,l=(u+(s===1?0:-1)+n)%n,F=E.slice();F[l]=m(F[l]+(particle?1:-1)*s);let dr=(r+(particle?s:-s)+n)%n,shift=particle?0:s,Er=Array.from({length:n},(_,j)=>F[(j+shift+n)%n]),ee=m(Er[n-1]);A(Er.every((x,j)=>x===m(ee+(j<dr?1:0))),'Gauss update');let ang=particle?0:k*s,amp=-(particle?t2:t1);adj[i].push([3*dr+ee,amp*Math.cos(ang),amp*Math.sin(ang)])
}}
let shift=g*n+2*(t1+t2)+1,R=new Float64Array(dim),I=new Float64Array(dim);R[0]=1;
const apply=(R,I)=>{let a=new Float64Array(dim),b=new Float64Array(dim);for(let j=0;j<dim;j++){a[j]+=diag[j]*R[j];b[j]+=diag[j]*I[j];for(let [i,x,y] of adj[j]){a[i]+=x*R[j]-y*I[j];b[i]+=x*I[j]+y*R[j]}}return [a,b]};
let energy=0,res=1,iter=0;for(;iter<20000;iter++){let [a,b]=apply(R,I),E=0;for(let i=0;i<dim;i++)E+=R[i]*a[i]+I[i]*b[i];res=Math.sqrt(a.reduce((s,x,i)=>s+(x-E*R[i])**2+(b[i]-E*I[i])**2,0));energy=E;if(res<1e-10)break;let norm=0;for(let i=0;i<dim;i++){a[i]=shift*R[i]-a[i];b[i]=shift*I[i]-b[i];norm+=a[i]**2+b[i]**2}norm=Math.sqrt(norm);R=a.map(x=>x/norm);I=b.map(x=>x/norm)}
A(res<1e-9,'ground residual');return {energy,res,iter}
}
let k=2*Math.PI/n,a=ground(0),b=ground(k),curv=(b.energy-a.energy)/(1-Math.cos(k));rows.push({n,t1,t2,g,ground0:a,groundk:b,band_curvature:curv,strong_coupling_prediction:4*t1*t2/g})
}
return rows
}
return {factory:factory(),meson:meson()}
}
console.log(JSON.stringify(extras(),null,2));
