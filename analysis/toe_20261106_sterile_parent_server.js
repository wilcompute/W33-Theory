/* Independent server-V8 collision integral and portal/scalar consistency replay.
   Ballistic j0 kernels below are a counterexample to mean-only inference,
   not self-gravitating cosmological transfer functions or a Ly-alpha fit. */
(() => {
  const integrate = (f,a,b,n) => {
    const h=(b-a)/n; let sum=f(a)+f(b);
    for(let i=1;i<n;i++) sum+=(i%2?4:2)*f(a+i*h);
    return sum*h/3;
  };
  const I=integrate(t=>6/Math.cosh(t)**3,0,25,20000);
  if(Math.abs(I-3*Math.PI/2)>1e-11) throw Error('collision integral');
  const PI=Math.PI, g=106.75, P=1.22e19, b=.053;
  // Derive the collision coefficient from integral, entropy and Hubble factors.
  const coefficient=2.744e8*2*45*I*P/(4*PI**4*1.66*g**1.5*16*PI);
  const point=(m,s)=>{
    const M=m*1e-6, y=Math.sqrt(.12*s/(coefficient*M));
    const v=Math.sqrt(2)*M/y;
    const low=Math.sqrt(32*PI*1.66*Math.sqrt(g)*s/P);
    const high=2.2e-6*125.25**2/(b*v*v);
    const w=v/Math.sqrt(2);
    return {M_keV:m,m_S_GeV:s,v_S_GeV:v,canonical_real_scalar_vev_GeV:w,lambda_S:s*s/(2*w*w),portal_floor:low,portal_clock_cap:high};
  };
  const boundary=m=>{
    // Independent logarithmic bisection instead of the Python closed form.
    let lo=1e-10, hi=1e18;
    for(let i=0;i<180;i++) {
      const s=Math.sqrt(lo*hi),p=point(m,s);
      if(p.portal_floor>p.portal_clock_cap)lo=s;else hi=s;
    }
    return point(m,Math.sqrt(lo*hi));
  };
  const maximum=limit=>{
    let lo=.1,hi=100;
    for(let i=0;i<100;i++){
      const m=(lo+hi)/2;
      if(boundary(m).lambda_S>limit)hi=m;else lo=m;
    }
    return {lambda_S_cut_input:limit,maximum_M_keV:(lo+hi)/2};
  };
  const j0=x=>x===0?1:Math.sin(x)/x;
  const spectra=[{name:'mono',shells:[[1,1]]},{name:'two_shell',shells:[[.9,.1],[.1,9.1]]}];
  const toy=spectra.map(s=>({name:s.name,
    normalization:s.shells.reduce((t,[w,p])=>t+w,0),
    mean_momentum:s.shells.reduce((t,[w,p])=>t+w*p,0),
    mean_squared_momentum:s.shells.reduce((t,[w,p])=>t+w*p*p,0),
    ballistic_density_kernel_at_k_tau_pi:s.shells.reduce((t,[w,p])=>t+w*j0(Math.PI*p),0)}));
  if(Math.abs(toy[0].mean_momentum-toy[1].mean_momentum)>1e-14)throw Error('means differ');
  if(Math.abs(toy[1].ballistic_density_kernel_at_k_tau_pi)<.8)throw Error('no separation');
  const twoMoments=[[[.5,1],[.5,3]],[[2/9,.5],[5/9,2],[2/9,3.5]]].map(shells=>({
    normalization:shells.reduce((t,[w,p])=>t+w,0),
    mean_momentum:shells.reduce((t,[w,p])=>t+w*p,0),
    mean_squared_momentum:shells.reduce((t,[w,p])=>t+w*p*p,0),
    ballistic_density_kernel_at_k_tau_pi:shells.reduce((t,[w,p])=>t+w*j0(Math.PI*p),0)}));
  if(Math.abs(twoMoments[0].mean_momentum-twoMoments[1].mean_momentum)>1e-14 || Math.abs(twoMoments[0].mean_squared_momentum-twoMoments[1].mean_squared_momentum)>1e-14)throw Error('two moments differ');
  if(Math.abs(twoMoments[0].ballistic_density_kernel_at_k_tau_pi-twoMoments[1].ballistic_density_kernel_at_k_tau_pi)<.12)throw Error('no two-moment separation');
  return {status:'PASS_SERVER_INTEGRAL_CONTINUOUS_BOUNDARY_AND_MEAN_COUNTEREXAMPLE',
    execution:'JavaScript executed in functions.exec server V8; no PC Python imports',
    collision_integral:I,collision_integral_exact:'3 pi / 2',
    incoming_points:[[16,3000],[16,10000],[18,10000],[20,10000]].map(([m,s])=>point(m,s)),
    continuous_boundaries:[7.1,15,16,18,20,30].map(boundary),
    cut_maxima:[1,4*PI,16*PI**2/18].map(maximum),same_mean_ballistic_counterexample:toy,
    same_mean_and_rms_ballistic_counterexample:twoMoments,
    scope:'Isotropic momentum shells propagate freely with j0(k v tau). This proves a mean momentum does not fix even a ballistic density kernel. It does not compute gravity, actual scalar-decay distributions or a cosmological exclusion.'};
})()
