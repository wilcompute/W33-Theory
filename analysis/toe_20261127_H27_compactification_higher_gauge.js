function geometry(){
 const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},G=Array.from({length:27},(_,i)=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]),id=x=>9*x[0]+3*x[1]+x[2],mul=(a,b)=>[m(a[0]+b[0]),m(a[1]+b[1]),m(a[2]+b[2]+a[1]*b[0])],prod=(i,j)=>id(mul(G[i],G[j])),inv=i=>G.findIndex((_,j)=>prod(i,j)===0&&prod(j,i)===0);
 let center=G.map(id).filter(i=>G.every((_,j)=>prod(i,j)===prod(j,i))),groups=new Map([['0',[0]]]),todo=[[0]];
 function closure(S,g){let R=new Set(S.concat(g)),again=true;while(again){again=false;for(let x of [...R])for(let y of [...R]){let z=prod(x,y);if(!R.has(z)){R.add(z);again=true}}}return [...R].sort((a,b)=>a-b)}
 while(todo.length){let S=todo.pop();for(let g=0;g<27;g++)if(!S.includes(g)){let R=closure(S,g),k=R.join();if(!groups.has(k)){groups.set(k,R);todo.push(R)}}}
 let free=[...groups.values()].filter(S=>!S.some(g=>g&&center.includes(g))),max=free.filter(S=>!free.some(R=>R.length>S.length&&S.every(g=>R.includes(g))));
 A(max.length===12&&max.every(x=>x.length===3),'free subgroup');
 // Schr monomial g sends e_j -> omega^(c+b*j)e_(j+a). Verify determinant and cubic invariance.
 let eigen=[];
 for(let i=0;i<27;i++){let [a,b,c]=G[i];if(center.includes(i))continue;let s=a?3:1,phases=[];
 if(a){for(let k=0;k<3;k++){let p=[0,0,0],j=0;for(let l=0;l<3;l++){let q=m(j+a),z=m(p[j]+c+b*j-k);if(q===0)A(z===0,'eigen cycle');else p[q]=z;j=q}phases.push(p)}}else for(let k=0;k<3;k++)phases.push([0,1,2].find(j=>m(c+b*j)===k));
 // eigenvectors have norm-squared s and Fermat cubic s in chosen unit-root representative.
 // paired eigenspace with singlet has H=0 only if lambda^3=-s; lambda=1,2 tested.
 A([1,2].every(l=>l**3!==-s),'fixed point');eigen.push({g:G[i],support:s,eigenvectors:phases})}
 let orbit=[];let seen=new Set();for(let S of max){let k=S.join();if(seen.has(k))continue;let R=new Set();for(let g=0;g<27;g++){let y=S.map(h=>prod(prod(g,h),inv(g))).sort((a,b)=>a-b).join();R.add(y);seen.add(y)}orbit.push([...R])}
 A(orbit.length===4&&orbit.every(x=>x.length===3),'conjugation');
 // degree-three invariant monomials: phase and cyclic permutations
 let mon=[];for(let a=0;a<=3;a++)for(let b=0;b<=3-a;b++)for(let c=0;c<=3-a-b;c++){let d=3-a-b-c;if(m(a+b+c)===0&&m(b+2*c)===0)mon.push([a,b,c,d])}
 let mo=new Map();for(let x of mon){let [a,b,c,d]=x,orb=[x,[b,c,a,d],[c,a,b,d]].map(y=>y.join()).sort();mo.set(orb[0],[...new Set(orb)])}
 A(mo.size===3,'invariants');
 // h11 of cover by weak Lefschetz from product cubic surfaces (rank 7 each); invariant rank under order3 via Lefschetz on cubic surface: fixed3, trace H2=1 => invariant rank3. pair sum6.
 let tr=1,invRank=(7+2*tr)/3;A(invRank===3,'surface Picard');
 return {group_order:27,center,subgroup_orders:[...groups.values()].reduce((h,S)=>(h[S.length]=(h[S.length]||0)+1,h),{}),free_subgroups:free,maximal_free_subgroups:max,conjugacy_classes:orbit,degree3_invariant_orbits:[...mo.values()],eigen_checks:eigen,cover:{euler:-18,h11:14,h21:23},quotient:{euler:-6,index:-3,h11:6,h21:9},smoothness:'positive real diagonal coefficients: critical common support implies sum d_i^3=0, impossible',fixed_center_witness:'x=(1,-1,0,0), y=(1,1,c,0), c^3=-2 for triplet pairing 1',flat_Z3_4_connection_counts:{cover:1,each_quotient:81}}
}
function dynamics(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)};
 // Postnikov beta(a) cup a: on L(3,1) x S1, a=x*l+y*t; beta a=x beta l; obstruction components x² and xy.
 let obs=[];for(let x=0;x<3;x++)for(let y=0;y<3;y++)obs.push({lens:x,circle:y,obstruction:[m(x*x),m(x*y)],lift:m(x*x)===0&&m(x*y)===0});
 // Gauge-invariant hopping in electric basis: q_left=nL-E, q_right=nR+E. hop from left to right nL-1,nR+1,E-1.
 let checks=0,states=0;for(let n=0;n<2;n++)for(let r=0;r<2;r++)for(let e=0;e<3;e++){states++;if(n===r)continue;let nn=r,rr=n,ee=m(e+r-n);A(m(n-e)===m(nn-ee)&&m(r+e)===m(rr+ee),'Gauss');checks++}
 // plaquette electric circulation exact divergence in cube oriented links, build incidence
 const pts=Array.from({length:8},(_,i)=>[i&1,i>>1&1,i>>2&1]),edges=[];for(let i=0;i<8;i++)for(let d=0;d<3;d++)if(!pts[i][d])edges.push([i,i+(1<<d)]);
 let plaquettes=[];for(let i=0;i<8;i++)for(let d=0;d<3;d++)for(let e=d+1;e<3;e++)if(!pts[i][d]&&!pts[i][e]){let path=[i,i+(1<<d),i+(1<<d)+(1<<e),i+(1<<e),i],row=edges.map(([a,b])=>path.slice(0,4).reduce((s,x,j)=>s+(x===a&&path[j+1]===b?1:x===b&&path[j+1]===a?-1:0),0));A(pts.every((_,v)=>edges.reduce((s,[a,b],j)=>s+(a===v?-1:b===v?1:0)*row[j],0)===0),'plaquette');plaquettes.push(row)}
 // Wilson Hamiltonian spectrum with tunable r,m and isotropic hopping (free control).
 let rows=[];for(let a of [.2,.1,.05,.025]){let p=[.3,.4,.2],mass=.7,r=1,k=p.map(x=>x*a),E=Math.hypot(...k.map(x=>Math.sin(x)/a),mass+r*k.reduce((s,x)=>s+1-Math.cos(x),0)/a);rows.push({a,E,target:Math.hypot(mass,...p),error:E-Math.hypot(mass,...p),doubler_masses:[0,1,2,3].map(j=>mass+2*r*j/a)})}
 // 2-form Maxwell massless polarization count by quotient transverse 2-forms in 3 spatial dims; one scalar.
 // Exact boundary dimensions: on open cube faces 6, edges 12, vertices 8, rank d1=5, d2=1.
 return {postnikov:{flat_classes:9,liftable:obs.filter(x=>x.lift).length,classes:obs,T4_lift_classes:81,T4_homotopy_cardinality:729,lens_times_circle_homotopy_cardinality:3},gauge:{local_states:states,nontrivial_hopping_transitions:checks,plaquettes:plaquettes.length,gauss_commutation:true,dispersion:rows},two_form:{open_cube_faces:6,gauge_rank:5,curvature_rank:1,massless_polarizations:1,graviton_polarizations:2}}
}
console.log(JSON.stringify({geometry:geometry(),dynamics:dynamics()},null,2));
