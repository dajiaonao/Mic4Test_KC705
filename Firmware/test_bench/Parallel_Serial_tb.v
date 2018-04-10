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

module Parallel_Serial_tb();

parameter FIFO_WIDTH=36;
reg clk;
reg start;
reg rst;
reg fd0, fd1, fd2, fd3, fd4, fd5, fd6, fd7;
reg mode;
reg fifo_full;
wire fifo_wr_en;
wire [FIFO_WIDTH-1:0] data_out;

initial begin
     clk = 1'b1;
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
     fifo_full = 1'b0;
     
     #10 start=1'b1;
     #3 start=1'b0;
     #28 fd3 = 1'b0;
     #100 $finish;
 end
     always begin
     #1 clk = ~clk;
     end
     
Parallel_Serial #(.NDATA(10)) tA1(
   .clk(clk),
   .start(start),
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
   .fifo_full(fifo_full), //% feed back from fifo
   .fifo_wr_en(fifo_wr_en), //% to trigger the fifo writing
   .data_out(data_out) //% data pass to fifo
);

endmodule

