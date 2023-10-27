from BinhoSupernova.commands.definitions import *
from supernova_controller import SupernovaController


class I2cExample(SupernovaController):
    def __init__(self):
        super().__init__()

    def set_parameters(self):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.setI2cSpiUartBusVoltage(transfer_id, 3300),
            lambda transfer_id: self.supernova.i2cSetParameters(transfer_id, baudrate=1000000),
        ])

        return responses

    def write(self, address, register, data):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.i2cWrite(transfer_id, address, register, data),
        ])

        return responses

    def write_non_stop(self, address, register, data):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.i2cWriteNonStop(transfer_id, address, register, data),
        ])

        return responses

    def read(self, address, length):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.i2cRead(transfer_id, address, length),
        ])

        return responses

    def read_from(self, address, register, length):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.i2cReadFrom(transfer_id, address, register, length),
        ])

        return responses

def main():
    example = I2cExample()
    example.init()
    result = example.set_parameters()
    print(result)
    result = example.write(0x50, [0,0], [33 for i in range(1,129)])
    print(result)
    result = example.write_non_stop(0x50, [0,0], [55 for i in range(1,129)])
    print(result)
    result = example.read(0x50, 70)
    print(result)
    result = example.read_from(0x50, [0,0], 70)
    print(result)
    example.done()


if __name__ == "__main__":
    main()
