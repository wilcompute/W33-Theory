function matterAndSelector(){
const A=(x,s)=>{if(!x)throw Error(s)},m=x=>(x%3+3)%3;
// All matter has center charge +1 and U1 gauge charge 3n, n=1 mod3.
let mult=[16,10,1],ns=[1,-2,4],linear=mult.reduce((s,k,i)=>s+k*ns[i],0),cubic=mult.reduce((s,k,i)=>s+k*ns[i]**3,0);A(!linear&&!cubic,"anomaly");
let kernel=[];for(let a=0;a<9;a++)for(let b=0;b<3;b++)if(ns.every(n=>!m(a*n+b)))kernel.push([a,b]);A(kernel.length===9,"center");
let generator=Array.from({length:9},(_,i)=>[i,m(-i)]);A(generator.every(g=>kernel.some(k=>k.join()==g.join())),"cyclic");
// Single-copy Fourier counterexample and repair.
let D=[];for(let i=0;i<2187;i++){let v=Array.from({length:7},(_,j)=>Math.floor(i/3**j)%3);if(v.filter(Boolean).length===6&&v.find(Boolean)===1&&!m(v.reduce((s,x)=>s+x,0)))D.push(v)}
let masks=[];for(let i=0;i<729;i++){let q=Array.from({length:7},(_,j)=>Math.floor(i/3**j)%3),b=0n;for(let j=0;j<D.length;j++)if(!m(q.reduce((s,x,k)=>s+x*D[j][k],0)))b|=1n<<BigInt(j);masks.push(b)}
A(masks.every(Boolean),"single-copy orthogonality");let absent=0;for(let a of masks)for(let b of masks)if(!(a&b))absent++;A(absent===1008,"previous rank");
return {matter:{multiplicities:mult,normalized_charges:ns,physical_charges:ns.map(x=>3*x),weyl_count:27*27,linear,cubic,combined_center_kernel:kernel,min_equal_flavor_multiplets:27},golay:{directions:D.length,single_copy_quotients:masks.length,single_copy_incompatible:0,pair_incompatible:absent,old_hamiltonian_counterexample:"|0>^12 ⊗ |+>^12, and reverse",four_independent_fourier_terms_product_expectation:792*9072/9**7,scope:"Each individual Fourier transform preserves selfdual code state. Four independent Fourier orientations exclude the four uniform computational/Fourier product types, not arbitrary product states or full ground space."},scope:"U1 dynamical gauge, E6_sc flavor, 27 charged matter; exact electric one-form C3 and combined kernel C9. Perturbative U1 cubic, mixed gravitational and U1-E6^2 vanish. E6 has no cubic adjoint invariant. Not full global anomaly audit, not an E6 gauge theory or physical SM matter. 27 multiplets lower bound assumes all same flavor representation and normalized charges 1 mod3; follows sum n=0 and sum n^3 ≡ -2N mod27."}
}
console.log(JSON.stringify(matterAndSelector(),null,2));
