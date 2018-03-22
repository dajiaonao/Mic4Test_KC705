`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: ccnu
// Engineer: Poyi Xiong
// 
// Create Date: 01/13/2017 11:27:24 AM
// Design Name: 
// Module Name: SR_Control_tb
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


module SR_Control_tb();
parameter WIDTH=170;
parameter CNT_WIDTH=8;
reg [WIDTH-1:0] din;
reg clk;
reg rst;
reg start;
wire data_out;
wire clk_sr;
wire din_sr;
wire [CNT_WIDTH-1:0] cnt_dly;
wire load_sr;

SR_Control DUT2(
    .din(din),
    .clk(clk),
    .rst(rst),
    .start(start),
    .data_out(data_out),
    .load_sr(load_sr),
    .count_delay(cnt_dly),
    .clk_sr(clk_sr)
    );
/* 
initial begin
$dumpfile("sr_control.dump");
$dumpvars(0,SR_Control);
end
*/
initial begin
clk=0;
forever #50 clk=~clk;
end

initial begin
rst=1;
#200 rst=0;
end

initial begin
din={1'b1,169'b1011};
start=0;
#450 start=1;
#100 start=0;
end

endmodule
