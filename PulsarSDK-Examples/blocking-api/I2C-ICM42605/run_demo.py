import time
import matplotlib.pyplot as plt
from pulsar_blocking_api import PulsarBlockingApi
from IMU14CLICK import IMU14CLICK

def main():
    pulsar = PulsarBlockingApi()

    response = pulsar.open()

    if response["opcode"] != 0:
        print("Error opening Pulsar")
        exit(1)
    
    voltage_mV = 3300
    response = pulsar.set_i2c_spi_uart_gpio_voltage(voltage_mV=voltage_mV)
        
    if response['result'] != pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name:
        print("Error setting the I3C voltage")
        exit(1)

    i2c_bus = pulsar.i2c_definitions.I2cBus.I2C_BUS_A
    frequency = 1000000
    pullUpResistorsValue = pulsar.i2c_definitions.I2cPullUpResistorsValue.I2C_PULLUP_2_2kOhm
    response = pulsar.i2c_controller_init(busId=i2c_bus,
                                          frequency=frequency,
                                          pullUpResistorsValue=pullUpResistorsValue)

    if not response['result'] in [pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name, pulsar.i2c_definitions.CommonResultCodes.BUS_ALREADY_INITIALIZED.name]:
        print("Error initializing the I2C bus")
        exit(1)

    imu = IMU14CLICK(pulsar, i2c_bus)

    imu.init_device()

    imu.calibrate()

    # Setup the matplotlib figure and axes
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.subplots_adjust(hspace=0.5)
    fig.suptitle('Pulsar with Mikroe IMU 14 Click Demo', fontsize=16)
    plt.get_current_fig_manager().set_window_title("Sensor Data Visualization")

    # Initialize lists to store the data
    times = []
    acc_data = {'x': [], 'y': [], 'z': []}
    gyro_data = {'x': [], 'y': [], 'z': []}

    start_time = time.time()

    keep_running = True

    def on_key(event):
        nonlocal keep_running
        if event.key == 'q':
            keep_running = False

    fig.canvas.mpl_connect('key_press_event', on_key)

    while keep_running:
        current_time = time.time() - start_time
        times.append(current_time)

        # Read data from sensor
        (acc, gyro) = imu.read()

        # Update accelerometer data
        acc_data['x'].append(acc[0])
        acc_data['y'].append(acc[1])
        acc_data['z'].append(acc[2])

        # Update gyroscope data
        gyro_data['x'].append(gyro[0])
        gyro_data['y'].append(gyro[1])
        gyro_data['z'].append(gyro[2])

        # Plot accelerometer data
        ax1.cla()
        ax1.plot(times, acc_data['x'], label='X')
        ax1.plot(times, acc_data['y'], label='Y')
        ax1.plot(times, acc_data['z'], label='Z')
        ax1.legend()
        ax1.set_title('Accelerometer Data')
        ax1.set_ylabel('Acceleration (g)')

        # Plot gyroscope data
        ax2.cla()
        ax2.plot(times, gyro_data['x'], label='X')
        ax2.plot(times, gyro_data['y'], label='Y')
        ax2.plot(times, gyro_data['z'], label='Z')
        ax2.legend()
        ax2.set_title('Gyroscope Data')
        ax2.set_ylabel('Angular Velocity (dps)')

        plt.pause(0.1)

        # Limit the size of the data lists
        if len(times) > 50:
            times.pop(0)
            for data_list in acc_data.values():
                data_list.pop(0)
            for data_list in gyro_data.values():
                data_list.pop(0)

    plt.close(fig)

    pulsar.close()

if __name__ == "__main__":
    main()