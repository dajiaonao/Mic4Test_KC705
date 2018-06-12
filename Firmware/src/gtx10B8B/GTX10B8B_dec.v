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
  output wire [7:0] D_DATAOUT1
  ////////////////////////////////////////////
);
	 
reg   [19:0]  gt0_txdata_i;
wire  [19:0]  gt0_rxdata_i;
wire          gt0_txusrclk2_i;
wire          gt0_rxusrclk2_i;
wire          gt0_rxcommadet_i;
wire          gt0_rxbyteisaligned_i;
wire          gt0_rxbyterealign_i;

wire CLK_100_TX;

CLK MY_CLK (
    .CLK_IN1(gt0_txusrclk2_i), 
    .CLK_OUT1(CLK_100_TX)
    );
	 
wire CLK_100_RX;

CLK MY_CLK1 (
    .CLK_IN1(gt0_rxusrclk2_i), 
    .CLK_OUT1(CLK_100_RX)
    );
	
reg KI;	
reg [7:0] DATAIN;
wire [9:0] DATAOUT;
	
reg [3:0] kcounter;
reg [7:0] dcounter;
reg KIbuffer;

parameter  K28d0 = 8'b00011100; //Balanced
parameter  K28d1 = 8'b00111100; //Unbalanced comma
parameter  K28d2 = 8'b01011100; //Unbalanced
parameter  K28d3 = 8'b01111100; //Unbalanced
parameter  K28d4 = 8'b10011100; //Balanced
parameter  K28d5 = 8'b10111100; //Unbalanced comma
parameter  K28d6 = 8'b11011100; //Unbalanced
parameter  K28d7 = 8'b11111100; //Balanced comma
parameter  K23d7 = 8'b11110111; //Balanced
parameter  K27d7 = 8'b11111011; //Balanced
parameter  K29d7 = 8'b11111101; //Balanced
parameter  K30d7 = 8'b11111110; //Balanced
	 
always @ (posedge RESET or posedge CLK_100_TX)
begin
	if (RESET)
	begin
		DATAIN <= 8'b0 ;
		KIbuffer <= 1'b1 ; // Set for K initially
		KI <= 1'b0;
		kcounter <= 4'b0 ; // Preset K counter
		dcounter <= 8'b0 ;	// Preset D counter
	end
	else
	begin
	KI <= KIbuffer;
		if (KIbuffer)	// Output K characters
		begin
			kcounter <= kcounter + 1'b1 ;	// Increment counter
			dcounter <= 8'b00000000 ;
			case (kcounter) 
				4'b0000:  DATAIN <= K28d0 ;
				4'b0001:  DATAIN <= K28d1 ;
				4'b0010:  DATAIN <= K28d2 ;
				4'b0011:  DATAIN <= K28d3 ;
				4'b0100:  DATAIN <= K28d4 ;
				4'b0101:  DATAIN <= K28d5 ;
				4'b0110:  DATAIN <= K28d6 ;
				4'b0111:  DATAIN <= K28d7 ;
				4'b1000:  DATAIN <= K23d7 ;
				4'b1001:  DATAIN <= K27d7 ;
				4'b1010:   DATAIN <= K29d7 ;				          
				4'b1011:   begin DATAIN <= K30d7 ;
					         KIbuffer <= 1'b0 ; end	// Switch to D output							 
				4'b1100:  DATAIN <= 8'b00000000 ;
				default:  DATAIN <= K28d5 ; 
			endcase
		end
		else 
		begin
			dcounter <= dcounter + 1'b1 ;	// Output D values
			DATAIN <= dcounter ;
			if (dcounter == 8'b11111111)
			begin
				KIbuffer <= 1'b1 ;	// Repeat K portion
				kcounter <= 4'b0000 ; // Reset K counter
			end
		end 
	end
end 


ENC8B10B MY_ENC8B10B(
    .RESET(RESET), 
    .CLK(CLK_100_TX), 
    .KI(KI), 
    .DATAIN(DATAIN), 
    .DATAOUT(DATAOUT)
    );
	 
reg flag;	 
always @ (posedge RESET or posedge CLK_100_TX)
begin
	if (RESET)
	begin
	flag<=1'b0;
	end
	else
	begin
	flag<=~flag;
	end
end

always @ (posedge CLK_100_TX)
begin
	if (!flag)
	begin
	gt0_txdata_i[9:0]<=DATAOUT;
	end
	else
	begin
	gt0_txdata_i[19:10]<=DATAOUT;
	end
end

wire gt0_txusrclk_i, gt0_rxusrclk_i;
wire gt0_qplloutclt_i, gt0_qplloutrefclk_i;

gtwizard_v2_5 gtx_support_int0(
    .SOFT_RESET_TX_IN(1'b0),
    .SOFT_RESET_RX_IN(1'b0),
    .DONT_RESET_ON_DATA_ERROR_IN(1'b0),
    .GT0_TX_FSM_RESET_DONE_OUT(1'b0),
    .GT0_RX_FSM_RESET_DONE_OUT(1'b0),
    .GT0_DATA_VALID_IN(1'b0),
    .GT0_TXUSRCLK_OUT(gt0_txusrclk_i),
    .GT0_RXUSRCLK_OUT(gt0_rxusrclk_i),
    .GT0_QPLLOUTCLK_OUT(gt0_qplloutclt_i),
    .GT0_QPLLOUTREFCLK_OUT(gt0_qplloutrefclk_i),
    .gt0_drpaddr_in(9'b0),
    .gt0_drpdi_in(16'b0),
    .gt0_drpen_in(1'b0),
    .gt0_drpwe_in(1'b0),
    

    .Q0_CLK1_GTREFCLK_PAD_N_IN(Q2_CLK1_GTREFCLK_PAD_N_IN),
    .Q0_CLK1_GTREFCLK_PAD_P_IN(Q2_CLK1_GTREFCLK_PAD_P_IN),
    .sysclk_in(SYSCLK_IN),
    .gt0_gtxrxn_in(RXN_IN),
    .gt0_gtxrxp_in(RXP_IN), 
    .gt0_gtxtxn_out(TXN_OUT), 
    .gt0_gtxtxp_out(TXP_OUT), 
    .gt0_txdata_in(gt0_txdata_i),//
    .gt0_rxdata_out(gt0_rxdata_i), 
    .GT0_TXUSRCLK2_OUT(gt0_txusrclk2_i), 
    .GT0_RXUSRCLK2_OUT(gt0_rxusrclk2_i),
    .gt0_rxcommadet_out(gt0_rxcommadet_i),
    .gt0_rxbyteisaligned_out(gt0_rxbyteisaligned_i),
    .gt0_rxbyterealign_out(gt0_rxbyterealign_i)
);

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
	D_DATAIN<=gt0_rxdata_i[19:10];
	end
	else
	begin
	D_DATAIN<=gt0_rxdata_i[9:0];
	end
end
	 
wire KO1;
dec_8b10b MY_dec_8b10b1 (
    .RESET(RESET), 
    .RBYTECLK(CLK_100_RX), 
    .AI(D_DATAIN[0]), 
    .BI(D_DATAIN[1]), 
    .CI(D_DATAIN[2]), 
    .DI(D_DATAIN[3]), 
    .EI(D_DATAIN[4]), 
    .II(D_DATAIN[5]), 
    .FI(D_DATAIN[6]), 
    .GI(D_DATAIN[7]), 
    .HI(D_DATAIN[8]), 
    .JI(D_DATAIN[9]), 
    .KO(KO1), 
    .HO(D_DATAOUT1[7]), 
    .GO(D_DATAOUT1[6]), 
    .FO(D_DATAOUT1[5]), 
    .EO(D_DATAOUT1[4]), 
    .DO(D_DATAOUT1[3]), 
    .CO(D_DATAOUT1[2]), 
    .BO(D_DATAOUT1[1]), 
    .AO(D_DATAOUT1[0])
    );
/* 
(* keep = "TRUE" *) wire   [7:0] xilinxDOUT;
(* keep = "TRUE" *) wire	 xilinxKOUT;
(* keep = "TRUE" *) wire	 xilinxCODE_ERR;
(* keep = "TRUE" *) wire	 xilinxDISP_ERR;
(* keep = "TRUE" *) wire	 xilinxRUN_DISP;
(* keep = "TRUE" *) wire   [1:0] xilinxSYM_DISP;

decode_8b10b_top MYdecode_8b10b_top (
    .CLK(CLK_100_RX), 
    .DIN(D_DATAIN), 
    .DOUT(xilinxDOUT), 
    .KOUT(xilinxKOUT), 
    .CE(),	 
    .CE_B(), 
    .CLK_B(), 
    .DIN_B(),	 
    .DISP_IN(), 	 
    .DISP_IN_B(),	 
    .SINIT(), 
    .SINIT_B(), 
    .CODE_ERR(xilinxCODE_ERR), 
    .CODE_ERR_B(), 
    .DISP_ERR(xilinxDISP_ERR), 
    .DISP_ERR_B(), 
    .DOUT_B(), 
    .KOUT_B(), 
    .ND(), 
    .ND_B(), 
    .RUN_DISP(xilinxRUN_DISP), 
    .RUN_DISP_B(), 
    .SYM_DISP(xilinxSYM_DISP), 
    .SYM_DISP_B()
    );
*/	 
endmodule
