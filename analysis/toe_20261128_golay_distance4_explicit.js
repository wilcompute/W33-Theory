function explicit4(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
function basis(rows,p=3){let R=[],piv=[];for(let a of rows){let v=a.slice();for(let i=0;i<R.length;i++){let f=v[piv[i]];if(f)v=v.map((x,j)=>(x-f*R[i][j]+p*p)%p)}let k=v.findIndex(Boolean);if(k>=0){let inv=1;while(inv*v[k]%p!==1)inv++;R.push(v.map(x=>x*inv%p));piv.push(k)}}return R}
let B=basis(C),words=[Array(12).fill(0)];for(let r of B)words=words.flatMap(v=>[0,1,2].map(t=>v.map((x,i)=>m(x+t*r[i]))));let ones=words.find(v=>v.every(Boolean));B=B.map(v=>v.map((x,i)=>m(x*ones[i])));A(B.length===6&&words.filter(v=>v.some(Boolean)).every(v=>v.filter(Boolean).length>=6),"Golay");
const mod=x=>(x%11+11)%11,inv=x=>Array.from({length:10},(_,i)=>i+1).find(y=>mod(x*y)===1),G=new Map();
for(let a=0;a<11;a++)for(let b=0;b<11;b++)for(let c=0;c<11;c++)for(let d=0;d<11;d++)if(mod(a*d-b*c)){let p=Array.from({length:12},(_,x)=>{let u=x===11?a:mod(a*x+b),v=x===11?c:mod(c*x+d);return v?mod(u*inv(v)):11});G.set(p.join(","),p)}
let P=[...G.values()];A(P.length===1320&&new Set(P.map(p=>p.slice(0,3).join(","))).size===1320,"3transitive");
const mask=4095,pack=v=>v.reduce((s,x,i)=>s|((x===1?1:x===2?4096:0)<<i),0),neg=x=>((x&mask)<<12)|(x>>>12);
function add(x,y){let a=x&mask,b=x>>>12,c=y&mask,d=y>>>12;return (((a&~(c|d))|(c&~(a|b))|(b&d))&mask)|((((b&~(c|d))|(d&~(a|b))|(a&c))&mask)<<12)}
function canonical(rows){let r=rows.slice(),n=0;for(let j=0;j<12;j++){let b=1<<j,k=r.findIndex((x,i)=>i>=n&&((x|x>>>12)&b));if(k<0)continue;[r[n],r[k]]=[r[k],r[n]];if(r[n]&(b<<12))r[n]=neg(r[n]);for(let i=0;i<r.length;i++)if(i!==n){if(r[i]&b)r[i]=add(r[i],neg(r[n]));else if(r[i]&(b<<12))r[i]=add(r[i],r[n])}n++}return r.slice(0,n)}
let seed=193,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},permute=(B,p)=>B.map(v=>p.map(i=>v[i])),samples=[],orbits=[],used=new Set(),tries=0;
for(let i=0;i<250&&samples.length<46;i++){tries++;let p=Array.from({length:12},(_,j)=>j);for(let j=11;j>0;j--){let k=Math.floor(rng()*(j+1));[p[j],p[k]]=[p[k],p[j]]}let b=permute(B,p),key=canonical(b.map(pack)).join(",");if(used.has(key))continue;let orbit=new Map();for(let q of P){let r=canonical(permute(b,q).map(pack)),k=r.join(",");orbit.set(k,r);used.add(k)}samples.push(b);orbits.push([...orbit.values()])}
let packed=samples.map(b=>b.map(pack)),gram=packed.map((b,i)=>orbits.map(o=>o.reduce((s,c)=>s+3**(2*(11-canonical(b.concat(c)).length)),0)*(1320/o.length)));
A(gram.every((r,i)=>r.every((v,j)=>v===gram[j][i])),"symmetric");let rank=basis(gram.map(r=>r.map(x=>x%101)),101).length;

let ix=[];for(let i=0;i<samples.length&&ix.length<26;i++){let j=ix.concat(i);if(basis(j.map(a=>j.map(b=>gram[a][b]%101)),101).length===j.length)ix=j}A(ix.length===26,"rank26");
let n=ix.length,U=Array.from({length:12},(_,i)=>1<<i),trip=[];for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)for(let k=j+1;k<12;k++)trip.push([i,j,k]);
function count(b,c){let r=b.concat(c),d=b.map(()=>0).concat(c),h=0,p=[];for(let j=0;j<12;j++){let bit=1<<j,k=r.findIndex((x,i)=>i>=h&&((x|x>>>12)&bit));if(k<0)continue;[r[h],r[k]]=[r[k],r[h]];[d[h],d[k]]=[d[k],d[h]];if(r[h]&(bit<<12)){r[h]=neg(r[h]);d[h]=neg(d[h])}for(let i=h+1;i<r.length;i++){if(r[i]&bit){r[i]=add(r[i],neg(r[h]));d[i]=add(d[i],neg(d[h]))}else if(r[i]&(bit<<12)){r[i]=add(r[i],r[h]);d[i]=add(d[i],d[h])}}p.push(j);h++}
let rem=[],part=[];for(let u of U){let t=0;for(let i=0;i<h;i++){let bit=1<<p[i];if(u&bit){u=add(u,neg(r[i]));t=add(t,d[i])}else if(u&(bit<<12)){u=add(u,r[i]);t=add(t,neg(d[i]))}}rem.push(u);part.push(t)}
let pair=0,rank1=0,iso=0,sym=0;for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)if(rem[i]===rem[j])pair++;
let val=(v,j)=>(v>>j&1)+2*(v>>(12+j)&1);
for(let [i,j,k] of trip){if(add(add(rem[i],rem[j]),rem[k])===0)rank1++;if(rem[i]===rem[j]&&rem[j]===rem[k]){iso++;let v=add(part[i],neg(part[k])),phase=m(2-val(v,j)+val(v,k));sym+=phase===0?2:-1}}
return [pair,rank1,iso,sym].map(v=>v*3**(2*(11-h)))}
let nums=Array.from({length:4},()=>Array.from({length:n},()=>Array(n).fill(0)));
for(let i=0;i<n;i++)for(let j=i;j<n;j++){let o=orbits[ix[j]],v=[0,0,0,0];for(let c of o){let a=count(packed[ix[i]],c);for(let k=0;k<4;k++)v[k]+=a[k]}for(let k=0;k<4;k++)nums[k][i][j]=nums[k][j][i]=v[k]*1320/o.length}
let g=ix.map(i=>ix.map(j=>gram[i][j]/(1320*59049))),den=[66,220,220,440].map(x=>x*1320*59049),Q=nums.map((a,k)=>a.map(r=>r.map(x=>x/den[k])));
let L=Array.from({length:n},()=>Array(n).fill(0));for(let i=0;i<n;i++)for(let j=0;j<=i;j++){let x=g[i][j];for(let k=0;k<j;k++)x-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(x):x/L[j][j];A(Number.isFinite(L[i][j]),"Cholesky")}
let T=Array.from({length:n},()=>Array(n).fill(0));for(let j=0;j<n;j++)for(let i=n-1;i>=0;i--){let x=+(i===j);for(let k=i+1;k<n;k++)x-=L[k][i]*T[k][j];T[i][j]=x/L[i][i]}
let tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),mul=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((s,x,k)=>s+x*b[k][j],0))),W=Q.map(a=>mul(tr(T),mul(a,T))),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),mv=(a,v)=>a.map(r=>dot(r,v)),orth=[],vs=[];
function project(v){for(let k=0;k<2;k++)for(let u of orth){let a=dot(u,v);v=v.map((x,i)=>x-a*u[i])}return v}
function insert(v){v=project(v);let a=Math.sqrt(dot(v,v));if(a>1e-11)orth.push(v.map(x=>x/a))}
for(let k=0;k<6;k++){let cand=Array.from({length:n},(_,i)=>project(Array.from({length:n},(_,j)=>+(i===j)))).sort((a,b)=>dot(b,b)-dot(a,a))[0],norm=Math.sqrt(dot(cand,cand));A(norm>1e-6,"greedy");let v=cand.map(x=>x/norm);vs.push(v);insert(v);for(let a of W)insert(mv(a,v))}
let mat=[Array(6).fill(1),...W.map(a=>vs.map(v=>dot(v,mv(a,v))))],piv=[],r=0;for(let j=0;j<6&&r<5;j++){let k=r;for(let i=r+1;i<5;i++)if(Math.abs(mat[i][j])>Math.abs(mat[k][j]))k=i;if(Math.abs(mat[k][j])<1e-12)continue;[mat[r],mat[k]]=[mat[k],mat[r]];let f=mat[r][j];mat[r]=mat[r].map(x=>x/f);for(let i=0;i<5;i++)if(i!==r){let a=mat[i][j];mat[i]=mat[i].map((x,k)=>x-a*mat[r][k])}piv.push(j);r++}
let free=Array.from({length:6},(_,i)=>i).find(i=>!piv.includes(i)),z=Array(6).fill(0);z[free]=1;for(let i=0;i<r;i++)z[piv[i]]=-mat[i][free];let a=z.filter(x=>x>0).reduce((s,x)=>s+x,0),b=-z.filter(x=>x<0).reduce((s,x)=>s+x,0),logical=[1,-1].map(sign=>Array.from({length:n},(_,j)=>vs.reduce((s,v,i)=>s+Math.sqrt(Math.max(0,sign*z[i])/(sign===1?a:b))*v[j],0))),coef=mul(T,tr(logical)),ng=mul(tr(coef),mul(g,coef)),cs=Q.map(q=>mul(tr(coef),mul(q,coef))),res=Math.max(...cs.map(c=>Math.max(Math.abs(c[0][1]),Math.abs(c[0][0]-c[1][1]))),Math.abs(ng[0][0]-1),Math.abs(ng[1][1]-1),Math.abs(ng[0][1]));
A(res<1e-9,"compression");return {sample_indices:ix,sample_bases:ix.map(i=>samples[i]),gram:ix.map(i=>ix.map(j=>gram[i][j])),gram_denominator:1320*59049,compression_numerators:nums,compression_denominators:den,logical_coefficients:coef,compressed:cs,orthonormality:ng,residual:res,scope:"Exact orbit-averaged pair/triple matrix elements via C+D quotient and tracked D contribution. Hermitian Weyl convention W(x,z)=omega^(x.z/2) X^x Z^z. Six greedy vectors, Radon relation, numerical logical basis. Analytic existence from previous certificate. Symmetry reduction of weight<=3 assumed from prior proof. No physical preparation or recovery."}}

console.log(JSON.stringify(explicit4(),null,2));
