# Utils

This folder contains a Python script to change the devices mode into boot. This script works for both Supernova and Pulsar.

## Prerequisites

- Python >= 3.8
- BinhoSupernova SDK == v4.0.0
- BinhoPulsar SDK == v1.0.0
- Supernova/Pulsar host adapter running `firmware version >= 4.0.0`

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the Supernova device, run: ``python enter_boot_mode.py --device supernova``
To use the Pulsar device, run: ``python enter_boot_mode.py --device pulsar``