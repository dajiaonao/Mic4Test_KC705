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

ENTITY top_test IS
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
END top_test;

ARCHITECTURE Behavioral OF top_test IS
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

  SIGNAL mem_out     : std_logic_vector(31 DOWNTO 0);
    
  
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
  ---------------------------------------------> UART/RS232
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

    -- receive to cmd_fifo
    gig_eth_tcp_use_fifo         <= '1';
    gig_eth_rx_fifo_rdclk        <= control_clk;
    cmd_fifo_q(31 DOWNTO 0)      <= gig_eth_rx_fifo_q;
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

  --------------------------------------------> Test signals
   FMC_HPC_LA_P(05)<= control_clk; -- SYNC
   FMC_HPC_LA_P(09)<= control_clk; -- SCLK
   FMC_HPC_LA_P(13)<= control_clk; -- SDATA

   FMC_HPC_LA_P(21)<= control_clk; -- APLUSE
   FMC_HPC_LA_P(24)<= control_clk; -- DPLUSE
   FMC_HPC_LA_P(22)<= control_clk; -- CON_SCLK
   FMC_HPC_LA_P(25)<= control_clk; -- CON_SDIN
   FMC_HPC_LA_P(28)<= control_clk; -- GRST_B
   FMC_HPC_LA_P(20)<= control_clk; -- REG_SCK
   FMC_HPC_LA_P(30)<= control_clk; -- STROBE_B
   FMC_HPC_LA_P(31)<= control_clk; -- REG_LOAD
   FMC_HPC_LA_P(32)<= control_clk; -- RESET
   FMC_HPC_LA_P(33)<= control_clk; -- REG_SDI

   FMC_HPC_LA_P(06)<= control_clk; -- REG_SDI
   FMC_HPC_LA_P(10)<= control_clk; -- REG_SDI
   FMC_HPC_LA_P(03)<= control_clk; -- REG_SDI
   FMC_HPC_LA_P(08)<= control_clk; -- REG_SDI

   FMC_HPC_HA_P(05)<= control_clk; -- valid_out
   FMC_HPC_HA_P(09)<= control_clk; -- REG_SDO
   FMC_HPC_HA_P(21)<= control_clk; -- TS_OUT
   FMC_HPC_HA_P(23)<= control_clk; -- BUSY

   ---- FD ports
   FD0_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(18),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(18) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD1_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(17),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(17) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD2_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(14),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(14) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD3_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(10),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(10) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD4_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(03),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(03) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD5_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(02),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(02) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD6_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(07),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(07) -- Diff_n buffer input (connect directly to top-level port)
   );

   FD7_inst : OBUFDS
   generic map (
      IOSTANDARD => "LVDS")
   port map (
      I => control_clk,
      O =>  FMC_HPC_HA_P(06),  -- Diff_p buffer input (connect directly to top-level port)
      OB => FMC_HPC_HA_N(06) -- Diff_n buffer input (connect directly to top-level port)
   );
  --------------------------------------------> Test signals

END Behavioral;
