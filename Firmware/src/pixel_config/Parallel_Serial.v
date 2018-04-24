//% @file Parallel_Serial.v
//% @brief Module used to resample the parallel digital output to serial ones.
//% @author Dongliang Zhang <dzhang@mail.ccnu.edu.cn>
//%
//% This module contains 8 data input. Will convert it into 36 bit and save
//into fifo. When the start signal is given, the fifo is cleared. And the
//module will search for header. Once the header is found, the subsequent data
//are saved to fifo.
//
`timescale 1ns / 1ps

module Parallel_Serial #( parameter NDATA=100, //% 2**NDATA number of data to be saved
                          parameter FIFO_WIDTH=36, //% Width of fifo that data_out sent to
                          parameter NUM_WIDTH=2,
			  parameter FRAME_WIDTH=48
  )(
  input clk,
  input rst, //% system reset
  input start, // to trigger the data dumpt
  input fd0,
  input fd1,
  input fd2,
  input fd3,
  input fd4,
  input fd5,
  input fd6,
  input fd7,
  input mode, //! trigger mode: 1
   input fifo_full, //% feed back from fifo
   output reg fifo_wr_en, //% to trigger the fifo writing
   output reg [FIFO_WIDTH-1:0] data_out //% data pass to fifo
  );
reg valid;
reg [NUM_WIDTH-1:0] counter0; /// for number of words
reg [9:0] counter1; /// for number of data
reg [5:0] counter2; /// number of words in a frame: 8+23*16+8=48*8=12*32, reserve 64 words
reg [1:0] counter3;

parameter COUNTER0_FULL = 2'b11;

reg has_header;
reg in_mission;
reg ready;
reg started;
reg done;

wire [7:0] t_data;
wire in_header;
wire header_lost;
reg [3:0] current_state, next_state;
reg [FIFO_WIDTH-1:0] data_out_temp; /// to save the data before it's ready
//% state machine:
//% s0: idle, track the headers, get ready to start
//% s1: start, find the next header
//% s2: doing the work
//% s3: finishing

parameter s0=3'b001;
parameter s1=3'b010;
parameter s2=3'b100;
parameter s3=3'b000;

/// current data at the ports
assign t_data = {fd0,fd1,fd2,fd3,fd4,fd5,fd6,fd7}; //fd0 is the higher bit
assign in_header = (t_data == 8'b10111100); 
assign header_lost = ((in_header==1'b1) && (counter2 != FRAME_WIDTH));

///% move to next state
always@(negedge clk or posedge rst)
begin
if(rst)
 begin
 current_state<=s0;
 end
else
 begin
 current_state<=next_state;
 end
end

// always@(posedge start or negedge clk)
// begin
// //  started <= 1;
//   if(start==1 && started==0) begin
//     started <= 1'b1;
//     counter3 <= 0;
//   end
//   else begin
//     started <= 1'b0;
//     counter3 <= 0;
//   end
// end

///% determine the next state
always@(negedge clk)
begin
 if(rst)
  begin
  next_state=s0;
  end
 else
  begin
   case(current_state)
     s0:next_state=s1;
     s1:next_state=(has_header==1&&in_mission==1&&fifo_full==0)?s2:s1;
     s2:next_state=(has_header==0||in_mission==0||fifo_full==1)?s1:s2;
     s3:next_state=s1;
     default:next_state=s0;
    endcase
  end
end

///% doing the combination
always@(negedge clk)
begin
  if(start==1)begin
    in_mission <= 1'b1;
  end

  case(current_state)
    s0:
      begin /// initialize variables
        counter0 <= COUNTER0_FULL;
        counter1 <= 0;
        counter2 <= 0;
        data_out_temp <= 0;
        has_header <= 1'b0;
        fifo_wr_en <= 0;
	done <= 0;

//       if(in_header) //% K28.5 header
//         begin //% check it
// 	  if(counter2 == FRAME_WIDTH) begin
//               ready <=1'b1;
// 	    end
//           else if(counter2 > FRAME_WIDTH) //% lost track
//             begin
//               counter2 <=1;
// 	      ready <=1'b0;
//             end
// 	end
      end
    s1:
      begin //% find header, get ready
        fifo_wr_en <= 0;

	if(has_header==0) begin
	  ///-- find header
	  has_header <= 1'b1;
	end
      end
    s2:
      begin //% pass data
        /// check counter
        data_out_temp = (data_out_temp | t_data<<(counter0*8));
	fifo_wr_en <= 1'b0;

        if(counter0 == 0) /// ready to send the data
        begin
	      data_out <= (data_out_temp & 36'h0ffffffff);
	      fifo_wr_en <= 1'b1;
	      data_out_temp <= 0;
        end
        counter0 = counter0-1;

	counter2 = counter2+1;
	/// if a frame is done
        if(counter2 == FRAME_WIDTH) begin
	  counter1 = counter1 +1;
	  counter2 = 0;
	end

	/// finished the request
	if(counter1 == NDATA) begin
	  in_mission <= 1'b0;
	  counter1 <= 0;
	end
      end
    s3:
      begin //% do nothing
      end
    default:
      begin //% do nothing
      end
  endcase
end

endmodule
