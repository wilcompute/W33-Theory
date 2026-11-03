/* Independent coordinate construction and modular DP, also run in functions.exec
 * on the V8 server while Python validation ran through Remote Desktop Commander.
 * Reproduce locally: node analysis/w33_20261103_kagome_server_crosscheck.js
 * The frozen data receipt records the original server-side run.
 */
function crosscheck() {
  const m=4,n=6,vs=[];
  for(let x=0;x<m;x++)for(let y=0;y<n;y++)if(x%2||y%2)vs.push([x,y]);
  const key=(x,y)=>`${(x+m)%m},${(y+n)%n}`;
  const ix=new Map(vs.map((v,i)=>[key(...v),i]));
  const masks=vs.map(([x,y])=>[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1]].reduce((r,[a,b])=>{
    const j=ix.get(key(x+a,y+b));return j===undefined?r:r|(1<<j);
  },0));
  function bits(x){let n=0;for(;x;x&=x-1)n++;return n;}
  const size=1<<vs.length,cut=new Int16Array(size),checks=[];
  for(let S=1;S<size;S++){
    const bit=S&-S,j=31-Math.clz32(bit),T=S^bit;
    cut[S]=cut[T]+bits(masks[j])-2*bits(T&masks[j]);
  }
  for(const pp of [1000000007,1000000009]){
    const p=BigInt(pp);
    function pow(a,b){let r=1n;for(;b;b>>=1n,a=a*a%p)if(b&1n)r=r*a%p;return r;}
    const inv=new Map([...new Set(cut.slice(1,-1))].map(c=>[c,pow(BigInt(3*c/2),p-2n)]));
    const d=new Float64Array(size);d[0]=1;
    for(let S=1;S<size;S++){
      let sum=0;for(let T=S;T;T&=T-1)sum+=d[S^(T&-T)];
      d[S]=S===size-1?sum%pp:Number(BigInt(sum%pp)*inv.get(cut[S])%p);
    }
    const expected=Number((23259766347797390440995449137n%p)*pow(2645785072959855023554560000000000n%p,p-2n)%p);
    if(d[size-1]!==expected)throw Error('Independent coefficient mismatch');
    checks.push({prime:pp,computed_residue:d[size-1],certificate_residue:expected});
  }
  return {status:'PASS_INDEPENDENT_SERVER_MODULAR_4X6_TUNNELING',active_vertices:vs.length,
    edges:masks.reduce((a,b)=>a+bits(b),0)/2,subsets:size,checks};
}
if(typeof module!=='undefined'){
  module.exports={crosscheck};
  if(require.main===module)process.stdout.write(JSON.stringify(crosscheck(),null,2)+'\n');
}
