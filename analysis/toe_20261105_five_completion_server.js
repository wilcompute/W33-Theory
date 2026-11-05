(() => {
  const check=(x,s)=>{if(!x)throw Error(s);};
  const rows=[];
  for(let n=2;n<=40;n++) {
    const charges=[[-1,6*n],[n,6],[1,6*n],[-n,6]];
    check(charges.reduce((z,[q,m])=>z+m*q,0)===0,'linear anomaly');
    check(charges.reduce((z,[q,m])=>z+m*q*q*q,0)===0,'cubic anomaly');
    const f=1e11*Math.sqrt(n*n+1),d=n+1;
    const logR=Math.log(2)+d*Math.log(f/Math.SQRT2)-(d-4)*Math.log(2.435e18)-4*Math.log(.0756);
    const r=Math.exp(logR),pass=r<1/3 && r/(1-3*r)<1e-10;
    rows.push({n,leading_dimension:d,pass});
  }
  const first=rows.find(x=>x.pass);check(first.n===13,'protection cost');
  const bX=8*13*14+4*(1+13*13)/3;
  const mu=3964835648946381,mp=2.435e18,k=mu**3/(2*mp*mp);
  const result={status:'PASS_INDEPENDENT_SERVER_FIVE_COMPLETION_CONTROLS',first_quality_n:first.n,
    leading_dimension:first.leading_dimension,integer_anomaly_cases:39,bX,
    corrected_common_Yukawa_coefficient:1+3+6+6,k_over_M5:k/mu,
    scope:'Independent integer, logarithmic quality and dimensional controls, not full physical completion.'};
  if(typeof process!=='undefined')console.log(JSON.stringify(result));return result;
})()
