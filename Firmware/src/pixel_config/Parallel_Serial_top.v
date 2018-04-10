//% used to glue the Parallel_Serial module to the FIFO
`timescale 1ns / 1ps

module Parallel_Serial_top #( parameter NDATA=1, //% 2**NDATA number of data to be saved
                          parameter FIFO_WIDTH=36, //% Width of fifo that data_out sent to
                          parameter NUM_WIDTH=2,
			  parameter FRAME_WIDTH=48
  )(
  input clk_in,
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
  input fifo_rd_en, //% control_interface FIFO full signal.
  output fifo_empty, //% FIFO empty signal sent to control_interface.
  output [FIFO_WIDTH-1:0] fifo_q //% data send to internal FIFO of control interface.
  );

wire reset_fifo;
wire fifo_full;
wire fifo_wr_en;
wire [FIFO_WIDTH-1:0] data_to_fifo;

assign reset_fifo = rst | start; 

Parallel_Serial #(.NDATA(NDATA), .FIFO_WIDTH(FIFO_WIDTH), .NUM_WIDTH(NUM_WIDTH), .FRAME_WIDTH(FRAME_WIDTH))
  PS_inst0(
   .clk(clk_in),
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
   .data_out(data_to_fifo) //% data pass to fifo
);

fifo36x512 fifo_sr_inst1(
        .rst(reset_fifo),
        .wr_clk(clk_in),
        .rd_clk(clk_in),
        .din(data_to_fifo),
        .wr_en(fifo_wr_en),
        .rd_en(fifo_rd_en),
        .dout(fifo_q),
        .full(fifo_full),
        .empty(fifo_empty)
        );   

  endmodule
