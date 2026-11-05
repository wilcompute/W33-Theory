/* Independent integer and double-precision checks; executed in server V8. */
(() => {
  const gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a);
  let maxDegree=0,twoCharged=0,count=0;
  for(let x=0;x<4;x++)for(let y=0;y<4;y++)for(let z=0;z<4;z++){
    let A=0,B=0;
    [x,y,z].forEach((k,i)=>{const w=[1,2,2][i],s=k%2?-1:1;if(k<2)A+=w*s;else B+=w*s;});
    const g=gcd(A,B),degree=(Math.abs(A)+Math.abs(B))/g;
    maxDegree=Math.max(maxDegree,degree);twoCharged+=Number(A!==0&&B!==0);count++;
  }
  let min=28,solutions=0;
  for(let a=-14;a<=14;a++)for(let b=-14;b<=14;b++)for(let h=-9;h<=9;h++){
    const l=-2*a-26*b-13*h,cost=2*(Math.abs(a)+Math.abs(b))+3*(Math.abs(l)+Math.abs(h));
    if(cost>min||(Math.abs(l)+Math.abs(h))%2||2*a+l===0)continue;
    if(cost<min){min=cost;solutions=0;}solutions++;
  }
  const MP=2.435e18,M=27279937181.61975,r=2*M**5/(MP*.0756**4);
  if(count!==64||maxDegree!==5||min!==18)throw Error('independent check failed');
  return {status:'PASS_SERVER_V8_DETERMINANT_AND_OPERATOR_CHECKS',assignments:count,maxDegree,twoCharged,
    minimumOperatorDimension:min/2,minimizers:solutions,amplitudeOverChi:r,
    sufficientC:1e-10/(r*(1+3e-10)),inducedC:Math.log(MP/(1e11*Math.sqrt(170)))/(8*Math.PI**2),
    scope:'Independent arithmetic, not a second proof of anomaly assumptions or full UV completion.'};
})()
