//% @file delayed_rise.v
//% @brief A module to control strobe_b signal.
//% @author Dongliang Zhang
//%
//% This module monitors the tigger signal, on the rise edge of which, it send a pulse after a delay of DELAY_COUNT clock cycles.
//% The tigger signal is supposed to be the valid_out signal. And it could be A-pulse, but the delay will need to be tuned.
 
`timescale 1ns / 1ps

module delayed_rise#(parameter DELAY_COUNT=14)(
  input clk,
  input rst,
  input trigger,
  output out1 );

reg[7:0] counter1=0;
reg prev1;

assign out1 = (counter1==DELAY_COUNT)?1:0;

always @(posedge clk) begin
   if(rst==1'b1) begin
     counter1 <= 0;
     prev1 <= 0;
   end   
   else begin
     prev1 <= trigger;

     //// start counting at the posedge
     if(prev1 == 1'b0 && trigger == 1'b1) begin
       counter1 <= 1;
     end
     else begin
       if(counter1 > 0 && counter1<DELAY_COUNT) begin
         counter1 <= counter1 + 1;
       end

       //// keep the count until tigger goes down
       if(counter1 == DELAY_COUNT) begin
         if(trigger == 1'b0) counter1 <= 0;
       end
     end 
   end
end

endmodule