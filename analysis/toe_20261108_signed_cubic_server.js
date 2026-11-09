// Server-side prime-field and bracket replay of the committed signed triads.
function signedCubicServer(triads) {
  const prime = 103;
  const phases = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
  const mod = x => (x % prime + prime) % prime;
  const sign = w => ((w[0] > w[1]) + (w[0] > w[2]) + (w[1] > w[2])) % 2 ? -1 : 1;
  const word = w => [...w].sort((a,b) => a-b).join(',');
  const inverse = Array(prime).fill(0);
  for (let a = 1; a < prime; ++a) {
    for (let b = 1; b < prime; ++b) if (a*b % prime === 1) inverse[a] = b;
  }
  const terms = triads.map(r => [r.triple, r.sign]);
  const alternating = terms.flatMap(([v,s]) => phases.map(p => [v.map((i,j) => 3*i+p[j]), s*sign(p)]));
  function rank(dimension, input, exterior) {
    const equations = new Map();
    for (const [v, coefficient] of input) {
      for (let axis = 0; axis < 3; ++axis) {
        for (let j = 0; j < dimension; ++j) {
          const w = [...v]; w[axis] = j;
          if (exterior && new Set(w).size < 3) continue;
          const key = word(w), index = dimension*v[axis]+j;
          if (!equations.has(key)) equations.set(key,new Map());
          const row = equations.get(key);
          row.set(index,mod((row.get(index) || 0)+coefficient*(exterior ? sign(w) : 1)));
        }
      }
    }
    const basis = new Map();
    for (const row of equations.values()) {
      for (const [index,value] of row) if (!value) row.delete(index);
      while (row.size) {
        let pivot = -1;
        for (const j of row.keys()) if (j > pivot) pivot = j;
        const value = row.get(pivot);
        if (!basis.has(pivot)) {
          for (const [j,v] of row) row.set(j, mod(v*inverse[value]));
          basis.set(pivot,row);
          break;
        }
        for (const [j,v] of basis.get(pivot)) {
          const entry = mod((row.get(j) || 0)-value*v);
          if (entry) row.set(j,entry); else row.delete(j);
        }
      }
    }
    return {rows:equations.size, rank:basis.size, nullity:dimension**2-basis.size};
  }
  const records = new Map();
  for (const [v,s] of alternating) for (const p of phases) {
    const w = p.map(i => v[i]);
    records.set(81*w[0]+w[1],[w[2],s*sign(p)]);
  }
  const supports = [[0,52,80],[5,37,75],[26,40,54]];
  const bracketL1 = [];
  for (let i = 0; i < 3; ++i) for (let j = i+1; j < 3; ++j) {
    const output = Array(81).fill(0);
    for (const u of supports[i]) for (const v of supports[j]) {
      const entry = records.get(81*u+v);
      if (entry) output[entry[0]] += entry[1];
    }
    bracketL1.push(output.reduce((s,x) => s+Math.abs(x),0));
  }
  return {runtime:'Actual functions.exec V8', prime, symmetric27:rank(27,terms,false),
    exterior81:rank(81,alternating,true), bracketL1, selectedSupports:supports,
    orderedBracketRecords:records.size,
    scope:'Independent descending-pivot modular coefficient ranks and exact selected support brackets. Rational root basis and vacuum Hessian are certified by the separate Python producers.'};
}
