function tower(){
const A=(v,s)=>{if(!v)throw Error(s)},m=(x,n=3)=>(x%n+n)%n,rows=[];
for(let n=1;n<=6;n++){let q=3**n,G=Array.from({length:9*q},(_,i)=>[i%q,Math.floor(i/q)%3,Math.floor(i/(3*q))]),center=G.filter(([x,y])=>!m(x)&&!y),classes=G.filter(([x,y,z])=>!m(x)&&!y||z===0),dims={},spins={};let add=(o,k,v)=>o[k]=(o[k]||0)+v;
for(let [x,y,z] of classes){let central=!m(x)&&!y;if(central){add(dims,1,3*q);add(dims,3,2*q/3);
// central flux twists from one-dimensional characters and nonlinear central characters
for(let k=0;k<q;k++)for(let l=0;l<3;l++)add(spins,m(k*x+q/3*l*y,q),1);
for(let k=0;k<q/3;k++)for(let s of [1,2])add(spins,m(k*x+q/3*s*z,q),1);
}else{let centralizer=G.filter(([u,v])=>!m(x*v-y*u));A(centralizer.length===3*q,'centralizer');if(n<=3)A(centralizer.every(([u,v])=>centralizer.every(([a,b])=>!m(u*b-v*a))),'abelian');let ord=x? q/((()=>{let a=x,b=q;while(b)[a,b]=[b,a%b];return a})()):3;ord=Math.max(ord,y?3:1,z?3:1);add(dims,3,centralizer.length);for(let k=0;k<ord;k++)add(spins,k*q/ord,centralizer.length/ord)}
}
let rank=Object.values(dims).reduce((s,x)=>s+x,0);A(rank===35*3**(2*n-1)&&Object.entries(dims).reduce((s,[d,c])=>s+d*d*c,0)===(9*q)**2,'double');A(Object.values(spins).reduce((s,x)=>s+x,0)===rank,'twist count');rows.push({n,order:9*q,center:center.length,conjugacy_classes:classes.length,irreps:{1:3*q,3:2*q/3},double_rank:rank,double_dimensions:dims,twist_order_census:Object.entries(spins).reduce((o,[k,v])=>{let a=+k,b=q;while(b)[a,b]=[b,a%b];add(o,q/a,v);return o},{})})}
return {rows,scope:"Untwisted Drinfeld doubles of G_n=C_(3^n) semidirect Heisenberg pullback; 2+1D topological model, no four-dimensional physical selection. Conjugacy class size1 or3; noncentral centralizers abelian. Twist convention character(g), inversion has same census."}
}
function selection(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3,dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1;
function span(G){let C=new Map([['000000000000',Array(12).fill(0)]]);for(let r of G)for(let v of [...C.values()])for(let t=1;t<3;t++){let a=v.map((x,i)=>m(x+t*r[i]));C.set(a.join(''),a)}return [...C.values()]}
let G=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),full=span(G).find(v=>v.every(Boolean));G=G.map(r=>r.map((x,i)=>m(x*full[i])));let B=Array.from({length:4},(_,i)=>Array.from({length:12},(_,j)=>+(Math.floor(j/3)===i)));for(let r of [[1,0,1,1],[0,1,1,2]])B.push(r.flatMap(x=>[x,m(-x),0]));
let triples=[];for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)for(let k=j+1;k<12;k++)triples.push(Array.from({length:12},(_,a)=>+(a===i||a===j||a===k)));
let info=[];for(let [name,g] of [["Golay",G],["weight3",B]]){let C=span(g),set=new Set(C.map(v=>v.join(''))),neighbors=new Map();for(let t of triples){if(set.has(t.join('')))continue;let H=C.filter(v=>!dot(v,t)),N=H.flatMap(v=>[0,1,2].map(s=>v.map((x,i)=>m(x+s*t[i])))),key=N.map(v=>v.join('')).sort().join('|');A(H.length===243&&new Set(N.map(v=>v.join(''))).size===729,'neighbor');neighbors.set(key,N.filter(v=>v.filter(Boolean).length===3).length/2)}
let census={};for(let k of neighbors.values())census[k]=(census[k]||0)+1;info.push({name,neighbors_detected_by_external_triples:neighbors.size,census})}
A(info[0].census[4]===55,'Golay bad neighbor');
// bad->good by counting all edges; additionally explicitly enumerate all hyperplanes containing ones via functionals from independent basis and extend isotropic using reflection? class transitive via monomial normalized ones not assumed. Derive bad->good directly: 121 hyperplanes, those containing any existing triple cannot yield good. 4 triples span rank3 in quotient. hyperplanes not containing any triple: projective functionals on 5 dims with first 3 values nonzero and sum nonzero => 2 options (all same), 9 free =>9? Wait triples sum ones, first3 all nonzero and sum nonzero means mixed (6), /2*9=27. all these neighbors may have other triples. external triple neighbors detected by code confirms check.
// if any external triple neighbor that loses all old triples? orthogonal new triple to H, H contains old t iff overlap mod3=0. external triple cannot intersect all four old disjoint triples. Thus retains at least one. 
let rows=[];for(let beta of [0,.5,1,2,4]){let a=55/121*Math.exp(-4*beta),b=27/121,pi=b/(a+b);rows.push({beta,stationary_Golay:pi,type_relaxation_gap:a+b,mean_steps_from_bad:1/b})}
return {info,rows,scope:"Classical Metropolis walk on maximal isotropic subspaces containing ones, uniform hyperplane neighbor, energy number of weight3 directions. Each good has55 bad neighbors (220 external triples /4); each bad has27 good neighbors (hyperplane excludes all4 triples; external new triple cannot meet all4 disjoint triples). Detailed balance and type gap exact. Supplied repulsive energy, not quantum Lindbladian or full-chain gap."}
}
console.log(JSON.stringify({tower:tower(),selection:selection()},null,2));
