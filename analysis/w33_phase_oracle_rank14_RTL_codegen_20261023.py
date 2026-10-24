#!/usr/bin/env python3
"""Generate registered UP5K 14-cross-term W33 phase oracle from 7-pair cert.

The resulting 14 masks are CLASSICAL FPGA truth bits specifying required
parity-product phase terms. They do not actually apply a coherent quantum CZ,
nor do FPGA pins directly drive optical electrodes without suitable DACs.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_photonic_five_fronts_GF2_phase_causal_break_20261023 import adjacency
from w33_phase_oracle_seven_symplectic_pairs_20261023 import certificate
def produce():
    p=certificate()
    A=adjacency()
    masks_a=[];masks_b=[]
    for a in range(40):
        ma=0;mb=0
        for k,sp in enumerate(p['seven_pairs']):
            x=sp['x_flag_40'][a];y=sp['y_flag_40'][a]
            if x:ma|=1<<(2*k)
            if y:ma|=1<<(2*k+1)
            if y:mb|=1<<(2*k)
            if x:mb|=1<<(2*k+1)
        masks_a.append(ma|(p['first_local_sign_table'][a]<<14))
        masks_b.append(mb|(p['second_local_sign_table'][a]<<14))
    def decoder(fn,arr):
        lines=[f'  function automatic [14:0] {fn}(input logic [5:0] addr);',
          '   case(addr)']
        for k,v in enumerate(arr):lines.append(f"    6'd{k}: {fn}=15'h{v:04x};")
        return '\n'.join(lines+[
           f"    default: {fn}=15'h0000;",
           '   endcase',
           '  endfunction'])
    rtl='\n'.join([
      '// Compiler-derived exact W33 GF(2) oracle: seven symplectic pairs = 14 products.',
      '// Requires local phases and coherent physical CZ hardware; HDL is classical control ONLY.',
      'module w33_phase_oracle_rank14_20261023(',
      ' input logic clk, rst_n, valid_in,',
      ' input logic [5:0] addr_a, addr_b,',
      ' output logic valid_out, invalid_addr, oracle_bit,',
      ' output logic [13:0] cross_phase_flags,',
      ' output logic local_phase_a,local_phase_b',
      ');',
      decoder('decode_a',masks_a),
      decoder('decode_b',masks_b),
      'wire [14:0] da=decode_a(addr_a), db=decode_b(addr_b);',
      'wire invalid_comb=(addr_a>=6\'d40)||(addr_b>=6\'d40);',
      'wire [13:0] cross_comb=da[13:0]&db[13:0];',
      'wire flip_comb=(^cross_comb)^da[14]^db[14];',
      'always_ff @(posedge clk or negedge rst_n) begin',
      " if (!rst_n) begin valid_out<=0;invalid_addr<=0;oracle_bit<=0;",
      " cross_phase_flags<=0;local_phase_a<=0;local_phase_b<=0;end",
      ' else begin',
      '   valid_out<=valid_in;',
      '   invalid_addr<=valid_in&&invalid_comb;',
      '   oracle_bit<=valid_in&&!invalid_comb&&flip_comb;',
      "   cross_phase_flags<=(valid_in&&!invalid_comb)?cross_comb:14'd0;",
      '   local_phase_a<=valid_in&&!invalid_comb&&da[14];',
      '   local_phase_b<=valid_in&&!invalid_comb&&db[14];',
      ' end',
      'end',
      'endmodule',''])
    tb=['module tb_w33_phase_oracle_rank14_20261023;',
       'reg clk=0;always #5 clk=~clk;',
       'reg rst_n=0,valid_in=0;reg [5:0] addr_a=0,addr_b=0;',
       'wire valid_out,invalid_addr,oracle_bit,local_phase_a,local_phase_b;',
       'wire [13:0] cross_phase_flags;',
       'w33_phase_oracle_rank14_20261023 dut(.*);',
       'reg [39:0] expected_rows[0:39];',
       'integer i,j,ok=0,bad=0;',
       'initial begin']
    for a in range(40):
        row=int(sum(int(A[a,b])<<b for b in range(40)))
        tb.append(f" expected_rows[{a}]=40'h{row:010x};")
    tb.extend([
       ' repeat(2) @(negedge clk);rst_n=1;',
       ' for(i=0;i<64;i=i+1) for(j=0;j<64;j=j+1)begin',
       '  @(negedge clk); addr_a=i;addr_b=j;valid_in=1;',
       '  @(posedge clk);#1;',
       '  if(!valid_out)$fatal(1,"missing valid: %d,%d",i,j);',
       '  if(i>=40 || j>=40)begin',
       '    if(!invalid_addr || oracle_bit || cross_phase_flags || local_phase_a || local_phase_b)',
       '       $fatal(1,"invalid address accepted at %d,%d",i,j);',
       '    bad=bad+1;',
       '  end else begin',
       '    if(invalid_addr || oracle_bit!==expected_rows[i][j])',
       '       $fatal(1,"oracle disagreement at %d,%d",i,j);',
       '    if(oracle_bit!==((^cross_phase_flags)^local_phase_a^local_phase_b))',
       '       $fatal(1,"local gauge and cross flags inconsistent at %d,%d",i,j);',
       '    ok=ok+1;',
       '  end',
       ' end',
       ' if(ok!=1600 || bad!=2496)$fatal(1,"coverage count");',
       ' @(negedge clk);valid_in=0;',
       ' @(posedge clk);#1;',
       ' if(valid_out || oracle_bit || cross_phase_flags)$fatal(1,"no valid gating");',
       ' $display("PASS 14-term oracle: all %0d W33 phases, %0d invalid addresses, 7 symplectic pairs",ok,bad);',
       ' $finish;',
       'end',
       'endmodule',''])
    outdir=ROOT/'hardware'
    (outdir/'w33_phase_oracle_rank14_20261023.sv').write_text(rtl)
    (outdir/'tb_w33_phase_oracle_rank14_20261023.sv').write_text('\n'.join(tb))
    return {'schema':'w33.phase_oracle.rank14.RTL_codegen.v1',
      'RTL':'hardware/w33_phase_oracle_rank14_20261023.sv',
      'testbench':'hardware/tb_w33_phase_oracle_rank14_20261023.sv',
      'symplectic_pairs':7,'cross_cz_terms':14,'plus_local_phase_tables':2,
      'valid_address_tests':1600,'invalid_address_tests':2496,
      'total_interface_io_bits':34,'target':'iCE40UP5K SG48',
      'logical_only':'The FPGA computes control masks; it contains NO quantum CZ gate, no photon waveguide, no optical phase actuator or board pinout.'}
if __name__=='__main__':
    obj=produce()
    obj['sha256']=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    p=ROOT/'data/w33_phase_oracle_rank14_RTL_compiler_20261023.json'
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print('PASS generated two SystemVerilog files for 1600 + 2496 oracle and invalid cases')
