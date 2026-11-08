// Load toe_20261107_scalar_self_server.js first, then execute this on server V8.
function coupledScalarRateServer() {
  const rows=[];
  for(const r of [1,3]) {
    // n_eq=units=1 cancels the old wrapper's normalization, leaving
    // beta*|M|^2/(768*pi*E1E2E3). lambdaS=1 defines the rate coefficient.
    const input={r,q:[0,1000],n_eq:1,points:[{M_keV:0,lambdaS:1,units:1,log_ratio:[0,0]}]};
    const raw=scalarSelfServer(input,262144).rows[0];
    rows.push({inverse_dark_temperature:r,
      gamma32_over_n_eq_cubed_per_lambdaS_cubed:raw.gamma32_over_nS_H,
      estimated_standard_error:raw.estimated_standard_error[0],count:262144});
  }
  return {runtime:'Actual server V8; independent ordinary MC gamma-rejection sampler',rows,
    scope:'Thermal chemical rate coefficients only; not an independent coupled ODE integration.'};
}
