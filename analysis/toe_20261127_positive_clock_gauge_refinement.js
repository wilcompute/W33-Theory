function gauge(){
const A=(x,s)=>{if(!x)throw Error(s)},m=(x,n=3)=>(x%n+n)%n,V=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**j)%3)).map(v=>v.concat(m(-v.reduce((s,x)=>s+x,0)))),j=v=>v.reduce((s,x)=>s+(x===2?-1:x),0)/3;
let points=Array.from({length:5},(_,i)=>[Math.cos(2*Math.PI*i/9),Math.cos(4*Math.PI*i/9)]),rows=[];
let test=mu=>{let x=Math.exp(-mu),y=Math.exp(-4*mu);for(let i=0;i<5;i++)for(let k=i+1;k<5;k++)for(let l=k+1;l<5;l++){let [a,b,c]=[points[i],points[k],points[l]],D=(a[0]-c[0])*(b[1]-c[1])-(a[1]-c[1])*(b[0]-c[0]),u=((x-c[0])*(b[1]-c[1])-(y-c[1])*(b[0]-c[0]))/D,v=((a[0]-c[0])*(y-c[1])-(a[1]-c[1])*(x-c[0]))/D,w=1-u-v;if(Math.min(u,v,w)>=-1e-12){let p=Array(5).fill(0);p[i]=u;p[k]=v;p[l]=w;return p}}return null};
let lo=0,hi=1;for(let k=0;k<60;k++){let u=(lo+hi)/2;if(test(u))hi=u;else lo=u}
for(let mu of [.01,.05,.1,.2,.5,1,2,4]){let p=test(mu),error=null;if(p){error=Math.max(...V.map(v=>Math.abs(p.reduce((s,x,k)=>s+x*Math.cos(2*Math.PI*k*j(v)/9),0)-Math.exp(-mu*j(v)**2))));A(error<1e-10,'exact amplitude')}rows.push({mu,positive_clock_distribution:p,error})}
let moves=0;for(let f of V)for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)for(let s of [1,2]){let g=f.slice();g[a]=m(g[a]+s);g[b]=m(g[b]-s);let carry=v=>m(v.reduce((z,x)=>z+(x===2?0:x+1),0),27);let r=m(carry(f)+carry(g)-carry(f),27);A(r===3*j(g)+6,'carry update');A(m(r-carry(g),27)===0,'uncompute');moves++}
return {min_positive_mu_numeric:hi,analytic_condition:"(1-exp(-4mu))/(1-exp(-mu)) <= 2(1+cos(2pi/9)); necessary, saturated on 0 and ±1 at onset",rows,local_carry_transitions:moves,scope:"Positive distribution of coherent clock phase labels, not a thermal trace of unitary. Ancilla prepared in sqrt probabilities, controlled phase, unprepare/postselect; weights chosen to match target. Exact local flux updates for arbitrary opposite face pair, not full spacetime matter evolution or photon pole."}
}
function refinement(){
const A=(x,s)=>{if(!x)throw Error(s)},m=x=>(x%3+3)%3,rows=[];
for(let t of [.1,.5,1,2,4]){let r=Math.exp(-t),w=x=>1+r*(x===0?2:-1),vals=[];
for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){let actual=[0,1,2].reduce((s,g)=>s+w(m(g+a))*w(m(g+b))*w(m(g+c)),0)/3,pair=[a-b,a-c,b-c].reduce((s,d)=>s+Math.cos(2*Math.PI*d/3),0),triple=Math.cos(2*Math.PI*(a+b+c)/3),pred=1+2*r*r*pair+2*r**3*triple;A(Math.abs(actual-pred)<1e-12,'star exact');vals.push({pair,triple,actual})}
let [u,v,z]=[vals.find(x=>x.pair===3),vals.find(x=>Math.abs(x.pair)<1e-10),vals.find(x=>x.pair< -1)].map(x=>-Math.log(x.actual)),J=(u-z)/4.5,K=(v-z-1.5*J)/(-1.5),C=z+1.5*J-K;A(vals.every(x=>Math.abs(-Math.log(x.actual)-(C+J*x.pair+K*x.triple))<1e-10),'log closure');rows.push({t,C,J,K,series_refinement_t:2*t})}
let four=[];for(let a of [.5,1,2])for(let b of [.5,1,2]){let pts=Array.from({length:6},(_,i)=>{let theta=2*Math.PI*(i%3)/3;return i<3?[a*Math.cos(theta),a*Math.sin(theta),0,0]:[0,0,b*Math.cos(theta),b*Math.sin(theta)]});
function det(M){if(M.length===1)return M[0][0];return M[0].reduce((s,x,i)=>s+(-1)**i*x*det(M.slice(1).map(r=>r.filter((_,j)=>j!==i))),0)}
let vol=Array.from({length:6},(_,i)=>{let v=pts.filter((_,j)=>j!==i);return Math.abs(det(v.slice(1).map(r=>r.map((x,j)=>x-v[0][j]))))/24});
let left=vol.slice(0,3).reduce((s,x)=>s+x,0),right=vol.slice(3).reduce((s,x)=>s+x,0);A(Math.abs(left-right)<1e-12,'4d volume');
four.push({a,b,left,right})}
return {rows,four,scope:"Exact induced pair and triple interactions of Z3 internal edge integration; log expands in equality classes, not a closed repeated 3D RG. 4D 3-3 circuit of two orthogonal equilateral triangles, equal flat total 4-volume. Two internal triangle fluxes on disjoint edge sets independently uniform; their heat kernel ratio varies for any finite coupling, no constant normalization. No gravitational fluctuation determinant or continuum tensor modes."}
}
console.log(JSON.stringify({gauge:gauge(),refinement:refinement()},null,2));
