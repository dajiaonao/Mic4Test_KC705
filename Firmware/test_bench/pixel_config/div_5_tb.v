

`timescale 1ns/1ns
module div_5_tb  ;
 
 reg   clkin   ;
 reg  reset;
 wire   clkout   ;
  wire step1,step2;
  div_5 
   DUT(
      .clkin (clkin ) ,
      .rst(reset),
     .clkout (clkout ) );
     initial
     begin
         clkin=0;
         reset = 0;
         #198 reset=1;
         #1 reset=0; 
         #500 $finish;
     end
     
     always begin
       #1 clkin=~clkin;
     end
              
assign step1=DUT.step1[0];//
assign step2=DUT.step2[0];//
endmodule
