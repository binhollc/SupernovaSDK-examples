from BinhoSupernova.commands.definitions import *
from supernova_controller import SupernovaController


class ConnectionExample(SupernovaController):
    def __init__(self):
        super().__init__()

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



def main():
    example = ConnectionExample()
    example.init()
    result = example.run()
    print(result)
    example.done()


if __name__ == "__main__":
    main()
