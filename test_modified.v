module top( clkx, enx, rstx, dx, qx2 );

input clkx, enx, dx, rstx;
output qx2;

  DFFRX2 dff( .D( dx ), .Q( qx_i ), .CK( clkx ), .RN( rstx ));
  NAND2X4 u1 ( .AN ( qx_i ) , .B ( enx ) , .Y ( qx2 ) ) ;
endmodule

