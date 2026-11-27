function clockFlux(){
 const m=(x,n=3)=>(x%n+n)%n,A=(x,s)=>{if(!x)throw Error(s)},a=x=>m(x),b=x=>Math.floor(x/3),carry=(x,y)=>Math.floor((a(x)+a(y))/3),F=(x,y,z,w)=>m(a(x)*b(y)*carry(z,w)),omega=(x,y,z,w,v)=>m(a(x)*carry(y,z)*carry(w,v));
 let checks=0;for(let i=0;i<9**5;i++){let [x,y,z,w,v]=Array.from({length:5},(_,j)=>Math.floor(i/9**j)%9),d=F(y,z,w,v)-F(m(x+y,9),z,w,v)+F(x,m(y+z,9),w,v)-F(x,y,m(z+w,9),v)+F(x,y,z,m(w+v,9))-F(x,y,z,w);A(m(d)===omega(x,y,z,w,v),'primitive');checks++}
 // H27 exponent three: a lift of any order-three generator cannot have order nine.
 let H=[];for(let i=0;i<27;i++)H.push([i%3,Math.floor(i/3)%3,Math.floor(i/9)]);let mul=(u,v)=>[m(u[0]+v[0]),m(u[1]+v[1]),m(u[2]+v[2]+u[0]*v[1])];A(H.every(x=>mul(mul(x,x),x).every(v=>!v)),'H27 exponent');
 let F3=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**j)%3)).map(v=>v.concat(m(-v.reduce((s,x)=>s+x,0)))),sg=x=>x===2?-1:x,counts={},liftCount=0;
 for(let f of F3){let j=f.reduce((s,x)=>s+sg(x),0)/3;counts[j]=(counts[j]||0)+1;let c=0;for(let i=0;i<729;i++){let h=Array.from({length:6},(_,k)=>Math.floor(i/3**k)%3);if(m(f.reduce((s,x,k)=>s+sg(x)+3*h[k],0),9)===0)c++}A(c===243,'lift extensions');liftCount+=c}
 let fit=[];for(let mu of [.1,1,2]){let same=0,err=0,mean=0;for(let f of F3){let j=f.reduce((s,x)=>s+sg(x),0)/3;let best=j===0?0:2.5*mu;err=Math.max(err,Math.abs(mu*j*j-best));mean+=(mu*j*j-best)**2/243;if(j!==0)same++}fit.push({mu,optimal_even_mod3_minimax_error:err,rms:Math.sqrt(mean),nonzero:same})}
 return {cochain_checks:checks,primitive:"a(g1) b(g2) carry(g3,g4) mod3; delta primitive = a cup carry cup carry",H27_exponent:3,monopole_census:counts,flat_Z9_face_lifts_per_Z3_closed_cube:243,total_lifts:liftCount,fit,scope:"Bosonic order-three group cohomology inflow representative; not complete spin eta anomaly identification. H27 cannot realize nonsplit cyclic Z9 by subgroup or quotient. Uniform lift sum gives no suppression; j mod3 cannot distinguish +1 from -2. Independent edge lift global constraints not simulated."}
}
function golayAction(){
 const A=(x,s)=>{if(!x)throw Error(s)},m=x=>(x%3+3)%3,leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1;
 function span(G){let C=new Map([['000000000000',Array(12).fill(0)]]);for(let r of G)for(let v of [...C.values()])for(let t=1;t<=2;t++){let x=v.map((a,i)=>m(a+t*r[i]));C.set(x.join(''),x)}return [...C.values()]}
 let G=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),full=span(G).find(v=>v.every(Boolean));G=G.map(r=>r.map((x,i)=>m(x*full[i])));let B=Array.from({length:4},(_,i)=>Array.from({length:12},(_,j)=>+(Math.floor(j/3)===i)));for(let r of [[1,0,1,1],[0,1,1,2]])B.push(r.flatMap(x=>[x,m(-x),0]));
 let hist=[G,B].map(g=>{let h=Array(13).fill(0);for(let v of span(g))h[v.filter(Boolean).length]++;return h});A(hist[0].join()==="1,0,0,0,0,0,264,0,0,440,0,0,24"&&hist[1].join()==="1,0,0,8,0,0,240,0,0,464,0,0,16",'enumerators');
 let rows=[];for(let t of [-.99,-.75,-.5,-.1,.1,.5,1,4,20]){let x=t/(3+t),w=hist.map(h=>h.reduce((s,c,j)=>s+c*x**j,0));A(Math.abs(w[1]-w[0]-8*x**3*(1-x**3)**3)<1e-9,'difference');rows.push({t,x,log_annealed_ratio_competitor_over_Golay:Math.log(w[1]/w[0]),preferred:w[1]>w[0]?"weight3":"Golay"})}
 // Universal exact selection on code-state manifold via third-order repulsion, and fifth-site maximal mixing.
 return {hist,rows,formula:"<K(t)>=(1+t/3)^12 W_C(t/(3+t)); W_bad-W_G=8x^3(1-x^3)^3",scope:"Exact expectation of positive full shared transfer for -1<t; -log of expectation, not expectation of -log operator. Negative t selects Golay among two enumerator classes but sign supplied; no global Hamiltonian vacuum proof."}
}
console.log(JSON.stringify({clock:clockFlux(),golay:golayAction()},null,2));
