"use strict";
function build(){
const A=(b,m)=>{if(!b)throw Error(m)},sum=x=>x.reduce((a,b)=>a+b,0),mod=(x,p)=>(x%p+p)%p,dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),norm=a=>sum(a.map(Math.abs)),arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),mat=(n,m,f)=>arr(n,i=>arr(m,j=>f(i,j))),mul=(a,b)=>mat(a.length,b[0].length,(i,j)=>sum(a[i].map((x,k)=>x*b[k][j]))),trace=a=>sum(a.map((r,i)=>r[i])),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),det=a=>a.length===0?1:sum(a[0].map((x,i)=>x*(-1)**i*det(a.slice(1).map(r=>r.filter((_,j)=>j!==i))))),hist=a=>{let h={};for(const x of a)h[x]=(h[x]||0)+1;return h};
function dimension(){
 let rows=[];const gammaHalf=[null,null,1,Math.sqrt(Math.PI)/2,1,3*Math.sqrt(Math.PI)/4,2,15*Math.sqrt(Math.PI)/8,6];
 for(let d=3;d<=8;d++)for(let g of [.5,1,2,4])rows.push({d,g,energies:[.001,.01,.1,1,10,100].map(r=>d/(2*r*r)-g/gammaHalf[d]/r**(d-2))});
 let hydrogen=[.1,1,5].map(g=>({g,E:g*g/4-g*g/2}));A(hydrogen.every(x=>Math.abs(x.E+x.g*x.g/4)<1e-14),"hydrogen");
 return {rows,hydrogen,hardy_4_critical_g:1,dimension_intersection:[3],maxwell:arr(6,i=>({spatial_dimension:i+2,dual_potential_degree:i,conformal_weight:i-1})),scope:"Continuum unregularized Gauss potential, quadratic nonrelativistic kinetic energy and finite lattice Green function imposed. Gaussian controls do not prove sharp Hardy. Maxwell conformal scaling is for a supplied relativistic one-form."}
}
function chiral(){
 const out=[];let N=24,cs=arr(N,i=>Math.cos(2*Math.PI*(i+.5)/N)),ss=cs.map(x=>1-x*x);
 for(let m of [-1,1,3,5,7,9]){
 let corners=arr(16,i=>{let j=arr(4,k=>(i>>k)&1).reduce((s,x)=>s+x,0);return {j,M:m-2*j,sign:(-1)**j}}),degree=sum(corners.filter(x=>x.M>0).map(x=>x.sign)),integral=0,minGap=Infinity;
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)for(let k=0;k<N;k++)for(let l=0;l<N;l++){
  let c=[cs[i],cs[j],cs[k],cs[l]],s=[ss[i],ss[j],ss[k],ss[l]],M=m-4+sum(c),r2=M*M+sum(s),numer=M*c[0]*c[1]*c[2]*c[3]+s[0]*c[1]*c[2]*c[3]+s[1]*c[0]*c[2]*c[3]+s[2]*c[0]*c[1]*c[3]+s[3]*c[0]*c[1]*c[2];
  integral+=numer/r2**2.5;minGap=Math.min(minGap,Math.sqrt(r2))
 }
 integral*=(2*Math.PI/N)**4/(8*Math.PI**2/3);A(Math.abs(integral-degree)<.00001,"Chern integral");out.push({m,degree,quadrature:integral,min_sample_gap:minGap,corner_mass_histogram:hist(corners.map(x=>x.M))})
 }
 A(eq(out.map(x=>x.degree),[0,1,-3,3,-1,0]),"degree census");return {N,rows:out,scope:"4D supplied free Wilson Hamiltonian; oriented map degree, C2 sign depends on gamma and occupied-band convention. No interacting mirror gapping or dynamical fourth dimension."}
}
function category(){
 const vectors=d=>arr(3**d,i=>arr(d,j=>Math.floor(i/3**j)%3)),canon=v=>{let f=v.find(x=>x!==0);return f?v.map(x=>mod(x*f,3)).join(""):""},pts=[...new Set(vectors(4).map(canon).filter(Boolean))].map(x=>x.split("").map(Number)),N=mat(40,40,(i,j)=>+(dot(pts[i],pts[j])%3===0));
 A(pts.length===40&&N.every(r=>sum(r)===13),"PG count");A(eq(mul(N,N),mat(40,40,(i,j)=>i===j?13:4)),"design");
 const U=mat(40,40,(i,j)=>4*N[i][j]-1);A(eq(mul(U,U),mat(40,40,(i,j)=>i===j?144:0)),"orthogonal transform");
 let pl=(a,b)=>[[0,1],[2,3],[0,2],[1,3],[0,3],[1,2]].map(([i,j],k)=>mod((a[i]*b[j]-a[j]*b[i])*(k===3?-1:1),3)),lines=new Map();
 for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){let v=pl(pts[i],pts[j]),key=canon(v);if(!lines.has(key)){let on=new Set();for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a||b)on.add(canon(pts[i].map((x,k)=>mod(a*x+b*pts[j][k],3))));lines.set(key,{on,perp:pts.map((w,k)=>dot(w,pts[i])%3===0&&dot(w,pts[j])%3===0?k:-1).filter(k=>k>=0)})}}
 A(lines.size===130,"Klein lines");const bosons=vectors(6).filter(v=>mod(v[0]*v[1]+v[2]*v[3]+v[4]*v[5],3)===0);
 A(bosons.length===261,"boson count");A([...lines.keys()].every(k=>{let v=k.split("").map(Number);return (v[0]*v[1]+v[2]*v[3]+v[4]*v[5])%3===0}),"Plucker");
 const boundary=arr(80,i=>new Set(["000000",...[...lines].filter(([_,v])=>i<40?v.on.has(pts[i].join("")):v.perp.includes(i-40)).flatMap(([key])=>[key,key.split("").map(x=>mod(2*+x,3)).join("")])]));
 A(boundary.every(b=>b.size===27),"boundary size");for(const b of boundary)for(const x of b)for(const y of b)A(b.has(x.split("").map((z,i)=>mod(+z+ +y[i],3)).join("")),"closure");
 const G=mat(80,80,(i,j)=>[...boundary[i]].filter(x=>boundary[j].has(x)).length);
 A(eq(G,mat(80,80,(i,j)=>i===j?27:(i<40)===(j<40)?3:1+8*N[i%40][j%40])),"intersection");
 const G2=mul(G,G),G3=mul(G2,G);A(eq(G3,mat(80,80,(i,j)=>336*G2[i][j]-13824*G[i][j])),"Gram polynomial");A(trace(G)===2160&&trace(G2)===172800,"Gram moments");
 return {bosons_including_vacuum:bosons.length,boundaries:80,boundary_size:27,projective_lines:130,ordered_intersection_histogram:hist(G.flat()),Gram_spectrum:{"32/3":1,"16/9":39,"0":40},rank:40,transversality_spectrum:{"27":1,"3":39,"-3":39,"-27":1},orthogonal_transform:"(4N-J)/12",scope:"Untwisted D(F3^3), uniform subgroup vectors in C^729. Not physical Witting rays or a native gate."}
}
function gravity(){
 const rows=[];
 for(const type of ["rook","shrikhande"]){
 let vertices=arr(16,i=>[Math.floor(i/4),i%4]),adj=mat(16,16,(i,j)=>{let [a,b]=vertices[i],[c,d]=vertices[j];return +(type==="rook"?i!==j&&(a===c||b===d):["1,0","3,0","0,1","0,3","1,1","3,3"].includes([mod(a-c,4),mod(b-d,4)].join(",")))});
 A(eq(mul(adj,adj),mat(16,16,(i,j)=>i===j?6:2)),"SRG");
 let edges=[];for(let i=0;i<16;i++)for(let j=i+1;j<16;j++)if(adj[i][j])edges.push([i,j]);
 let C=mat(16,16,(i,j)=>6*+(i===j)+adj[i][j]),T=mat(48,48,(i,j)=>{let [a,b]=edges[i],[c,d]=edges[j];return C[a][c]-C[a][d]-C[b][c]+C[b][d]});
 A(T.every((r,i)=>r[i]===10),"resistance");A(eq(mul(T,T),T.map(r=>r.map(x=>32*x))),"projection");
 let K=T.map(r=>r.map(x=>x*x)),K2=mul(K,K),pairHist=hist(K.flatMap((r,i)=>r.slice(i+1)));
 const pairInteractions=Object.entries(pairHist).map(([k,count])=>({transfer_numerator_squared:+k,count,logdet_mixed_response:Math.log1p(-(+k)/(42*42)),tree_joint_probability:(100-(+k))/1024}));
 A(sum(pairInteractions.map(x=>x.count))===1128,"pair census");
 rows.push({type,transfer_square_histogram:hist(K.flat()),trace_K2:trace(K2),trace_K3:trace(mul(K2,K)),gaussian_Fisher_trace_square:trace(K2)/2048**2,edge_resistance:10/32,gaussian_Fisher_trace:trace(K)/2048,pairInteractions})
 }
 A(rows[0].trace_K2===676608&&rows[1].trace_K2===675456,"Fisher spectra differ");
 return {rows,scope:"Gaussian scalar field on mean-zero vertex space. Fisher response of edge conductances distinguishes scalar-cospectral graphs. Spanning-tree pair probability follows transfer-current theorem. Not Einstein dynamics."}
}
function codes(){
 function rank3(M){M=M.map(r=>r.map(x=>mod(x,3)));let r=0;for(let j=0;j<M[0].length&&r<M.length;j++){let k=M.findIndex((v,i)=>i>=r&&v[j]);if(k<0)continue;[M[r],M[k]]=[M[k],M[r]];let z=M[r][j];M[r]=M[r].map(x=>mod(z*x,3));for(let i=r+1;i<M.length;i++)if(M[i][j]){let t=M[i][j];for(let c=j;c<M[i].length;c++)M[i][c]=mod(M[i][c]-t*M[r][c],3)}r++}return r}
 function test(p,d){
 let b=Math.ceil(p**(1/d)),a=arr(d,i=>mod(b**i,p)),basis=arr(d-1,i=>arr(d,j=>j===i?b:j===i+1?-1:0));let rest=p,digits=arr(d,i=>{let v=i===d-1?rest:rest%b;rest=Math.floor(rest/b);return v});basis.push(digits);A(Math.abs(det(basis))===p&&basis.every(v=>mod(dot(v,a),p)===0),"basis");
 let D=det(basis),dual=arr(d,j=>arr(d,i=>Math.round(p*((-1)**(i+j))*det(basis.filter((_,k)=>k!==j).map(r=>r.filter((_,k)=>k!==i)))/D)));
 A(eq(mat(d,d,(i,j)=>dot(basis[i],dual[j])),mat(d,d,(i,j)=>p*+(i===j))),"dual");
 let max=Math.max(...basis.map(norm)),best=Math.min(...basis.map(norm)),w=null;
 function visit(v,left){if(v.length===d){let n=norm(v);if(n>0&&n<=best&&dot(v,a)%p===0){best=n;w=v.slice()}return}for(let i=-left;i<=left;i++)visit([...v,i],left-Math.abs(i))}
 visit([],best);A(w!==null&&best===norm(w),"systole");
 let E=p*d,shift=(v,i)=>mod(v+a[i],p),edge=(v,i)=>v*d+i,cochains=dual.map(u=>arr(E,k=>{let v=Math.floor(k/d),i=k%d;return Math.floor((u[0]*v+u[i])/p)-Math.floor(u[0]*v/p)}));
 let squares=[];for(let v=0;v<p;v++)for(let i=0;i<d;i++)for(let j=i+1;j<d;j++)squares.push([[edge(v,i),1],[edge(shift(v,i),j),1],[edge(shift(v,j),i),-1],[edge(v,j),-1]]);
 for(let c of cochains)A(squares.every(s=>sum(s.map(([e,z])=>c[e]*z))===0),"closed cocycle");
 function path(v){let at=0,path=[];for(let i=0;i<d;i++)for(let k=0;k<Math.abs(v[i]);k++){if(v[i]>0){path.push([edge(at,i),1]);at=shift(at,i)}else{at=mod(at-a[i],p);path.push([edge(at,i),-1])}}A(at===0,"closed path");return path}
 let paths=basis.map(path);A(eq(mat(d,d,(i,j)=>sum(paths[i].map(([e,z])=>cochains[j][e]*z))),mat(d,d,(i,j)=>+(i===j))),"logical pairing");
 let support=cochains.map(c=>c.filter(x=>mod(x,3)).length),bounds=dual.map(norm);A(support.every((x,j)=>x<=bounds[j]),"dual support bound");
 let zpath=path(w);A(cochains.some(c=>mod(sum(zpath.map(([e,s])=>c[e]*s)),3)!==0),"nontrivial shortest cycle");
 let ranks=null;if(p<=31){let B1=mat(p,E,(v,k)=>+(v===shift(Math.floor(k/d),k%d))-+(v===Math.floor(k/d))),B2=squares.map(s=>{let x=Array(E).fill(0);for(let [k,z] of s)x[k]+=z;return x});A(B2.every(r=>B1.every(b=>dot(r,b)===0)),"chain");ranks=[rank3(B1),rank3(B2)];A(E-sum(ranks)===d,"homology rank")}
 let synd=Array(p).fill(0),barrier=0;for(let [e,z] of zpath){let v=Math.floor(e/d),i=e%d;synd[v]-=z;synd[shift(v,i)]+=z;barrier=Math.max(barrier,synd.filter(x=>mod(x,3)).length)}A(barrier<=2&&synd.every(x=>x===0),"energy barrier");
 return {p,d,a,basis,dual_numerators:dual,physical_qutrits:E,logical_qutrits:d,dZ_exact:best,shortest_relation:w,dX_lower:Math.ceil(p/max),dX_upper:Math.min(...support),X_witness_weights:support,ranks,max_string_defects:barrier}
 }
 let rows=[];for(let d of [2,3,4])for(let p of [7,13,31,127,509])rows.push(test(p,d));return {rows,scope:"Cubical flat covers supplied. Exact dZ and certified dX bounds, not exhaustive dX optimization. Fixed d, random prime cover tightness gives typical exponents; constant Z energy barrier."}
}
return {status:"PASS",dimension:dimension(),chirality:chiral(),category:category(),information_geometry:gravity(),codes:codes()}
}
console.log(JSON.stringify(build(),null,2));
