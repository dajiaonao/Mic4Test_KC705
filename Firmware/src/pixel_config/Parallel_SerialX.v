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

module Parallel_SerialX #( parameter NDATA=100, //% 2**NDATA number of data to be saved
                          parameter FIFO_WIDTH=36, //% Width of fifo that data_out sent to
                          parameter NUM_WIDTH=2,
			  parameter FRAME_WIDTH=48
  )(
  input clk,
  input rst, //% system reset
  input start, // to trigger the data dumpt
  input [7:0]fd_in,
  input trigger, //! trigger mode: 1
  input fifo_full, //% feed back from fifo
  output reg fifo_wr_en, //% to trigger the fifo writing
  output reg [FIFO_WIDTH-1:0] data_out //% data pass to fifo
  );
reg valid;
reg [NUM_WIDTH-1:0] counter0; /// for number of words
reg [9:0] counter1; /// for number of data
reg [5:0] counter2; /// number of words in a frame: 8+23*16+8=48*8=12*32, reserve 64 words
reg [5:0] counter3;
reg [5:0] nData;

parameter COUNTER0_FULL = 2'b11;
parameter FRAME_HEADER = 8'b10111100;

reg has_header;
wire started;
wire in_header;


wire [7:0] t_data;
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

assign started = (has_header==1&&counter1>0&&fifo_full==0);
assign in_header = (fd_in == FRAME_HEADER);
wire moni0;
assign moni0 = (counter3==FRAME_WIDTH-1);

///% move to next state
always@(negedge clk or posedge rst)
begin
  if(rst) current_state<=s0;
  else    current_state<=next_state;
end

///% doing the combination
always@(negedge clk)
begin
  /// trigger mode: only save 1 frame
  if(trigger==1) begin
    counter1 = 1;
    counter2 = 0;
  end

  /// auto mode, save 20 frames
  if(start==1)begin
    counter1 = NDATA;
    counter2 = 0;
  end

  if(rst) next_state=s0;

  case(current_state)
    s0: begin /// initialize variables
      counter0 <= COUNTER0_FULL;
      counter1 <= 0;
      counter2 <= 0;
      counter3 <= 0;
      data_out_temp <= 0;
      data_out <= 0;
      has_header <= 1'b0;
      fifo_wr_en <= 0;
      next_state <= s1;
    end
    s1: begin/// find header
      fifo_wr_en <= 0; /// needed when the previous state is s3
      data_out <= 0;
      counter0 <= COUNTER0_FULL;

      if(has_header == 1'b0) begin /// find header
        if(in_header==1'b1) begin
          has_header = 1'b1;
          counter3 = 0;
        end
      end
      else begin /// track header
        counter3 = counter3+1;
        if (counter3==FRAME_WIDTH) begin
          has_header = in_header;
          counter3 = 0;
        end
      end

      /// decide the next state
      if(started == 1'b1 && in_header == 1'b1) begin
        next_state=s2;
        data_out_temp = (fd_in<<(counter0*8));
        counter0 = counter0-1;
      end
    end
    s2: begin //% pass data
      /// check counter
      data_out_temp = (data_out_temp | fd_in<<(counter0*8));
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
        counter1 = counter1 -1;
        counter2 = 0;
      end

      /// decide the next state
      if(started == 1'b0) next_state=s1;

    end
    default: begin //% do nothing
      next_state=s0;
    end
  endcase
end

endmodule
