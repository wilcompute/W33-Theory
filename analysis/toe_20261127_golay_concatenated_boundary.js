function concatenation(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),words=new Map([['000000000000',Array(12).fill(0)]]);
for(let r of C)for(let v of [...words.values()])for(let t=1;t<=2;t++){let z=v.map((x,i)=>m(x+t*r[i]));words.set(z.join(''),z)}
function basis(rows){let B=[],p=[];for(let r of rows){let v=r.slice();for(let i=0;i<B.length;i++){let f=v[p[i]];v=v.map((x,j)=>m(x-f*B[i][j]))}let j=v.findIndex(Boolean);if(j>=0){B.push(v.map(x=>m(x*v[j])));p.push(j)}}return B}
let H=basis([...words.values()].filter(x=>!x[0]).map(x=>x.slice(1))),logical=[...words.values()].find(x=>x[0]===1).slice(1),syn=v=>H.map(r=>m(r.reduce((s,x,i)=>s+x*v[i],0))).join(''),phase=v=>m(logical.reduce((s,x,i)=>s+x*v[i],0)),lookup=new Map(),errors=[];
function add(v){let key=syn(v);A(!lookup.has(key),'perfect syndrome');lookup.set(key,v);errors.push(v)}
add(Array(11).fill(0));for(let i=0;i<11;i++)for(let a=1;a<3;a++){let v=Array(11).fill(0);v[i]=a;add(v);for(let j=i+1;j<11;j++)for(let b=1;b<3;b++){let w=v.slice();w[j]=b;add(w)}}A(lookup.size===243,'perfect');

const encode=s=>Array.from(s).reduce((a,x,i)=>a+(+x)*3**i,0),table=Array.from({length:243},(_,i)=>Uint16Array.from({length:243},(_,j)=>{let a=i,b=j,v=0;for(let k=0;k<5;k++){v+=m(a%3+b%3)*3**k;a=Math.floor(a/3);b=Math.floor(b/3)}return v})),leaders=Array.from({length:243},()=>null);
for(let [s,v] of lookup)leaders[encode(s)]={mask:v.reduce((a,x,i)=>a+(x?1<<i:0),0),phase:phase(v)};
let pop=x=>{let n=0;while(x){x&=x-1;n++}return n},cols=Array.from({length:11},(_,i)=>[0,1,2].map(k=>encode(H.map(v=>m(k*v[i])).join("")))),count=Array.from({length:5},()=>Array.from({length:2},()=>({correct:0,flag:0,silent:0})));
function visit(i,w,sx,sz,lx,lz){let a=leaders[sx],b=leaders[sz],wt=pop(a.mask|b.mask);for(let r=1;r<=2;r++){let key=wt>r?"flag":m(lx-a.phase)||m(lz-b.phase)?"silent":"correct";count[w][r-1][key]++}if(w===4)return;
for(let j=i;j<11;j++)for(let k=1;k<9;k++){let x=k%3,z=Math.floor(k/3);visit(j+1,w+1,table[sx][cols[j][x]],table[sz][cols[j][z]],m(lx+x*logical[j]),m(lz+z*logical[j]))}}
visit(0,0,0,0,0,0);const choose=(n,k)=>{let a=1;for(let i=1;i<=k;i++)a=a*(n-i+1)/i;return a};for(let w=0;w<=4;w++)for(let r of count[w])A(Object.values(r).reduce((a,b)=>a+b,0)===choose(11,w)*8**w,"enumeration");
A(count[2][0].silent===0&&count[3][0].silent===0&&count[2][1].silent===0,"radius guarantee");
function probs(p,r){let a={correct:0,flag:0,silent:0},tail=1;for(let w=0;w<=4;w++){let v=(p/8)**w*(1-p)**(11-w);for(let k in a)a[k]+=v*count[w][r-1][k];tail-=choose(11,w)*p**w*(1-p)**(11-w)}return {...a,unclassified_tail:Math.max(0,tail)}}
function bound(n,d,p,r){let v=probs(p,r),f=v.flag,u=v.silent+v.unclassified_tail,c=1-f-u,pass=0;for(let t=0;2*t<d;t++)for(let s=0;2*t+s<d;s++)pass+=choose(n,t)*choose(n-t,s)*u**t*f**s*c**(n-t-s);return {p,r,inner:v,outer_failure_upper:Math.max(0,1-pass)}}
let rows=[];for(let [name,n,d,k] of [["memory",240,3,81],["processor",40,4,1]])for(let p of [.0001,.001,.005,.01])for(let r of [1,2])rows.push({name,n,d,k,concatenated_sites:n*11,concatenated_distance:d*5,...bound(n,d,p,r)});
return {weight_census:count,rows,scope:"Ideal inner Golay syndrome, full Pauli union-support bounded decoder, flags when leader union exceeds radius. Exact enumerated all weight<=4 labels; >=5 conservatively counted as silent error for upper bound. Outer ideal errors-and-erasures decoder guaranteed when 2t+s<d. No physical fault-bearing syndrome or gate synthesis; ideal concatenated storage/output benchmark, not T/CCZ circuit simulation."}
}

console.log(JSON.stringify(concatenation(),null,2));
