function projective(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},V=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**j)%3)),P=V(4).filter(v=>v.find(x=>x!==0)===1),q=v=>v.flatMap((x,i)=>v.slice(i).map(y=>m(x*y))),Q=P.map(q),dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),w=x=>x.filter(Boolean).length,phase=x=>x===2?-1:x;
A(P.length===40,'PG');
let enumerators=[Array(41).fill(0),Array(41).fill(0),Array(41).fill(0)],dx=40,phaseChecks=0;
for(let c of V(10)){let u=Q.map(v=>dot(v,c));for(let a=0;a<3;a++){let v=u.map(x=>m(x+a));enumerators[a][w(v)]++;if(a)dx=Math.min(dx,w(v));A((v.reduce((s,x)=>s+phase(x),0)-4*phase(a))%9===0,'T^4');phaseChecks++}}
A(dx===13&&enumerators[0][0]===1&&enumerators[1][0]===0,'distance X and dimension');
let rows=[P.map(()=>1),...Array.from({length:10},(_,i)=>Q.map(v=>v[i]))],ccz=0;
for(let i=0;i<11;i++)for(let j=0;j<11;j++)for(let k=0;k<11;k++){A(m(P.reduce((s,_,l)=>s+rows[i][l]*rows[j][l]*rows[k][l],0))===+(i===0&&j===0&&k===0),'CCZ');ccz++}
const key=v=>v.join(''),canon=v=>{let f=v.find(Boolean);return v.map(x=>m(x*f))},idx=new Map(P.map((v,i)=>[key(v),i])),lines=new Set();
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){let u=P[i],v=P[j],l=[i,j,idx.get(key(canon(u.map((x,k)=>m(x+v[k]))))),idx.get(key(canon(u.map((x,k)=>m(x-v[k])))))].sort((a,b)=>a-b);lines.add(l.join(','))}
let isotropic=0;for(let s of lines){let l=s.split(',').map(Number),u=P[l[0]],v=P[l[1]];if(!m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1]))isotropic++;A(Q[0].every((_,j)=>m(l.reduce((s,i)=>s+Q[i][j],0))===0),'line logical')}
let low=0;for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)for(let k=j+1;k<40;k++)for(let b of [1,2])for(let c of [1,2]){A(!Q[i].every((x,l)=>m(x+b*Q[j][l]+c*Q[k][l])===0),'weight3 dependence');low++}
const C=(n,k)=>{if(k<0||k>n)return 0n;let x=1n;for(let i=1;i<=k;i++)x=x*BigInt(n-i+1)/BigInt(i);return x},MW=(en,r)=>Array.from({length:41},(_,k)=>{let s=0n;for(let j=0;j<=40;j++){if(!en[j])continue;let z=0n;for(let l=0;l<=k;l++)z+=(-1n)**BigInt(l)*2n**BigInt(k-l)*C(j,l)*C(40-j,k-l);s+=BigInt(en[j])*z}A(s%3n**BigInt(r)===0n,'MW integer');return s/3n**BigInt(r)});
let full=enumerators[0].map((x,i)=>x+enumerators[1][i]+enumerators[2][i]),accept=MW(enumerators[0],10),good=MW(full,11),bad=accept.map((x,i)=>x-good[i]);
A(bad.slice(0,4).every(x=>x===0n)&&bad[4]>0n,'distance Z');
let prob=p=>{let sum=a=>a.reduce((s,n,k)=>s+Number(n)*(p/2)**k*(1-p)**(40-k),0),a=sum(accept);return {p,accept:a,output:sum(bad)/a,cost:40/a}};
let lo=.0001,hi=.4;for(let i=0;i<60;i++){let p=(lo+hi)/2;if(prob(p).output<p)lo=p;else hi=p}
return {code:'[[40,1,4]]_3',dX:dx,dZ:4,rankX:10,rankZ:29,phaseChecks,logicalT:'T^4',cczChecks:ccz,logicalCCZ:'CCZ',projective_lines:lines.size,isotropic_lines:isotropic,three_column_checks:low,logical_Z_weight4:bad[4].toString(),leading_error_coefficient:Number(bad[4])/16,weight_enumerators:enumerators,accepted_error_weights:accept.map(String),bad_error_weights:bad.map(String),noise:[.001,.01,.02,.05,.1,.15,.2,.25].map(prob),fixed_point:(lo+hi)/2,points:P,quadratic_rows:rows}
}
console.log(JSON.stringify(projective(),null,2));
