function connected(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},gcd=(a,b)=>b?gcd(b,a%b):a<0n?-a:a,F=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return [a/g,b/g]},add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),fmt=a=>a.join('/'),fac=n=>{let p=1n;for(let i=2;i<=n;i++)p*=BigInt(i);return p};
function partitions(n){let out=[];function rec(i,b){if(i===n){out.push(b.map(a=>a.slice()));return}for(let a of b){a.push(i);rec(i+1,b);a.pop()}b.push([i]);rec(i+1,b);b.pop()}rec(0,[]);return out}
function moment(a){let nz=a.filter(x=>x!==0);if(!nz.length)return F(1n,3n**BigInt(a.length));if(nz.some(x=>Math.ceil(x/2)!==Math.ceil(nz[0]/2))||m(nz.reduce((s,x)=>s+(x%2?1:2),0)))return F(0);return F(1n,40n*3n**BigInt(a.length))}
function cum(a,part){let s=F(0);for(let p of part){let t=F((p.length%2?1n:-1n)*fac(p.length-1));for(let b of p){t=mul(t,moment(b.map(i=>a[i])));if(!t[0])break}s=add(s,t)}return s}
let rows=[],census=[];for(let n=2;n<=6;n++){let p=partitions(n),freq={},zero=0;for(let k=0;k<5**n;k++){let a=Array.from({length:n},(_,i)=>Math.floor(k/5**i)%5),v=cum(a,p);if(a.includes(0))A(v[0]===0n,'identity leg');if(!v[0])zero++;else freq[fmt(v)]=(freq[fmt(v)]||0)+1}census.push({n,tuples:5**n,partitions:p.length,zero,nonzero:freq})}
for(let a of [[1,2],[1,1,1],[1,1,2,2],[1,2,3,4],[1,1,1,1,2],[1,1,1,3,4],[1,1,1,1,1,1],[1,2,1,2,3,4]])rows.push({labels:a,coefficient:fmt(cum(a,partitions(a.length)))});
return {census,examples:rows,scope:"Square-free coefficient of log of the multivariate shared-label generating operator. Each valid partition block must be same projective direction and balanced mod3, with normalized Weyl coefficient 1/(40*3^|B|). No identity legs at connected order >=2. This is not entire univariate log, which includes repeated-site powers."}
}
console.log(JSON.stringify(connected(),null,2));
