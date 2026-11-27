function fourthMoment(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3,V=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)),P=V.filter(v=>v.find(Boolean)===1),idx=v=>v.reduce((s,x,j)=>s+m(x)*3**j,0),N=9**4,pow=[1,9,81,729],svec=[[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],act=V.map(v=>Array.from({length:9},(_,q)=>[m(q%3+v[0])+3*m(Math.floor(q/3)+v[1]),m(v[2]*(q%3)+v[3]*Math.floor(q/3)+2*(v[0]*v[2]+v[1]*v[3]))]));
let terms=[];for(let p of P)for(let i=0;i<81;i++){let a=V[i];if(m(a.reduce((s,x)=>s+x,0)))continue;terms.push(a.map(t=>idx(p.map(x=>x*t))))}
A(terms.length===1080,'expansion');let r=new Int32Array(N),s=new Int32Array(N),seen=new Uint8Array(N),touched=[];
function add(i,e,c){if(!seen[i]){seen[i]=1;touched.push(i)}if(e===0)r[i]+=c;else if(e===1)s[i]+=c;else{r[i]-=c;s[i]-=c}}
function apply(q,v,c){let a=act[v[0]][q[0]],b=act[v[1]][q[1]],d=act[v[2]][q[2]],e=act[v[3]][q[3]];add(a[0]+9*b[0]+81*d[0]+729*e[0],(a[1]+b[1]+d[1]+e[1])%3,c)}
function reflect(q,w){let x=m(q.reduce((s,a,i)=>s+w[i]*(a%3),0)),y=m(q.reduce((s,a,i)=>s+w[i]*Math.floor(a/3),0));return q.map((a,i)=>m(a%3+w[i]*x)+3*m(Math.floor(a/3)+w[i]*y))}
let trace=0,traceImag=0;
for(let i=0;i<N;i++){let q=pow.map(p=>Math.floor(i/p)%9);for(let v of terms)apply(q,v,1);trace+=r[i];traceImag+=s[i];add(i,0,-27);for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){let z=q.slice();[z[a],z[b]]=[z[b],z[a]];add(z.reduce((s,x,j)=>s+x*pow[j],0),0,-9)}
for(let a=0;a<4;a++)for(let v=0;v<81;v++)apply(q,Array.from({length:4},(_,j)=>j===a?0:v),-1);
for(let w of svec){let z=reflect(q,w);A(reflect(z,w).join()===q.join(),'involution');add(z.reduce((s,x,j)=>s+x*pow[j],0),0,-9)}
for(let j of touched){A(!r[j]&&!s[j],'identity '+i+' '+j);r[j]=s[j]=seen[j]=0}touched.length=0;
}
A(trace===27*120*81&&!traceImag,'trace');
return {basis_columns:N,terms_per_column:terms.length,trace_M4:trace/27,reflection_vectors:svec,formula:"M4 = I + (1/3) sum_6 S_ij + 3 sum_4 Pi_ijk + (1/3) sum_3 R_s",reflection_action:"q_i -> q_i+s_i sum_j s_j q_j over F3, separately on both qutrit coordinates",reflection_trace:729,reflection_eigenmultiplicity:{plus:3645,minus:2916},scope:"Exact fourth tick moment identity in Eisenstein integers. R_s are orthogonal involutive permutations, preserve sum of replica coordinates, mutually commute; no proof of physical four-body dynamics beyond assumed shared-label ensemble."}
}
console.log(JSON.stringify(fourthMoment(),null,2));
