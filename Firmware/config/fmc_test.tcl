#
# Vivado (TM) v2015.4.2 (64-bit)
#
# fmc_test.tcl: Tcl script for re-creating project 'test_fmc'
#
# Generated by Vivado on Tue Oct 16 14:12:51 CST 2018
# IP Build 1491208 on Wed Feb 24 03:25:39 MST 2016
#
# This file contains the Vivado Tcl commands for re-creating the project to the state*
# when this script was generated. In order to re-create the project, please source this
# file in the Vivado Tcl Shell.
#
# * Note that the runs in the created project will be configured the same way as the
#   original project, however they will not be launched automatically. To regenerate the
#   run results please launch the synthesis/implementation runs as needed.
#
#*****************************************************************************************
# NOTE: In order to use this script for source control purposes, please make sure that the
#       following files are added to the source control system:-
#
# 1. This project restoration tcl script (fmc_test.tcl) that was generated.
#
# 2. The following source(s) files that were local or imported into the original project.
#    (Please see the '$orig_proj_dir' and '$origin_dir' variable setting below at the start of the script)
#
#    <none>
#
# 3. The following remote source files that were added to the original project:-
#
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/common/tri_mode_ethernet_mac_0_sync_block.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/common/tri_mode_ethernet_mac_0_reset_sync.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_bram_tdp.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_tx_client_fifo.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support_resets.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support_clocking.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_rx_client_fifo.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/com5402pkg.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/bram_dp.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/whois2.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/udp_rx.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/udp2serial.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_ten_100_1g_eth_fifo.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/timer_4us.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/tcp_txbuf.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/tcp_tx.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/tcp_server.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/tcp_rxbufndemux2.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/serial2udp_tx.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/ping.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/packet_parsing.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/arp_cache2.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/arp.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/global_resetter.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/axi_lite_sm/tri_mode_ethernet_mac_0_axi_lite_sm.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/gig_eth_mac_resets.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/gig_eth_mac_fifo_block.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/tcp_server/com5402.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/utility_pkg.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/global_clock_reset.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/edge_sync.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/control_interface.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/gig_eth/KC705/gig_eth.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/src/top_KC705_fmc.vhd"
#    "/data/repos/Mic4Test_KC705/Firmware/ipcore_dir/KC705/tri_mode_ethernet_mac_0/tri_mode_ethernet_mac_0.xci"
#    "/data/repos/Mic4Test_KC705/Firmware/ipcore_dir/KC705/fifo32to8/fifo32to8.xci"
#    "/data/repos/Mic4Test_KC705/Firmware/ipcore_dir/KC705/fifo8to32/fifo8to32.xci"
#    "/data/repos/Mic4Test_KC705/Firmware/ipcore_dir/KC705/clockwiz/clockwiz.xci"
#    "/data/repos/Mic4Test_KC705/Firmware/ipcore_dir/KC705/fifo36x512/fifo36x512.xci"
#    "/data/repos/Mic4Test_KC705/Firmware/src/top_KC705.xdc"
#    "/data/repos/Mic4Test_KC705/Firmware/src/FMC_KC705.xdc"
#
#*****************************************************************************************

# Set the reference directory for source file relative paths (by default the value is script directory path)
set origin_dir "."

# Use origin directory path location variable, if specified in the tcl shell
if { [info exists ::origin_dir_loc] } {
  set origin_dir $::origin_dir_loc
}

variable script_file
set script_file "fmc_test.tcl"

# Help information for this script
proc help {} {
  variable script_file
  puts "\nDescription:"
  puts "Recreate a Vivado project from this script. The created project will be"
  puts "functionally equivalent to the original project for which this script was"
  puts "generated. The script contains commands for creating a project, filesets,"
  puts "runs, adding/importing sources and setting properties on various objects.\n"
  puts "Syntax:"
  puts "$script_file"
  puts "$script_file -tclargs \[--origin_dir <path>\]"
  puts "$script_file -tclargs \[--help\]\n"
  puts "Usage:"
  puts "Name                   Description"
  puts "-------------------------------------------------------------------------"
  puts "\[--origin_dir <path>\]  Determine source file paths wrt this path. Default"
  puts "                       origin_dir path value is \".\", otherwise, the value"
  puts "                       that was set with the \"-paths_relative_to\" switch"
  puts "                       when this script was generated.\n"
  puts "\[--help\]               Print help information for this script"
  puts "-------------------------------------------------------------------------\n"
  exit 0
}

if { $::argc > 0 } {
  for {set i 0} {$i < [llength $::argc]} {incr i} {
    set option [string trim [lindex $::argv $i]]
    switch -regexp -- $option {
      "--origin_dir" { incr i; set origin_dir [lindex $::argv $i] }
      "--help"       { help }
      default {
        if { [regexp {^-} $option] } {
          puts "ERROR: Unknown option '$option' specified, please type '$script_file -tclargs --help' for usage info.\n"
          return 1
        }
      }
    }
  }
}

# Set the directory path for the original project from where this script was exported
set orig_proj_dir "[file normalize "$origin_dir/../test_fmc"]"

# Create project
create_project test_fmc ./test_fmc

# Set the directory path for the new project
set proj_dir [get_property directory [current_project]]

# Set project properties
set obj [get_projects test_fmc]
set_property "board_part" "xilinx.com:kc705:part0:1.2" $obj
set_property "default_lib" "xil_defaultlib" $obj
set_property "sim.ip.auto_export_scripts" "1" $obj
set_property "simulator_language" "Mixed" $obj

# Create 'sources_1' fileset (if not found)
if {[string equal [get_filesets -quiet sources_1] ""]} {
  create_fileset -srcset sources_1
}

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
set files [list \
 "[file normalize "$origin_dir/../src/gig_eth/KC705/common/tri_mode_ethernet_mac_0_sync_block.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/common/tri_mode_ethernet_mac_0_reset_sync.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_bram_tdp.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_tx_client_fifo.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support_resets.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support_clocking.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_rx_client_fifo.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/com5402pkg.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/bram_dp.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/whois2.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/udp_rx.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/udp2serial.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_ten_100_1g_eth_fifo.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/timer_4us.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_txbuf.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_tx.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_server.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_rxbufndemux2.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/serial2udp_tx.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/ping.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/packet_parsing.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/arp_cache2.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/arp.vhd"]"\
 "[file normalize "$origin_dir/../src/global_resetter.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/axi_lite_sm/tri_mode_ethernet_mac_0_axi_lite_sm.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/gig_eth_mac_resets.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/gig_eth_mac_fifo_block.vhd"]"\
 "[file normalize "$origin_dir/../../../local_resource/COM5402TCPServer/com5402.vhd"]"\
 "[file normalize "$origin_dir/../src/utility_pkg.vhd"]"\
 "[file normalize "$origin_dir/../src/global_clock_reset.vhd"]"\
 "[file normalize "$origin_dir/../src/edge_sync.vhd"]"\
 "[file normalize "$origin_dir/../src/control_interface.vhd"]"\
 "[file normalize "$origin_dir/../src/gig_eth/KC705/gig_eth.vhd"]"\
 "[file normalize "$origin_dir/../src/top_KC705_fmc.vhd"]"\
]
add_files -norecurse -fileset $obj $files

# Set 'sources_1' fileset file properties for remote files
set file "$origin_dir/../src/gig_eth/KC705/common/tri_mode_ethernet_mac_0_sync_block.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/common/tri_mode_ethernet_mac_0_reset_sync.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_bram_tdp.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_tx_client_fifo.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support_resets.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support_clocking.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_rx_client_fifo.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/com5402pkg.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/bram_dp.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/whois2.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/udp_rx.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/udp2serial.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/fifo/tri_mode_ethernet_mac_0_ten_100_1g_eth_fifo.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/support/tri_mode_ethernet_mac_0_support.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/timer_4us.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_txbuf.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_tx.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_server.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/tcp_rxbufndemux2.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/serial2udp_tx.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/ping.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/packet_parsing.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/arp_cache2.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/arp.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/global_resetter.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/axi_lite_sm/tri_mode_ethernet_mac_0_axi_lite_sm.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/gig_eth_mac_resets.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/gig_eth_mac_fifo_block.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../../../local_resource/COM5402TCPServer/com5402.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/utility_pkg.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/global_clock_reset.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/edge_sync.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/control_interface.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/gig_eth/KC705/gig_eth.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj

set file "$origin_dir/../src/top_KC705_fmc.vhd"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets sources_1] [list "*$file"]]
set_property "file_type" "VHDL" $file_obj


# Set 'sources_1' fileset file properties for local files
# None

# Set 'sources_1' fileset properties
set obj [get_filesets sources_1]
set_property "top" "top_test" $obj

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
set files [list \
 "[file normalize "$origin_dir/../ipcore_dir/KC705/tri_mode_ethernet_mac_0/tri_mode_ethernet_mac_0.xci"]"\
]
add_files -norecurse -fileset $obj $files

# Set 'sources_1' fileset file properties for remote files
# None

# Set 'sources_1' fileset file properties for local files
# None

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
set files [list \
 "[file normalize "$origin_dir/../ipcore_dir/KC705/fifo32to8/fifo32to8.xci"]"\
]
add_files -norecurse -fileset $obj $files

# Set 'sources_1' fileset file properties for remote files
# None

# Set 'sources_1' fileset file properties for local files
# None

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
set files [list \
 "[file normalize "$origin_dir/../ipcore_dir/KC705/fifo8to32/fifo8to32.xci"]"\
]
add_files -norecurse -fileset $obj $files

# Set 'sources_1' fileset file properties for remote files
# None

# Set 'sources_1' fileset file properties for local files
# None

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
set files [list \
 "[file normalize "$origin_dir/../ipcore_dir/KC705/clockwiz/clockwiz.xci"]"\
]
add_files -norecurse -fileset $obj $files

# Set 'sources_1' fileset file properties for remote files
# None

# Set 'sources_1' fileset file properties for local files
# None

# Set 'sources_1' fileset object
set obj [get_filesets sources_1]
set files [list \
 "[file normalize "$origin_dir/../ipcore_dir/KC705/fifo36x512/fifo36x512.xci"]"\
]
add_files -norecurse -fileset $obj $files

# Set 'sources_1' fileset file properties for remote files
# None

# Set 'sources_1' fileset file properties for local files
# None

# Create 'constrs_1' fileset (if not found)
if {[string equal [get_filesets -quiet constrs_1] ""]} {
  create_fileset -constrset constrs_1
}

# Set 'constrs_1' fileset object
set obj [get_filesets constrs_1]

# Add/Import constrs file and set constrs file properties
set file "[file normalize "$origin_dir/../src/top_KC705.xdc"]"
set file_added [add_files -norecurse -fileset $obj $file]
set file "$origin_dir/../src/top_KC705.xdc"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets constrs_1] [list "*$file"]]
set_property "file_type" "XDC" $file_obj

# Add/Import constrs file and set constrs file properties
set file "[file normalize "$origin_dir/../src/FMC_KC705.xdc"]"
set file_added [add_files -norecurse -fileset $obj $file]
set file "$origin_dir/../src/FMC_KC705.xdc"
set file [file normalize $file]
set file_obj [get_files -of_objects [get_filesets constrs_1] [list "*$file"]]
set_property "file_type" "XDC" $file_obj

# Set 'constrs_1' fileset properties
set obj [get_filesets constrs_1]

# Create 'sim_1' fileset (if not found)
if {[string equal [get_filesets -quiet sim_1] ""]} {
  create_fileset -simset sim_1
}

# Set 'sim_1' fileset object
set obj [get_filesets sim_1]
# Empty (no sources present)

# Set 'sim_1' fileset properties
set obj [get_filesets sim_1]
set_property "top" "top_test" $obj
set_property "xelab.nosort" "1" $obj
set_property "xelab.unifast" "" $obj

# Create 'synth_1' run (if not found)
if {[string equal [get_runs -quiet synth_1] ""]} {
  create_run -name synth_1 -part xc7k325tffg900-2 -flow {Vivado Synthesis 2015} -strategy "Vivado Synthesis Defaults" -constrset constrs_1
} else {
  set_property strategy "Vivado Synthesis Defaults" [get_runs synth_1]
  set_property flow "Vivado Synthesis 2015" [get_runs synth_1]
}
set obj [get_runs synth_1]

# set the current synth run
current_run -synthesis [get_runs synth_1]

# Create 'impl_1' run (if not found)
if {[string equal [get_runs -quiet impl_1] ""]} {
  create_run -name impl_1 -part xc7k325tffg900-2 -flow {Vivado Implementation 2015} -strategy "Vivado Implementation Defaults" -constrset constrs_1 -parent_run synth_1
} else {
  set_property strategy "Vivado Implementation Defaults" [get_runs impl_1]
  set_property flow "Vivado Implementation 2015" [get_runs impl_1]
}
set obj [get_runs impl_1]
set_property "steps.write_bitstream.args.readback_file" "0" $obj
set_property "steps.write_bitstream.args.verbose" "0" $obj

# set the current impl run
current_run -implementation [get_runs impl_1]

puts "INFO: Project created:test_fmc"