function bridge(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},V=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**(n-1-j))%3)),dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),B=(a,g,h)=>m(a[0]*g[1]*h[2]+g[0]*h[1]*a[2]-g[0]*a[1]*h[2]),W=V(3),id=a=>a[0]*9+a[1]*3+a[2];
let L=[];
for(let a of W){let R=W.filter(g=>W.every(h=>B(a,g,h)===B(a,h,g))),d=Math.sqrt(27/R.length),chars=[...new Map(W.map(k=>[R.map(g=>dot(k,g)).join(),k])).values()];for(let k of chars){let chi={};for(let g of R)chi[id(g)]=m(-2*B(a,g,g)+dot(k,g));let t=chi[id(a)],H;if(a[0]||a[1])H={kind:'noncentral',u:a.slice(0,2),z:a[2],t};else if(a[2])H={kind:'central3',r:k[2],z:a[2],t};else H={kind:'central1',r:k[2],k:k.slice(0,2),t:0};L.push({a,d,chi,t,H})}}
const G=W, mul=(a,b)=>[m(a[0]+b[0]),m(a[1]+b[1]),m(a[2]+b[2]+2*(a[0]*b[1]-a[1]*b[0]))],inv=a=>a.map(x=>m(-x)),eq=(a,b)=>a.join()===b.join(),conj=(g,a)=>mul(mul(g,a),inv(g));
function rep(H){return H.kind==='noncentral'?[...H.u,0]:[0,0,H.r]}
function char(H,g){if(H.kind==='central1')return [1,dot(H.k,g.slice(0,2))];if(H.kind==='central3')return g[0]||g[1]?[0,0]:[3,m(H.z*g[2])];let j=[0,1,2].find(j=>H.u.every((x,i)=>m(x*j)===g[i]));A(j!==undefined,'centralizer');return [1,m(j*H.t+H.z*g[2])]}
const cen=H=>H.kind==='noncentral'?9:27;
let comparisons=0;
for(let a of L)for(let b of L){let z=[0,0,0],x=rep(a.H),y=rep(b.H);
for(let g of G){let y1=conj(g,y);if(!eq(mul(x,y1),mul(y1,x)))continue;let u=char(a.H,y1),v=char(b.H,conj(inv(g),x));z[m(-u[1]-v[1])]+=u[0]*v[0]}
let t=[0,0,0],e=a.chi[id(b.a)],f=b.chi[id(a.a)];if(e!==undefined&&f!==undefined)t[m(-e-f)]=a.d*b.d*cen(a.H)*cen(b.H)/27;
A(z[0]-z[1]===t[0]-t[1]&&z[2]-z[1]===t[2]-t[1],'H27 modular mapping');comparisons++}
for(let a of L){let [d,t]=char(a.H,rep(a.H));A(d>0&&t===a.t,'spin')}
A(new Set(L.map(x=>JSON.stringify(x.H))).size===105,'bijection');
 // Discrete Wigner function of CCZ|+++>. Use gross phase-point convention and exact root sums.
 let hist={},sum=0,l1=0,negative=0;const f=x=>m(x[0]*x[1]*x[2]);
 for(let u of W)for(let v of W){let z=[0,0,0];for(let x of W){let plus=u.map((a,i)=>m(a+2*x[i])),minus=u.map((a,i)=>m(a-2*x[i]));z[m(f(plus)-f(minus)-dot(v,x))]++}A(z[1]===z[2],'real Wigner');let n=z[0]-z[1];hist[n]=(hist[n]||0)+1;sum+=n;l1+=Math.abs(n);if(n<0)negative++}
 A(sum===729,'normalization');
 return {H27_double:{sectors:L.length,S_entries_compared:comparisons,T_entries_compared:L.length,explicit_label_map:L.map(x=>({flux:x.a,spin:x.t,projective_char:x.chi,group_double:x.H}))},cocycle_magic:{Wigner_numerators_over_729:hist,negative_entries:negative,l1:l1/729,mana_ln:Math.log(l1/729)}}
}
console.log(JSON.stringify(bridge(),null,2));
