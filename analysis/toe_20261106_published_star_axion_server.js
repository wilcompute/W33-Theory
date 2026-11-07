/* Reproduce published factual charge data in Big Axions2606.05276v2 Tables1-2.
   All anomaly and gauge-matrix methods are prior physics. Full matrix RG is also
   already implemented in toe_20261105_new_front1_abelian_matrix.py.
   This is an independent server calculation, not a new axion construction. */
(() => {
 const pairs=[[10,0,[0,0,2],[1,1,-1]],[3,0,[0,-1,0],[1,2,1]],[3,0,[1,2,3],[0,-1,-2]],[1,1,[1,-1,2],[0,2,-1]],[1,1,[1,-1,3],[0,2,-2]],[1,1,[1,2,3],[0,-1,-2]],[1,0,[1,3,0],[0,-2,1]],[6,0,[2,-2,-3],[-3,1,2]],[5,0,[2,0,-2],[-3,-1,1]],[4,0,[-3,-1,0],[2,0,-1]],[3,0,[2,-3,1],[-3,2,-2]],[2,0,[2,-1,0],[-3,0,-1]],[2,-1,[-2,-3,-3],[-3,3,3]],[1,-1,[-2,3,2],[-3,-3,-2]],[2,1,[3,0,1],[2,0,-1]],[1,1,[3,3,2],[2,-3,-2]],[1,1,[1,0,0],[-1,-1,0]],[1,-1,[1,2,-3],[-1,-3,3]],[1,-1,[2,1,0],[-2,-2,0]],[1,0,[2,3,-3],[-2,-2,3]],[1,0,[3,2,3],[-3,-1,-3]],[1,0,[3,3,2],[-3,-2,-2]]];
 const sites=[[-1,-1,-1],[5,0,0],[0,1,0],[0,0,1]];
 const n=[5,1,5,5], k=[2,1,2,5], d=[3,0,3,0];
 const check=(x,m)=>{if(!x)throw Error(m);};
 for(let i=0;i<3;i++)check(sites.reduce((s,q,j)=>s+q[i]*n[j],0)===0,'kernel');
 check(k.every((v,i)=>v+d[i]===n[i]),'QCD anomaly alignment');
 const fields=[{n:18,q:[0,0,0,1]},{n:9,q:[-1,0,-1,-4]},{n:9,q:[0,0,0,2]},{n:6,q:[0,0,0,-3]},{n:3,q:[0,0,0,6]}];
 k.forEach((v,i)=>fields.push({n:3*v,q:[...sites[i],-2]},{n:3*v,q:[0,0,0,2]}));
 const massChecks=[];
 pairs.forEach(([mult,y,a,b],i)=>{
   fields.push({n:mult,q:[...a,6*y]},{n:mult,q:[...b,-6*y]});
   const index=i<12?0:i<16?1:2;
   const conjugate=(i>=7&&i<12)||(i>=14&&i<16)||i>=19;
   const sign=conjugate?-1:1;
   const residual=a.map((v,j)=>v+b[j]+sign*sites[index][j]);
   check(residual.every(v=>v===0),'spectator mass term');
   massChecks.push({type:i+1,scalar_site:index+1,conjugate,residual});
 });
 const grav=[0,1,2,3].map(i=>fields.reduce((s,f)=>s+f.n*f.q[i],0));
 check(grav.every(v=>v===0),'mixed gravitational anomaly');
 const cubic=[];
 for(let i=0;i<4;i++)for(let j=i;j<4;j++)for(let h=j;h<4;h++){
   const sum=fields.reduce((s,f)=>s+f.n*f.q[i]*f.q[j]*f.q[h],0);
   check(sum===0,'Abelian cubic anomaly');cubic.push({indices:[i,j,h],sum});
 }
 // q4=6Y in exact integer anomaly calculation; physical Y for kinetic B.
 const B=Array.from({length:4},()=>Array(4).fill(0));
 const add=(mult,q,weight)=>{for(let i=0;i<4;i++)for(let j=0;j<4;j++)B[i][j]+=weight*mult*q[i]*q[j];};
 fields.forEach(f=>add(f.n,[...f.q.slice(0,3),f.q[3]/6],2/3));
 const scalars=sites.map(q=>({n:1,q:[...q,0]})).concat([{n:2,q:[1,0,1,.5]},{n:2,q:[0,0,0,-.5]}]);
 scalars.forEach(f=>add(f.n,f.q,1/3));
 const K=(gx)=>B.map((row,i)=>row.map((v,j)=>(i===j?1/(i===3?.4:gx)**2:0)-v*Math.log(2.435e18/1e12)/(8*Math.PI**2)));
 const cholesky=(A)=>{
   const L=A.map(r=>r.map(v=>0));let min=Infinity;
   for(let i=0;i<4;i++)for(let j=0;j<=i;j++){
     let v=A[i][j];for(let h=0;h<j;h++)v-=L[i][h]*L[j][h];
     if(i===j){if(v<=0)return {positive:false,failed_pivot:v};L[i][j]=Math.sqrt(v);min=Math.min(min,v);}
     else L[i][j]=v/L[j][j];
   }
   return {positive:true,min_cholesky_pivot:min};
 };
 let lo=.001,hi=1;
 for(let i=0;i<100;i++){const mid=(lo+hi)/2;if(cholesky(K(mid)).positive)lo=mid;else hi=mid;}
 const rows=[.05,.1,.15,.2].map(gx=>({g_hidden_input:gx,K_high:K(gx),positive_kinetic:cholesky(K(gx))}));
 const out={status:'PASS_PUBLISHED_STAR_CHARGE_AND_MATRIX_REPRODUCTION',
 source:'https://arxiv.org/html/2606.05276v2',source_scope:'Tables1-2 factual charge data; equations10,14,16 and AppendixC. Mathematical reproduction of published model, not a newly discovered protection.',
 table2_pairs:pairs,field_blocks_q4_equals_6Y:fields,scalar_blocks_physical_Y:scalars,allowed_spectator_mass_checks:massChecks,
 primitive_kernel:n,published_quality_dimension:16,
 domain_wall_input_alignment:{k,d,k_plus_d:n},additional_colored_Dirac_flavors:10,QCD_one_loop_asymptotic_freedom_coefficient:'11-2*16/3=1/3',
 gravitational_Abelian_sums:grav,all_symmetric_Abelian_cubic_sums:cubic,
 spectator_pairs:pairs.reduce((s,p)=>s+p[0],0),sum_multiplicity_Y_squared:pairs.reduce((s,p)=>s+p[0]*p[1]**2,0),
 B_full_at_common_threshold:B,illustrative_running:rows,
 benchmark:{threshold_GeV:1e12,high_GeV:2.435e18,gY_at_threshold_input:.4,initial_kinetic_mixing:0,common_hidden_coupling_upper_positive_K:(lo+hi)/2},
 boundary:'Charge and one-loop unbroken common-threshold audit only. Couplings/scales supplied. Not finite matching, completed EW/hidden scalar vacuum, cosmological spectator decays, full generic-mass determinant quality audit, Z9 seesaw embedding, or TOE. QCD alignment and Abelian anomaly checks do not by themselves certify every physical requirement.',
 ownership:'Matrix RG is prior repo new_front1; model and anomaly spectrum are published Banks-Kongsore-Weiner. No full-UV viability claim from a positive K.'};
 check(rows[0].positive_kinetic.positive,'weak gauge benchmark');
 return out;
})()
