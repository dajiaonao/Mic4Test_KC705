//%
//% Taken from https://blog.csdn.net/limanjihe/article/details/52383101
module div_5 (
	input clkin,
	input rst,
	output clkout);

reg [2:0] step1, step2;

always @(posedge clkin or posedge rst) begin
  if(rst) begin
    step1<=3'b000;
  end
  else begin
    case (step1)
      3'b000: step1<=3'b001;
      3'b001: step1<=3'b011;
      3'b011: step1<=3'b100;
      3'b100: step1<=3'b010;
      3'b010: step1<=3'b000;
      default:step1<=3'b000;
    endcase
  end
end

always @(negedge clkin or posedge rst) begin
  if(rst) begin
    step2<=3'b000;
  end
  else begin
    case (step2)
      3'b000: step2<=3'b001;
      3'b001: step2<=3'b011;
      3'b011: step2<=3'b100;
      3'b100: step2<=3'b010;
      3'b010: step2<=3'b000;
      default:step2<=3'b000;
    endcase
  end
end

assign clkout=step1[0]|step2[0];

endmodule
