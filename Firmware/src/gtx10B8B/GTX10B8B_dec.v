`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:06:32 01/29/2015 
// Design Name: 
// Module Name:    top 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module GTX10B8B_dec(
  input wire RESET,
  input wire Q2_CLK1_GTREFCLK_PAD_N_IN,
  input wire Q2_CLK1_GTREFCLK_PAD_P_IN,
  input wire SYSCLK_IN,

  ////////////////////////////////////////////
  input  wire RXN_IN,
  input  wire RXP_IN,
  output wire TXN_OUT,
  output wire TXP_OUT,
  output reg [7:0] D_DATAOUT1,
  output wire rxcommadet,
  output wire rxisaligned,
  output wire track_out
  ////////////////////////////////////////////
);
	 
wire  [15:0]  gt0_rxdata_i;
wire          gt0_rxusrclk2_i;

wire CLK_100_RX;
CLK MY_CLK1 (
    .CLK_IN1(gt0_rxusrclk2_i), 
    .CLK_OUT1(CLK_100_RX)
    );

gtwizard_v2_5_TEST gtx_test1(
    .Q0_CLK1_GTREFCLK_PAD_N_IN(Q2_CLK1_GTREFCLK_PAD_N_IN),
    .Q0_CLK1_GTREFCLK_PAD_P_IN(Q2_CLK1_GTREFCLK_PAD_P_IN),
    .DRPCLK_IN(SYSCLK_IN),
    .TRACK_DATA_OUT(track_out),
    .RXN_IN(RXN_IN),
    .RXP_IN(RXP_IN),
    .TXN_OUT(TXN_OUT),
    .TXP_OUT(TXP_OUT),
    .rxusrclk2(gt0_rxusrclk2_i),
    .rxdata(gt0_rxdata_i),
    .rxbyteisaligned(rxdata),
    .rxcommadet(rxcommadet)
);

/// split the output data
reg flag1;	 
always @ (posedge RESET or posedge CLK_100_RX)
begin
	if (RESET)
	begin
	flag1<=1'b0;
	end
	else
	begin
	flag1<=~flag1;
	end
end
	 
reg [9:0] D_DATAIN;
always @ (posedge CLK_100_RX)
begin
	if (!flag1)
	begin
	D_DATAOUT1<=gt0_rxdata_i[15:8];
	end
	else
	begin
	D_DATAOUT1<=gt0_rxdata_i[7:0];
	end
end

endmodule
