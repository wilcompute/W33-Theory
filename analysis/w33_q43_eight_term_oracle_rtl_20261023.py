#!/usr/bin/env python3
"""Q(4,3) eight-cross-term companion to W33 14-term registered phase oracle.

Both circuits: 6-bit address A,B, 0..39 valid, input valid, one-cycle
registered oracle truth bit, cross term AND flags, two one-body phase
flags. They are classical phase-control mask logic, NOT physical CZ gates.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_q43_cospectral_mode_entanglement_phase_complexity_20261023 import graphs,phase_model

def produce():
    _,A=graphs()
    p=phase_model('Q(4,3)',A)
    pairs=p['symplectic_pair_flag_tables']
    assert len(pairs)==4
    rank=2*len(pairs)
    first=p['left_local_phase_table'];second=p['right_local_phase_table']
    ma=[];mb=[]
    for a in range(40):
        va=0;vb=0
        for k,z in enumerate(pairs):
            x=z['x'][a];y=z['y'][a]
            if x:va|=1<<(2*k)
            if y:va|=1<<(2*k+1)
            if y:vb|=1<<(2*k)
            if x:vb|=1<<(2*k+1)
        ma.append(va|(first[a]<<rank))
        mb.append(vb|(second[a]<<rank))
    def fn(name,values):
        v=[f'function automatic [{rank}:0] {name}(input logic [5:0] addr);','  case(addr)']
        for i,z in enumerate(values):v.append(f"    6'd{i}: {name}={rank+1}'h{z:03x};")
        v.extend([f"    default: {name}={rank+1}'h000;",
                    '  endcase','endfunction'])
        return '\n'.join(v)
    rtl='\n'.join([
      '// Four hyperbolic pairs (8 cross terms), plus two local sign lookups.',
      '// Purely CLASSICAL codeword phase metadata; no coherent physical CZ implemented.',
      'module q43_phase_oracle_rank8_20261023(',
      'input logic clk,rst_n,valid_in,',
      'input logic [5:0] addr_a,addr_b,',
      'output logic valid_out,invalid_addr,oracle_bit,',
      'output logic [7:0] cross_phase_flags,',
      'output logic local_phase_a,local_phase_b',
      ');',
      fn('decode_a',ma),fn('decode_b',mb),
      'wire [8:0] da=decode_a(addr_a), db=decode_b(addr_b);',
      "wire invalid_comb=(addr_a>=6'd40)||(addr_b>=6'd40);",
      'wire [7:0] cross_comb=da[7:0]&db[7:0];',
      'wire flip_comb=(^cross_comb)^da[8]^db[8];',
      'always_ff @(posedge clk or negedge rst_n) begin',
      ' if(!rst_n) begin',
      '  valid_out<=0;invalid_addr<=0;oracle_bit<=0;',
      '  cross_phase_flags<=0;local_phase_a<=0;local_phase_b<=0;',
      ' end else begin',
      '  valid_out<=valid_in;',
      '  invalid_addr<=valid_in&&invalid_comb;',
      '  oracle_bit<=valid_in&&!invalid_comb&&flip_comb;',
      "  cross_phase_flags<=(valid_in&&!invalid_comb)?cross_comb:8'd0;",
      '  local_phase_a<=valid_in&&!invalid_comb&&da[8];',
      '  local_phase_b<=valid_in&&!invalid_comb&&db[8];',
      ' end',
      'end',
      'endmodule',''])
    tb=[
      'module tb_q43_phase_oracle_rank8_20261023;',
      'reg clk=0;always #5 clk=~clk;',
      'reg rst_n=0,valid_in=0;reg [5:0] addr_a=0,addr_b=0;',
      'wire valid_out,invalid_addr,oracle_bit,local_phase_a,local_phase_b;',
      'wire [7:0] cross_phase_flags;',
      'q43_phase_oracle_rank8_20261023 dut(.*);',
      'reg [39:0] expected_rows[0:39];',
      'integer i,j,valid_cases=0,invalid_cases=0;',
      'initial begin']
    for a in range(40):
        row=sum(int(A[a,b])<<b for b in range(40))
        tb.append(f"expected_rows[{a}]=40'h{row:010x};")
    tb.extend([
      'repeat(2) @(negedge clk);rst_n=1;',
      'for(i=0;i<64;i=i+1)for(j=0;j<64;j=j+1)begin',
      ' @(negedge clk);addr_a=i;addr_b=j;valid_in=1;',
      ' @(posedge clk);#1;',
      ' if(!valid_out)$fatal(1,"valid missing");',
      ' if(i>=40||j>=40)begin',
      '   if(!invalid_addr||oracle_bit||cross_phase_flags||local_phase_a||local_phase_b)',
      '     $fatal(1,"invalid address accepted %d,%d",i,j);',
      '   invalid_cases=invalid_cases+1;',
      ' end else begin',
      '   if(invalid_addr || oracle_bit!==expected_rows[i][j])',
      '     $fatal(1,"Q43 oracle wrong %d,%d",i,j);',
      '   if(oracle_bit!==((^cross_phase_flags)^local_phase_a^local_phase_b))',
      '     $fatal(1,"Q43 gauge wrong %d,%d",i,j);',
      '   valid_cases=valid_cases+1;',
      ' end',
      'end',
      'if(valid_cases!=1600||invalid_cases!=2496)$fatal(1,"coverage");',
      '@(negedge clk);valid_in=0;',
      '@(posedge clk);#1;',
      'if(valid_out||oracle_bit||cross_phase_flags)$fatal(1,"invalid deassert");',
      '$display("PASS Q43 8-term oracle %0d valid and %0d invalid; 4 symplectic pairs",valid_cases,invalid_cases);',
      '$finish;end','endmodule',''])
    (ROOT/'hardware/q43_phase_oracle_rank8_20261023.sv').write_text(rtl)
    (ROOT/'hardware/tb_q43_phase_oracle_rank8_20261023.sv').write_text('\n'.join(tb)+'\n')
    return {'schema':'w33.q43.eight_term_RTL.v1','generator':'analysis/w33_q43_eight_term_oracle_rtl_20261023.py',
      'rtl':'hardware/q43_phase_oracle_rank8_20261023.sv',
      'testbench':'hardware/tb_q43_phase_oracle_rank8_20261023.sv',
      'binary_cross_terms':8,'symplectic_pairs':4,'one_body_phase_tables':2,
      'valid_address_truth_table_cases':1600,'invalid_address_cases':2496,
      'full_interface_bits':28,
      'reference_w33_cross_terms':14,'reference_w33_interface_bits':34,
      'physical_claim':'Classical registered mask oracle; not a coherent optical phase gate or deployed FPGA'}
if __name__=='__main__':
    x=produce()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (ROOT/'data/q43_phase_oracle_rank8_RTL_manifest_20261023.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS Q43 8-term SystemVerilog generator')
