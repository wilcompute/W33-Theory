function selection(){
const A=(x,s)=>{if(!x)throw Error(s)},m=x=>(x%3+3)%3,leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1;
function span(G){let words=new Map([['000000000000',Array(12).fill(0)]]);for(let row of G)for(let v of [...words.values()])for(let t=1;t<=2;t++){let a=v.map((x,i)=>m(x+t*row[i]));words.set(a.join(''),a)}return [...words.values()]}
let golay=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),full=span(golay).find(v=>v.every(Boolean));golay=golay.map(r=>r.map((x,i)=>m(x*full[i])));
let fragmented=Array.from({length:4},(_,i)=>Array.from({length:12},(_,j)=>+(Math.floor(j/3)===i)));for(let t of [[1,0,1,1],[0,1,1,2]])fragmented.push(t.flatMap(x=>[x,m(-x),0]));
let pop=x=>{let n=0;while(x){x&=x-1;n++}return n},rows=[];
for(let [name,G] of [["Golay",golay],["weight3",fragmented]]){A(G.every(a=>G.every(b=>!m(a.reduce((s,x,i)=>s+x*b[i],0)))),'self-dual');let C=span(G);A(C.length===729,'dim');let hist=Array(13).fill(0),supportCount=new Int32Array(4096);for(let v of C){let mask=v.reduce((s,x,i)=>s+(x?1<<i:0),0);supportCount[mask]++;hist[pop(mask)]++}
for(let j=0;j<12;j++)for(let k=0;k<4096;k++)if(k>>j&1)supportCount[k]+=supportCount[k^(1<<j)];
let subsets=Array.from({length:13},()=>({n:0,sumMoment:0,entropy:0,minimumEntropy:Infinity,dimensionCensus:{}}));
for(let k=0;k<4096;k++){let r=pop(k),d=Math.round(Math.log(supportCount[k])/Math.log(3)),s=subsets[r];A(3**d===supportCount[k],'dim exact');let S=r-2*d;s.n++;s.sumMoment+=40*supportCount[k]/3**(r-1);s.entropy+=S;s.minimumEntropy=Math.min(s.minimumEntropy,S);s.dimensionCensus[d]=(s.dimensionCensus[d]||0)+1}
for(let s of subsets){s.meanEntropyLog9=s.entropy/s.n;delete s.entropy}
rows.push({name,hist,subsets})}
let difference=rows[1].subsets[3].sumMoment-rows[0].subsets[3].sumMoment;A(Math.abs(difference-320/9)<1e-10,'third gap');
return {rows,third_moment_sum_difference:difference,connected_action_difference_coefficient:"-8/27",scope:"Two explicit self-dual code states (two copies of uniform code superposition) on12 registers. All local subset shortened dimensions and entropy in units log9 exactly determined. Third square-free connected action coefficient favors weight-three sector for positive uniform coupling; not global ground state or complete thermal Hamiltonian."}
}
function gaugeObstruction(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},sg=x=>x===2?-1:x,V=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**j)%3)).map(v=>v.concat(m(-v.reduce((s,x)=>s+x,0)))),j=v=>v.reduce((s,x)=>s+sg(x),0)/3;
let rows=[];for(let t of [.1,1,4]){let maxShift=0,monopoleShift=0,nonzero=0;for(let v of V){let w=v.map(x=>m(x+1)),K=v=>(117*(1+t/3)**6+[0,1,2].reduce((s,k)=>s+(1+t)**v.filter(x=>x===k).length,0))/120;maxShift=Math.max(maxShift,Math.abs(K(v)-K(w)));monopoleShift=Math.max(monopoleShift,Math.abs(j(v)**2-j(w)**2));if(j(v)**2!==j(w)**2)nonzero++}A(maxShift<1e-10&&monopoleShift===4,'shift symmetry');rows.push({t,maxShift,monopoleShift,configurations_changing_charge_squared:nonzero})}
return {rows,scope:"Actual shared-tick K expectation on product rank-three mixed face-eigenstates of one common Pauli direction. Uniform outcome label enforces global ternary flux shift symmetry, so cannot reproduce Wilson+positive monopole penalty except trivial coefficients (all-zero vs all-one, and other orbits); integer lift or nonuniform/anchored history needed."}
}
function helicity(){
let rows=[];for(let s of [0.5,1,1.5,2]){let m=Array.from({length:2*s+1},(_,i)=>i-s);rows.push({spin:s,generator_eigenvalues:m,extremal_speed_relative_to_spin_half:2*s,required_angle_factor_for_equal_speed:1/(2*s)})}return {rows,scope:"Representation-theoretic obstruction for one common SU2 rotation angle in spin representations, physical extremal helicity projection assumed. Does not forbid different microscopic representations, tuned generators or interacting common light cone. Canonical gradient mixing eigenvelocities coincide only if kinetic-normalized matrix scalar."}
}
console.log(JSON.stringify({selection:selection(),gauge:gaugeObstruction(),helicity:helicity()},null,2));
