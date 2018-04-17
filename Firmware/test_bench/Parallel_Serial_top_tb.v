`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/17/2018 06:04:48 PM
// Design Name: 
// Module Name: Top_SR_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module Parallel_Serial_top_tb();

parameter FIFO_WIDTH=36;
reg clk;
reg clk2;
reg start;
reg rst;
reg fd0, fd1, fd2, fd3, fd4, fd5, fd6, fd7;
reg mode;
reg fifo_rd_en;
wire fifo_empty;
wire [FIFO_WIDTH-1:0] data_out;
wire startX;
wire clk_subX;

initial begin
     clk = 1'b1;
     clk2 = 1'b1;
     start = 1'b0;
     rst = 1'b0;
     fd0 = 1'b1;
     fd1 = 1'b1;
     fd2 = 1'b1;
     fd3 = 1'b1;
     fd4 = 1'b1;
     fd5 = 1'b1;
     fd6 = 1'b0;
     fd7 = 1'b1;
     mode = 1'b1;
     fifo_rd_en<=1'b0;
     #1 rst=1'b1;
     #13 rst=1'b0;
     #12 start=1'b1;
     #20 start=1'b0;
     #128 fd3 = 1'b0;
     #1000 fifo_rd_en<=1'b1;
     
 //    #500 $finish;
 end
 
 initial begin
      forever #6 clk2 = ~clk2; 
      end
        
     always begin
     #1 clk = ~clk;
     end
     

  //   always begin
  //   #1 clk2 = ~clk2;
 //    clk2 = ~clk2;
  //   end
     
Parallel_Serial_top #(.NDATA(10)) tA1(
   .clk_in(clk),
   .clk_control(clk2),
   .start_pulse(start),
   .rst(rst),
   .fd0(fd0),
   .fd1(fd1),
   .fd2(fd2),
   .fd3(fd3),
   .fd4(fd4),
   .fd5(fd5),
   .fd6(fd6),
   .fd7(fd7),
   .mode(mode),
   .fifo_empty(fifo_empty), //% feed back from fifo
   .fifo_rd_en(fifo_rd_en), //% to trigger the fifo writing
   .fifo_q(data_out) //% data pass to fifo
);

assign startX = tA1.start;
assign clk_subX = tA1.clk_sub;

endmodule
