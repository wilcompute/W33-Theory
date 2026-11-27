function verify(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},V=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**(n-1-j))%3)),hist=a=>{let h={};for(let x of a)h[x]=(h[x]||0)+1;return h};
let C=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>i===j?0:i===0||j===0?1:[1,4].includes((i-j+5)%5)?1:2));
let G=V(6).map(x=>x.concat(C[0].map((_,j)=>m(x.reduce((s,a,i)=>s+a*C[i][j],0))))),ref=[0,1,2].map(a=>G.find(x=>x[0]===a)),row=x=>x.slice(1).flatMap(a=>[+(a===1),+(a===2)]),M=G.map(x=>row(x).map((v,i)=>(v-row(ref[x[0]])[i]+9)%9));
let r=0,piv=[],mod9=x=>(x%9+9)%9,inv=x=>[1,2,4,5,7,8].find(y=>x*y%9===1);
for(let j=0;j<22;j++){let k=M.findIndex((x,i)=>i>=r&&x[j]%3);if(k<0)continue;[M[r],M[k]]=[M[k],M[r]];let u=inv(M[r][j]);M[r]=M[r].map(x=>mod9(x*u));for(let i=0;i<M.length;i++)if(i!==r&&M[i][j]){let f=M[i][j];M[i]=M[i].map((x,k)=>mod9(x-f*M[r][k]))}piv.push(j);r++}
let free=Array.from({length:22},(_,i)=>i).filter(i=>!piv.includes(i)),N=M.slice(r).map(x=>free.map(j=>x[j]/3)),s=0,np=[];
for(let j=0;j<free.length;j++){let k=N.findIndex((x,i)=>i>=s&&x[j]);if(k<0)continue;[N[s],N[k]]=[N[k],N[s]];let f=N[s][j];N[s]=N[s].map(x=>m(x*f));for(let i=0;i<N.length;i++)if(i!==s&&N[i][j]){let f=N[i][j];N[i]=N[i].map((x,k)=>m(x-f*N[s][k]))}np.push(j);s++}
let nf=free.map((_,i)=>i).filter(i=>!np.includes(i)),gens=[];
function lift(v){let x=Array(22).fill(0);free.forEach((j,i)=>x[j]=v[i]);piv.forEach((j,i)=>x[j]=mod9(-free.reduce((z,k)=>z+M[i][k]*x[k],0)));A(M.every(w=>mod9(w.reduce((s,a,i)=>s+a*x[i],0))===0),'lift');return x}
for(let i of nf){let v=free.map(()=>0);v[i]=1;np.forEach((j,k)=>v[j]=m(-N[k][i]));gens.push(lift(v))}
for(let i=0;i<free.length;i++){let v=free.map(()=>0);v[i]=3;gens.push(lift(v))}
let images=gens.map(x=>ref.map(w=>mod9(row(w).reduce((s,a,i)=>s+a*x[i],0))));A(images.every(w=>w.every(x=>x%3===0)),'magic obstruction');
let L=V(2),F=L.map(([a,b])=>L.map(([c,d])=>{let z=[0,0,0];for(let x=0;x<3;x++)for(let y=0;y<3;y++)for(let t=0;t<3;t++){if(y!==m(x+a)||t!==a||y!==m(t+c)||x!==c)continue;z[m(d*t-b*x)]++}A(z.reduce((s,x)=>s+x,0)===1,'flat');return z.indexOf(1)}));
for(let i=0;i<9;i++)for(let j=0;j<9;j++){let h=hist(F[i].map((x,k)=>m(x-F[j][k])));A(i===j?h[0]===9:h[0]===3&&h[1]===3&&h[2]===3,'unitary')}
return {golay:{unit_rank:r,three_torsion_rank:s,free_columns:free.length,solution_count:3**(2*free.length-s),generators:gens,logical_phase_images:images},recoupling:{dimension:9,modulus:1/3,phase_exponents:F}}
}
console.log(JSON.stringify(verify(),null,2));
