function geometry(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3,m6=x=>(x%6+6)%6,lines=[],part=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]];
for(let p=0;p<3;p++)for(let a=0;a<3;a++)for(let b=0;b<3;b++)lines.push({p,a,b});
function equations(L){return part[L.p].map(([i,j],k)=>[i,j,3+2*(k?L.b:L.a)])}
function intersect(L,R){let adj=Array.from({length:4},()=>[]);for(let [i,j,e] of equations(L).concat(equations(R))){adj[i].push([j,m6(-e)]);adj[j].push([i,m6(e)])}let seen=Array(4).fill(null),dim=0;for(let i=0;i<4;i++)if(seen[i]===null){let q=[i],ok=true;seen[i]=0;for(let a=0;a<q.length;a++)for(let [j,e] of adj[q[a]]){let t=m6(seen[q[a]]+e);if(seen[j]===null){seen[j]=t;q.push(j)}else if(seen[j]!==t)ok=false}if(ok)dim++}return dim}
let I=lines.map((l,i)=>lines.map((r,j)=>i===j?-1:intersect(l,r)));A(I.every((r,i)=>r.filter((x,j)=>i!==j&&x===1).length===10),'line valency');
const rank=M=>{M=M.map(r=>r.slice());let r=0;for(let j=0;j<M[0].length;j++){let i=M.findIndex((x,k)=>k>=r&&Math.abs(x[j])>1e-8);if(i<0)continue;[M[r],M[i]]=[M[i],M[r]];let c=M[r][j];M[r]=M[r].map(x=>x/c);for(let k=r+1;k<M.length;k++){let f=M[k][j];M[k]=M[k].map((x,l)=>x-f*M[r][l])}r++}return r};
A(rank(I)===7,'Picard rank');
let e=[0,1,2,0],perm=lines.map(l=>{let [[i,j],[u,v]]=part[l.p];return 9*l.p+3*m(l.a+e[i]-e[j])+m(l.b+e[u]-e[v])}),orbs=[],seen=new Set();
for(let i=0;i<27;i++)if(!seen.has(i)){let o=[i,perm[i],perm[perm[i]]];A(new Set(o).size===3,'orbit');o.forEach(x=>seen.add(x));orbs.push(o)}
let G=orbs.map(o=>orbs.map(p=>o.reduce((s,i)=>s+p.reduce((z,j)=>z+I[i][j],0),0)));A(rank(G)===3,'invariant Picard rank');
let ids=[];for(let i=0;i<9;i++){if(rank(ids.concat(i).map(j=>G[j]))>ids.length)ids.push(i)}
let Q=ids.map(i=>ids.map(j=>G[i][j])),D=(i,j,k)=>{let a=[i,j,k].filter(x=>x<3),b=[i,j,k].filter(x=>x>=3).map(x=>x-3);return a.length===2?Q[a[0]][a[1]]:b.length===2?Q[b[0]][b[1]]:0},C=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>Array.from({length:6},(_,k)=>D(i,j,k))));
let H=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>C[i][j].reduce((s,x,k)=>s+x*[1,2,3,2,1,3][k],0)));
let nz=0;for(let i=0;i<6;i++)for(let j=i;j<6;j++)for(let k=j;k<6;k++)if(D(i,j,k))nz++;
// representation-based cubic invariants H21 char 23,5,5,2; Sym^3 chi=(chi^3+3 chi(g)chi(g²)+2 chi(g³))/6
let sym=t=>(t**3+3*t*t+46)/6,inv=(sym(23)+2*sym(5)+24*sym(2))/27;A(Number.isInteger(inv),'Sym3');
let allowed=0;for(let i=0;i<23;i++)for(let j=i;j<23;j++)for(let k=j;k<23;k++){let c=x=>x<9?0:x<16?1:2;if(m(c(i)+c(j)+c(k))===0)allowed++}
return {surface_lines:27,line_intersection_rank:7,orbit_sums:orbs,orbit_gram:G,basis_ids:ids,basis_gram:Q,quotient_classical_cubic:C,nonzero_unordered_cubic_entries:nz,example_Higgs_vector:[1,2,3,2,1,3],classical_contraction:H,contraction_rank:rank(H),H21_sym3_invariant_dimension:inv,H21_C3_allowed_cubics:allowed,scope:'rational pullback divisor subspace; A-model classical cubic, not B-model residue or physical masses'}
}
console.log(JSON.stringify(geometry(),null,2));
