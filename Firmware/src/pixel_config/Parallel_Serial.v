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

module Parallel_Serial #( parameter NDATA=9, //% 2**NDATA number of data to be saved
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
   input fifo_full, //% feed back from fifo
   output reg fifo_wr_en, //% to trigger the fifo writing
   output reg [FIFO_WIDTH-1:0] data_out //% data pass to fifo
  );
reg valid;
reg [NUM_WIDTH-1:0] counter; /// for number of words
reg [NDATA-1:0] counter1; /// for number of data
reg [4:0] counter2; /// number of words in a frame: 8+23*16+8=48*8, reserve 64 words

reg in_mission;
reg ready;

wire [7:0] t_data;
wire in_header;
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
assign t_data = {fd7,fd6,fd5,fd4,fd3,fd2,fd1,fd0};
assign in_header = (t_data == 8'b10111100) 

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

///% determine the next state
always@(current_state or rst or valid or counter or start or fifo_full)
begin
 if(rst)
  begin
  next_state=s0;
  end
 else
  begin
   case(current_state)
     s0:next_state=(start==1)?s1:s0;
     s1:next_state=(valid==1&&fifo_full==0)?s2:s1;
     s2:next_state=(fifo_full==1)?s3:
                     (counter==0)?s0:s2;
     s3:next_state=(fifo_full==0)?s2:s3;      
     default:next_state=s0;
    endcase
  end
end

always@(negedge clk)
begin
  case(current_state)
    s0:
      begin
      counter = 0;
      valid = 1'b1;

      if(in_header) //% K28.5 header
        begin //% check it
	  if(counter2 == FRAME_WIDTH) begin
              ready <=1'b1;
	    end
          else if(counter2 > FRAME_WIDTH) //% lost track
            begin
              counter2 <=1;
	      ready <=0'b0;
            end
	end
      end
    s1,s2,s3:
      begin
        counter <= counter+1'b1;
        fifo_wr_en <= counter[0];
        //if(counter==3) begin
        //   fifo_wr_en <= 1'b1;
        //end
      end
  endcase
end


endmodule
