import threading
import re
from binhopulsar.pulsar import Pulsar

# ==================================================================================
# Blocking API
# ==================================================================================

MIN_TRANSFER_ID = 1
MAX_TRANSFER_ID = 65535

class PulsarBlockingApi:

    def __init__(self):
        self.transfer_id = 0

        self.pulsar = Pulsar()
        self.pulsar.onEvent(self.__on_receive_callback)
        self.i2c_definitions = __import__("BinhoPulsar.commands.i2c.definitions", fromlist=[""])

        self.response_event = threading.Event()
        self.response = dict()

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
        if dut_message is not None and dut_message.get("id") != 0:
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