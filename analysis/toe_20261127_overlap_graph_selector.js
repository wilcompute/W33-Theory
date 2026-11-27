function graphSelector(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3;
function rank(M){M=M.map(r=>r.slice());if(!M.length)return 0;let t=0;for(let j=0;j<M[0].length;j++){let k=M.findIndex((x,i)=>i>=t&&x[j]);if(k<0)continue;[M[t],M[k]]=[M[k],M[t]];let c=M[t][j];M[t]=M[t].map(x=>m(x*c));for(let i=t+1;i<M.length;i++){let f=M[i][j];M[i]=M[i].map((x,k)=>m(x-f*M[t][k]))}t++}return t}
function graph(kind){
let N=16,adj=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>{if(i===j)return 0;let x=(j%4-i%4+4)%4,y=(Math.floor(j/4)-Math.floor(i/4)+4)%4;return +(kind==="rook"?(x===0||y===0):[[1,0],[3,0],[0,1],[0,3],[1,1],[3,3]].some(([a,b])=>a===x&&b===y))}));
for(let i=0;i<N;i++)for(let j=0;j<N;j++){let z=adj[i].reduce((s,x,k)=>s+x*adj[k][j],0);A(z===(i===j?6:2),'SRG')}
let C=[Array.from({length:N},(_,i)=>[i])];for(let d=1;d<=4;d++){let next=[];for(let c of C[d-1])for(let i=c[c.length-1]+1;i<N;i++)if(c.every(j=>adj[i][j]))next.push(c.concat(i));C.push(next)}
let r=[0];for(let d=1;d<=4;d++){let idx=new Map(C[d-1].map((x,i)=>[x.join(),i])),D=C[d].map(c=>{let v=C[d-1].map(()=>0);for(let i=0;i<c.length;i++)v[idx.get(c.filter((_,j)=>j!==i).join())]=i%2?2:1;return v});r.push(rank(D))}
return {kind,cliques:C.map(x=>x.length),boundary_ranks:r,betti:C.slice(0,4).map((c,i)=>c.length-r[i]-r[i+1]),euler:C.reduce((s,c,i)=>s+(-1)**i*c.length,0),adj_spectrum:[[6,1],[2,6],[-2,9]],laplacian_spectrum:[[0,1],[4,6],[8,9]]}
}
let graphs=["rook","shrikhande"].map(graph);A(graphs[0].betti.join()==="1,9,0,0"&&graphs[1].betti.join()==="1,2,1,0",'topology');
let heat=[.01,.1,.25,.5,1,2].map(t=>{let K=1+6*Math.exp(-4*t)+9*Math.exp(-8*t),ds=2*t*(24*Math.exp(-4*t)+72*Math.exp(-8*t))/K;return {t,K,spectral_dimension:ds}});
return {graphs,heat,scope:"Scalar adjacency or Laplacian spectral selectors fail to distinguish these two clique topologies. Not a smooth Calabi-Yau counterexample; higher-form spectra distinguish."}
}
function overlap(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},rows=[];
for(let n=3;n<=7;n++){
let k=n-2,B=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>m(Math.max(0,3-Math.abs(i-j))))),M=B.map(r=>r.slice()),r=0;
for(let j=0;j<k;j++){let t=M.findIndex((x,i)=>i>=r&&x[j]);if(t<0)continue;[M[t],M[r]]=[M[r],M[t]];let c=M[r][j];M[r]=M[r].map(x=>m(x*c));for(let i=r+1;i<k;i++){let f=M[i][j];M[i]=M[i].map((x,l)=>m(x-f*M[r][l]))}r++}
let D=9**k,pow=Array.from({length:k},(_,i)=>9**i),good=Array.from({length:k},()=>new Uint8Array(D));
for(let a=0;a<D;a++){let v=pow.map(p=>Math.floor(a/p)%9);for(let i=0;i<k;i++)good[i][a]=+(m(v.reduce((s,x,j)=>s+B[i][j]*(x%3),0))===0&&m(v.reduce((s,x,j)=>s+B[i][j]*Math.floor(x/3),0))===0)}
let x=new Float64Array(D).fill(1/Math.sqrt(D)),y=new Float64Array(D),lambda=0,res=0,it=0;
for(;it<500;it++){y.fill(0);for(let i=0;i<k;i++){let p=pow[i];for(let a=0;a<D;a++)if(Math.floor(a/p)%9===0&&good[i][a]){let z=0;for(let j=0;j<9;j++)z+=x[a+j*p];z/=9;for(let j=0;j<9;j++)y[a+j*p]+=z}}
lambda=0;let norm=0;for(let a=0;a<D;a++){lambda+=x[a]*y[a];norm+=y[a]*y[a]}res=Math.sqrt(Math.max(0,norm-lambda*lambda));norm=Math.sqrt(norm);if(res<1e-7)break;for(let a=0;a<D;a++)x[a]=y[a]/norm}
A(res<1e-5,'iteration');rows.push({n,cells:k,overlap_rank:r,radical:k-r,orbit_dimension:D,max_eigenvalue_zero_orbit:lambda,per_cell:lambda/k,residual:res,iterations:it})
}
return {rows,scope:"Nonnegative projector sum in zero affine translation orbit only. Perron eigenvalue of that block, not proven global across all affine sectors. No thermodynamic gap or symmetry breaking inferred."}
}
console.log(JSON.stringify({graph:graphSelector(),chain:overlap()},null,2));
