function tensorCritical(){
const A=(v,s)=>{if(!v)throw Error(s)},P=[[0,0],[1,1],[2,2],[0,1],[0,2],[1,2]],mons=d=>{let out=[];for(let a=0;a<=d;a++)for(let b=0;b<=d-a;b++)out.push([a,b,d-a-b]);return out},key=v=>v.join(','),add=(a,b)=>a.map((x,i)=>x+b[i]),unit=i=>[0,1,2].map(j=>+(i===j));
function kernel(M,p){
let mod=x=>p?((x%p)+p)%p:x,inv=x=>p?Array.from({length:p},(_,i)=>i).find(i=>mod(x*i)===1):1/x;M=M.map(r=>r.map(mod));let r=0,piv=[];for(let j=0;j<M[0].length;j++){let k=M.findIndex((x,i)=>i>=r&&Math.abs(x[j])>1e-9);if(k<0)continue;[M[r],M[k]]=[M[k],M[r]];let c=inv(M[r][j]);M[r]=M[r].map(x=>mod(x*c));for(let i=0;i<M.length;i++)if(i!==r){let f=M[i][j];M[i]=M[i].map((x,k)=>mod(x-f*M[r][k]))}piv.push(j);r++}
let basis=[];for(let j=0;j<M[0].length;j++)if(!piv.includes(j)){let v=M[0].map(()=>0);v[j]=1;piv.forEach((k,i)=>v[k]=mod(-M[i][j]));basis.push(v)}return {rank:r,basis}}
function symbol(d,type,p){
let I=mons(d),O=mons(d+(type==='X'?2:1)),N=6*I.length,R=Array.from({length:O.length*(type==='X'?1:3)},()=>Array(N).fill(0)),idx=new Map(O.map((v,i)=>[key(v),i]));
for(let c=0;c<6;c++){let [i,j]=P[c];for(let k=0;k<I.length;k++){let v=I[k],col=c*I.length+k;if(type==='X'){
let terms=i===j?[0,1,2].filter(a=>a!==i).map(a=>[add(unit(a),unit(a)),1]):[[add(unit(i),unit(j)),-2]];for(let [u,w] of terms)R[idx.get(key(add(u,v)))][col]+=w
}else{R[j*O.length+idx.get(key(add(unit(i),v)))][col]++;R[i*O.length+idx.get(key(add(unit(j),v)))][col]++}}}
let K=kernel(R,p);return {type,degree:d,prime:p,variables:N,rank:K.rank,nullity:K.basis.length,basis:K.basis,monomials:I}}
let symbols=[];for(let p of [0,3])for(let t of ['X','Z'])for(let d=0;d<=2;d++)symbols.push(symbol(d,t,p));
for(let p of [0,3]){let x=symbols.find(s=>s.prime===p&&s.type==='X'&&s.degree===1),z=symbols.find(s=>s.prime===p&&s.type==='Z'&&s.degree===1);A(x.nullity===8&&z.nullity===0,'order obstruction')}
let X=symbols.find(s=>s.prime===3&&s.type==='X'&&s.degree===1),Z=symbols.find(s=>s.prime===3&&s.type==='Z'&&s.degree===2),mom=[];
for(let a=0;a<27;a++){let k=[a%3,Math.floor(a/3)%3,Math.floor(a/9)];if(!a)continue;let evals=s=>s.basis.map(v=>P.map((_,i)=>s.monomials.reduce((r,u,j)=>r+v[i*s.monomials.length+j]*u.reduce((z,n,l)=>z*k[l]**n,1),0)%3)),x=evals(X),z=evals(Z),g=Array.from({length:3},(_,a)=>P.map(([i,j])=>(k[i]*+(j===a)+k[j]*+(i===a))%3));let rank=M=>kernel(M,3).rank;
let rx=rank(x),rz=rank(z),rg=rank(g),pair=x.map(u=>z.map(v=>u.reduce((s,x,i)=>s+x*v[i],0)%3));mom.push({k,rankX:rx,rankZ:rz,rankGauge:rg,pairing:rank(pair)});A(rx===5&&rz===3&&rg===3&&rank(pair)===2,'momentum ranks')}
function eigen(n,k){
let delta2=2*Math.PI/n,a=k*k/(2*delta2),b=k**4/(2*delta2),H=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?2*a+2*b*(1-Math.cos(2*Math.PI*i/n)):((i-j+n)%n===1||(j-i+n)%n===1)?-a:0));
let max=0,sweep=0;for(;sweep<40;sweep++){max=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let x=H[i][j];max=Math.max(max,Math.abs(x));if(Math.abs(x)<1e-12)continue;let theta=.5*Math.atan2(2*x,H[j][j]-H[i][i]),c=Math.cos(theta),s=Math.sin(theta),aa=H[i][i],bb=H[j][j];H[i][i]=c*c*aa-2*c*s*x+s*s*bb;H[j][j]=s*s*aa+2*c*s*x+c*c*bb;H[i][j]=H[j][i]=0;for(let l=0;l<n;l++)if(l!==i&&l!==j){let u=H[l][i],v=H[l][j];H[l][i]=H[i][l]=c*u-s*v;H[l][j]=H[j][l]=s*u+c*v}}if(max<1e-10)break}
A(max<1e-9,'diagonalization');let e=H.map((r,i)=>r[i]).sort((a,b)=>a-b);return {n,k,gap:e[1]-e[0],gap_over_k3:(e[1]-e[0])/k**3,ground:e[0],sweeps:sweep}}
let spectrum=[];for(let n of [3,9,27,81])for(let k of [.5,.25,.125])spectrum.push(eigen(n,k));
return {symbols:symbols.map(({basis,...s})=>s),momentum_ranks:mom,spectrum,scope:'homogeneous local-symbol constraints over R (floating rank for tiny integer matrices) and F3 (exact); finite rotor mode toy, not full local interacting tensor lattice or graviton phase'}
}
console.log(JSON.stringify(tensorCritical(),null,2));
