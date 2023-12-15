import time
from BinhoSupernova.commands.definitions import *
from supernova_controller import SupernovaController

class I2cBenchmark(SupernovaController):
    def __init__(self):
        super().__init__()

    def set_parameters(self):
        responses = self.invoke_sync([
            lambda transfer_id: self.supernova.setI2cSpiUartBusVoltage(transfer_id, 3300),
            lambda transfer_id: self.supernova.i2cSetParameters(transfer_id, baudrate=1000000),
        ])
        return responses

    def write_read_cycle(self, address, register, write_data, read_length):
        start_time = time.time()

        self.invoke_sync([
            lambda transfer_id: self.supernova.i2cWrite(transfer_id, address, register, write_data),
            lambda transfer_id: self.supernova.i2cReadFrom(transfer_id, address, register, read_length),
        ])

        end_time = time.time()
        return end_time - start_time

def main():
    benchmark = I2cBenchmark()
    benchmark.init()
    benchmark.set_parameters()

    total_time = 0.0
    iterations = 100
    address = 0x50
    register = [0, 0]
    write_data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    read_length = 10

    for _ in range(iterations):
        round_trip_time = benchmark.write_read_cycle(address, register, write_data, read_length)
        total_time += round_trip_time

    average_time = total_time / iterations
    print(f"Average round-trip time: {average_time * 1000:.6f} ms")

    benchmark.done()

if __name__ == "__main__":
    main()
