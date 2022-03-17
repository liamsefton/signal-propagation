module top(N_0_1, N_0_5);

input N_0_1;
output N_0_5;

wire N_1_1;
wire N_2_1;

//wire N_0_2:
wire N_1_2;
wire N_2_2;

//wire N_0_3:
wire N_1_3;
wire N_2_3;

//wire N_0_4:
wire N_1_4;
wire N_2_4;



XOR1 XOR_1 ( .A(N_0_1), .B(N_2_1), .Y(N_1_1) );
XOR1 XOR_2 ( .A(N_0_2), .B(N_2_2), .Y(N_1_2) );
XOR1 XOR_3 ( .A(N_0_3), .B(N_2_3), .Y(N_1_3) );
XOR1 XOR_4 ( .A(N_0_4), .B(N_2_4), .Y(N_1_4) );

AND AND_1 ( .A(N_0_1), .B(N_2_1), .Y(N_0_2) );
AND AND_2 ( .A(N_0_2), .B(N_2_2), .Y(N_0_3) );
AND AND_3 ( .A(N_0_3), .B(N_2_3), .Y(N_0_4) );
AND AND_4 ( .A(N_0_4), .B(N_2_4), .Y(N_0_5) );

dff dff_1 ( .d(N_1_1), .q(N_2_1) );
dff dff_2 ( .d(N_1_2), .q(N_2_2) );
dff dff_3 ( .d(N_1_3), .q(N_2_3) );
dff dff_4 ( .d(N_1_4), .q(N_2_4) );

endmodule
