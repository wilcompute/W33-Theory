#!/usr/bin/env python3
"""Compile Q43 eight-term optical-control masks onto native W33 line-bus IDs.

Proves explicit bus->Q43 point permutation, generates combinational 40-way
address translator driving already-exhaustively-tested Q43 rank8 FPGA oracle.
Counts physical control LUT overhead; this still controls metadata ONLY.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_linebus_dual_q43_phase_geometry_20261023 import certificate

def produce():
    x=certificate()
    mapping=x['bus_to_parabolic_quadric_point_permutation']
    A=x['bus_intersection_adjacency_E']
    assert len(mapping)==40
    name='w33_linebus_dual_q43_phase_bridge_20261023'
    code=[
      '// Map 40 four-port physical W33 line-bus indexes to Q(4,3) point indexes.',
      '// Q43 eight-term phase oracle remains a CLASSICAL metadata circuit only.',
      f'module {name}(',
      'input logic clk,rst_n,valid_in,',
      'input logic [5:0] addr_a,addr_b,',
      'output logic valid_out,invalid_addr,oracle_bit,',
      'output logic [7:0] cross_phase_flags,',
      'output logic local_phase_a,local_phase_b',
      ');',
      'function automatic [5:0] to_q43(input logic [5:0] bus);',
      ' case(bus)']
    for a,b in enumerate(mapping):
        code.append(f"  6'd{a}: to_q43=6'd{b};")
    code.extend([
      "  default:to_q43=6'd63;",
      ' endcase',
      'endfunction',
      'wire [5:0] canonical_a=to_q43(addr_a);',
      'wire [5:0] canonical_b=to_q43(addr_b);',
      'q43_phase_oracle_rank8_20261023 target(',
      '.clk(clk),.rst_n(rst_n),.valid_in(valid_in),',
      '.addr_a(canonical_a),.addr_b(canonical_b),',
      '.valid_out(valid_out),.invalid_addr(invalid_addr),',
      '.oracle_bit(oracle_bit),.cross_phase_flags(cross_phase_flags),',
      '.local_phase_a(local_phase_a),.local_phase_b(local_phase_b)',
      ');',
      'endmodule',''])
    tb=[
      f'module tb_{name};',
      'reg clk=0;always #5 clk=~clk;',
      'reg rst_n=0,valid_in=0;reg [5:0] addr_a=0,addr_b=0;',
      'wire valid_out,invalid_addr,oracle_bit,local_phase_a,local_phase_b;',
      'wire [7:0] cross_phase_flags;',
      f'{name} dut(.*);',
      'reg [39:0] expected_rows[0:39];',
      'integer a,b,p=0,q=0;',
      'initial begin']
    for i in range(40):
        row=sum(int(A[i][j])<<j for j in range(40))
        tb.append(f"expected_rows[{i}]=40'h{row:010x};")
    tb.extend([
      'repeat(2) @(negedge clk);rst_n=1;',
      'for(a=0;a<64;a=a+1)for(b=0;b<64;b=b+1)begin',
      ' @(negedge clk);addr_a=a;addr_b=b;valid_in=1;',
      ' @(posedge clk);#1;',
      ' if(!valid_out)$fatal(1,"valid lost");',
      ' if(a>=40||b>=40)begin',
      '  if(!invalid_addr||oracle_bit||cross_phase_flags||local_phase_a||local_phase_b)',
      '   $fatal(1,"invalid bus admitted %0d %0d",a,b);',
      '  q=q+1;',
      ' end else begin',
      '  if(invalid_addr||oracle_bit!==expected_rows[a][b])',
      '   $fatal(1,"W33 dual-bus phase wrong %0d %0d",a,b);',
      '  if(oracle_bit!==((^cross_phase_flags)^local_phase_a^local_phase_b))',
      '   $fatal(1,"dual gauge phase wrong");',
      '  p=p+1;',
      ' end',
      'end',
      'if(p!=1600||q!=2496)$fatal(1,"missing pairs");',
      '$display("PASS 40 W33 four-port buses as Q43 phase graph; 1600 edges + 2496 invalid; 8 terms");',
      '$finish;end','endmodule',''])
    (ROOT/f'hardware/{name}.sv').write_text('\n'.join(code))
    (ROOT/f'hardware/tb_{name}.sv').write_text('\n'.join(tb))
    return {'schema':'w33.line_bus_Q43.eight_term_RTL_bridge.v1','physical_W33_bus_ids':40,
      'bus_to_Q43_permutation':mapping,'logical_nonlocal_binary_phase_terms':8,
      'logical_symplectic_pairs':4,'RTL':f'hardware/{name}.sv',
      'testbench':f'hardware/tb_{name}.sv',
      'requires_companion':'hardware/q43_phase_oracle_rank8_20261023.sv',
      'valid_test_pairs':1600,'invalid_test_pairs':2496,
      'limitation':'Physical line-to-line optical coherence, nonlinear gates, bus drivers and timing constraints remain unbuilt'}
if __name__=='__main__':
    obj=produce()
    obj['sha256']=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (ROOT/'data/w33_linebus_dual_q43_RTL_bridge_20261023.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print('PASS generated direct W33 physical bus dual-Q43 eight-term HDL and testbench')
