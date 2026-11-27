function gaugeCycles(){
const A=(v,s)=>{if(!v)throw Error(s)},soft=x=>Math.max(x,0)+Math.log1p(Math.exp(-Math.abs(x))),rows=[];
for(let [b,mu,beta] of [[.5,0,2],[2,0,2],[4,1,2],[2,0,0]]){
 let N=8192,f=0;for(let i=0;i<N;i++)f+=soft(mu-b*(2-2*Math.cos(2*Math.PI*i/N)))/N;
 let q=(1+2*Math.exp(-1.5*beta))/3,w=Array(5001).fill(q),sample=[];
 for(let l=3;l<=256;l++){let z=[];for(let h=0;h<3;h++){let t=0;for(let j=0;j<l;j++)t+=soft(mu-b*(2-2*Math.cos(2*Math.PI*(j+h/3)/l)));z.push(Math.exp(t-l*f))}w[l]=(z[0]+Math.exp(-1.5*beta)*(z[1]+z[2]))/3;if([3,4,8,16,32,64,128,256].includes(l))sample.push({l,w:w[l],holonomy_partition_ratios:z})}
 A(Math.abs(w[256]-q)<1e-10,'asymptotic weight');
 // exponential generating function with cycle weights w_l /2l
 let c=new Float64Array(5001);c[0]=1;let probs=[];for(let n=3;n<=5000;n++){let s=0;for(let l=3;l<=n;l++)s+=w[l]*c[n-l]/2;c[n]=s/n;if([8,32,128,512,2048,5000].includes(n))probs.push({n,connected:w[n]/(2*n*c[n])})}
 rows.push({b,mu,beta,bulk_free_energy:f,q,sample,probs})
}
return {rows,scope:"Static Z3 link holonomies genuinely enter free-fermion matter energies; grand canonical finite-density matter on degree-two graphs. Analytic periodic log partition integrand at finite b and finite mu implies exponentially small trapezoidal correction, w_l=q+O(exp(-c l)), hence EGF same singular exponent q/2. Numerically replace w_l by q beyond256 (verified endpoint), not dynamical temporal gauge fields."}
}
function nativeKrylov(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),sp=(a,b)=>m(a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1]),T=[];
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!sp(P[i],P[j]))for(let k=j+1;k<40;k++)if(!sp(P[i],P[k])&&!sp(P[j],P[k]))T.push([i,j,k]);A(T.length===160,'triangles');
let states=[{q:Array(40).fill(0),a:49}];for(let t of T)for(let z=1;z<9;z++){let q=Array(40).fill(0);for(let i of t)q[i]=z;states.push({q,a:1})}
let key=q=>q.join(''),D=new Map(states.map((s,i)=>[key(s.q),i])),num=0,den=0,rowSums=[];for(let {q,a} of states){let r=0;den+=a*a;for(let t of T){if(m(t.reduce((s,i)=>s+q[i]%3,0))||m(t.reduce((s,i)=>s+Math.floor(q[i]/3),0)))continue;for(let z=0;z<9;z++){let x=q.slice();for(let i of t)x[i]=m(x[i]%3+z%3)+3*m(Math.floor(x[i]/3)+Math.floor(z/3));let j=D.get(key(x));if(j!==undefined)r+=states[j].a}}num+=a*r;rowSums.push(r)}
let exact=num/(9*den);A(exact>160/9,'improvement');let predicted=(160*49**2+2*1280*49+137*1280)/(9*(49**2+1280));A(Math.abs(exact-predicted)<1e-12,'compressed matrix');
let eig=(297+Math.sqrt(23**2+4*1280))/18;return {states:states.length,integer_numerator:num,integer_denominator:9*den,rayleigh:exact,normalized:exact/160,optimal_two_dimensional_ritz:eig,previous_packing_lower:400/27,product_lower:160/9,upper:800/27,scope:"Exact integer variational certificate on native 40-register W33 triangle projector Hamiltonian; no full ground state or gap."}
}
console.log(JSON.stringify({gauge:gaugeCycles(),native:nativeKrylov()},null,2));
