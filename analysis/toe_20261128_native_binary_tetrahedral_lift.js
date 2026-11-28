"use strict";
function run(){
 const a=(n,f)=>Array.from({length:n},(_,i)=>f(i)),m=x=>(x%3+3)%3,B=(u,v)=>m(u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2]),V=a(81,i=>a(4,j=>Math.floor(i/3**j)%3)),P=V.filter(v=>v.find(Boolean)===1),A=(x,msg)=>{if(!x)throw Error(msg)},mul=(x,y)=>a(4,i=>m(x[2*(i>>1)]*y[i%2]+x[2*(i>>1)+1]*y[2+i%2])),I=[1,0,0,1],negI=[2,0,0,2],key=x=>x.join(""),order=x=>{let y=I;for(let n=1;n<=24;n++){y=mul(x,y);if(key(y)===key(I))return n}throw Error("order")};
 const frames=P.map(p=>{let r=V.find(v=>!B(p,v)&&v.some(Boolean)&&!([1,2].some(c=>v.every((x,i)=>x===m(c*p[i]))))),s=V.find(v=>!B(p,v)&&B(r,v)===1);A(r&&s,"basis");return [r,s]});
 const T=P.map((p,i)=>P.map((q,j)=>{let pq=B(p,q);if(!pq)return null;let cols=frames[i].map(v=>{let w=v.map((x,k)=>m(x-B(v,q)*pq*p[k]));A(!B(w,p)&&!B(w,q),"intersection");return [B(w,frames[j][1]),B(frames[j][0],w)]});let t=[cols[0][0],cols[1][0],cols[0][1],cols[1][1]];A(m(t[0]*t[3]-t[1]*t[2])===1,"symplectic");return t}));
 let hist={},traces={},gens=[],n=0;for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)for(let k=j+1;k<40;k++)if(T[i][j]&&T[j][k]&&T[k][i]){let H=mul(T[k][i],mul(T[j][k],T[i][j])),o=order(H),tr=m(H[0]+H[3]);hist[o]=(hist[o]||0)+1;traces[tr]=(traces[tr]||0)+1;n++;if(i===0)gens.push(H)}
 let G=new Map([[key(I),I]]);while(true){let l=G.size;for(let x of [...G.values()])for(let y of gens){let z=mul(x,y);G.set(key(z),z)}if(G.size===l)break}
 let gh={};for(let x of G.values()){let o=order(x);gh[o]=(gh[o]||0)+1}A(G.size===24&&G.has(key(negI))&&n===3240,"lift");
 for(let i=0;i<40;i++)for(let j=0;j<40;j++)if(T[i][j])A(key(mul(T[i][j],T[j][i]))===key(I),"inverse");
 return {status:"PASS",edge_count:540,triangles:n,triangle_order_histogram:hist,triangle_trace_histogram:traces,base_generators:gens.length,holonomy_order:G.size,holonomy_element_orders:gh,center:[I,negI],scope:"Canonical symplectic F3 quotient transports, SL2(3) holonomy (binary tetrahedral), no continuum spin dynamics or fermion derivation."}
}
console.log(JSON.stringify(run(),null,2));
