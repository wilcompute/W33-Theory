"""TOE93 conditional finite-block Witting key-rate ledger.

Trusted known IID isotropic ququart model and virtual complementary
MUB estimate, not a composable device-independent security proof.
Pessimistically subtract the exact public syndrome/tag bit counts.
"""
from __future__ import annotations
import json, math
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
N=196
TAG=16
EPS=1e-6
def qary_max_entropy(q):
    return 2*math.log2(math.sqrt(1-q)+math.sqrt(3*q))
def ledger(v):
    q=3*(1-v)/4
    hmin=N*(2-qary_max_entropy(q))
    synd=6*(N//7)
    transcript=synd+TAG+1
    overhead=2*math.log2(1/(2*EPS))
    ell=max(0,math.floor(hmin-transcript-overhead))
    return {'visibility':v,'ququart_error_rate':round(q,12),
      'one_shot_MUB_uncertainty_lower_per_raw_ququart':round(hmin/N,12),
      'whole_block_conditional_min_entropy_lower':round(hmin,9),
      'public_hamming_syndrome_bits':synd,
      'verification_tag_bits':TAG,'accept_flag_bits':1,
      'public_transcript_leak_upper':transcript,
      'privacy_amplification_penalty':round(overhead,9),
      'illustrative_conditional_key_length_bits':ell,
      'correctness_verification_collision_upper':2**(-TAG)}
def xor_columns(block):
    s=0
    for j,b in enumerate(block):
        if b:s^=(j+1)
    return s
def correct_one_block(block,desired):
    corrected=list(block)
    delta=xor_columns(block)^desired
    if delta:corrected[delta-1]^=1
    assert xor_columns(corrected)==desired
    return corrected
def test_single_error_decoder():
    checked=0
    for word in range(128):
        bits=[(word>>k)&1 for k in range(7)]
        s=xor_columns(bits)
        assert correct_one_block(bits,s)==bits
        for i in range(7):
            noisy=bits[:];noisy[i]^=1
            assert correct_one_block(noisy,s)==bits
            checked+=1
    return checked
def certificate():
    decoded=test_single_error_decoder()
    assert decoded==896
    samples=[ledger(v) for v in (0.95,0.98,0.99,0.995,0.999,1.0)]
    assert samples[-1]['illustrative_conditional_key_length_bits']>0
    assert all(samples[i]['illustrative_conditional_key_length_bits']<=samples[i+1]['illustrative_conditional_key_length_bits']
               for i in range(len(samples)-1))
    return {
      'security_premises':'Exact trusted IID isotropic state with virtual conjugate MUB statistics known, uniform secret basis choices, authenticated discussion, and 2-universal public seeded verification/extraction.',
      'MUB_entropy_bound':'Hmin(Z_A^N|E) >= N[2-2log2(sqrt(1-Q)+sqrt(3Q))] assuming compatible trusted virtual X-basis error rate Q.',
      'reconciliation_plan':'Apply separate Hamming(7,4) syndrome decoders to each of the two raw-outcome binary planes. A 7-bit block with at most one bit error is corrected exactly. Multi-error patterns can miscorrect; separate universal-2 equality verification must catch discrepancies except with probability 2^-16.',
      'public_bit_budget':'3 syndrome bits per 7-bit block per bit plane, 16 verification bits, 1 pass/abort announcement; independent public random seeds are included in protocol authentication, not subtracted from entropy.',
      'leftover_hashing_bound':'Under a sound min-entropy lower bound after public transcript, 2-universal hashing with ell <= floor(Hmin - transcript - 2log2(1/(2 eps))) has privacy distance <= eps. Key correctness has additional verification failure bound.',
      'critical_limit':'This is conditional bookkeeping, NOT general composable finite-key security: no finite-sample state estimation, no coherent-attack reduction, no constructed authenticated transcript, and no physically demonstrated correction success.',
      'block_length':N,'single_error_Hamming_decoder_cases_verified':decoded,
      'privacy_epsilon_used':EPS,'audit':samples}
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261015_toe93_conditional_key_ledger.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('KEY',[(r['visibility'],r['illustrative_conditional_key_length_bits']) for r in d['audit']])
