from transfer_controller import TransferController
from BinhoSupernova.Supernova import Supernova
from BinhoSupernova.commands.definitions import *
import queue
import threading


def id_gen():
    i = 0
    while True:
        i += 1
        yield i


class ConnectionExample:
    def __init__(self):
        self.controller = TransferController(id_gen())

    def init(self):
        self.response_queue = queue.SimpleQueue()

        self.process_response_thread = threading.Thread(target=self._pull_sdk_response, daemon=True)
        self.running = True
        self.process_response_thread.start()

        self.supernova = Supernova()
        self.supernova.open()
        self.supernova.onEvent(self._push_sdk_response)

    def _push_sdk_response(self, supernova_response, system_message):
        self.response_queue.put((supernova_response, system_message))

    def _pull_sdk_response(self):
        while self.running:
            try:
                supernova_response, system_message = self.response_queue.get(timeout=1)
                self._process_sdk_response(supernova_response, system_message)
            except queue.Empty:
                continue

    def _process_sdk_response(self, supernova_response, system_message):
        if supernova_response == None:
            return

        is_handled = self.controller.handle_response(
            transfer_id=supernova_response['id'], response=supernova_response)

        if is_handled:
            return

        # Process non-sequenced responses
        # ...

    def invoke_sync(self, sequence):
        result = None

        def collect_responses(responses):
            nonlocal result
            result = responses

        sequence_id = self.controller.submit(
            sequence=sequence,
            on_ready=collect_responses
        )

        self.controller.wait_for(sequence_id)

        return result

    def run(self):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.getUsbString(id=transfer_id, subCommand=GetUsbStringSubCommand.MANUFACTURER),
            lambda transfer_id: self.supernova.getUsbString(id=transfer_id, subCommand=GetUsbStringSubCommand.FW_VERSION),
            lambda transfer_id: self.supernova.getUsbString(id=transfer_id, subCommand=GetUsbStringSubCommand.HW_VERSION),
            lambda transfer_id: self.supernova.getUsbString(id=transfer_id, subCommand=GetUsbStringSubCommand.SERIAL_NUMBER),
            lambda transfer_id: self.supernova.getUsbString(id=transfer_id, subCommand=GetUsbStringSubCommand.PRODUCT_NAME),
        ])

        return {
            'manufacturer': responses[0]['message'],
            'fw_version': responses[1]['message'],
            'hw_version': responses[2]['message'],
            'serial_number': responses[3]['message'],
            'product_name': responses[4]['message'],
        }

    def done(self):
        self.supernova.close()
        self.running = False


def main():
    example = ConnectionExample()
    example.init()
    result = example.run()
    print(result)
    example.done()


if __name__ == "__main__":
    main()
