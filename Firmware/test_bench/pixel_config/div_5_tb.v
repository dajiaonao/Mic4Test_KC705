

`timescale 1ns/1ns
module div_5_tb  ;
 
 reg   clkin   ;
 wire   clkout   ;
  wire step1,step2;
  div_5 
   DUT(
      .clkin (clkin ) ,
     .clkout (clkout ) );
     initial
     begin
         clkin=0;
         forever #5 clkin=~clkin;
          
     end
assign step1=DUT.step1[0];//
assign step2=DUT.step2[0];//
endmodule
