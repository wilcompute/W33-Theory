function higher(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},comb=(n,k)=>{let R=[];function f(a,j){if(a.length===k){R.push(a);return}for(let i=j;i<n;i++)f(a.concat(i),i+1)}f([],0);return R},n=5,edges=comb(n,2),faces=comb(n,3),tets=comb(n,4),key=x=>x.join(''),get=(M,s)=>M[key(s)],D=(M,s)=>m(s.reduce((a,_,i)=>a+(i%2?-1:1)*get(M,s.filter((_,j)=>j!==i)),0)),mk=(L,f)=>Object.fromEntries(L.map(s=>[key(s),f(s)])),beta=E=>mk(faces,([i,j,k])=>m((get(E,[j,k])-get(E,[i,k])+get(E,[i,j]))/3)),post=(E,F)=>mk(tets,([i,j,k,l])=>m(get(E,[i,j])*get(F,[j,k,l])));
let total=0,nonflat=0,seed=13;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%3};
for(let p=0;p<81;p++){let v=[0,...Array.from({length:4},(_,i)=>Math.floor(p/3**i)%3)],E=mk(edges,([i,j])=>m(v[j]-v[i])),F=beta(E),P=post(E,F);A(D(P,[0,1,2,3,4])===0,'Postnikov cocycle');
for(let q=0;q<243;q++){let f=Array.from({length:5},(_,i)=>Math.floor(q/3**i)%3),E1=mk(edges,([i,j])=>m(get(E,[i,j])+f[j]-f[i])),t=mk(edges,([i,j])=>m((get(E1,[i,j])-get(E,[i,j])-f[j]+f[i])/3)),F1=beta(E1),P1=post(E1,F1),C=mk(faces,([i,j,k])=>m(f[i]*get(F,[i,j,k])-get(E,[i,j])*get(t,[j,k])+f[i]*D(t,[i,j,k]))),B=mk(faces,rand),B1=mk(faces,s=>m(get(B,s)+get(C,s)));
for(let s of faces)A(m(get(F1,s)-get(F,s))===D(t,s),'Bockstein transform');
for(let s of tets){A(m(get(P1,s)-get(P,s))===D(C,s),'descent');let H=m(D(B,s)-get(P,s)),H1=m(D(B1,s)-get(P1,s));A(H===H1,'curvature invariance');if(H)nonflat++;total++}
}}
return {flat_edge_fields:81,vertex_gauge_transformations_per_field:243,curvature_checks:total,nonzero_curvature_checks:nonflat,action:'sum_t (1-cos(2pi H_t/3)) exactly invariant',scope:'flat A, non-flat B; 2-group Postnikov descent on 4-simplex; no propagating spin-two result'}
}
console.log(JSON.stringify(higher(),null,2));
