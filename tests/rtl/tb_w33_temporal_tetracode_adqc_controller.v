module tb_w33_temporal_tetracode_adqc_controller;
  reg [1:0] n_inf, n_zero, n_plus, n_minus;
  reg c3_apply, pw_enable, pw_reverse, t_enable;
  wire [1:0] hist_a, hist_b, hist_c;
  wire tetracode_plane;
  wire [1:0] common_mode_correction, program_id;
  wire invalid_trit;
  integer a,b,c,d,e;
  integer mi,mz,mp,mm;
  integer ea,eb,ec,es,eg;
  integer errors;
  w33_temporal_tetracode_adqc_controller dut(
    .n_inf(n_inf),.n_zero(n_zero),.n_plus(n_plus),.n_minus(n_minus),
    .c3_apply(c3_apply),.pw_enable(pw_enable),.pw_reverse(pw_reverse),
    .t_enable(t_enable),.hist_a(hist_a),.hist_b(hist_b),.hist_c(hist_c),
    .tetracode_plane(tetracode_plane),
    .common_mode_correction(common_mode_correction),
    .program_id(program_id),.invalid_trit(invalid_trit)
  );

  function integer m3;
    input integer x;
    begin m3 = x % 3; end
  endfunction
  task check_word;
    begin
      if (c3_apply) begin
        mi=a; mz=c; mp=d; mm=b;
      end else begin
        mi=a; mz=b; mp=c; mm=d;
      end
      ea=m3(mz+mp+mm);
      eb=m3(mp+2*mm);
      ec=m3(mi+mp+mm);
      es=m3(mi+mp+2*mm);
      eg=(3-es)%3;
      #1;
      if (invalid_trit !== 1'b0) errors=errors+1;
      if (hist_a !== ea[1:0]) errors=errors+1;
      if (hist_b !== eb[1:0]) errors=errors+1;
      if (hist_c !== ec[1:0]) errors=errors+1;
      if (tetracode_plane !== (ea==0)) errors=errors+1;
      if (ea==0) begin
        if (common_mode_correction !== eg[1:0]) errors=errors+1;
      end else if (common_mode_correction !== 2'd0) errors=errors+1;
    end
  endtask

  initial begin
    errors=0;
    pw_enable=0; pw_reverse=0; t_enable=0;
    for (e=0;e<2;e=e+1) begin
      c3_apply=e;
      for (a=0;a<3;a=a+1)
      for (b=0;b<3;b=b+1)
      for (c=0;c<3;c=c+1)
      for (d=0;d<3;d=d+1) begin
        n_inf=a; n_zero=b; n_plus=c; n_minus=d;
        check_word;
      end
    end

    // Program priority and Page-Wootters orientation selectors.
    n_inf=0; n_zero=0; n_plus=0; n_minus=0; c3_apply=0;
    t_enable=0; pw_enable=0; pw_reverse=0; #1;
    if (program_id!==2'd0) errors=errors+1;
    pw_enable=1; pw_reverse=0; #1;
    if (program_id!==2'd1) errors=errors+1;
    pw_reverse=1; #1;
    if (program_id!==2'd2) errors=errors+1;
    t_enable=1; #1;
    if (program_id!==2'd3) errors=errors+1;

    // Invalid-trit firewall.
    t_enable=0; pw_enable=0; n_inf=3; #1;
    if (invalid_trit!==1'b1 || tetracode_plane!==1'b0) errors=errors+1;

    if (errors==0) begin
      $display("PASS 162_valid_counter_cases_plus_control_checks");
      $finish(0);
    end
    else begin
      $display("FAIL errors=%0d",errors);
      $finish(1);
    end
  end
endmodule
