// Independent actual server V8: scalar-monomial generating function and worldline integral.
const MP=2.435e27,H0=1.44667e-33,M=16000;
function simpson(f,a,b,n){let h=(b-a)/n,s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3;}
function worldline(a,l=1){let R=a/M,x=2*Math.PI*a*l;
 let integral=simpson(v=>Math.exp(-2.5*v-x*(Math.cosh(v)-1)),-8,8,4096);
 return M**2.5/(4*Math.PI**4*R**1.5*l**2.5)*Math.exp(-x)*integral;
}
function closed(a,l=1){let R=a/M,x=2*Math.PI*a*l;
 return 3/(16*Math.PI**6*R**4*l**5)*Math.exp(-x)*(1+x+x*x/3);
}
function ring(N,r,nu){let F=r*MP/Math.sqrt(N),cut=nu?MP/Math.sqrt(nu*N):MP,floop=r*MP/N,u=F*F/(2*cut*cut);
 let log= Math.log10(2)+4*Math.log10(cut)-2*Math.log10(floop*H0)+N/2*Math.log10(u);
 let v=u**(N/2);
 return {N,r,nu,u,leading:log,all:u>=1?null:log-N*Math.log10(1-u)+Math.log10(1+v)-3*Math.log10(1-v)};
}
function choose(n,k){let z=1;for(let j=1;j<=k;j++)z*= (n-k+j)/j;return z;}
function generating(N,u){
 let v=u**(N/2),sum=0;
 for(let m=1;m<=20;m++)for(let k=0;k<=40;k++)sum+=m*m*v**m*choose(N+k-1,k)*u**k;
 let exact=(1-u)**(-N)*v*(1+v)/(1-v)**3;
 return {N,u,truncated:sum,closed:exact};
}
function build(){let a=12,r=.01,R=a/M,f=r*MP,B=2*Math.PI*r*.053,x=-2*B*a*a/(1+Math.sqrt(1-4*B*B*a*a));
 return {runtime:"Actual functions.exec server V8",worldline:[1,6,12].map(a=>({a,positive_integral:worldline(a),closed_harmonic:closed(a)})),
 ring:[[24,1,0],[110,1,0],[850,1,1],[300,.15,9]].map(z=>ring(...z)),
 generating:[2,3,5].map(N=>generating(N,.02)),benchmark:{log10_two_Dirac_curvature_first_harmonic:Math.log10(2*closed(a)/(f*f*H0*H0)),x,beta:-x/(2*Math.PI*r*(a*a+x*x)),ground_max_log_mass:.5*Math.log1p(1/(4*a*a)),g4:1/(2*Math.PI*R*f)},
 scope:"Independent positive proper-time quadrature, scalar-series sum and branch/normalization arithmetic. No independent full KK population kinetics, radial vacuum or cosmology."};}
