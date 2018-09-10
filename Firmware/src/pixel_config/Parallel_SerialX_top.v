//% used to glue the Parallel_Serial module to the FIFO
`timescale 1ns / 1ps

module Parallel_SerialX_top #( parameter NDATA=1, //% 2**NDATA number of data to be saved
                          parameter FIFO_WIDTH=36, //% Width of fifo that data_out sent to
                          parameter NUM_WIDTH=2,
			  parameter FRAME_WIDTH=48
  )(
  input clk_in,
  input clk_control,
  input rst, //% system reset
  input start_pulse, // to trigger the data dumpt
  input [7:0] fd_in,
  input trigger, //! trigger
  input evt_trig,
  input fifo_rd_en, //% control_interface FIFO full signal.
  output fifo_empty, //% FIFO empty signal sent to control_interface.
  output [FIFO_WIDTH-1:0] fifo_q //% data send to internal FIFO of control interface.
  );

wire clk_sub;
wire start;
wire reset_fifo;
wire fifo_full;
wire fifo_wr_en;
wire [FIFO_WIDTH-1:0] data_to_fifo;

assign reset_fifo = rst | start; 

div_5 div_5_instx01(
     .clkin(clk_in),
     .rst(rst),
     .clkout(clk_sub));

pulse_synchronise pulse_synchronise_10(
      .pulse_in (start_pulse),
      .clk_in   (clk_control),
      .clk_out  (clk_sub),
      .rst      (rst),
      .pulse_out(start)
    );

Parallel_SerialX #(.NDATA(NDATA), .FIFO_WIDTH(FIFO_WIDTH), .NUM_WIDTH(NUM_WIDTH), .FRAME_WIDTH(FRAME_WIDTH))
  PS_inst0(
   .clk(clk_sub),
   .start(start),
   .rst(rst),
   .fd_in(fd_in),
   .trigger(trigger),
   .evt_trig(evt_trig),
   .fifo_full(fifo_full), //% feed back from fifo
   .fifo_wr_en(fifo_wr_en), //% to trigger the fifo writing
   .data_out(data_to_fifo) //% data pass to fifo
);

fifo36x512 fifo_sr_inst1(
        .rst(reset_fifo),
        .wr_clk(clk_sub),
        .rd_clk(clk_control),
        .din(data_to_fifo),
        .wr_en(fifo_wr_en),
        .rd_en(fifo_rd_en),
        .dout(fifo_q),
        .full(fifo_full),
        .empty(fifo_empty)
        );   

endmodule
