# Demo of Supernova I3C Controller API

This folder contains two different notebooks to show how to use the Supernova SDK API to set and control the Supernova device as an I3C Controller. There are 2 notebooks:

- [I3C-Protocol-Supernova-API.ipynb](I3C-Protocol-Supernova-API.ipynb) shows a general use case of the Supernova SDK API
- [I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb](I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb) shows how the Supernova SDK handles the In-Band Interrupt notification based on the TDK ICM42605 sensor.

## Prerequisites

- Python 3.10
- Supernova host adapter running `firmware version >= 2.4.0`
- To run [I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb](I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb), an ICM42605 or ICM42688 sensor is required since the notebook modifies target-specific registers to configure the In-Band Interrupt feature. The [I3C-Protocol-Supernova-API](I3C-Protocol-Supernova-API.ipynb) notebook is also intended to be used with the ICM42605 sensor, but it shows general I3C transfer, so it can be modified to use other targets very quickly.

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the [I3C-Protocol-Supernova-API.ipynb](I3C-Protocol-Supernova-API.ipynb) and [I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb](I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb) notebooks in each case.