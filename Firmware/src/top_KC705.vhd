--------------------------------------------------------------------------------
--! @file top.vhd
--! @brief Toplevel module for KC705 eval board.
--! @author Yuan Mei
--!
--! Target Devices: Kintex-7 XC7K325T-FFG900-2
--------------------------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
USE ieee.numeric_std.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
LIBRARY UNISIM;
USE UNISIM.VComponents.ALL;

LIBRARY work;
USE work.utility.ALL;

ENTITY top IS
  GENERIC (
    ENABLE_DEBUG       : boolean := false;
    ENABLE_GIG_ETH     : boolean := true;
    ENABLE_TEN_GIG_ETH : boolean := true
  );
  PORT (
    SYS_RST          : IN    std_logic;
    SYS_CLK_P        : IN    std_logic;
    SYS_CLK_N        : IN    std_logic;
    USER_CLK_P       : IN    std_logic;  --! 156.250 MHz
    USER_CLK_N       : IN    std_logic;
    SGMIICLK_Q0_P    : IN    std_logic;  --! 125 MHz, for GTP/GTH/GTX
    SGMIICLK_Q0_N    : IN    std_logic;
    --
    LED8Bit          : OUT   std_logic_vector(7 DOWNTO 0);
    DIPSw4Bit        : IN    std_logic_vector(3 DOWNTO 0);
    BTN5Bit          : IN    std_logic_vector(4 DOWNTO 0);
    USER_SMA_CLOCK_P : OUT   std_logic;
    USER_SMA_CLOCK_N : OUT   std_logic;
    USER_SMA_GPIO_P  : OUT   std_logic;
    USER_SMA_GPIO_N  : OUT   std_logic;

    -- SMA MGT
    GTREFCLK_N       : IN    std_logic; 
    GTREFCLK_P       : IN    std_logic; 
    SMA_MGT_TX_P     : OUT   std_logic;
    SMA_MGT_TX_N     : OUT   std_logic;
    SMA_MGT_RX_P     : IN    std_logic;
    SMA_MGT_RX_N     : IN    std_logic;

    -- UART via usb
    USB_RX           : OUT   std_logic;
    USB_TX           : IN    std_logic;
    -- SFP
    SFP_TX_P         : OUT   std_logic;
    SFP_TX_N         : OUT   std_logic;
    SFP_RX_P         : IN    std_logic;
    SFP_RX_N         : IN    std_logic;
    SFP_LOS_LS       : IN    std_logic;
    SFP_TX_DISABLE_N : OUT   std_logic;
    -- Gigbit eth interface (RGMII)
    PHY_RESET_N      : OUT   std_logic;
    RGMII_TXD        : OUT   std_logic_vector(3 DOWNTO 0);
    RGMII_TX_CTL     : OUT   std_logic;
    RGMII_TXC        : OUT   std_logic;
    RGMII_RXD        : IN    std_logic_vector(3 DOWNTO 0);
    RGMII_RX_CTL     : IN    std_logic;
    RGMII_RXC        : IN    std_logic;
    MDIO             : INOUT std_logic;
    MDC              : OUT   std_logic;
    -- SDRAM
    DDR3_DQ          : INOUT std_logic_vector(63 DOWNTO 0);
    DDR3_DQS_P       : INOUT std_logic_vector(7 DOWNTO 0);
    DDR3_DQS_N       : INOUT std_logic_vector(7 DOWNTO 0);
    -- Outputs
    DDR3_ADDR        : OUT   std_logic_vector(13 DOWNTO 0);
    DDR3_BA          : OUT   std_logic_vector(2 DOWNTO 0);
    DDR3_RAS_N       : OUT   std_logic;
    DDR3_CAS_N       : OUT   std_logic;
    DDR3_WE_N        : OUT   std_logic;
    DDR3_RESET_N     : OUT   std_logic;
    DDR3_CK_P        : OUT   std_logic_vector(0 DOWNTO 0);
    DDR3_CK_N        : OUT   std_logic_vector(0 DOWNTO 0);
    DDR3_CKE         : OUT   std_logic_vector(0 DOWNTO 0);
    DDR3_CS_N        : OUT   std_logic_vector(0 DOWNTO 0);
    DDR3_DM          : OUT   std_logic_vector(7 DOWNTO 0);
    DDR3_ODT         : OUT   std_logic_vector(0 DOWNTO 0);
    --
    I2C_SCL          : INOUT std_logic;
    I2C_SDA          : INOUT std_logic;
    -- FMC HPC
    FMC_HPC_HA_P     :INOUT    std_logic_vector(23 DOWNTO 0);
    FMC_HPC_HA_N     :INOUT    std_logic_vector(23 DOWNTO 0);
    FMC_HPC_LA_P     :INOUT    std_logic_vector(33 DOWNTO 0);
    FMC_HPC_LA_N     :INOUT    std_logic_vector(33 DOWNTO 0);
    FMC_HPC_CLK1_M2C_P : INOUT std_logic;
    FMC_HPC_CLK1_M2C_N : INOUT std_logic;
    -- FMC LPC
    FMC_LPC_LA_P     :INOUT    std_logic_vector(33 DOWNTO 0);
    FMC_LPC_LA_N     :INOUT    std_logic_vector(33 DOWNTO 0)
  );
END top;

ARCHITECTURE Behavioral OF top IS
  -- Components
  COMPONENT global_clock_reset
    PORT (
      SYS_CLK_P  : IN  std_logic;
      SYS_CLK_N  : IN  std_logic;
      FORCE_RST  : IN  std_logic;
      -- output
      GLOBAL_RST : OUT std_logic;
      SYS_CLK    : OUT std_logic;
      CLK_OUT1   : OUT std_logic;
      CLK_OUT2   : OUT std_logic;
      CLK_OUT3   : OUT std_logic;
      CLK_OUT4   : OUT std_logic
    );
  END COMPONENT;
--  ---------------------------------------------< ten_gig_eth
--  COMPONENT ten_gig_eth
--    PORT (
--      REFCLK_P             : IN  std_logic;  -- 156.25MHz for transceiver
--      REFCLK_N             : IN  std_logic;
--      RESET                : IN  std_logic;
--      SFP_TX_P             : OUT std_logic;
--      SFP_TX_N             : OUT std_logic;
--      SFP_RX_P             : IN  std_logic;
--      SFP_RX_N             : IN  std_logic;
--      SFP_LOS              : IN  std_logic;  -- loss of receiver signal
--      SFP_TX_DISABLE       : OUT std_logic;
--      -- clk156 domain, clock generated by the core
--      CLK156               : OUT std_logic;
--      PCS_PMA_CORE_STATUS  : OUT std_logic_vector(7 DOWNTO 0);
--      TX_STATISTICS_VECTOR : OUT std_logic_vector(25 DOWNTO 0);
--      TX_STATISTICS_VALID  : OUT std_logic;
--      RX_STATISTICS_VECTOR : OUT std_logic_vector(29 DOWNTO 0);
--      RX_STATISTICS_VALID  : OUT std_logic;
--      PAUSE_VAL            : IN  std_logic_vector(15 DOWNTO 0);
--      PAUSE_REQ            : IN  std_logic;
--      TX_IFG_DELAY         : IN  std_logic_vector(7 DOWNTO 0);
--      -- emac control interface
--      S_AXI_ACLK           : IN  std_logic;
--      S_AXI_ARESETN        : IN  std_logic;
--      S_AXI_AWADDR         : IN  std_logic_vector(10 DOWNTO 0);
--      S_AXI_AWVALID        : IN  std_logic;
--      S_AXI_AWREADY        : OUT std_logic;
--      S_AXI_WDATA          : IN  std_logic_vector(31 DOWNTO 0);
--      S_AXI_WVALID         : IN  std_logic;
--      S_AXI_WREADY         : OUT std_logic;
--      S_AXI_BRESP          : OUT std_logic_vector(1 DOWNTO 0);
--      S_AXI_BVALID         : OUT std_logic;
--      S_AXI_BREADY         : IN  std_logic;
--      S_AXI_ARADDR         : IN  std_logic_vector(10 DOWNTO 0);
--      S_AXI_ARVALID        : IN  std_logic;
--      S_AXI_ARREADY        : OUT std_logic;
--      S_AXI_RDATA          : OUT std_logic_vector(31 DOWNTO 0);
--      S_AXI_RRESP          : OUT std_logic_vector(1 DOWNTO 0);
--      S_AXI_RVALID         : OUT std_logic;
--      S_AXI_RREADY         : IN  std_logic;
--      -- tx_wr_clk domain
--      TX_AXIS_FIFO_ARESETN : IN  std_logic;
--      TX_AXIS_FIFO_ACLK    : IN  std_logic;
--      TX_AXIS_FIFO_TDATA   : IN  std_logic_vector(63 DOWNTO 0);
--      TX_AXIS_FIFO_TKEEP   : IN  std_logic_vector(7 DOWNTO 0);
--      TX_AXIS_FIFO_TVALID  : IN  std_logic;
--      TX_AXIS_FIFO_TLAST   : IN  std_logic;
--      TX_AXIS_FIFO_TREADY  : OUT std_logic;
--      -- rx_rd_clk domain
--      RX_AXIS_FIFO_ARESETN : IN  std_logic;
--      RX_AXIS_FIFO_ACLK    : IN  std_logic;
--      RX_AXIS_FIFO_TDATA   : OUT std_logic_vector(63 DOWNTO 0);
--      RX_AXIS_FIFO_TKEEP   : OUT std_logic_vector(7 DOWNTO 0);
--      RX_AXIS_FIFO_TVALID  : OUT std_logic;
--      RX_AXIS_FIFO_TLAST   : OUT std_logic;
--      RX_AXIS_FIFO_TREADY  : IN  std_logic
--    );
--  END COMPONENT;
--  COMPONENT ten_gig_eth_packet_gen
--    PORT (
--      RESET          : IN  std_logic;
--      MEM_CLK        : IN  std_logic;
--      MEM_WE         : IN  std_logic;   -- memory write enable
--      MEM_ADDR       : IN  std_logic_vector(31 DOWNTO 0);
--      MEM_D          : IN  std_logic_vector(31 DOWNTO 0);  -- memory data
--      --
--      TX_AXIS_ACLK   : IN  std_logic;
--      TX_START       : IN  std_logic;
--      TX_BYTES       : IN  std_logic_vector(15 DOWNTO 0);  -- number of bytes to send
--      TX_AXIS_TDATA  : OUT std_logic_vector(63 DOWNTO 0);
--      TX_AXIS_TKEEP  : OUT std_logic_vector(7 DOWNTO 0);
--      TX_AXIS_TVALID : OUT std_logic;
--      TX_AXIS_TLAST  : OUT std_logic;
--      TX_AXIS_TREADY : IN  std_logic
--    );
--  END COMPONENT;
--  COMPONENT ten_gig_eth_rx_parser
--    PORT (
--      RESET                : IN  std_logic;
--      RX_AXIS_FIFO_ARESETN : OUT std_logic;
--      -- Everything internal to this module is synchronous to this clock `ACLK'
--      RX_AXIS_FIFO_ACLK    : IN  std_logic;
--      RX_AXIS_FIFO_TDATA   : IN  std_logic_vector(63 DOWNTO 0);
--      RX_AXIS_FIFO_TKEEP   : IN  std_logic_vector(7 DOWNTO 0);
--      RX_AXIS_FIFO_TVALID  : IN  std_logic;
--      RX_AXIS_FIFO_TLAST   : IN  std_logic;
--      RX_AXIS_FIFO_TREADY  : OUT std_logic;
--      -- Constants
--      SRC_MAC              : IN  std_logic_vector(47 DOWNTO 0);
--      SRC_IP               : IN  std_logic_vector(31 DOWNTO 0);
--      SRC_PORT             : IN  std_logic_vector(15 DOWNTO 0);
--      -- Command output fifo interface AFTER parsing the packet
--      -- dstMAC(48) dstIP(32) dstPort(16) opcode(32)
--      CMD_FIFO_Q           : OUT std_logic_vector(127 DOWNTO 0);
--      CMD_FIFO_EMPTY       : OUT std_logic;
--      CMD_FIFO_RDREQ       : IN  std_logic;
--      CMD_FIFO_RDCLK       : IN  std_logic
--    );
--  END COMPONENT;
--  ---------------------------------------------> ten_gig_eth
  ---------------------------------------------< gig_eth
  COMPONENT gig_eth
    PORT (
      -- asynchronous reset
      GLBL_RST             : IN    std_logic;
      -- clocks
      GTX_CLK              : IN    std_logic;  -- 125MHz
      REF_CLK              : IN    std_logic;  -- 200MHz for IODELAY
      -- PHY interface
      PHY_RESETN           : OUT   std_logic;
      -- RGMII Interface
      RGMII_TXD            : OUT   std_logic_vector(3 DOWNTO 0);
      RGMII_TX_CTL         : OUT   std_logic;
      RGMII_TXC            : OUT   std_logic;
      RGMII_RXD            : IN    std_logic_vector(3 DOWNTO 0);
      RGMII_RX_CTL         : IN    std_logic;
      RGMII_RXC            : IN    std_logic;
      -- MDIO Interface
      MDIO                 : INOUT std_logic;
      MDC                  : OUT   std_logic;
      -- TCP
      MAC_ADDR             : IN    std_logic_vector(47 DOWNTO 0);
      IPv4_ADDR            : IN    std_logic_vector(31 DOWNTO 0);
      IPv6_ADDR            : IN    std_logic_vector(127 DOWNTO 0);
      SUBNET_MASK          : IN    std_logic_vector(31 DOWNTO 0);
      GATEWAY_IP_ADDR      : IN    std_logic_vector(31 DOWNTO 0);
      TCP_CONNECTION_RESET : IN    std_logic;
      TX_TDATA             : IN    std_logic_vector(7 DOWNTO 0);
      TX_TVALID            : IN    std_logic;
      TX_TREADY            : OUT   std_logic;
      RX_TDATA             : OUT   std_logic_vector(7 DOWNTO 0);
      RX_TVALID            : OUT   std_logic;
      RX_TREADY            : IN    std_logic;
      -- FIFO
      TCP_USE_FIFO         : IN    std_logic;
      TX_FIFO_WRCLK        : IN    std_logic;
      TX_FIFO_Q            : IN    std_logic_vector(31 DOWNTO 0);
      TX_FIFO_WREN         : IN    std_logic;
      TX_FIFO_FULL         : OUT   std_logic;
      RX_FIFO_RDCLK        : IN    std_logic;
      RX_FIFO_Q            : OUT   std_logic_vector(31 DOWNTO 0);
      RX_FIFO_RDEN         : IN    std_logic;
      RX_FIFO_EMPTY        : OUT   std_logic
    );
  END COMPONENT;
  ---------------------------------------------> gig_eth
  ---------------------------------------------< TOP_SR
  COMPONENT Top_SR IS
    GENERIC (
      WIDTH           : positive := 200;
      CNT_WIDTH       : positive := 8;
      DIV_WIDTH       : positive := 6;
      COUNT_WIDTH     : positive := 64;
      VALID_WIDTH     : positive := 32;
      NUM_WIDTH       : positive := 4;
      FIFO_WIDTH      : positive := 36;
      SHIFT_DIRECTION : positive := 1;
      READ_TRIG_SRC   : natural  := 0;
      READ_DELAY      : natural  := 1
    );
    PORT (
      clk_in      :IN   std_logic;
      rst         :IN   std_logic;
      start       :IN   std_logic;
--      wr_en       :IN   std_logic;
      din         :IN   std_logic_vector(199 DOWNTO 0);
      data_in     :IN   std_logic;
      div         :IN   std_logic_vector(5 DOWNTO 0);
      fifo_rd_en  :IN   std_logic;
      clk         :OUT  std_logic;
      clk_sr      :OUT  std_logic;
      data_out    :OUT  std_logic;
      load_sr     :OUT  std_logic;
      fifo_empty  :OUT  std_logic;
      fifo_q      :OUT  std_logic_vector(35 DOWNTO 0)
    );
  END COMPONENT;
 
  ---------------------------------------------> TOP_SR
  ---------------------------------------------< PULSE_SYNCHRONISE
  COMPONENT pulse_synchronise
    PORT (
      pulse_in     :IN  std_logic;
      clk_in       :IN  std_logic;
      clk_out      :IN  std_logic;
      rst          :IN  std_logic;
      pulse_out    :OUT std_logic
    );
  END COMPONENT;
  ---------------------------------------------> PULSE_SYNCHRONISE
  ---------------------------------------------< shiftreg driver for DAC8568
  COMPONENT fifo2shiftreg
    GENERIC (
      DATA_WIDTH        : positive  := 32;  -- parallel data width
      CLK_DIV_WIDTH     : positive  := 16;
      DELAY_AFTER_SYNCn : natural   := 0;  -- number of SCLK cycles' wait after falling edge OF SYNCn
      SCLK_IDLE_LEVEL   : std_logic := '0';  -- High or Low for SCLK when not switching
      DOUT_DRIVE_EDGE   : std_logic := '1';  -- 1/0 rising/falling edge of SCLK drives new DOUT bit
      DIN_CAPTURE_EDGE  : std_logic := '0'  -- 1/0 rising/falling edge of SCLK captures new DIN bit
    );
    PORT (
      CLK      : IN  std_logic;         -- clock
      RESET    : IN  std_logic;         -- reset
      -- input data interface
      WR_CLK   : IN  std_logic;         -- FIFO write clock
      DINFIFO  : IN  std_logic_vector(15 DOWNTO 0);
      WR_EN    : IN  std_logic;
      WR_PULSE : IN  std_logic;  -- one pulse writes one word, regardless of pulse duration
      FULL     : OUT std_logic;
      -- captured data
      BUSY     : OUT std_logic;
      DATAOUT  : OUT std_logic_vector(DATA_WIDTH-1 DOWNTO 0);
      -- serial interface
      CLK_DIV  : IN  std_logic_vector(CLK_DIV_WIDTH-1 DOWNTO 0);  -- SCLK freq is CLK / 2**(CLK_DIV)
      SCLK     : OUT std_logic;
      DOUT     : OUT std_logic;
      SYNCn    : OUT std_logic;
      DIN      : IN  std_logic
    );
  END COMPONENT;
  ---------------------------------------------> shiftreg driver for DAC8568
  ---------------------------------------------< UART/RS232
  COMPONENT control_interface
    PORT (
      RESET           : IN  std_logic;
      CLK             : IN  std_logic;    -- system clock
      -- From FPGA to PC
      FIFO_Q          : OUT std_logic_vector(35 DOWNTO 0);  -- interface fifo data output port
      FIFO_EMPTY      : OUT std_logic;    -- interface fifo "emtpy" signal
      FIFO_RDREQ      : IN  std_logic;    -- interface fifo read request
      FIFO_RDCLK      : IN  std_logic;    -- interface fifo read clock
      -- From PC to FPGA, FWFT
      CMD_FIFO_Q      : IN  std_logic_vector(35 DOWNTO 0);  -- interface command fifo data out port
      CMD_FIFO_EMPTY  : IN  std_logic;    -- interface command fifo "emtpy" signal
      CMD_FIFO_RDREQ  : OUT std_logic;    -- interface command fifo read request
      -- Digital I/O
      CONFIG_REG      : OUT std_logic_vector(511 DOWNTO 0); -- thirtytwo 16bit registers
      PULSE_REG       : OUT std_logic_vector(15 DOWNTO 0);  -- 16bit pulse register
      STATUS_REG      : IN  std_logic_vector(175 DOWNTO 0); -- eleven 16bit registers
      -- Memory interface
      MEM_WE          : OUT std_logic;    -- memory write enable
      MEM_ADDR        : OUT std_logic_vector(31 DOWNTO 0);
      MEM_DIN         : OUT std_logic_vector(31 DOWNTO 0);  -- memory data input
      MEM_DOUT        : IN  std_logic_vector(31 DOWNTO 0);  -- memory data output
      -- Data FIFO interface, FWFT
      DATA_FIFO_Q     : IN  std_logic_vector(31 DOWNTO 0);
      DATA_FIFO_EMPTY : IN  std_logic;
      DATA_FIFO_RDREQ : OUT std_logic;
      DATA_FIFO_RDCLK : OUT std_logic
    );
  END COMPONENT;
  ---------------------------------------------> UART/RS232
  ---------------------------------------------< SDRAM
--  COMPONENT sdram_ddr3
--    GENERIC (
--      INDATA_WIDTH   : positive := 256;
--      OUTDATA_WIDTH  : positive := 32;
--      APP_ADDR_WIDTH : positive := 28;
--      APP_DATA_WIDTH : positive := 512;
--      APP_MASK_WIDTH : positive := 64;
--      APP_ADDR_BURST : positive := 8
--    );
--    PORT (
--      CLK                   : IN    std_logic;  -- system clock, must be the same as intended in MIG
--      REFCLK                : IN    std_logic;  -- 200MHz for iodelay
--      RESET                 : IN    std_logic;
--      -- SDRAM_DDR3
--      -- Inouts
--      DDR3_DQ               : INOUT std_logic_vector(63 DOWNTO 0);
--      DDR3_DQS_P            : INOUT std_logic_vector(7 DOWNTO 0);
--      DDR3_DQS_N            : INOUT std_logic_vector(7 DOWNTO 0);
--      -- Outputs
--      DDR3_ADDR             : OUT   std_logic_vector(13 DOWNTO 0);
--      DDR3_BA               : OUT   std_logic_vector(2 DOWNTO 0);
--      DDR3_RAS_N            : OUT   std_logic;
--      DDR3_CAS_N            : OUT   std_logic;
--      DDR3_WE_N             : OUT   std_logic;
--      DDR3_RESET_N          : OUT   std_logic;
--      DDR3_CK_P             : OUT   std_logic_vector(0 DOWNTO 0);
--      DDR3_CK_N             : OUT   std_logic_vector(0 DOWNTO 0);
--      DDR3_CKE              : OUT   std_logic_vector(0 DOWNTO 0);
--      DDR3_CS_N             : OUT   std_logic_vector(0 DOWNTO 0);
--      DDR3_DM               : OUT   std_logic_vector(7 DOWNTO 0);
--      DDR3_ODT              : OUT   std_logic_vector(0 DOWNTO 0);
--      -- Status Outputs
--      INIT_CALIB_COMPLETE   : OUT   std_logic;
--      -- Internal data r/w interface
--      UI_CLK                : OUT   std_logic;
--      --
--      CTRL_RESET            : IN    std_logic;
--      WR_START              : IN    std_logic;
--      WR_ADDR_BEGIN         : IN    std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      WR_STOP               : IN    std_logic;
--      WR_WRAP_AROUND        : IN    std_logic;
--      POST_TRIGGER          : IN    std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      WR_BUSY               : OUT   std_logic;
--      WR_POINTER            : OUT   std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      TRIGGER_POINTER       : OUT   std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      WR_WRAPPED            : OUT   std_logic;
--      RD_START              : IN    std_logic;
--      RD_ADDR_BEGIN         : IN    std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      RD_ADDR_END           : IN    std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      RD_BUSY               : OUT   std_logic;
--      --
--      DATA_FIFO_RESET       : IN    std_logic;
--      INDATA_FIFO_WRCLK     : IN    std_logic;
--      INDATA_FIFO_Q         : IN    std_logic_vector(INDATA_WIDTH-1 DOWNTO 0);
--      INDATA_FIFO_FULL      : OUT   std_logic;
--      INDATA_FIFO_WREN      : IN    std_logic;
--      --
--      OUTDATA_FIFO_RDCLK    : IN    std_logic;
--      OUTDATA_FIFO_Q        : OUT   std_logic_vector(OUTDATA_WIDTH-1 DOWNTO 0);
--      OUTDATA_FIFO_EMPTY    : OUT   std_logic;
--      OUTDATA_FIFO_RDEN     : IN    std_logic;
--      --
--      DBG_APP_ADDR          : OUT   std_logic_vector(APP_ADDR_WIDTH-1 DOWNTO 0);
--      DBG_APP_EN            : OUT   std_logic;
--      DBG_APP_RDY           : OUT   std_logic;
--      DBG_APP_WDF_DATA      : OUT   std_logic_vector(APP_DATA_WIDTH-1 DOWNTO 0);
--      DBG_APP_WDF_END       : OUT   std_logic;
--      DBG_APP_WDF_WREN      : OUT   std_logic;
--      DBG_APP_WDF_RDY       : OUT   std_logic;
--      DBG_APP_RD_DATA       : OUT   std_logic_vector(APP_DATA_WIDTH-1 DOWNTO 0);
--      DBG_APP_RD_DATA_VALID : OUT   std_logic
--    );
--  END COMPONENT;
  ---------------------------------------------> SDRAM
  ---------------------------------------------< debug : ILA and VIO (`Chipscope')
  COMPONENT dbg_ila
    PORT (
      CLK    : IN std_logic;
      PROBE0 : IN std_logic_vector(63 DOWNTO 0);
      PROBE1 : IN std_logic_vector(79 DOWNTO 0);
      PROBE2 : IN std_logic_vector(79 DOWNTO 0);
      PROBE3 : IN std_logic_vector(2047 DOWNTO 0)
    );
  END COMPONENT;
  COMPONENT dbg_ila1
    PORT (
      CLK    : IN std_logic;
      PROBE0 : IN std_logic_vector(15 DOWNTO 0);
      PROBE1 : IN std_logic_vector(15 DOWNTO 0)
    );
  END COMPONENT;
COMPONENT dbg_ila2
  
  PORT (
      clk : IN STD_LOGIC;
      probe0 : IN STD_LOGIC_VECTOR(7 DOWNTO 0); 
      probe1 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
      probe2 : IN STD_LOGIC_VECTOR(15 DOWNTO 0)
  );
  END COMPONENT  ;
  
  COMPONENT dbg_vio
    PORT (
      CLK        : IN  std_logic;
      PROBE_IN0  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN1  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN2  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN3  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN4  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN5  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN6  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN7  : IN  std_logic_vector(63 DOWNTO 0);
      PROBE_IN8  : IN  std_logic_vector(35 DOWNTO 0);
      PROBE_OUT0 : OUT std_logic_vector(63 DOWNTO 0)
    );
  END COMPONENT;
  ---------------------------------------------> debug : ILA and VIO (`Chipscope')
  ---------------------------------------------< Mic4 pixel config
  COMPONENT Pixel_Config
    GENERIC (
      DIV_WIDTH : positive := 6;
      COUNT_WIDTH : positive := 64;
      DATA_WIDTH : positive := 15;
      SHIFT_DIRECTION : positive := 1;
      CNT_WIDTH : positive := 4
    );
    PORT (
      SYS_CLK     : IN  std_logic;      -- clock, S_CLK is derived from this one
      RESET       : IN  std_logic;      -- reset
      -- data input for writing to in-chip FIFO
      SRAM_WE     : IN  std_logic;
      SRAM_DATA   : IN  std_logic_vector(31 DOWNTO 0);
      -- configuration
      DIV         : IN  std_logic_vector(DIV_WIDTH-1 DOWNTO 0);  -- CLK/(2**DIV)
      -- input
      pulse_start : IN  std_logic;
      BUSY        : IN  std_logic;
      -- output
      S_CLK       : OUT std_logic;
      S_DATA      : OUT std_logic
    );
  END COMPONENT;
  ---------------------------------------------> Mic4 pixel config
  ---------------------------------------------< Mic4 temperature sensor
  COMPONENT Temp_Sensor
    GENERIC (
      TS_COUNT_WIDTH : positive := 32
    );
    PORT (
      clk_100MHz : IN std_logic;
      RESET      : IN std_logic;
      pulse_in   : IN std_logic;
      ts_data    : INOUT std_logic;
      MEM_OUT    : OUT std_logic_vector(TS_COUNT_WIDTH-1 DOWNTO 0)
    );
  END COMPONENT;
  ---------------------------------------------> Mic4 temperature sensor
  ---------------------------------------------< Mic4 control
  COMPONENT Mic4_Cntrl
    GENERIC (
      DIV_WIDTH : positive := 6;
      COUNT_WIDTH : positive := 64;
      APULSE_LENGTH : positive := 100;
      DPULSE_LENGTH : positive := 300;
      GRST_LENGTH : positive := 5;
      STROBE_LENGTH : positive := 2
    );
    PORT (
      clk_in      : IN std_logic; 
      clk_control : IN std_logic;
      rst         : IN std_logic;
      div0        : IN std_logic_Vector(DIV_WIDTH-1 DOWNTO 0);
      div1        : IN std_logic_Vector(DIV_WIDTH-1 DOWNTO 0);
      pulse_a     : IN std_logic;
      pulse_d     : IN std_logic;
      pulse_s     : IN std_logic;
      pulse_grst  : IN std_logic;
      clk_out     : OUT std_logic; --CLK_IN of mic4
      lt_out      : OUT std_logic; --LT_IN of mic4
      a_pulse_out : OUT std_logic;
      d_pulse_out : OUT std_logic;
      grst_n_out  : OUT std_logic;
      strobe_out  : OUT std_logic
    );
  END COMPONENT;
  ---------------------------------------------> Mic4 control
    ---------------------------------------------< Strobe
  COMPONENT delayed_rise
      GENERIC (
    DELAY_COUNT : positive := 14
    );
    PORT (
      clk          :IN  std_logic;
      rst          :IN  std_logic;
      trigger      :IN  std_logic;
      out1         :OUT std_logic
    );
  END COMPONENT;
  ---------------------------------------------> Strobe
  
  ---------------------------------------------< FDOUT
  COMPONENT Parallel_SerialX_top
    GENERIC (
      NDATA        : positive := 20;
      FIFO_WIDTH   : positive := 36;
      NUM_WIDTH    : positive := 2;
      FRAME_WIDTH  : positive := 48
    );
    PORT (
      clk_in     : IN  std_logic;
      clk_control: IN  std_logic;
      rst        : IN  std_logic;
      start_pulse: IN  std_logic;
      fd_in      : IN  std_logic_Vector(7 DOWNTO 0);
      trigger    : IN  std_logic;
      evt_trig   : IN  std_logic;
      fifo_rd_en : IN  std_logic;
      fifo_empty : OUT std_logic;
      fifo_q     : OUT std_logic_Vector(FIFO_WIDTH-1 DOWNTO 0)
  );
  END COMPONENT;

  COMPONENT Parallel_Serial_top
    GENERIC (
      NDATA        : positive := 20;
      FIFO_WIDTH   : positive := 36;
      NUM_WIDTH    : positive := 2;
      FRAME_WIDTH  : positive := 48
    );
    PORT (
      clk_in     : IN  std_logic;
      clk_control: IN  std_logic;
      rst        : IN  std_logic;
      start_pulse: IN  std_logic;
      fd0        : IN  std_logic;
      fd1        : IN  std_logic;
      fd2        : IN  std_logic;
      fd3        : IN  std_logic;
      fd4        : IN  std_logic;
      fd5        : IN  std_logic;
      fd6        : IN  std_logic;
      fd7        : IN  std_logic;
      mode       : IN  std_logic;
      fifo_rd_en : IN  std_logic;
      out_debug  : OUT std_logic;
      fifo_empty : OUT std_logic;
      fifo_q     : OUT std_logic_Vector(FIFO_WIDTH-1 DOWNTO 0)
  );
  END COMPONENT;
  ---------------------------------------------> FDOUT
  ---------------------------------------------< DIV_5
  COMPONENT div_5 
    PORT (
      clkin      : IN  std_logic;
      rst        : IN  std_logic;
      clkout     : OUT std_logic
  );
  END COMPONENT;
  ---------------------------------------------> DIV_5 

  ---------------------------------------------< DOUT
  COMPONENT GTX10B8B_dec 
    PORT (
      RESET                       : IN  std_logic;
      Q2_CLK1_GTREFCLK_PAD_N_IN   : IN  std_logic;
      Q2_CLK1_GTREFCLK_PAD_P_IN   : IN  std_logic;
      SYSCLK_IN                   : IN  std_logic;
      RXN_IN                      : IN  std_logic;
      RXP_IN                      : IN  std_logic;
      TXN_OUT                     : OUT std_logic;
      TXP_OUT                     : OUT std_logic;
      D_DATAOUT1                  : OUT std_logic_Vector(7 DOWNTO 0);
      rxcommadet                  : OUT std_logic;
      rxisaligned                 : OUT std_logic;
      rxbyterealign               : OUT std_logic;
      track_out                   : OUT std_logic
  );
  END COMPONENT;
  ---------------------------------------------> DOUT

  -- Signals
  SIGNAL reset                             : std_logic;  
  SIGNAL sys_clk                           : std_logic;
  SIGNAL clk_50MHz                         : std_logic;
  SIGNAL clk_100MHz                        : std_logic;
  SIGNAL clk_125MHz                        : std_logic;
  SIGNAL clk_200MHz                        : std_logic;
  SIGNAL clk_450MHz                        : std_logic;
  SIGNAL clk_600MHz                        : std_logic;
  SIGNAL clk_run                           : std_logic;
  SIGNAL clk156                            : std_logic;
  SIGNAL clk_sgmii_i                       : std_logic;
  SIGNAL clk_sgmii                         : std_logic;
  ---------------------------------------------< UART/RS232
  SIGNAL uart_rx_data                      : std_logic_vector(7 DOWNTO 0);
  SIGNAL uart_rx_rdy                       : std_logic;
  SIGNAL control_clk                       : std_logic;
  SIGNAL control_fifo_q                    : std_logic_vector(35 DOWNTO 0);
  SIGNAL control_fifo_rdreq                : std_logic;
  SIGNAL control_fifo_empty                : std_logic;
  SIGNAL control_fifo_rdclk                : std_logic;
  SIGNAL cmd_fifo_q                        : std_logic_vector(35 DOWNTO 0);
  SIGNAL cmd_fifo_empty                    : std_logic;
  SIGNAL cmd_fifo_rdreq                    : std_logic;
  -- thirtytwo 16bit registers  
  SIGNAL config_reg                        : std_logic_vector(511 DOWNTO 0);
  -- 16bit pulse register
  SIGNAL pulse_reg                         : std_logic_vector(15 DOWNTO 0);
  -- eleven 16bit registers
  SIGNAL status_reg                        : std_logic_vector(175 DOWNTO 0) := (OTHERS => '0');
  SIGNAL control_mem_we                    : std_logic;
  SIGNAL control_mem_addr                  : std_logic_vector(31 DOWNTO 0);
  SIGNAL control_mem_din                   : std_logic_vector(31 DOWNTO 0);
  ---------------------------------------------> UART/RS232
--  ---------------------------------------------< ten_gig_eth 
--  SIGNAL sfp_tx_disable_i                  : std_logic;
--  SIGNAL sPcs_pma_core_status              : std_logic_vector(7 DOWNTO 0);
--  SIGNAL sEmac_status_vector               : std_logic_vector(1 DOWNTO 0);
--  SIGNAL sTx_axis_fifo_aresetn             : std_logic;
--  SIGNAL sTx_axis_fifo_aclk                : std_logic;
--  SIGNAL sTx_axis_fifo_tdata               : std_logic_vector(63 DOWNTO 0);
--  SIGNAL sTx_axis_fifo_tkeep               : std_logic_vector(7 DOWNTO 0);
--  SIGNAL sTx_axis_fifo_tvalid              : std_logic;
--  SIGNAL sTx_axis_fifo_tlast               : std_logic;
--  SIGNAL sTx_axis_fifo_tready              : std_logic;
--  SIGNAL sRx_axis_fifo_aresetn             : std_logic;
--  SIGNAL sRx_axis_fifo_aclk                : std_logic;
--  SIGNAL sRx_axis_fifo_tdata               : std_logic_vector(63 DOWNTO 0);
--  SIGNAL sRx_axis_fifo_tkeep               : std_logic_vector(7 DOWNTO 0);
--  SIGNAL sRx_axis_fifo_tvalid              : std_logic;
--  SIGNAL sRx_axis_fifo_tlast               : std_logic;
--  SIGNAL sRx_axis_fifo_tready              : std_logic;
--  -- control interface
--  SIGNAL s_axi_aclk                        : std_logic;
--  SIGNAL s_axi_aresetn                     : std_logic;
--  SIGNAL s_axi_awaddr                      : std_logic_vector(10 DOWNTO 0);
--  SIGNAL s_axi_awvalid                     : std_logic;
--  SIGNAL s_axi_awready                     : std_logic;
--  SIGNAL s_axi_wdata                       : std_logic_vector(31 DOWNTO 0);
--  SIGNAL s_axi_wvalid                      : std_logic;
--  SIGNAL s_axi_wready                      : std_logic;
--  SIGNAL s_axi_bresp                       : std_logic_vector(1 DOWNTO 0);
--  SIGNAL s_axi_bvalid                      : std_logic;
--  SIGNAL s_axi_bready                      : std_logic;
--  SIGNAL s_axi_araddr                      : std_logic_vector(10 DOWNTO 0);
--  SIGNAL s_axi_arvalid                     : std_logic;
--  SIGNAL s_axi_arready                     : std_logic;
--  SIGNAL s_axi_rdata                       : std_logic_vector(31 DOWNTO 0);
--  SIGNAL s_axi_rresp                       : std_logic_vector(1 DOWNTO 0);
--  SIGNAL s_axi_rvalid                      : std_logic;
--  SIGNAL s_axi_rready                      : std_logic;
--  -- packets
--  SIGNAL ten_gig_eth_tx_start              : std_logic;
--  SIGNAL tge_cmd_fifo_q                    : std_logic_vector(127 DOWNTO 0);
--  SIGNAL tge_cmd_fifo_empty                : std_logic;
--  SIGNAL tge_cmd_fifo_rdreq                : std_logic;
--  ---------------------------------------------> ten_gig_eth
  SIGNAL usr_data_output                   : std_logic_vector (7 DOWNTO 0);
  ---------------------------------------------< gig_eth
  SIGNAL gig_eth_mac_addr                  : std_logic_vector(47 DOWNTO 0);
  SIGNAL gig_eth_ipv4_addr                 : std_logic_vector(31 DOWNTO 0);
  SIGNAL gig_eth_subnet_mask               : std_logic_vector(31 DOWNTO 0);
  SIGNAL gig_eth_gateway_ip_addr           : std_logic_vector(31 DOWNTO 0);
  SIGNAL gig_eth_tx_tdata                  : std_logic_vector(7 DOWNTO 0);
  SIGNAL gig_eth_tx_tvalid                 : std_logic;
  SIGNAL gig_eth_tx_tready                 : std_logic;  
  SIGNAL gig_eth_rx_tdata                  : std_logic_vector(7 DOWNTO 0);
  SIGNAL gig_eth_rx_tvalid                 : std_logic;
  SIGNAL gig_eth_rx_tready                 : std_logic;
  SIGNAL gig_eth_tcp_use_fifo              : std_logic;
  SIGNAL gig_eth_tx_fifo_wrclk             : std_logic;
  SIGNAL gig_eth_tx_fifo_q                 : std_logic_vector(31 DOWNTO 0);
  SIGNAL gig_eth_tx_fifo_wren              : std_logic;
  SIGNAL gig_eth_tx_fifo_full              : std_logic;
  SIGNAL gig_eth_rx_fifo_rdclk             : std_logic;
  SIGNAL gig_eth_rx_fifo_q                 : std_logic_vector(31 DOWNTO 0);
  SIGNAL gig_eth_rx_fifo_rden              : std_logic;
  SIGNAL gig_eth_rx_fifo_empty             : std_logic;
  ---------------------------------------------> gig_eth
  ---------------------------------------------< SDRAM
--  SIGNAL sdram_app_addr                    : std_logic_vector(28-1 DOWNTO 0);
--  SIGNAL sdram_app_en                      : std_logic;
--  SIGNAL sdram_app_rdy                     : std_logic;
--  SIGNAL sdram_app_wdf_data                : std_logic_vector(512-1 DOWNTO 0);
--  SIGNAL sdram_app_wdf_end                 : std_logic;
--  SIGNAL sdram_app_wdf_wren                : std_logic;
--  SIGNAL sdram_app_wdf_rdy                 : std_logic;
--  SIGNAL sdram_app_rd_data                 : std_logic_vector(512-1 DOWNTO 0);
--  SIGNAL sdram_app_rd_data_valid           : std_logic;
  ---------------------------------------------> SDRAM
  ---------------------------------------------< IDATA
  SIGNAL TRIG_OUT_0                        : std_logic;
  SIGNAL idata_cmd_out                     : std_logic_vector(63 DOWNTO 0);
  SIGNAL idata_cmd_out_val                 : std_logic;
  SIGNAL idata_cmd_in                      : std_logic_vector(63 DOWNTO 0);
  SIGNAL idata_cmd_in_val                  : std_logic;
  SIGNAL idata_adc_data_clk                : std_logic;
  SIGNAL idata_adc_refout_clkdiv           : std_logic;
  SIGNAL idata_adc_data0                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data1                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data2                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data3                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data4                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data5                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data6                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data7                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data8                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data9                   : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data10                  : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_adc_data11                  : std_logic_vector(15 DOWNTO 0);
  SIGNAL idata_data_fifo_reset             : std_logic;
  SIGNAL idata_data_fifo_rdclk             : std_logic;
  SIGNAL idata_data_fifo_din               : std_logic_vector(255 DOWNTO 0);
  SIGNAL idata_channel_avg_outdata_q       : std_logic_vector(255 DOWNTO 0);
  SIGNAL idata_channel_avg_outvalid        : std_logic;
  SIGNAL idata_data_fifo_wren              : std_logic;
  SIGNAL idata_data_fifo_rden              : std_logic;
  SIGNAL idata_data_fifo_dout              : std_logic_vector(31 DOWNTO 0);
  SIGNAL idata_data_fifo_full              : std_logic;
  SIGNAL idata_data_fifo_empty             : std_logic;
  SIGNAL idata_idata_fifo_q                : std_logic_vector(255 DOWNTO 0);
  SIGNAL idata_idata_fifo_wren             : std_logic;
  SIGNAL idata_idata_fifo_rden             : std_logic;
  SIGNAL idata_idata_fifo_full             : std_logic;
  SIGNAL idata_idata_fifo_empty            : std_logic;
  SIGNAL idata_trig_allow                  : std_logic;
  SIGNAL idata_trig_in                     : std_logic;
  SIGNAL idata_trig_synced                 : std_logic;
  SIGNAL idata_data_wr_start               : std_logic;
  SIGNAL idata_data_wr_busy                : std_logic;
  SIGNAL idata_data_wr_wrapped             : std_logic;
  ---------------------------------------------> IDATA
  ---------------------------------------------< debug
  SIGNAL dbg_ila_probe0                           : std_logic_vector (63 DOWNTO 0);
  SIGNAL dbg_ila_probe1                           : std_logic_vector (79 DOWNTO 0);
  SIGNAL dbg_ila_probe2                           : std_logic_vector (79 DOWNTO 0);
  SIGNAL dbg_ila_probe3                           : std_logic_vector (2047 DOWNTO 0);
  SIGNAL dbg_vio_probe_out0                       : std_logic_vector (63 DOWNTO 0);
  SIGNAL dbg_ila1_probe0                          : std_logic_vector (15 DOWNTO 0);
  SIGNAL dbg_ila1_probe1                          : std_logic_vector (15 DOWNTO 0);
  ATTRIBUTE mark_debug                            : string;
  ATTRIBUTE keep                                  : string;
  ATTRIBUTE mark_debug OF USB_TX                  : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF uart_rx_data            : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF uart_rx_rdy             : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF cmd_fifo_q              : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF cmd_fifo_empty          : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF cmd_fifo_rdreq          : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF config_reg              : SIGNAL IS "true";
--ATTRIBUTE mark_debug OF status_reg              : SIGNAL IS "true";
--ATTRIBUTE mark_debug OF pulse_reg               : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF control_mem_we          : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF control_mem_addr        : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF control_mem_din         : SIGNAL IS "true";
  --
--  ATTRIBUTE mark_debug OF sPcs_pma_core_status    : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sEmac_status_vector     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_aresetn   : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_aclk      : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_tdata     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_tkeep     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_tvalid    : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_tlast     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sTx_axis_fifo_tready    : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_aresetn   : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_aclk      : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_tdata     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_tkeep     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_tvalid    : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_tlast     : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sRx_axis_fifo_tready    : SIGNAL IS "true";
--  --ATTRIBUTE mark_debug OF ten_gig_eth_tx_start    : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF tge_cmd_fifo_q          : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF tge_cmd_fifo_empty      : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF tge_cmd_fifo_rdreq      : SIGNAL IS "true";
  --
  ATTRIBUTE mark_debug OF gig_eth_tx_tdata        : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_tx_tvalid       : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_tx_tready       : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_rx_tdata        : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_rx_tvalid       : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_rx_tready       : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_tx_fifo_q       : SIGNAL IS "true";
  ATTRIBUTE mark_debug OF gig_eth_rx_fifo_q       : SIGNAL IS "true";
  --
--  ATTRIBUTE mark_debug OF sdram_app_addr          : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_en            : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_rdy           : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_wdf_data      : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_wdf_end       : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_wdf_wren      : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_wdf_rdy       : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_rd_data       : SIGNAL IS "true";
--  ATTRIBUTE mark_debug OF sdram_app_rd_data_valid : SIGNAL IS "true";
  ---------------------------------------------> debug
  ---------------------------------------------< TOP_SR
  SIGNAL div                               : std_logic_vector(5 DOWNTO 0);
  SIGNAL din                               : std_logic_vector(199 DOWNTO 0);
  SIGNAL clk_sr_contr                      : std_logic;
  SIGNAL fifo_q1                           : std_logic_vector(35 DOWNTO 0);
  SIGNAL fifo_rden1  : std_logic;
  SIGNAL fifo_empty1 : std_logic;
  ---------------------------------------------> TOP_SR
  ---------------------------------------------< PULSE_SYNCHRONISE
  SIGNAL pulse_in                          : std_logic;
  SIGNAL clk_out                           : std_logic;
  SIGNAL pulse_out                         : std_logic;
  ---------------------------------------------> PULSE_SYNCHRONISE
  ---------------------------------------------< shiftreg driver for DAC8568
  SIGNAL spi_sclk                          : std_logic;
  SIGNAL spi_dout                          : std_logic;
  SIGNAL spi_din                           : std_logic;
  SIGNAL spi_sync_n                        : std_logic;
  SIGNAL spi_sync_n1                       : std_logic;
  SIGNAL spi_sync_n2                       : std_logic;  
  ---------------------------------------------> shiftreg driver for DAC8568
  ---------------------------------------------< Mic4 pixel config
  SIGNAL  mic_pc_div : std_logic_vector(5 DOWNTO 0);
  ---------------------------------------------> Mic4 pixel config
  ---------------------------------------------< Mic4 temperature sensor
  SIGNAL mem_out     : std_logic_vector(31 DOWNTO 0);
  ---------------------------------------------> Mic4 temperature sensor
  ---------------------------------------------< Mic4 control
  SIGNAL  div0_mc : std_logic_vector(5 DOWNTO 0);
  SIGNAL  div1_mc : std_logic_vector(5 DOWNTO 0);
  SIGNAL  clk_out_mc   : std_logic;
  SIGNAL  clk_out_mc_i : std_logic;
  SIGNAL  lt_out_mc    : std_logic;
  ---------------------------------------------> Mic4 control
  SIGNAL  fd_out0 : std_logic; 
  SIGNAL  fd_out1 : std_logic;
  SIGNAL  fd_out2 : std_logic;
  SIGNAL  fd_out3 : std_logic;
  SIGNAL  fd_out4 : std_logic;
  SIGNAL  fd_out5 : std_logic;
  SIGNAL  fd_out6 : std_logic;
  SIGNAL  fd_out7 : std_logic;
  SIGNAL  pulse10_out : std_logic;
  SIGNAL  fifo_rden2  : std_logic;
  SIGNAL  fifo_empty2 : std_logic;
  SIGNAL  fifo_q2     : std_logic_vector(35 DOWNTO 0);
  SIGNAL  probe0_FD   :std_logic_vector(7 DOWNTO 0);
  SIGNAL  data_out    :std_logic_vector(7 DOWNTO 0);
  SIGNAL  ila2_probe1 :std_logic_vector(3 DOWNTO 0);
  SIGNAL  ila2_probe2 :std_logic_vector(15 DOWNTO 0);
  SIGNAL  start_fd  : std_logic;
  SIGNAL  trigger_in  :std_logic;
  SIGNAL  strobe_i    :std_logic;
  SIGNAL  strobe_i2   :std_logic;
  SIGNAL  strobe_opt  :std_logic_vector(1 DOWNTO 0);
  SIGNAL  valid_out   :std_logic;
  ---------------------------------------------> FDOUT
  ---------------------------------------------> DIV_5
  SIGNAL div_5_out : std_logic;
  SIGNAL chip_rest: std_logic;
  ---------------------------------------------> DIV_5
  ---------------------------------------------< DOUT
  SIGNAL  data_DOut      :std_logic_vector(7 DOWNTO 0);
  SIGNAL  rxcommadet_i   :std_logic;
  SIGNAL  rxisaligned_i  :std_logic;
  SIGNAL  rxbyterealign_i:std_logic;
  SIGNAL  track_out_i    :std_logic;
  SIGNAL  gtx_refclk_P   :std_logic;
  SIGNAL  gtx_refclk_N   :std_logic;
  ---------------------------------------------> DOUT
  
BEGIN
  ---------------------------------------------< Clock
  global_clock_reset_inst : global_clock_reset
    PORT MAP (
      SYS_CLK_P  => SYS_CLK_P,
      SYS_CLK_N  => SYS_CLK_N,
      FORCE_RST  => SYS_RST,
      -- output
      GLOBAL_RST => reset,
      SYS_CLK    => sys_clk,
      CLK_OUT1   => clk_50MHz,
      CLK_OUT2   => clk_100MHz,
      CLK_OUT3   => clk_600MHz,
      CLK_OUT4   => clk_450MHz
    );

  -- gtx/gth reference clock can be used as general purpose clock this way
  sgmiiclk_ibufds_inst : IBUFDS_GTE2
    PORT MAP (
      O     => clk_sgmii_i,
      ODIV2 => OPEN,
      CEB   => '0',
      I     => SGMIICLK_Q0_P,
      IB    => SGMIICLK_Q0_N
    );
  sgmiiclk_bufg_inst : BUFG
    PORT MAP (
      I => clk_sgmii_i,
      O => clk_sgmii
    );
  clk_125MHz <= clk_sgmii;

  ---------------------------------------------> Clock
  ---------------------------------------------< debug : ILA and VIO (`Chipscope')
  dbg_cores : IF ENABLE_DEBUG GENERATE
    dbg_ila_inst : dbg_ila
      PORT MAP (
        CLK    => sys_clk,
        PROBE0 => dbg_ila_probe0,
        PROBE1 => dbg_ila_probe1,
        PROBE2 => dbg_ila_probe2,
        PROBE3 => dbg_ila_probe3
      );
    dbg_vio_inst : dbg_vio
      PORT MAP (
        CLK        => sys_clk,
        PROBE_IN0  => config_reg(64*1-1 DOWNTO 64*0),
        PROBE_IN1  => config_reg(64*2-1 DOWNTO 64*1),
        PROBE_IN2  => config_reg(64*3-1 DOWNTO 64*2),
        PROBE_IN3  => config_reg(64*4-1 DOWNTO 64*3),
        PROBE_IN4  => config_reg(64*5-1 DOWNTO 64*4),
        PROBE_IN5  => config_reg(64*6-1 DOWNTO 64*5),
        PROBE_IN6  => config_reg(64*7-1 DOWNTO 64*6),
        PROBE_IN7  => x"0000000000000000", -- config_reg(64*8-1 DOWNTO 64*7),
        PROBE_IN8  => cmd_fifo_q,
        PROBE_OUT0 => dbg_vio_probe_out0
      );
    --dbg_ila1_inst : dbg_ila1
    --  PORT MAP (
    --    CLK    => sys_clk,
    --    PROBE0 => dbg_ila1_probe0,
    --    PROBE1 => dbg_ila1_probe1
    --  );
  END GENERATE dbg_cores;
  
  dbg_ila2_FD : dbg_ila2
  PORT MAP (
      clk => sys_clk,
      probe0 => probe0_FD,
      probe1 => ila2_probe1,
      probe2 => ila2_probe2
  );
  ---------------------------------------------> debug : ILA and VIO (`Chipscope')
  ---------------------------------------------< UART/RS232
  uart_cores : IF false GENERATE
    uartio_inst : uartio
      GENERIC MAP (
        -- tick repetition frequency is (input freq) / (2**COUNTER_WIDTH / DIVISOR)
        COUNTER_WIDTH => 6,
        DIVISOR       => 1208*2
      )
      PORT MAP (
        CLK     => clk_50MHz,
        RESET   => reset,
        RX_DATA => uart_rx_data,
        RX_RDY  => uart_rx_rdy,
        TX_DATA => "0000" & DIPSw4Bit,
        TX_EN   => '1',
        TX_RDY  => dbg_ila_probe0(2),
        -- serial lines
        RX_PIN  => USB_TX,                -- notice the pin swap
        TX_PIN  => USB_RX
      );

    --dbg_ila1_probe0(7 DOWNTO 0)  <= uart_rx_data;
    --dbg_ila1_probe0(8)           <= uart_rx_rdy;
    --dbg_ila1_probe0(9)           <= USB_TX;

    -- dbg_ila_probe0(63 DOWNTO 32) <= cmd_fifo_q(31 DOWNTO 0);
    dbg_ila_probe0(31)           <= cmd_fifo_empty;
    dbg_ila_probe0(30)           <= cmd_fifo_rdreq;

    byte2cmd_inst : byte2cmd
      PORT MAP (
        CLK            => clk_50MHz,
        RESET          => reset,
        -- byte in
        RX_DATA        => uart_rx_data,
        RX_RDY         => uart_rx_rdy,
        -- cmd out
        CMD_FIFO_Q     => OPEN,-- cmd_fifo_q,
        CMD_FIFO_EMPTY => OPEN,-- cmd_fifo_empty,
        CMD_FIFO_RDCLK => control_clk,
        CMD_FIFO_RDREQ => '0'  -- cmd_fifo_rdreq
      );
  END GENERATE uart_cores;

  control_clk <= clk_100MHz;
  clk_run <= clk_600MHz;

  control_interface_inst : control_interface
    PORT MAP (
      RESET => reset,
      CLK   => control_clk,
      -- From FPGA to PC
      FIFO_Q          => control_fifo_q,
      FIFO_EMPTY      => control_fifo_empty,
      FIFO_RDREQ      => control_fifo_rdreq,
      FIFO_RDCLK      => control_fifo_rdclk,
      -- From PC to FPGA, FWFT
      CMD_FIFO_Q      => cmd_fifo_q,
      CMD_FIFO_EMPTY  => cmd_fifo_empty,
      CMD_FIFO_RDREQ  => cmd_fifo_rdreq,
      -- Digital I/O
      CONFIG_REG      => config_reg,
      PULSE_REG       => pulse_reg,
      STATUS_REG      => status_reg,
      -- Memory interface
      MEM_WE          => control_mem_we,
      MEM_ADDR        => control_mem_addr,
      MEM_DIN         => control_mem_din,
      MEM_DOUT        => mem_out,
      -- Data FIFO interface, FWFT
      DATA_FIFO_Q     => idata_data_fifo_dout,
      DATA_FIFO_EMPTY => idata_data_fifo_empty,
      DATA_FIFO_RDREQ => idata_data_fifo_rden,
      DATA_FIFO_RDCLK => idata_data_fifo_rdclk
    );
  dbg_ila_probe0(18 DOWNTO 3) <= pulse_reg;
  ---------------------------------------------> UART/RS232
--  ---------------------------------------------< ten_gig_eth
--  ten_gig_eth_cores : IF ENABLE_TEN_GIG_ETH GENERATE
--    ten_gig_eth_inst : ten_gig_eth
--      PORT MAP (
--        REFCLK_P             => USER_CLK_P,  -- 156.25MHz for transceiver
--        REFCLK_N             => USER_CLK_N,
--        RESET                => reset,
--        SFP_TX_P             => SFP_TX_P,
--        SFP_TX_N             => SFP_TX_N,
--        SFP_RX_P             => SFP_RX_P,
--        SFP_RX_N             => SFP_RX_N,
--        SFP_LOS              => SFP_LOS_LS,  -- loss of receiver signal
--        SFP_TX_DISABLE       => sfp_tx_disable_i,
--        -- clk156 domain, clock generated by the core
--        CLK156               => clk156,
--        PCS_PMA_CORE_STATUS  => sPcs_pma_core_status,
--        TX_STATISTICS_VECTOR => OPEN,
--        TX_STATISTICS_VALID  => OPEN,
--        RX_STATISTICS_VECTOR => OPEN,
--        RX_STATISTICS_VALID  => OPEN,
--        PAUSE_VAL            => (OTHERS => '0'),
--        PAUSE_REQ            => '0',
--        TX_IFG_DELAY         => x"ff",
--        -- emac control interface
--        S_AXI_ACLK           => s_axi_aclk,
--        S_AXI_ARESETN        => s_axi_aresetn,
--        S_AXI_AWADDR         => s_axi_awaddr,
--        S_AXI_AWVALID        => s_axi_awvalid,
--        S_AXI_AWREADY        => s_axi_awready,
--        S_AXI_WDATA          => s_axi_wdata,
--        S_AXI_WVALID         => s_axi_wvalid,
--        S_AXI_WREADY         => s_axi_wready,
--        S_AXI_BRESP          => s_axi_bresp,
--        S_AXI_BVALID         => s_axi_bvalid,
--        S_AXI_BREADY         => s_axi_bready,
--        S_AXI_ARADDR         => s_axi_araddr,
--        S_AXI_ARVALID        => s_axi_arvalid,
--        S_AXI_ARREADY        => s_axi_arready,
--        S_AXI_RDATA          => s_axi_rdata,
--        S_AXI_RRESP          => s_axi_rresp,
--        S_AXI_RVALID         => s_axi_rvalid,
--        S_AXI_RREADY         => s_axi_rready,
--        -- tx_wr_clk domain
--        TX_AXIS_FIFO_ARESETN => sTx_axis_fifo_aresetn,
--        Tx_AXIS_FIFO_ACLK    => sTx_axis_fifo_aclk,
--        TX_AXIS_FIFO_TDATA   => sTx_axis_fifo_tdata,
--        TX_AXIS_FIFO_TKEEP   => sTx_axis_fifo_tkeep,
--        TX_AXIS_FIFO_TVALID  => sTx_axis_fifo_tvalid,
--        TX_AXIS_FIFO_TLAST   => sTx_axis_fifo_tlast,
--        TX_AXIS_FIFO_TREADY  => sTx_axis_fifo_tready,
--        -- rx_rd_clk domain
--        RX_AXIS_FIFO_ARESETN => sRx_axis_fifo_aresetn,
--        RX_AXIS_FIFO_ACLK    => sRx_axis_fifo_aclk,
--        RX_AXIS_FIFO_TDATA   => sRx_axis_fifo_tdata,
--        RX_AXIS_FIFO_TKEEP   => sRx_axis_fifo_tkeep,
--        RX_AXIS_FIFO_TVALID  => sRx_axis_fifo_tvalid,
--        RX_AXIS_FIFO_TLAST   => sRx_axis_fifo_tlast,
--        RX_AXIS_FIFO_TREADY  => sRx_axis_fifo_tready
--      );

--    SFP_TX_DISABLE_N   <= NOT sfp_tx_disable_i;
--    LED8Bit(7)         <= sPcs_pma_core_status(0);
--    LED8Bit(6)         <= NOT sfp_tx_disable_i;
--    LED8Bit(5)         <= NOT SFP_LOS_LS;
--    s_axi_aclk         <= clk_50MHz;
--    sTx_axis_fifo_aclk <= clk_200MHz;
--    sRx_axis_fifo_aclk <= sTx_axis_fifo_aclk;

--    s_axi_aresetn         <= '1';
--    sTx_axis_fifo_aresetn <= '1';
--    -- sRx_axis_fifo_aresetn <= '1';

--    ten_gig_eth_packet_gen_inst : ten_gig_eth_packet_gen
--      PORT MAP (
--        RESET          => reset,
--        MEM_CLK        => control_clk,
--        MEM_WE         => control_mem_we,
--        MEM_ADDR       => control_mem_addr,
--        MEM_D          => control_mem_din,
--        --
--        TX_AXIS_ACLK   => sTx_axis_fifo_aclk,
--        TX_START       => ten_gig_eth_tx_start,
--        TX_BYTES       => config_reg(15 DOWNTO 0),
--        TX_AXIS_TDATA  => OPEN, -- sTx_axis_fifo_tdata,
--        TX_AXIS_TKEEP  => sTx_axis_fifo_tkeep,
--        TX_AXIS_TVALID => sTx_axis_fifo_tvalid,
--        TX_AXIS_TLAST  => sTx_axis_fifo_tlast,
--        TX_AXIS_TREADY => sTx_axis_fifo_tready
--      );

--    ten_gig_eth_rx_parser_inst : ten_gig_eth_rx_parser
--      PORT MAP (
--        RESET                => reset,
--        RX_AXIS_FIFO_ARESETN => sRx_axis_fifo_aresetn,
--        -- Everything internal to this module is synchronous to this clock `ACLK'
--        RX_AXIS_FIFO_ACLK    => sRx_axis_fifo_aclk,
--        RX_AXIS_FIFO_TDATA   => sRx_axis_fifo_tdata,
--        RX_AXIS_FIFO_TKEEP   => sRx_axis_fifo_tkeep,
--        RX_AXIS_FIFO_TVALID  => sRx_axis_fifo_tvalid,
--        RX_AXIS_FIFO_TLAST   => sRx_axis_fifo_tlast,
--        RX_AXIS_FIFO_TREADY  => sRx_axis_fifo_tready,
--        -- Constants
--        SRC_MAC              => x"000a3502a759",
--        SRC_IP               => x"c0a80302",
--        SRC_PORT             => x"ea62",
--        -- Command output fifo interface AFTER parsing the packet
--        -- dstMAC(48) dstIP(32) dstPort(16) opcode(32)
--        CMD_FIFO_Q           => tge_cmd_fifo_q,
--        CMD_FIFO_EMPTY       => tge_cmd_fifo_empty,
--        CMD_FIFO_RDREQ       => '1',
--        CMD_FIFO_RDCLK       => clk_200MHz
--      );

--    --pulsegen_inst : pulsegen
--    --  GENERIC MAP (
--    --    COUNTER_WIDTH => 16
--    --  )
--    --  PORT MAP (
--    --    CLK    => sTx_axis_fifo_aclk,
--    --    PERIOD => config_reg(31 DOWNTO 16),
--    --    I      => pulse_reg(0),
--    --    O      => ten_gig_eth_tx_start
--    --  );
--    ten_gig_eth_tx_start <= pulse_reg(0);

--    dbg_ila_probe0(0) <= clk156;
--    dbg_ila_probe0(1) <= ten_gig_eth_tx_start;

--    dbg_ila_probe1(79 DOWNTO 16) <= sTx_axis_fifo_tdata;
--    dbg_ila_probe1(15 DOWNTO 8)  <= sTx_axis_fifo_tkeep;
--    dbg_ila_probe1(7)            <= sTx_axis_fifo_tvalid;
--    dbg_ila_probe1(6)            <= sTx_axis_fifo_tlast;
--    dbg_ila_probe1(5)            <= sTx_axis_fifo_tready;
--    --dbg_ila_probe2(79 DOWNTO 16) <= sRx_axis_fifo_tdata;
--    --dbg_ila_probe2(79 DOWNTO 48) <= control_mem_addr;
--    --dbg_ila_probe2(47 DOWNTO 16) <= control_mem_din;
--    --dbg_ila_probe2(15 DOWNTO 8)  <= sRx_axis_fifo_tkeep;
--    dbg_ila_probe2(7)            <= sRx_axis_fifo_tvalid;
--    dbg_ila_probe2(6)            <= sRx_axis_fifo_tlast;
--    dbg_ila_probe2(5)            <= sRx_axis_fifo_tready;
--    dbg_ila_probe2(4)            <= control_mem_we;
--    --
--    --dbg_ila_probe3(127 DOWNTO 0) <= tge_cmd_fifo_q;
--    --dbg_ila_probe3(128)          <= tge_cmd_fifo_empty;
--  END GENERATE ten_gig_eth_cores;
--  ---------------------------------------------> ten_gig_eth
  ---------------------------------------------< gig_eth
  gig_eth_cores : IF ENABLE_GIG_ETH GENERATE
    gig_eth_mac_addr(gig_eth_mac_addr'length-1 DOWNTO 4)   <= x"000a3502a75";
    gig_eth_mac_addr(3 DOWNTO 0)                           <= DIPSw4Bit;
    gig_eth_ipv4_addr(gig_eth_ipv4_addr'length-1 DOWNTO 4) <= x"c0a8020";
    gig_eth_ipv4_addr(3 DOWNTO 0)                          <= DIPSw4Bit;
    gig_eth_subnet_mask                                    <= x"ffffff00";
    gig_eth_gateway_ip_addr                                <= x"c0a80201";
    gig_eth_inst : gig_eth
      PORT MAP (
        -- asynchronous reset
        GLBL_RST             => reset,
        -- clocks
        GTX_CLK              => clk_125MHz,
        REF_CLK              => sys_clk, -- 200MHz for IODELAY
        -- PHY interface
        PHY_RESETN           => PHY_RESET_N,
        -- RGMII Interface
        RGMII_TXD            => RGMII_TXD,
        RGMII_TX_CTL         => RGMII_TX_CTL,
        RGMII_TXC            => RGMII_TXC,
        RGMII_RXD            => RGMII_RXD,
        RGMII_RX_CTL         => RGMII_RX_CTL,
        RGMII_RXC            => RGMII_RXC,
        -- MDIO Interface
        MDIO                 => MDIO,
        MDC                  => MDC,
        -- TCP
        MAC_ADDR             => gig_eth_mac_addr,
        IPv4_ADDR            => gig_eth_ipv4_addr,
        IPv6_ADDR            => (OTHERS => '0'),
        SUBNET_MASK          => gig_eth_subnet_mask,
        GATEWAY_IP_ADDR      => gig_eth_gateway_ip_addr,
        TCP_CONNECTION_RESET => '0',
        TX_TDATA             => gig_eth_tx_tdata,
        TX_TVALID            => gig_eth_tx_tvalid,
        TX_TREADY            => gig_eth_tx_tready,
        RX_TDATA             => gig_eth_rx_tdata,
        RX_TVALID            => gig_eth_rx_tvalid,
        RX_TREADY            => gig_eth_rx_tready,
        -- FIFO
        TCP_USE_FIFO         => gig_eth_tcp_use_fifo,
        TX_FIFO_WRCLK        => gig_eth_tx_fifo_wrclk,
        TX_FIFO_Q            => gig_eth_tx_fifo_q,
        TX_FIFO_WREN         => gig_eth_tx_fifo_wren,
        TX_FIFO_FULL         => gig_eth_tx_fifo_full,
        RX_FIFO_RDCLK        => gig_eth_rx_fifo_rdclk,
        RX_FIFO_Q            => gig_eth_rx_fifo_q,
        RX_FIFO_RDEN         => gig_eth_rx_fifo_rden,
        RX_FIFO_EMPTY        => gig_eth_rx_fifo_empty
      );
    dbg_ila_probe0(26 DOWNTO 19) <= gig_eth_rx_tdata;
    dbg_ila_probe0(27)           <= gig_eth_rx_tvalid;
    dbg_ila_probe0(28)           <= gig_eth_rx_tready;

    -- loopback
    --gig_eth_tx_tdata  <= gig_eth_rx_tdata;
    --gig_eth_tx_tvalid <= gig_eth_rx_tvalid;
    --gig_eth_rx_tready <= gig_eth_tx_tready;

    -- receive to cmd_fifo
    gig_eth_tcp_use_fifo         <= '1';
    gig_eth_rx_fifo_rdclk        <= control_clk;
    cmd_fifo_q(31 DOWNTO 0)      <= gig_eth_rx_fifo_q;
    dbg_ila_probe0(63 DOWNTO 32) <= gig_eth_rx_fifo_q;
    cmd_fifo_empty               <= gig_eth_rx_fifo_empty;
    gig_eth_rx_fifo_rden         <= cmd_fifo_rdreq;

    -- send control_fifo data through gig_eth_tx_fifo
    gig_eth_tx_fifo_wrclk <= clk_125MHz;
    -- connect FWFT fifo interface
    control_fifo_rdclk    <= gig_eth_tx_fifo_wrclk;
    gig_eth_tx_fifo_q     <= control_fifo_q(31 DOWNTO 0);
    gig_eth_tx_fifo_wren  <= NOT control_fifo_empty;
    control_fifo_rdreq    <= NOT gig_eth_tx_fifo_full;
  END GENERATE gig_eth_cores;
  ---------------------------------------------> gig_eth

  -- capture the rising edge of trigger
  trig_edge_sync_inst : edge_sync
    PORT MAP (
      RESET => reset,
      CLK   => control_clk,
      EI    => idata_trig_in,
      SO    => idata_trig_synced
    );
  idata_trig_allow    <= config_reg(32*6+30);
  idata_data_wr_start <= pulse_reg(3) OR (idata_trig_synced AND idata_trig_allow
                                          AND (NOT idata_data_wr_busy)
                                          AND (NOT idata_data_wr_wrapped));
  USER_SMA_GPIO_P <= idata_trig_synced;

  dbg_ila1_probe0 <= idata_adc_data0;
  dbg_ila1_probe1 <= idata_adc_data4;

  --led_obufs : FOR i IN 0 TO 7 GENERATE
  --  led_obuf : OBUF
  --    PORT MAP (
  --      I => usr_data_output(i),
  --      O => LED8Bit(i)
  --    );
  --END GENERATE led_obufs;
  --LED8Bit(5 DOWNTO 1) <= (OTHERS => '0');

  ---------------------------------------------< TOP_SR
  div <= config_reg(5 DOWNTO 0);
  din <= config_reg(207 DOWNTO 8);
  idata_data_fifo_dout  <= fifo_q1(31 DOWNTO 0) WHEN config_reg(6)='1' ELSE fifo_q2(31 DOWNTO 0); -- x"0000" will be modified to FD_OUT of mic4 chip when the receiver is done.
  idata_data_fifo_empty <= fifo_empty1          WHEN config_reg(6)='1' ELSE fifo_empty2; 
  fifo_rden1<=idata_data_fifo_rden when config_reg(6)='1' else '0';
  fifo_rden2<=idata_data_fifo_rden when config_reg(6)='0' else '0';

--   idata_data_fifo_dout  <= x"1234" WHEN config_reg(6)='1' ELSE x"abcd"; -- x"0000" will be modified to FD_OUT of mic4 chip when the receiver is done.
--   idata_data_fifo_empty <= '0'; 
--  idata_data_fifo_rden  <= fifo_rden1           WHEN config_reg(6)='1' ELSE fifo_rden2; 
  Top_SR_0 : Top_SR
    GENERIC MAP (
      WIDTH           => 200,
      CNT_WIDTH       => 8,
      DIV_WIDTH       => 6,
      COUNT_WIDTH     => 64,
      VALID_WIDTH     => 32,
      NUM_WIDTH       => 4,
      FIFO_WIDTH      => 36,
      SHIFT_DIRECTION => 1,
      READ_TRIG_SRC   => 0,
      READ_DELAY      => 1
    )
    PORT MAP (
      clk_in     => control_clk,
      rst        => reset,
      start      => pulse_out,
--      wr_en      => pulse_reg(3),
      din        => din,
      data_in    => FMC_HPC_HA_P(9) ,
      div        => div,
      fifo_rd_en => fifo_rden1,
      clk        => clk_sr_contr,
      clk_sr     => FMC_HPC_LA_P(20),
      data_out   => FMC_HPC_LA_P(33),
      load_sr    => FMC_HPC_LA_P(31),
      fifo_empty => fifo_empty1,
      fifo_q     => fifo_q1
    );
  ---------------------------------------------> TOP_SR
  ---------------------------------------------< PULSE_SYNCHRONISE
  pulse_in <= pulse_reg(0);
  pulse_synchronise_0 : pulse_synchronise
    PORT MAP (
      pulse_in  => pulse_in,
      clk_in    => control_clk,
      clk_out   => clk_sr_contr,
      rst       => reset,
      pulse_out => pulse_out
    );
  ---------------------------------------------> PULSE_SYNCHRONISE
  ---------------------------------------------< shiftreg driver for DAC8568
  dac8568_inst : fifo2shiftreg
    GENERIC MAP (
      DATA_WIDTH        => 32,          -- parallel data width
      CLK_DIV_WIDTH     => 16,
      DELAY_AFTER_SYNCn => 0,  -- number of SCLK cycles' wait after falling edge OF SYNCn
      SCLK_IDLE_LEVEL   => '0',  -- High or Low for SCLK when not switching
      DOUT_DRIVE_EDGE   => '1',  -- 1/0 rising/falling edge of SCLK drives new DOUT bit
      DIN_CAPTURE_EDGE  => '0'  -- 1/0 rising/falling edge of SCLK captures new DIN bit
    )
    PORT MAP (
      CLK      => control_clk,          -- clock
      RESET    => reset,                -- reset
      -- input data interface
      WR_CLK   => control_clk,          -- FIFO write clock
      DINFIFO  => config_reg(16*16+15 DOWNTO 16*16),
      WR_EN    => '0',
      WR_PULSE => pulse_reg(1),  -- one pulse writes one word, regardless of pulse duration
      FULL     => OPEN,
      -- captured data
      BUSY     => OPEN,
      DATAOUT  => OPEN,
      -- serial interface
      CLK_DIV  => x"0002",
      SCLK     => FMC_HPC_LA_P(9),
      DOUT     => FMC_HPC_LA_P(13),
      SYNCn    => FMC_HPC_LA_P(5),
      DIN      => spi_din
    );
  ---------------------------------------------> shiftreg driver for DAC8568
  ---------------------------------------------< Mic4 pixel config
  mic_pc_div <= config_reg(16*17+5 DOWNTO 16*17);
  Pixel_Config_inst : Pixel_Config
    GENERIC MAP(
      DIV_WIDTH       => 6,
      COUNT_WIDTH     => 64,
      DATA_WIDTH      => 15,
      SHIFT_DIRECTION => 1,
      CNT_WIDTH       => 4
    )
    PORT MAP (
      SYS_CLK      => control_clk,
      RESET        => reset,
      DIV          => mic_pc_div,
      SRAM_DATA    => control_mem_din,
      SRAM_WE      => control_mem_we,
      pulse_start  => pulse_reg(2),
      BUSY         => FMC_HPC_HA_P(23), 
      S_CLK        => FMC_HPC_LA_P(22),
      S_DATA       => FMC_HPC_LA_P(25) 
   );
  ---------------------------------------------> Mic4 pixel config
  ---------------------------------------------< Mic4 temperature sensor
  Temp_Sensor_inst : Temp_Sensor
    GENERIC MAP(
      TS_COUNT_WIDTH => 32
    )
    PORT MAP (
      clk_100MHz => clk_100MHz,
      RESET      => reset,
      pulse_in   => pulse_reg(4),
      ts_data    => FMC_HPC_HA_P(21),
      MEM_OUT    => mem_out
   );
  ---------------------------------------------> Mic4 temperature sensor
  ---------------------------------------------< Mic4 control
  div0_mc <= config_reg(16*18+5 DOWNTO 16*18);
  div1_mc <= config_reg(16*18+11 DOWNTO 16*18+6);
  
  ------------------------------Strobe
  delayed_rise_inst0: delayed_rise
    GENERIC MAP(
      DELAY_COUNT => 14
    )
    PORT MAP (
      clk => clk_run,
      rst  => reset,
      trigger => valid_out,
      out1 => strobe_i
    );
  ---------------------------Strobe

  --------------------------- Chip reset
  pulse_synchronise_chip_reset : pulse_synchronise
    PORT MAP (
      pulse_in  => pulse_reg(11),
      clk_in    => control_clk,
      clk_out   => div_5_out,
      rst       => reset,
      pulse_out => chip_rest
    );
  ----------------------------

  --FMC_HPC_LA_P(30) <= config_reg(16*18+12); --STROBE
  --FMC_HPC_LA_P(30) <= strobe_i;
 
  strobe_opt <= config_reg(16*18+14 DOWNTO 16*18+13);
  
  FMC_HPC_LA_P(30) <= strobe_i when strobe_opt="01" else -- data-driven
		      strobe_i2 when strobe_opt="10" else -- trigger-driven
		      config_reg(16*18+12); -- constant

  FMC_HPC_HA_P(05) <= valid_out;
  FMC_HPC_LA_P(32) <= NOT (reset OR chip_rest); --RESET: the modules work with high voltage in the chip.
 
  --FMC_HPC_HA_N(19) <= trigger_in;

  BUFG_inst3 : BUFG
    PORT MAP (
      I => '0', --FMC_HPC_HA_N(19),
      O => trigger_in
    );

  Mic4_Cntrl_inst : Mic4_Cntrl
    GENERIC MAP(
      DIV_WIDTH     => 6,
      COUNT_WIDTH   => 64,
      APULSE_LENGTH => 90000,
      DPULSE_LENGTH => 10,
      GRST_LENGTH   => 5,
      STROBE_LENGTH => 2
    )
    PORT MAP (
      clk_in => clk_run,
      clk_control => control_clk,
      rst  => reset,
      div0 => div0_mc,
      div1 => div1_mc,
      pulse_grst => pulse_reg(5),
      pulse_a => pulse_reg(6),
      pulse_d => pulse_reg(7),
      pulse_s => trigger_in,
      clk_out => clk_out_mc_i, -- CLK_IN of mic4
      lt_out => lt_out_mc, --LT_IN of mic4
      a_pulse_out => FMC_HPC_LA_P(21),
      d_pulse_out => FMC_HPC_LA_P(24),
      grst_n_out => FMC_HPC_LA_P(28),
      strobe_out => strobe_i2
    );

  --- Make it a global clock to get better timing
  BUFG_inst2 : BUFG
    PORT MAP (
      I => clk_out_mc_i,
      O => clk_out_mc
    );

  clkmc_obufds_inst : OBUFDS
    GENERIC MAP (
      IOSTANDARD => "LVDS"
    )
    PORT MAP (
      O  => USER_SMA_CLOCK_P,  -- Diff_p output (connect directly to top-level port)
      OB => USER_SMA_CLOCK_N,  -- Diff_n output (connect directly to top-level port)
      I  => clk_out_mc
   );

  ltmc_obufds_inst : OBUFDS
    GENERIC MAP (
      IOSTANDARD => "LVDS"
    )
    PORT MAP (
      O  => FMC_HPC_LA_P(19),  -- Diff_p output (connect directly to top-level port)
      OB => FMC_HPC_LA_N(19),  -- Diff_n output (connect directly to top-level port)
      I  => lt_out_mc
   );
  ---------------------------------------------< Mic4 control


  test_obufds_inst : OBUFDS
  GENERIC MAP (
    IOSTANDARD => "LVDS"
  )
  PORT MAP (
    O  => FMC_HPC_HA_P(15),  -- Diff_p output (connect directly to top-level port)
    OB => FMC_HPC_HA_N(15),  -- Diff_n output (connect directly to top-level port)
    I  => div_5_out
 );

  --data_out <= probe0_FD;
--    data_out <= data_DOut;
  data_out <= probe0_FD when config_reg(16*18+15)='1' else data_DOut;
 
  ---------------------------------------------< FDOUT
  Parallel_SerialX_top_inst0: Parallel_SerialX_top
    GENERIC MAP (
      NDATA       => 20,
      FIFO_WIDTH  => 36,
      NUM_WIDTH   => 2 ,
      FRAME_WIDTH => 48
    )
    PORT MAP(
      clk_in      => clk_out_mc,
      clk_control => control_clk,
      rst         => reset,
      start_pulse => pulse_reg(10),
      fd_in       => data_out, 
      trigger     => valid_out,
      evt_trig    => trigger_in,
      fifo_rd_en  => fifo_rden2,
      fifo_empty  => fifo_empty2,
      fifo_q      => fifo_q2
  );

  ---------------------------------------------< DIV_5
  div_5_inst0 : div_5 
    PORT MAP (
      clkin      => clk_out_mc,
      rst        => reset,
      clkout     => div_5_out
  );
  ---------------------------------------------< DIV_5

   FMC_HPC_HA_N(19)<=div_5_out;
   FMC_HPC_HA_P(19)<=clk_out_mc;

   probe0_FD <= fd_out0 & fd_out1 & fd_out2 & fd_out3 & fd_out4 & fd_out5 & fd_out6 & fd_out7;
   ila2_probe1(0) <= config_reg(16*18+14); --- strobe option
   ila2_probe1(1) <= config_reg(16*18+13); --- strobe option
--    ila2_probe1(2) <= config_reg(16*18+12);
   ila2_probe1(2) <= FMC_HPC_LA_P(30); -- output strobe
   ila2_probe1(3) <= config_reg(6); --- strobe

--    ila2_probe1(0) <= fifo_empty1;
--    ila2_probe1(1) <= fifo_empty2;
--    ila2_probe1(2) <= FMC_HPC_HA_P(05);
--    ila2_probe1(3) <= pulse_reg(10);

   ila2_probe2(8) <= fifo_empty1;
   ila2_probe2(9) <= fifo_rden1;
   ila2_probe2(10) <= fifo_empty2;
   ila2_probe2(11) <= fifo_rden2;
   ila2_probe2(12) <= FMC_HPC_HA_N(19); --- input trigger pin
   ila2_probe2(13) <= trigger_in;
   ila2_probe2(14) <= strobe_i;
   ila2_probe2(15) <= strobe_i2;

   ila2_probe2(7 DOWNTO 0) <= data_out;
--    ila2_probe2(8) <= track_out_i; 
--    ila2_probe2(9) <= rxcommadet_i; 
--    ila2_probe2(10) <= rxisaligned_i; 
--    ila2_probe2(11) <= rxbyterealign_i;
--    ila2_probe2(12) <= div_5_out;
--    ila2_probe2(13) <= rxbyterealign_i;
--    ila2_probe2(14) <= rxbyterealign_i;
--    ila2_probe2(15) <= rxbyterealign_i;
   
   -- IBUFDS: Differential Input Buffer
   --         Kintex-7
   -- Xilinx HDL Language Template, version 2015.4
   FD0_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
--       IBUF_LOW_PWR => FALSE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
--       IOSTANDARD => "LVDS")
   port map (
      O => fd_out0,  -- Buffer output
      I =>  FMC_HPC_HA_P(18),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(18) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD1_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out1,  -- Buffer output
      I =>  FMC_HPC_HA_P(17),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(17) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD2_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out2,  -- Buffer output
      I =>  FMC_HPC_HA_P(14),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(14) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD3_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out3,  -- Buffer output
      I =>  FMC_HPC_HA_P(10),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(10) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD4_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out4,  -- Buffer output
      I =>  FMC_HPC_HA_P(03),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(03) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD5_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out5,  -- Buffer output
      I =>  FMC_HPC_HA_P(02),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(02) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD6_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out6,  -- Buffer output
      I =>  FMC_HPC_HA_P(07),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(07) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD7_inst : IBUFDS
   generic map (
      DIFF_TERM => TRUE, -- Differential Termination 
      IBUF_LOW_PWR => TRUE, -- Low power (TRUE) vs. performance (FALSE) setting for referenced I/O standards
      IOSTANDARD => "DEFAULT")
   port map (
      O => fd_out7,  -- Buffer output
      I =>  FMC_HPC_HA_P(06),  -- Diff_p buffer input (connect directly to top-level port)
      IB => FMC_HPC_HA_N(06) -- Diff_n buffer input (connect directly to top-level port)
   );
  ---------------------------------------------> FDOUT

  --- The convert module
--   ---------------------------------------------< PULSE_SYNCHRONISE
--   pulse_synchronise_10 : pulse_synchronise
--     PORT MAP (
--       pulse_in  => pulse_reg(10),
--       clk_in    => control_clk,
--       clk_out   => clk_out_mc,
--       rst       => reset,
--       pulse_out => pulse10_out
--     );
--   ---------------------------------------------> PULSE_SYNCHRONISE
 

-----------------------------------------< DOUT
   GTX10B8B_dec_inst1: GTX10B8B_dec
   port map (
	RESET                     => reset,
	Q2_CLK1_GTREFCLK_PAD_N_IN => GTREFCLK_N,
	Q2_CLK1_GTREFCLK_PAD_P_IN => GTREFCLK_P,
	SYSCLK_IN                 => sys_clk, 
	RXN_IN                    => SMA_MGT_RX_N,
	RXP_IN                    => SMA_MGT_RX_P,
	TXN_OUT                   => SMA_MGT_TX_N,
	TXP_OUT                   => SMA_MGT_TX_P,
	D_DATAOUT1                => data_DOut,
	rxcommadet                => rxcommadet_i,
	rxisaligned               => rxisaligned_i,
	rxbyterealign             => rxbyterealign_i,
	track_out                 => track_out_i
   );
   -----------------------------------------> DOUT
END Behavioral;
