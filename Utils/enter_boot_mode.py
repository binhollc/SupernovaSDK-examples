# Import Python package
import argparse
from binhosupernova.supernova import Supernova
from binhopulsar.pulsar import Pulsar

# Parse command-line arguments to determine the device type.
parser = argparse.ArgumentParser(description="Select device type.")
parser.add_argument("--device", type=str, required=True, choices=["supernova", "pulsar"],
                    help="Select the DUT device.")
args = parser.parse_args()

# Connect to the DUT device based on the selected type.
if args.device == "supernova":
    dut_device = Supernova()
elif args.device == "pulsar":
    dut_device = Pulsar()

# Open the connection to the DUT device.
dut_device.open()

# Request to enter in boot mode
dut_device.enterBootMode(1)