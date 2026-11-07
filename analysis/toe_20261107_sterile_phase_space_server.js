/* Independent positive exponential-midpoint kinetic solver, server V8.
   Established kinetic theory; same declared collision action, different
   quadrature construction and time integrator from the PC BDF solver. */
(async () => {
 const input=[{"M":16,"mS":3000,"w":671.1937248691195,"y":2.3838125130147706e-8,"low":6.511434143528489e-7,"high":7.227307109821025e-7},{"M":16,"mS":10000,"w":367.62794356673294,"y":4.3522262874708903e-8,"low":0.0000011888197873732949,"high":0.0000024091023699403416}];
 const pi=Math.PI,gs=106.75,M0=1.22e19/(1.66*Math.sqrt(gs)),cy=45/(4*pi**4*gs);
 function gauss(n,Q){
   const q=[],w=[];
   for(let i=0;i<n;i++){
     let z=Math.cos(pi*(i+.75)/(n+.5)),pp;
     for(let k=0;k<50;k++){
       let p1=1,p2=0;for(let j=1;j<=n;j++){let p3=p2;p2=p1;p1=((2*j-1)*z*p2-(j-1)*p3)/j;}
       pp=n*(z*p1-p2)/(z*z-1);let nz=z-p1/pp;
       if(Math.abs(nz-z)<1e-15){z=nz;break;}z=nz;
     }
     q.push((z+1)*Q/2);w.push(Q/((1-z*z)*pp*pp));
   }
   const order=q.map((v,i)=>i).sort((a,b)=>q[a]-q[b]);
   return [order.map(i=>q[i]),order.map(i=>w[i])];
 }
 const pack=(r,lam)=>({M:r.M,mS:r.mS,w:r.w,y:r.y,lam,
    A:lam*lam*M0/(32*pi**3*r.mS),
    DN:M0*r.y*r.y/(16*pi*r.mS),
    DH:M0*lam*lam*r.w*r.w/(8*pi*r.mS**3)});
 const old=r=>pack(r,Math.sqrt(r.low*r.high));
 function family(M){
   const mS=1000,eta=.8,mg=M*1e-6,K=2.2e-6*125.25**2/(Math.sqrt(2)*.053);
   const ratio=(eta*K/(mg*mS))**2;
   const dn0=.12/(2.744e8*mg*2*cy*3*pi/2);
   const y=Math.sqrt(16*pi*mS/M0*dn0*(1+1/ratio)),w=mg/y;
   const lam=eta*2.2e-6*125.25**2/(.053*2*w*w);
   return pack({M,mS,w,y},lam);
 }
 function evolve(p,thermal,n=48,steps=4096){
   const [q,w]=gauss(n,50),nw=q.map((v,i)=>w[i]*v*v);
   const ang=q.map(a=>q.map(b=>Math.exp(-Math.abs(a-b)/2)*(-Math.expm1(-Math.min(a,b)))));
   const f=q.map(x=>thermal?Math.exp(-Math.hypot(x,.001)):0);
   let N=0,M1=0,M2=0;
   const ratio=Math.log(120/.001)/steps;
   for(let k=0;k<steps;k++){
     const a=.001*Math.exp(ratio*k),b=.001*Math.exp(ratio*(k+1)),r=(a+b)/2,h=b-a;
     const E=q.map(x=>Math.hypot(x,r)),eq=E.map(x=>Math.exp(-x)),jw=nw.map((v,i)=>v/E[i]);
     let Jeq=0;for(let i=0;i<n;i++)Jeq+=jw[i]*eq[i];
     const gain=Array.from({length:n},()=>Array(n).fill(0)),loss=Array(n).fill(0);
     for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j){
       const common=2*p.A/(E[i]*q[i])*w[j]*q[j]/E[j]*ang[i][j],d=(E[j]-E[i])/2;
       gain[i][j]=common*Math.exp(d);loss[i]+=common*Math.exp(-d);
     }
     function stage(state,dt){
       let J=0;for(let i=0;i<n;i++)J+=jw[i]*state[i];
       const out=[];
       for(let i=0;i<n;i++){
         let G=(p.A*Jeq+p.DH*r*r)*eq[i]/E[i];
         for(let j=0;j<n;j++)G+=gain[i][j]*state[j];
         const R=(p.A*J+(p.DH+p.DN)*r*r)/E[i]+loss[i];
         const one=-Math.expm1(-R*dt);
         out[i]=f[i]*(1-one)+(R===0?G*dt:G/R*one);
       }
       return out;
     }
     const mid=stage(f,h/2),next=stage(mid,h);
     for(let i=0;i<n;i++){
       const sink=2*p.DN*r*r*jw[i]*mid[i]*h;
       N+=sink;M1+=sink*E[i]/2;M2+=sink*(E[i]*E[i]/4+q[i]*q[i]/12);
       f[i]=next[i];
       if(f[i]<0||!Number.isFinite(f[i]))throw Error('positivity');
     }
   }
   return {M_keV:p.M,m_S_GeV:p.mS,initial_scalar:thermal?'thermal_MB':'zero',nq:n,steps,
     omega_h2:2.744e8*p.M*1e-6*cy*N,mean_q:M1/N,rms_q:Math.sqrt(M2/N),
     remaining_scalar_Y:cy*f.reduce((s,v,i)=>s+v*nw[i],0),parameters:p};
 }
 const rows=[];
 for(const r of input)for(const thermal of [false,true]){
   const out=evolve(old(r),thermal);rows.push(out);
   if(typeof notify==='function')notify({server:'kinetic',M:out.M_keV,mS:out.m_S_GeV,initial:out.initial_scalar,omega:out.omega_h2});
   if(typeof yield_control==='function')await yield_control();
 }
 const reopened=[];
 for(const M of [16,30,100]){
   const out=evolve(family(M),false);reopened.push(out);
   if(typeof notify==='function')notify({server:'inverse_branch',M,omega:out.omega_h2});
   if(typeof yield_control==='function')await yield_control();
 }
 const refined=evolve(family(16),false,64,8192);
 return {status:'PASS_INDEPENDENT_SERVER_POSITIVE_KINETIC_INTEGRATOR',
   execution:'Actual functions.exec server V8; independent Newton-Legendre quadrature and positive exponential midpoint. No PC Python calls.',
   input_source:'data/toe_20261106_sterile_parent_consistency.json, first two stored points; new family uses declared mass/clock inputs',
   rows,reopened,refined_branch16:refined,
   scope:'Same classical collision truncation as PC: contact annihilation, elastic bath scattering, bath decays/inverse decays and one-way sterile decays. Finite-temperature masses, quantum factors, varying degrees of freedom, NN backreaction, scalar self interactions, UV protection and cosmological transfer function absent. Numerical agreement does not validate those missing physical assumptions.'};
})()
