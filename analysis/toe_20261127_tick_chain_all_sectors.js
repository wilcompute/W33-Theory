function sectors(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},rank=M=>{M=M.map(r=>r.slice());let r=0;for(let j=0;j<M[0].length;j++){let t=M.findIndex((x,i)=>i>=r&&x[j]);if(t<0)continue;[M[t],M[r]]=[M[r],M[t]];M[r]=M[r].map(x=>m(x*M[r][j]));for(let i=r+1;i<M.length;i++){let f=M[i][j];M[i]=M[i].map((x,k)=>m(x-f*M[r][k]))}r++}return r};
let census=[];for(let n=3;n<=39;n++){let k=n-2,B=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>m(Math.max(0,3-Math.abs(i-j))))),V=Array.from({length:n},(_,i)=>[[1,0],[0,1],[-1,-1]][i%3]),G=Array.from({length:2},(_,i)=>Array.from({length:2},(_,j)=>m(V.reduce((s,v)=>s+v[i]*v[j],0))));let nullity=k-rank(B);A(nullity===2-rank(G),'radical identity');census.push({n,nullity})}
let results=[];for(let n of [3,6]){let k=n-2,B=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>m(Math.max(0,3-Math.abs(i-j))))),D=9**k,pow=Array.from({length:k},(_,i)=>9**i);
let col=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>B[j][i])),base=rank(col),e=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>+(i===j))).find(v=>rank(col.concat([v]))>base);A(e,'coset complement');
for(let c=0;c<9;c++){let good=Array.from({length:k},()=>new Uint8Array(D));for(let a=0;a<D;a++){let v=pow.map(p=>Math.floor(a/p)%9);for(let i=0;i<k;i++)good[i][a]=+(m(e[i]*(c%3)+v.reduce((s,x,j)=>s+B[i][j]*(x%3),0))===0&&m(e[i]*Math.floor(c/3)+v.reduce((s,x,j)=>s+B[i][j]*Math.floor(x/3),0))===0)}
let x=new Float64Array(D).fill(1/Math.sqrt(D)),y=new Float64Array(D),l=0,err=0,it=0;
for(;it<500;it++){y.fill(0);for(let i=0;i<k;i++)for(let a=0;a<D;a++)if(Math.floor(a/pow[i])%9===0&&good[i][a]){let z=0;for(let j=0;j<9;j++)z+=x[a+j*pow[i]];for(let j=0;j<9;j++)y[a+j*pow[i]]+=z/9}
l=0;let norm=0;for(let a=0;a<D;a++){l+=x[a]*y[a];norm+=y[a]**2}err=0;for(let a=0;a<D;a++)err+=(y[a]-l*x[a])**2;err=Math.sqrt(err);if(err<1e-10||norm===0)break;for(let a=0;a<D;a++)x[a]=y[a]/Math.sqrt(norm)}
results.push({n,sector:c,lambda:l,residual:err,it});A(err<1e-8,'converged')
}}
return {radicals:census,affine_sectors:results,scope:"All distinct affine syndrome cosets for n3 and n6. For n4,5,7 full rank implies all orbits unitarily equivalent. Perron method starts positive, numerical maximum in each sector."}
}
console.log(JSON.stringify(sectors(),null,2));
