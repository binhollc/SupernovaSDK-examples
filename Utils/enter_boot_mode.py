# Import Python package
import argparse
from BinhoSupernova.Supernova import Supernova
from BinhoPulsar.Pulsar import Pulsar

# Define the on-event callback function.
def callback(response, sys_message):
    if response:
        print(response)
    if sys_message:
        print(sys_message)


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
dut_device.onEvent(callback_func=callback)

# Request to enter in boot mode
dut_device.enterBootMode(1)