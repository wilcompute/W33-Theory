function topology(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},V=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**(n-1-j))%3)),add=(a,b)=>a.map((x,i)=>m(x+b[i])),w=(a,b,c,d)=>m(a[0]*b[1]*c[2]*d[3]);
let checks=0;
for(let [a,b,c,d,e,f,g,h] of V(8)){
let [P,Q,R,S,T]=[[a,0,0,0],[b,c,0,0],[0,d,e,0],[0,0,f,g],[0,0,0,h]];
A(m(w(Q,R,S,T)-w(add(P,Q),R,S,T)+w(P,add(Q,R),S,T)-w(P,Q,add(R,S),T)+w(P,Q,R,add(S,T))-w(P,Q,R,S))===0,'cocycle');checks++}
let seed=42;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%3},W=V(4),moves={};
function term(v,i){let t=v.filter((_,j)=>i!==j),a=t.slice(1).map((x,j)=>x.map((y,l)=>m(y-t[j][l])));return (i%2?-1:1)*w(...a)}
for(let k of [1,2,3]){let count=0;for(let s=0;s<1000;s++){let v=Array.from({length:6},()=>Array.from({length:4},rng)),terms=v.map((_,i)=>term(v,i));A(m(terms.reduce((a,b)=>a+b,0))===0,'Pachner');count++;
if(k===1){let first=terms[0];for(let u of W){v[0]=u;A(m(first+v.slice(1).reduce((s,_,i)=>s+term(v,i+1),0))===0,'interior sum');count++}}}moves[k+'-'+(6-k)]=count}
function det(a){let M=a.map(r=>r.slice()),d=1;for(let i=0;i<M.length;i++){let j=M.findIndex((r,k)=>k>=i&&m(r[i])!==0);if(j<0)return 0;if(j!==i){[M[i],M[j]]=[M[j],M[i]];d=-d}let c=m(M[i][i]);d=m(d*c);for(let k=i+1;k<M.length;k++){let f=m(M[k][i]*c);M[k]=M[k].map((x,l)=>m(x-f*M[i][l]))}}return m(d)}
let v=[0,0,0,1],types={},rankhist={};for(let a of W){let rad=W.filter(b=>W.every(c=>det([v,a,b,c])===0)),r=rad.length,dim=Math.sqrt(81/r);types[dim]=(types[dim]||0)+r;rankhist[r]=(rankhist[r]||0)+1}
A(types[1]===243&&types[3]===702,'anyon census');A(Object.entries(types).reduce((s,[d,n])=>s+Number(d)**2*n,0)===81**2,'total quantum dimension');
let untwisted=81**3,twisted=untwisted-(81-1)*(81-3)*(81-9);A(twisted===81**2+80*(types[1]+types[3]),'circle trace');
return {cocycle_checks:checks,pachner_checks:moves,T4:{untwisted,twisted},circle_reduction:{zero_holonomy_sectors:81**2,nonzero_holonomy_sectors:types[1]+types[3],dimension_census:types,radical_histogram:rankhist,number_of_nonzero_holonomies:80}}
}
function index(){
const mul=(a,b)=>{let c=Array(16).fill(0);for(let i=0;i<16;i++)for(let j=0;j<16;j++){let x=(i>>2)+(j>>2),y=(i&3)+(j&3);if(x<=3&&y<=3)c[4*x+y]+=a[i]*b[j]}return c},one=()=>[1,...Array(15).fill(0)],lin=(x,y)=>{let a=one();a[4]=x;a[1]=y;return a},inv=(x,y)=>{let a=one(),p=one(),l=lin(-x,-y);l[0]=0;for(let i=1;i<=6;i++){p=mul(p,l);a=a.map((v,j)=>v+p[j])}return a};
let c=one();for(let i=0;i<4;i++)c=mul(mul(c,lin(1,0)),lin(0,1));for(let [x,y] of [[3,0],[0,3],[1,1]])c=mul(c,inv(x,y));
let fundamental=one();for(let [x,y] of [[3,0],[0,3],[1,1]]){let l=lin(x,y);l[0]=0;fundamental=mul(fundamental,l)}
let integ=a=>mul(a,fundamental)[15],part=n=>c.map((v,i)=>(i>>2)+(i&3)===n?v:0);if(!part(1).every(x=>!x)||integ(part(3))!==-18)throw Error('Chern');
let x=lin(1,0),y=lin(0,1);x[0]=y[0]=0;return {cover_euler:integ(part(3)),quotient_euler:integ(part(3))/3,index:integ(part(3))/6,c2_pairings:[integ(mul(part(2),x)),integ(mul(part(2),y))],intersection_numbers:[integ(mul(mul(x,x),x)),integ(mul(mul(x,x),y)),integ(mul(mul(x,y),y)),integ(mul(mul(y,y),y))],c3:part(3)}
}
console.log(JSON.stringify({topology:topology(),index:index()},null,2));
