`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    14:07:50 01/25/2015 
// Design Name: 
// Module Name:    ENC8B10B 
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
module ENC8B10B(
input wire RESET,
input wire CLK,
input wire KI,
input wire [7:0] DATAIN,
output reg [9:0] DATAOUT
    );
	 
wire    JO;
wire    HO;
wire    GO;
wire    FO; 
wire    IO;
wire    EO; 
wire    DO; 
wire    CO; 
wire    BO; 
wire    AO;

enc_8b10b my_enc_8b10b (
    .RESET(RESET), 
    .SBYTECLK(CLK), 
    .KI(KI), 
    .AI(DATAIN[0]), 
    .BI(DATAIN[1]), 
    .CI(DATAIN[2]), 
    .DI(DATAIN[3]), 
    .EI(DATAIN[4]), 
    .FI(DATAIN[5]), 
    .GI(DATAIN[6]), 
    .HI(DATAIN[7]), 
    .JO(JO), 
    .HO(HO), 
    .GO(GO), 
    .FO(FO), 
    .IO(IO), 
    .EO(EO), 
    .DO(DO), 
    .CO(CO), 
    .BO(BO), 
    .AO(AO)
    );
	 
always @ (posedge RESET or posedge CLK)
begin
	if(RESET)
	begin
	DATAOUT<=8'b00000000;
	end
	else
	begin
	DATAOUT[0] <= AO;
	DATAOUT[1] <= BO;
	DATAOUT[2] <= CO;
	DATAOUT[3] <= DO;
	DATAOUT[4] <= EO;
	DATAOUT[5] <= IO;
	DATAOUT[6] <= FO;
	DATAOUT[7] <= GO;
	DATAOUT[8] <= HO;
	DATAOUT[9] <= JO;
	end
end

endmodule
