This folder contains various Jupyter Notebooks with hands-on demonstrations and tutorials for working with the Supernova SDK, including:

- **GPIO-API**: Tutorial on how to use Supernova API to control the 6x GPIOs as digital inputs/outputs.
- **I2C-Protocol-API:** Tutorial on how to use Supernova API to perform I2C protocol transactions.
- **I3C-Protocol-API:** Tutorials on how to use Supernova API to perform I3C protocol transactions in both I3C Controller and I3C Target mode.
    - **I3C-Protocol-Controller-API:** Tutorial on how to use Supernova API to perform I3C protocol transactions and handle In-Band Interrupts in I3C Controller mode.
      - **I3C-Protocol-Controller-API-Basic:** Contains examples demonstrating basic use of the Supernova API to operate as an I3C Controller. This includes SDR (Single Data Rate) transfers, showcases different Dynamic Address Assignment (DAA) methods, and provides usage of the HDR-DDR (High Data Rate - Double Data Rate) API, along with other fundamental example of the I3C Controller interacting with a sensor and receiving In-Band Interrupts.
      - **PIC18QF16Q20-I3C-to-SPI-I2C-translator:** Tutorial on the PIC18QF16Q20 protocol translator example with Supernova API to control the Supernova as the I3C Controller. This tutorial shows how the Supernova SDK handles Hot-Join and In-Band Interrupts.
    - **I3C-Protocol-Target-API:** Tutorial on how to use Supernova API to control the Supernova devices in I3C Target mode.
- **SPI-Protocol-API:** Tutorial on how to use Supernova API to perform SPI protocol transactions.
- **SYS-API:** Tutorial on how to use Supernova API to perform set system configurations.
- **UART-Protocol-API:** Tutorial on how to use Supernova API to perform UART protocol transactions.