# Notes

## Hardware

### IC List

- BCM53346A0KFSBG
  - Broadcom
  - 24+4 port GbE switch SoC
  - [Product page](https://www.broadcom.com/products/ethernet-connectivity/switching/strataconnect/bcm5334x)
- NT5CC128M16IP-DI
  - Nanya
  - 256 MB DDR3L 1600 MHz DRAM
  - [Datasheet](http://static6.arrow.com/aropdfconversion/4870b2314d92e311d08df94e91cdbd8b3609b896/357986404255011135798553711652932gb_ddr3_i_die_component_datasheet.pdf.pdf)
- MX25L25635FMI-10G
  - Macronix
  - 32 MB SOIC-16 SPI flash
  - [Datasheet](https://datasheet.octopart.com/MX25L25635FMI-10G-Macronix-datasheet-17291205.pdf)
- LCMXO256C4TN100C
  - Lattice Semi
  - 256-LUT MachXO CPLD
  - [Datasheet](https://www.mouser.com/datasheet/2/225/DS1002-1489634.pdf)
- B50282C1KFBG
  - Broadcom
  - 8-port GbE PHY

### Connectors

- UART
  - 115200, 8N1, 3V3.
  - TX is on pin 11 of U11.
  - RX is on the pads of R123 and R124 that are adjacent to each other.
  - U11 is an unpopulated MAX232 that converts from the 3V3 logic levels
    to RS232, which is exposed on an unpopulated ethernet connector
    (console connector).
  - The TX and RX pins of the console connector can be swapped by moving
    the inductors between L14/L15 and L16/L17.
    - L14/L15 set the RX pin, and L16/L17 set the TX pin.
    - L14 and L17 are connected to one console pin, and L15 and L16 are
      connected to the other console pin.

## Software

- Bootloader
  - U-Boot 2012.10
    - Modified by Broadcom.
    - Sources unavailable (for now).
- OS
  - Linux 3.6.5
    - Modified by Broadcom.
    - Majority of sources are available.
      - Certain proprietary Broadcom kernel modules are excluded.
        - `linux-kernel-bde.ko`
        - `linux-user-bde.ko`
  - Sources downloadable from TRENDnet.
    - [gpl\_teg-30284\_v1(1.00.010).tar.gz](http://downloads.trendnet.com/gpl/gpl_teg-30284_v1(1.00.010).tar.gz).
    - sha1sum: `BFA4665258023543878630FEE6768FD301606A4D  gpl_teg-30284_v1(1.00.010).tar.gz`
  - Firmware upgrade image also available.
    - [fw\_teg-30284\_v1(1.00.024).zip](http://downloads.trendnet.com/teg-30284/firmware/fw_teg-30284_v1(1.00.024).zip)
    - sha1sum: `F32537ACB4211520CADED2F34A6C4AF00FF642A4  fw_teg-30284_v1(1.00.024).zip`
