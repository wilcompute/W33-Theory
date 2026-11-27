function explicitSubcode(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
function basis(rows,p=3){let R=[],piv=[];for(let a of rows){let v=a.slice();for(let i=0;i<R.length;i++){let f=v[piv[i]];if(f)v=v.map((x,j)=>(x-f*R[i][j]+p*p)%p)}let k=v.findIndex(Boolean);if(k>=0){let inv=1;while(inv*v[k]%p!==1)inv++;R.push(v.map(x=>x*inv%p));piv.push(k)}}return R}
let B=basis(C),words=[Array(12).fill(0)];for(let r of B)words=words.flatMap(v=>[0,1,2].map(t=>v.map((x,i)=>m(x+t*r[i]))));let ones=words.find(v=>v.every(Boolean));B=B.map(v=>v.map((x,i)=>m(x*ones[i])));A(B.length===6&&words.filter(v=>v.some(Boolean)).every(v=>v.filter(Boolean).length>=6),"Golay");
const mod=x=>(x%11+11)%11,inv=x=>Array.from({length:10},(_,i)=>i+1).find(y=>mod(x*y)===1),G=new Map();
for(let a=0;a<11;a++)for(let b=0;b<11;b++)for(let c=0;c<11;c++)for(let d=0;d<11;d++)if(mod(a*d-b*c)===1){let p=Array.from({length:12},(_,x)=>{let u=x===11?a:mod(a*x+b),v=x===11?c:mod(c*x+d);return v?mod(u*inv(v)):11});G.set(p.join(","),p)}
let P=[...G.values()];A(P.length===660,"group");A(new Set(P.map(p=>p[0]+","+p[1])).size===132,"2transitive");
let seed=193,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},permute=(B,p)=>B.map(v=>p.map(i=>v[i])),samples=[];
for(let i=0;i<12;i++){let p=Array.from({length:12},(_,j)=>j);for(let j=11;j>0;j--){let k=Math.floor(rng()*(j+1));[p[j],p[k]]=[p[k],p[j]]}samples.push(permute(B,p))}
let dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),orbits=samples.map(b=>P.map(p=>permute(b,p))),gram=samples.map((b,i)=>samples.map((_,j)=>orbits[j].reduce((s,c)=>{let r=basis(b.map(v=>c.map(w=>dot(v,w)))).length;return s+3**(10-2*r)},0)));
A(gram.every((r,i)=>r.every((v,j)=>v===gram[j][i])),"symmetric");
let rank=basis(gram.map(r=>r.map(x=>x%101)),101).length;
A(rank>=6,"independent");

let unit=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>+(i===j)));
function pairCount(b,c){let R=basis(b.concat(c));if(R.length===11)return 66;let piv=R.map(r=>r.findIndex(Boolean)),classes=new Map();for(let v of unit){let w=v.slice();for(let j=0;j<R.length;j++){let f=w[piv[j]];if(f)w=w.map((x,k)=>m(x-f*R[j][k]))}let key=w.join("");classes.set(key,(classes.get(key)||0)+1)}return [...classes.values()].reduce((s,n)=>s+n*(n-1)/2,0)}
let err=samples.map((b,i)=>samples.map((_,j)=>orbits[j].reduce((s,c)=>{let r=basis(b.map(v=>c.map(w=>dot(v,w)))).length;return s+3**(10-2*r)*pairCount(b,c)},0)));
A(err.every((r,i)=>r.every((v,j)=>v===err[j][i])),"error symmetric");
{
let n=12,G=gram.map(r=>r.map(x=>x/(660*59049))),Q=err.map(r=>r.map(x=>x/(66*660*59049))),L=Array.from({length:n},()=>Array(n).fill(0));
for(let i=0;i<n;i++)for(let j=0;j<=i;j++){let x=G[i][j];for(let k=0;k<j;k++)x-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(x):x/L[j][j];A(Number.isFinite(L[i][j]),"Cholesky")}
let C=Array.from({length:n},()=>Array(n).fill(0));for(let j=0;j<n;j++)for(let i=n-1;i>=0;i--){let x=+(i===j);for(let k=i+1;k<n;k++)x-=L[k][i]*C[k][j];C[i][j]=x/L[i][i]}
let tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),mul=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((s,x,k)=>s+x*b[k][j],0))),W=mul(tr(C),mul(Q,C)),V=unit.map(r=>r.slice());
for(let iter=0;iter<3000;iter++){let i=0,j=1,largest=0;for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)if(Math.abs(W[a][b])>largest){largest=Math.abs(W[a][b]);i=a;j=b}if(largest<1e-14)break;let t=.5*Math.atan2(2*W[i][j],W[j][j]-W[i][i]),c=Math.cos(t),s=Math.sin(t),J=unit.map(r=>r.slice());J[i][i]=J[j][j]=c;J[i][j]=s;J[j][i]=-s;W=mul(tr(J),mul(W,J));V=mul(V,J)}
let idx=Array.from({length:n},(_,i)=>i).sort((a,b)=>W[a][a]-W[b][b]),lambda=idx.map(i=>W[i][i]),mu=(lambda[5]+lambda[6])/2,ortho=Array.from({length:n},()=>Array(6).fill(0));
for(let k=0;k<6;k++){let a=idx[k],b=idx[11-k],gap=lambda[11-k]-lambda[k],x=gap<1e-14?1:Math.sqrt((lambda[11-k]-mu)/gap),y=Math.sqrt(Math.max(0,1-x*x));for(let j=0;j<n;j++)ortho[j][k]=x*V[j][a]+y*V[j][b]}
let coeff=mul(C,ortho),norm=mul(tr(coeff),mul(G,coeff)),comp=mul(tr(coeff),mul(Q,coeff)),maxerr=(a,t)=>Math.max(...a.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-t*+(i===j)))));
A(maxerr(norm,1)<1e-10&&maxerr(comp,mu)<1e-10,"compression");
return {sample_bases:samples,gram_numerators:gram,gram_denominator:660*59049,error_numerators:err,error_denominator:66*660*59049,eigenvalues:lambda,compression_scalar:mu,logical_basis_coefficients:coeff,orthonormality_residual:maxerr(norm,1),KL_residual:maxerr(comp,mu),scope:"Exact Gram and balanced X pair compression matrix on PSL2(11)-averaged Golay states; numerical Cholesky/Jacobi and paired eigenvectors implement the analytic existence proof. All weight<=2 errors reduce by symmetry; coefficients numerical not exact algebraic, no recovery circuit."}
}
}

console.log(JSON.stringify(explicitSubcode(),null,2));
