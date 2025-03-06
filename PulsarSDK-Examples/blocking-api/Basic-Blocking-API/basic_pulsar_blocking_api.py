import threading
import re
from BinhoPulsar.Pulsar import Pulsar
from BinhoPulsar.commands.system.definitions import *

# ==================================================================================
# region Blocking API
# ==================================================================================

MIN_TRANSFER_ID = 1
MAX_TRANSFER_ID = 65535

class PulsarBlockingApi:

    def __init__(self):
        self.transfer_id = 0

        self.pulsar = Pulsar()
        self.pulsar.onEvent(self.__on_receive_callback)

        self.response_event = threading.Event()
        self.notification_event = threading.Event()
        self.response = dict()
        self.notification = dict()

        self.__set_common_methods()
        self.__decorate_methods()

    def __set_common_methods(self):
        """
        This private methods set the methods that do not return a response from the host adapter.
        For this reason, they are not decorated with the sequential decorator.
        """
        self.open = self.pulsar.open
        self.close = self.pulsar.close
        self.reset_device = self.pulsar.resetDevice
        self.enter_boot_mode = self.pulsar.enterBootMode

    def __decorate_methods(self):
        # Apply sequential decorator dynamically for all methods of the SDK instance except the one listed below.
        exclude_methods = ["open", "close", "resetDevice", "enterBootMode", "onEvent"]

        for method_name in dir(self.pulsar):
            if not method_name.startswith("_") and not method_name in exclude_methods and callable(getattr(self.pulsar, method_name)):
                method = getattr(self.pulsar, method_name)
                setattr(self, self.__camel_to_snake(method_name), self.__sequential_call(method))

    def __on_receive_callback(self, dut_message = None, system_message = None):
        if dut_message is not None:
            if dut_message.get("id") == 0:
                self.notification = dut_message
                self.notification_event.set()
            else:
                self.response = dut_message
                self.response_event.set()

    def __sequential_call(self, method):
        def wrapper(*args, **kwargs):
            id = self.__get_new_transfer_id()
            self.response_event.clear()
            response = method(id=id, *args, **kwargs)

            # Block until response is received only when the request was successfully sent to the DUT.
            if response["opcode"] == 0:
                # Check if the response is already received.
                if self.response_event.is_set() == True:
                    return self.response
                else:
                    is_set = self.response_event.wait(timeout=5.0)
                    if is_set == True:
                        return self.response
                    else:
                        return None

            # Otherwise, return the response immediately.
            return response

        return wrapper

    def __get_new_transfer_id(self):
        self.transfer_id += MIN_TRANSFER_ID

        if self.transfer_id == MAX_TRANSFER_ID:
            self.transfer_id = MIN_TRANSFER_ID

        return self.transfer_id

    def __camel_to_snake(self, name):
        return re.sub(r'(?<!^)(?<![A-Z])([A-Z])', r'_\1', name).lower()

    def wait_for_notification(self, timeout = None):
        self.notification_event.clear()
        self.notification_event.wait(timeout=timeout)
        return self.notification

# endregion

# ==================================================================================
# region Main code
# ==================================================================================

pulsar_device = PulsarBlockingApi()

# Open the device.
pulsar_device.open()

# Get device manufacturer.
response = pulsar_device.get_usb_string(subCommand=GetUsbStringSubCommand.MANUFACTURER)

if response["result"] == CommonResultCodes.SUCCESS.name:
    print(f"Manufacturer: {response['payload']}")
else:
    print(f"Error {response['result']}")

# Get product name.
response = pulsar_device.get_usb_string(subCommand=GetUsbStringSubCommand.PRODUCT_NAME)

if response["result"] == CommonResultCodes.SUCCESS.name:
    print(f"Product name: {response['payload']}")
else:
    print(f"Error {response['result']}")

# Get firmware version
response = pulsar_device.get_usb_string(subCommand=GetUsbStringSubCommand.FW_VERSION)

if response["result"] == CommonResultCodes.SUCCESS.name:
    print(f"Firmware version: {response['payload']}")
else:
    print(f"Error {response['result']}")

# Get hardware version
response = pulsar_device.get_usb_string(subCommand=GetUsbStringSubCommand.HW_VERSION)

if response["result"] == CommonResultCodes.SUCCESS.name:
    print(f"Hardware version: {response['payload']}")
else:
    print(f"Error {response['result']}")

# Get Serial Number
response = pulsar_device.get_usb_string(subCommand=GetUsbStringSubCommand.SERIAL_NUMBER)

if response["result"] == CommonResultCodes.SUCCESS.name:
    print(f"Serial number: {response['payload']}")
else:
    print(f"Error {response['result']}")

# Close the device.
pulsar_device.close()

# endregion