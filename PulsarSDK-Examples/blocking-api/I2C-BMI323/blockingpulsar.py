from __future__ import annotations

import threading
from functools import wraps
from typing import Any, Callable, Dict, Iterable, Type

from binhopulsar.pulsar import Pulsar
from binhopulsar.commands.system.definitions import *
from binhopulsar.commands.i2c.definitions import *
from binhopulsar.commands.spi.definitions import *
from binhopulsar.commands.uart.definitions import *
from binhopulsar.commands.gpio.definitions import *

# -------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------

TIMEOUT_SECONDS = 1.0

# -------------------------------------------------------------------------------
# Metaclass
# -------------------------------------------------------------------------------

class BlockingApiMeta(type):

    # --- Wrapper factory -------------------------------------------------------

    @classmethod
    def blocking_wrapper(mcls, method: Callable[..., Dict[str, Any]]) -> Callable[..., Dict[str, Any]]:
        """
        Turn an SDK method into a blocking call:
          - Enforces keyword-only arguments (prevents accidental positional use).
          - Auto-injects a unique transfer id.
          - Waits for a response event when opcode==0.
        """
        @wraps(method)  # Keep original method name/doc on the *overridden* CamelCase name
        def wrapper(instance, *args, **kwargs):
            if args:
                raise TypeError(f"Method '{method.__name__}' must be called with keyword arguments only.")
            
            kwargs.pop('id', None)  # The SDK manages 'id' internally here; ignore any caller-supplied one

            tx_id = instance.get_new_transfer_id()
            instance.response_event.clear()

            response = method(instance, id=tx_id, **kwargs) # Call original method with new id
            
            # Check that the request was successfully sent to the DUT.
            if response.get("opcode") == 0:
                # Check if the response is already received. It might occur a race condition.
                if instance.response_event.is_set():
                    return instance.response 
                else:
                    is_set = instance.response_event.wait(timeout=getattr(instance, "TIMEOUT_SECONDS", TIMEOUT_SECONDS))
                    if is_set:
                        return instance.response
                    return {"result": "TIMEOUT", "payload": "Device did not respond in time."}
            
            # Otherwise, return the response immediately which contains the error message.
            return response
        
        return wrapper
    
    # --- Class construction hook ----------------------------------------------

    def __new__(
        mcls: Type[type],
        name: str,
        bases: Iterable[type],
        attrs: Dict[str, Any]
    ):
        exclude = ["open", "close", "resetDevice", "enterBootMode", "onEvent"]
        attrs.setdefault("TIMEOUT_SECONDS", TIMEOUT_SECONDS)

        for base in bases:
            if base.__name__ == "Pulsar":
                for attr_name in dir(base):
                    if attr_name.startswith("_") or attr_name in exclude:
                        continue
                    original = getattr(base, attr_name)
                    if not callable(original):
                        continue

                    # Override mixedCase method with a blocking wrapper
                    blocked = mcls.blocking_wrapper(original)
                    attrs[attr_name] = blocked

        return super().__new__(mcls, name, bases, attrs)

# -------------------------------------------------------------------------------
# Blocking subclass
# -------------------------------------------------------------------------------

class BlockingPulsar(Pulsar, metaclass=BlockingApiMeta):
    
    MIN_TRANSFER_ID: int = 1
    MAX_TRANSFER_ID: int = 65535
    
    def __init__(self):
        super().__init__()
        self.transfer_id = 0
        self.response_event = threading.Event()
        self.notification_event = threading.Event()
        self.response: Dict[str, Any] = {}
        self.notification_handlers: Dict[str, Callable] = {}
        self.notification_list = ["SYSTEM EVENT"]
        
        # Register callback to capture device/system messages
        self.onEvent(self.__on_receive_callback)

    def __on_receive_callback(self, dut_message: Dict[str, Any] | None = None,
                              system_message: Dict[str, Any] | None = None) -> None:
        """
        Called by the SDK when a message arrives.
        - id == 0    : notification
        - id != 0    : response to a specific transfer
        """
        if dut_message:
            if dut_message.get("id") == 0:
                print(dut_message)
                
                if dut_message.get("command") in self.notification_handlers.keys():
                    self.notification_handlers[dut_message.get("command")](dut_message) # Invoke the handler
                self.notification_event.set()
            else:
                self.response = dut_message
                self.response_event.set()

        # If needed, handle system_message here.

    def get_new_transfer_id(self) -> int:
        """
        Generate the next transfer id (1..65534), skipping 0 (reserved for notifications).
        """
        self.transfer_id += 1
        if self.transfer_id >= self.MAX_TRANSFER_ID:
            self.transfer_id = self.MIN_TRANSFER_ID
        return self.transfer_id

    def get_available_notifications(self) -> list:
        """Return a list of available notification types."""
        return self.notification_list
    
    def on_notification(self, name, handler_func) -> None:
        """Register a handler function for a specific notification type."""
        if name not in self.notification_list:
            raise ValueError(f"Notification '{name}' is not recognized. Available: {self.notification_list}")
        self.notification_handlers[name] = handler_func
    
    def clear_notification_handlers(self) -> None:
        """Clear all registered notification handlers."""
        self.notification_handlers.clear()

    def wait_for_notification(self, timeout: float | None = None) -> Dict[str, Any]:
        """Block until a notification (id==0) arrives or the timeout elapses."""
        self.notification_event.clear()
        return self.notification_event.wait(timeout=timeout)
