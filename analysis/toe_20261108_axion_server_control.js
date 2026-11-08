// Independent server V8 controls; dimensionless supplied benchmark only.
function pin(kappa,u,f=.01,F=10){
 let lo=-u,hi=0;
 for(let j=0;j<100;j++){let a=(lo+hi)/2;if(kappa*a+Math.sin(a+u)>0)hi=a;else lo=a;}
 let alpha=(lo+hi)/2,phase=alpha+u,c=Math.cos(phase);
 let A=(kappa+c)/(f*f),B=c/(f*F),D=c/(F*F);
 let high=(A+D+Math.hypot(A-D,2*B))/2;
 let angle=.5*Math.atan2(2*B,A-D),dot=Math.cos(angle)/f+Math.sin(angle)/F;
 let slope=-f/F*c/(kappa+c);
 let td=(slope/f+1/F)/Math.sqrt(1+slope*slope);
 return {kappa,u,alpha,high,beta:Math.sin(phase)*dot*dot*td/(2*high)};
}
function populations(N,eps,T){
 const k=Array.from({length:N},(_,i)=>2*Math.PI*i/N);
 const mi=k.map(p=>Math.sqrt(1+eps*eps+2*eps*Math.cos(.37+p)));
 const logw=mi.map(m=>1.5*Math.log(m)-m/T),mx=Math.max(...logw);
 let w=logw.map(x=>Math.exp(x-mx)),sum=w.reduce((a,b)=>a+b,0);w=w.map(x=>x/sum);
 let masses=[],maxBeta=0;
 for(let j=0;j<4096;j++){
  const theta=2*Math.PI*j/4096;
  let m=0,dm=0;
  for(let i=0;i<N;i++){let phase=theta+k[i],v=Math.sqrt(1+eps*eps+2*eps*Math.cos(phase));m+=w[i]*v;dm-=w[i]*eps*Math.sin(phase)/v;}
  masses.push(m);maxBeta=Math.max(maxBeta,Math.abs(dm/m));
 }
 const mean=masses.reduce((a,b)=>a+b,0)/masses.length;
 return {N,T,rms:Math.sqrt(masses.reduce((a,b)=>a+(b-mean)**2,0)/masses.length)/mean,maxBeta};
}
function build(){
 const b=.053,eps=2*b/(1+Math.sqrt(1-4*b*b));
 const scan=Array.from({length:38},(_,i)=>{let N=i+3;return {N,log10ratio:Math.log10(N*N/((N-1)*(N-2)*4*Math.PI*Math.PI))+N*Math.log10(eps)+4*Math.log10(16000)-2*Math.log10(2.435e27)-2*Math.log10(1.44667e-33)};});
 const first=scan.find(x=>x.log10ratio<0).N;
 return {runtime:"Actual functions.exec server V8",first_N:first,scan,pinning:[.3,Math.PI/4,1.2].flatMap(u=>[1e-6,.001,1,1000,1e6].map(k=>pin(k,u))),populations:[12,18,first,27].flatMap(N=>[.1,.03,.01,.003].map(T=>populations(N,eps,T))),scope:"Independent bisection/eigenvalue/log-CW-envelope and fixed-weight population controls; not a full cosmology or high-precision CW solver."};
}
