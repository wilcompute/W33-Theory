`timescale 1ns/1ps
module tb_w33_pass2762_holonet_isa;
    logic [1:0] xp,zp,xf,zf,p,f;
    logic [2:0] opcode,lrot,rrot,orot;
    logic dir,regsel,lref,rref,oref;
    logic [1:0] xpn,zpn,xfn,zfn,po,fo;
    integer a,b,c,d,op,di,rs;

    // Sequential ISA interface.
    logic clk = 0;
    logic rst, valid, ready;
    logic [2:0] isa_opcode;
    logic isa_direction, isa_register_select;
    logic [2:0] mirror_rot_operand;
    logic mirror_reflect_operand;
    logic [5:0] magic_index;
    logic magic_ack;
    logic [1:0] isa_xp,isa_zp,isa_xf,isa_zf;
    logic [2:0] mirror_rot;
    logic mirror_reflect,magic_req,retired,fault;
    logic [5:0] magic_ray;
    logic [1:0] magic_grade;
    logic [15:0] magic_consumed;

    always #5 clk = ~clk;

    w33_pass2762_frame_step fs(.xp(xp),.zp(zp),.xf(xf),.zf(zf),.opcode(opcode),
        .direction(dir),.register_select(regsel),.xp_next(xpn),.zp_next(zpn),
        .xf_next(xfn),.zf_next(zfn));
    w33_pass2762_basis_sum bs(.p(p),.f(f),.direction(dir),.p_out(po),.f_out(fo));
    w33_pass2762_d12_mul dm(.left_rot(lrot),.left_reflect(lref),.right_rot(rrot),
        .right_reflect(rref),.out_rot(orot),.out_reflect(oref));
    w33_pass2762_holonet_isa isa(
        .clk(clk),.rst(rst),.valid(valid),.ready(ready),.opcode(isa_opcode),
        .direction(isa_direction),.register_select(isa_register_select),
        .mirror_rot_operand(mirror_rot_operand),
        .mirror_reflect_operand(mirror_reflect_operand),
        .magic_index(magic_index),.magic_ack(magic_ack),
        .xp(isa_xp),.zp(isa_zp),.xf(isa_xf),.zf(isa_zf),
        .mirror_rot(mirror_rot),.mirror_reflect(mirror_reflect),
        .magic_req(magic_req),.magic_ray(magic_ray),.magic_grade(magic_grade),
        .magic_consumed(magic_consumed),.retired(retired),.fault(fault)
    );

    function automatic integer mod3(input integer x);
        begin mod3 = x % 3; if (mod3 < 0) mod3 = mod3 + 3; end
    endfunction
    function automatic integer mod6(input integer x);
        begin mod6 = x % 6; if (mod6 < 0) mod6 = mod6 + 6; end
    endfunction

    task automatic reset_isa;
        begin
            rst=1; valid=0; magic_ack=0; isa_opcode=0; isa_direction=0;
            isa_register_select=0; mirror_rot_operand=0;
            mirror_reflect_operand=0; magic_index=0;
            repeat (2) @(posedge clk);
            #1 rst=0;
        end
    endtask

    task automatic issue(
        input [2:0] op_i,
        input dir_i,
        input reg_i,
        input [2:0] rot_i,
        input ref_i,
        input [5:0] magic_i
    );
        begin
            @(negedge clk);
            isa_opcode=op_i; isa_direction=dir_i; isa_register_select=reg_i;
            mirror_rot_operand=rot_i; mirror_reflect_operand=ref_i;
            magic_index=magic_i; valid=1;
            @(posedge clk); #1 valid=0;
        end
    endtask

    initial begin
        xp=0;zp=0;xf=0;zf=0;opcode=0;dir=0;regsel=0;
        p=0;f=0;lrot=0;lref=0;rrot=0;rref=0;
        rst=0;valid=0;magic_ack=0;isa_opcode=0;isa_direction=0;
        isa_register_select=0;mirror_rot_operand=0;
        mirror_reflect_operand=0;magic_index=0;

        // Both SUM directions on all nine basis states.
        for (di=0; di<2; di=di+1) for (a=0;a<3;a=a+1) for (b=0;b<3;b=b+1) begin
            dir=di; p=a; f=b; #1;
            if (!di && (po!==a || fo!==mod3(a+b))) $fatal(1,"basis p->f");
            if ( di && (po!==mod3(a+b) || fo!==b)) $fatal(1,"basis f->p");
        end

        // Exact frame update for every frame and arithmetic opcode.
        for (a=0;a<3;a=a+1) for (b=0;b<3;b=b+1)
        for (c=0;c<3;c=c+1) for (d=0;d<3;d=d+1)
        for (op=0;op<6;op=op+1) for (di=0;di<2;di=di+1) for (rs=0;rs<2;rs=rs+1) begin
            xp=a;zp=b;xf=c;zf=d;opcode=op;dir=di;regsel=rs;#1;
            case(op)
                0: if(xpn!==mod3(-b)||zpn!==a||xfn!==c||zfn!==d) $fatal(1,"Fp");
                1: if(xpn!==a||zpn!==b||xfn!==mod3(-d)||zfn!==c) $fatal(1,"Ff");
                2: if(zpn!==mod3(b+a)) $fatal(1,"Sp");
                3: if(zfn!==mod3(d+c)) $fatal(1,"Sf");
                4: begin
                    if(!di && (zpn!==mod3(b-d)||xfn!==mod3(c+a))) $fatal(1,"CXpf");
                    if( di && (xpn!==mod3(a+c)||zfn!==mod3(d-b))) $fatal(1,"CXfp");
                end
                5: begin
                    if(!rs && zpn!==mod3(b+1)) $fatal(1,"Zp");
                    if( rs && zfn!==mod3(d+1)) $fatal(1,"Zf");
                end
            endcase
        end

        // Complete D12 multiplication table.
        for(a=0;a<6;a=a+1) for(b=0;b<2;b=b+1)
        for(c=0;c<6;c=c+1) for(d=0;d<2;d=d+1) begin
            lrot=a;lref=b;rrot=c;rref=d;#1;
            if(orot!==mod6(a+(b?-c:c)) || oref!==(b^d)) $fatal(1,"D12");
        end

        // Sequential retirement contract for all opcode families.
        reset_isa();
        if (!ready || magic_req || fault || magic_consumed!=0) $fatal(1,"reset contract");

        // Z_p then F_p: (0,1,0,0) -> (2,0,0,0).
        issue(3'd5,0,0,0,0,0);
        if (!retired || isa_zp!==1) $fatal(1,"sequential Zp");
        issue(3'd0,0,0,0,0,0);
        if (!retired || isa_xp!==2 || isa_zp!==0) $fatal(1,"sequential Fp");

        // D12 left products: r^2 m, then r gives r^3 m.
        issue(3'd6,0,0,3'd2,1,0);
        if (!retired || mirror_rot!==2 || mirror_reflect!==1) $fatal(1,"mirror first");
        issue(3'd6,0,0,3'd1,0,0);
        if (!retired || mirror_rot!==3 || mirror_reflect!==1) $fatal(1,"mirror second");

        // M36 is a blocking typed transaction.
        issue(3'd7,0,0,0,0,6'd17);
        if (!magic_req || ready || retired || magic_ray!==17 || magic_grade!==1) $fatal(1,"magic request");
        @(negedge clk); magic_ack=0; valid=0;
        @(posedge clk); #1;
        if (!magic_req || ready || retired) $fatal(1,"magic must wait");
        @(negedge clk); magic_ack=1;
        @(posedge clk); #1; magic_ack=0;
        if (magic_req || !ready || !retired || magic_consumed!==1) $fatal(1,"magic ack");

        // Canonical BT822 M36 grade ROM boundaries: shallow, deep, mid.
        reset_isa(); issue(3'd7,0,0,0,0,6'd0);
        if (magic_grade!==2) $fatal(1,"shallow grade");
        @(negedge clk); magic_ack=1; @(posedge clk); #1; magic_ack=0;
        issue(3'd7,0,0,0,0,6'd20);
        if (magic_grade!==0) $fatal(1,"deep grade");
        @(negedge clk); magic_ack=1; @(posedge clk); #1; magic_ack=0;
        issue(3'd7,0,0,0,0,6'd24);
        if (magic_grade!==1) $fatal(1,"mid grade");
        @(negedge clk); magic_ack=1; @(posedge clk); #1; magic_ack=0;

        // Invalid resource identifiers and mirror rotations fail closed.
        reset_isa();
        issue(3'd7,0,0,0,0,6'd36);
        if (!fault || !retired || magic_req) $fatal(1,"invalid magic");
        reset_isa();
        issue(3'd6,0,0,3'd6,0,0);
        if (!fault || !retired) $fatal(1,"invalid mirror");

        $display("PASS: basis 18, frame 3888, D12 144, sequential ISA contract");
        $finish;
    end
endmodule
