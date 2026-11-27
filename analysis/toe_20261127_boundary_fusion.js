function defects(){
 const mod=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},V=Array.from({length:9},(_,i)=>[Math.floor(i/3),i%3]),id=v=>3*v[0]+v[1],add=(a,b)=>id(V[a].map((x,i)=>mod(x+V[b][i]))),dot=(a,b)=>mod(V[a][0]*V[b][0]+V[a][1]*V[b][1]);
 const H=[[0],...[1,3,4,5].map(a=>[0,a,add(a,a)].sort((x,y)=>x-y)),V.map(id),V.map(id),V.map(id)],t=[0,0,0,0,0,0,1,2],B=(i,j,g,h)=>mod((t[i]-t[j])*V[g][0]*V[h][1]);
 const X=H.map(h=>{let rep=V.map(id).map(a=>Math.min(...h.map(b=>add(a,b))));return {rep,points:[...new Set(rep)]}}),pairs=Array.from({length:8},()=>Array(8)),all=[];
 for(let i=0;i<8;i++)for(let j=0;j<8;j++){
 let S=H[i].filter(a=>H[j].includes(a)),R=S.filter(g=>S.every(h=>B(i,j,g,h)===B(i,j,h,g))),dim=Math.sqrt(S.length/R.length),chars=[...new Map(V.map(id).map(k=>[R.map(g=>dot(k,g)).join(),k])).values()],seen=new Set(),list=[];
 for(let x of X[i].points)for(let y of X[j].points){let key=9*x+y;if(seen.has(key))continue;let orbit=new Map();for(let u=0;u<9;u++){let xy=9*X[i].rep[add(x,u)]+X[j].rep[add(y,u)];if(!orbit.has(xy))orbit.set(xy,u);seen.add(xy)}
 for(let c of chars){let a={id:all.length,i,j,d:dim*Math.sqrt(H[i].length*H[j].length)/S.length,chi:{}};for(let [xy,u] of orbit)for(let g of R){let exp=mod(-2*B(i,j,g,g)+dot(c,g)+B(i,j,g,u)-B(i,j,u,g));a.chi[81*g+xy]=[dim,exp]}list.push(a);all.push(a)}
 }pairs[i][j]=list}
 A(all.length===192,'simple count');
 const conj=(a,b)=>{let z=[0,0,0];for(let [key,[v,e]] of Object.entries(a.chi)){let c=b.chi[key];if(c)z[mod(e-c[1])]+=v*c[0]}A(z[1]===z[2]&&(z[0]-z[1])%9===0,'character norm');return (z[0]-z[1])/9};
 for(let row of pairs)for(let L of row)for(let a of L)for(let b of L)A(conj(a,b)===(a===b?1:0),'orthonormality');
 const fusion=Array.from({length:all.length},()=>({}));let prod=0,maxN=0,types={},dims={};
 for(let a of all){let k=Math.round(a.d*1e9)/1e9;dims[k]=(dims[k]||0)+1}
 for(let a of all)for(let k=0;k<8;k++)for(let b of pairs[a.j][k]){
 let f=[];for(let c of pairs[a.i][k]){let z=[0,0,0];for(let [key,[v,e]] of Object.entries(c.chi)){let q=Number(key),g=Math.floor(q/81),x=Math.floor(q%81/9),y=q%9;for(let h of X[a.j].points){let A1=a.chi[81*g+9*x+h],B1=b.chi[81*g+9*h+y];if(A1&&B1)z[mod(A1[1]+B1[1]-e)]+=A1[0]*B1[0]*v}}A(z[1]===z[2]&&(z[0]-z[1])%9===0,'integral fusion');let n=(z[0]-z[1])/9;A(n>=0,'positive');if(n){f.push([c.id,n]);maxN=Math.max(maxN,n)}}
 A(Math.abs(f.reduce((s,[i,n])=>s+all[i].d*n,0)-a.d*b.d)<1e-8,'dimension');fusion[a.id][b.id]=f;prod++;let key=f.map(x=>x[1]).sort().join();types[key]=(types[key]||0)+1}
 let assoc=0;for(let a of all)for(let k=0;k<8;k++)for(let b of pairs[a.j][k])for(let l=0;l<8;l++)for(let c of pairs[k][l]){let u={},v={};for(let [d,m] of fusion[a.id][b.id])for(let [e,n] of fusion[d][c.id])u[e]=(u[e]||0)+m*n;for(let [d,m] of fusion[b.id][c.id])for(let [e,n] of fusion[a.id][d])v[e]=(v[e]||0)+m*n;A(Object.keys(u).length===Object.keys(v).length&&Object.keys(u).every(e=>u[e]===v[e]),'associativity');assoc++}
 return {summary:{subgroups:H,twists:t,simple_count:all.length,hom_sizes:pairs.map(row=>row.map(L=>L.length)),dimensions:dims,products:prod,associativity_tests:assoc,max_multiplicity:maxN,fusion_types:types},labels:all,fusion}
}
const r=defects();console.log(JSON.stringify(process.argv.includes('--full')?r:r.summary,null,2));
