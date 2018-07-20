`timescale 1ns / 1ps

module delayed_rise_tb();
reg clkin;
reg reset;
reg trig;
wire out;

initial begin
  clkin = 0;
  reset = 0;
  trig = 0;
  
  #6 trig = 1;
  #140 reset = 1;
  #30 reset = 0;
  #505 trig = 0;

  #10 trig = 1;
  #20 trig = 0;
  #20 trig = 1;
  #20 trig = 0;
end

always begin
      #5 clkin = ~clkin;
end 

delayed_rise test1(
.clk(clkin),
.rst(reset),
.trigger(trig),
.out(out)
);

endmodule
