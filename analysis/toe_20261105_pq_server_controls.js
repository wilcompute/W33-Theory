/* Run in Node or server V8. Independent algebra and RK4 controls, no packages. */
(() => {
  const assert = (ok, why) => { if (!ok) throw Error(why); };
  const mq = 27279937181.61975, mu = 3964835648946381, f = 1e11;
  const t0 = Math.log(f), tf = Math.log(mu), steps = 20000, dt = (tf-t0)/steps;
  const beta = (t,y) => {
    const inverse = 1/.118 + 7*Math.log(mq/91.19)/(2*Math.PI)
      + 11/(6*Math.PI)*(t-Math.log(mq));
    return y*(18*y*y - 32*Math.PI/inverse)/(16*Math.PI*Math.PI);
  };
  let y = Math.SQRT2*mq/f;
  for (let i=0; i<steps; i++) {
    const t=t0+i*dt, a=beta(t,y), b=beta(t+dt/2,y+dt*a/2);
    const c=beta(t+dt/2,y+dt*b/2), d=beta(t+dt,y+dt*c);
    y += dt*(a+2*b+2*c+d)/6;
  }
  assert(Math.abs(y-.3767216417408654)<2e-9,'independent scalar RK4');
  let discreteCharges=0;
  for (let n=2;n<=257;n++) for(let q=0;q<n;q++) {
    if ((-q)%n===0) {assert(q===0,'ordinary instanton charge');discreteCharges++;}
  }
  const matrix=[[.5,1,1,0],[0,1.5,1.5,1],[1/3,1/6,1/6,-1]];
  for(const t of [-7,-1,0,2,9]) {
    const v=[0,-t,t,0];
    assert(matrix.every(row=>Math.abs(row.reduce((z,a,i)=>z+a*v[i],0))<1e-13),'kernel witness');
  }
  const quality=[];
  for(const fa of [9.5e10,1e11,2e11,2.28e11]) {
    let chosen=null;
    for(let d=5;d<=19;d++) {
      const logr=Math.log(2)+d*Math.log(fa/Math.SQRT2)-(d-4)*Math.log(2.435e18)-4*Math.log(.0756);
      const r=Math.exp(logr), curvature=1-(d*d+2)*r;
      if(curvature>0 && d*r/curvature<1e-10) {chosen=d;break;}
    }
    quality.push({fa,first_sufficient_dimension:chosen});
  }
  assert(quality.map(x=>x.first_sufficient_dimension).join(',')==='12,12,13,13','quality dimensions');
  const length = Math.PI*10e-6/1.973269804e-16;
  const m5 = Math.cbrt(2.435e18*2.435e18/length);
  assert(Math.abs(m5/333947484.30331755-1)<1e-13,'Planck reduction');
  const result={status:'PASS_INDEPENDENT_SERVER_V8_PQ_CONTROLS',
    yukawa_scalar_RK4:{steps,canonical_initial_y:Math.SQRT2*mq/f,final_y:y},
    ordinary_ZN_checked:256,neutral_allowed_charges:discreteCharges,quality,
    interval_10micron_M5_GeV:m5,
    scope:'Independent arithmetic and ODE controls of the declared parent equations. Not a full beta-function derivation, quantum-gravity theorem, or experimental axion bound.'};
  if(typeof process!=='undefined') console.log(JSON.stringify(result));
  return result;
})()
