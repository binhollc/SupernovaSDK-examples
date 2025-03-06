import ctypes
from IMU14CLICK_definitions import *

class IMU14CLICK:
    address = 0x68

    # Sensor resolutions
    a_scale = IMU14CLICK_ACCEL_FS.FS_2g.value # 2g full scale
    g_scale = IMU14CLICK_GYRO_FS.FS_250dps.value # 250 dps full scale
    a_res = IMU14CLICK_ACCEL_FS_VALUES[a_scale] / IMU14CLICK_ACCEL_RESOLUTION # 2 g full scale
    g_res = IMU14CLICK_GYRO_FS_VALUES[g_scale] / IMU14CLICK_GYRO_RESOLUTION # 250 dps full scale
    a_odr = IMU14CLICK_ACCEL_ODR.ODR_1kHz.value #AODR_1000Hz
    g_odr = IMU14CLICK_GYRO_ODR.ODR_1kHz.value #GODR_1000Hz

    # Calibration
    accel_bias = None
    gyro_bias = None

    def __init__(self, pulsar_blocking_api, i2c_bus):
        self.pulsar = pulsar_blocking_api
        self.i2c_bus = i2c_bus
        
        self.__check_device_connection()
        print("Device found")

    def __check_device_connection(self):
        response = self.pulsar.i2c_controller_read(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        requestDataLength=WHO_AM_I_length,
                                        registerAddress=[WHO_AM_I_register])
        if response['result'] != self.pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name or response['payload'][0] != WHO_AM_I_value:
            print("Error: Device not found")
            exit(1)
    
    def init_device(self):
        # Enable gyro and accel in low noise mode
        power_management_register = self.pulsar.i2c_controller_read(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        requestDataLength=PWR_MGMT0_length,
                                        registerAddress=[PWR_MGMT0_register]).get('payload', [])

        response = self.pulsar.i2c_controller_write(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        registerAddress=[PWR_MGMT0_register],
                                        data=[power_management_register[0] | IMU14CLICK_ACCEL_MODE.LOW_NOISE.value | IMU14CLICK_GYRO_MODE.LOW_NOISE.value])
        
        if response['result'] != self.pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name:
            print("Error: Could not initialize the device")
            exit(1)

        # Gyro full scale and data rate
        gyro_config_register0 = self.pulsar.i2c_controller_read(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        requestDataLength=GYRO_CONFIG0_length,
                                        registerAddress=[GYRO_CONFIG0_register]).get('payload', [])
        
        response = self.pulsar.i2c_controller_write(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        registerAddress=[GYRO_CONFIG0_register],
                                        data=[gyro_config_register0[0] | self.g_scale | self.g_odr])
        
        if response['result'] != self.pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name:
            print("Error: Could not initialize the device")
            exit(1)

        # Set accel full scale and data rate
        accel_config_register0 = self.pulsar.i2c_controller_read(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        requestDataLength=ACCEL_CONFIG0_length,
                                        registerAddress=[ACCEL_CONFIG0_register]).get('payload', [])
        
        response = self.pulsar.i2c_controller_write(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        registerAddress=[ACCEL_CONFIG0_register],
                                        data=[accel_config_register0[0] | self.a_scale | self.a_odr])
        
        if response['result'] != self.pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name:
            print("Error: Could not initialize the device")
            exit(1)

        # Set temperature sensor low pass filter to 5Hz, use first order gyro filter
        gyro_config_register1 = self.pulsar.i2c_controller_read(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        requestDataLength=GYRO_CONFIG1_length,
                                        registerAddress=[GYRO_CONFIG1_register]).get('payload', [])
        
        response = self.pulsar.i2c_controller_write(busId=self.i2c_bus,
                                        targetAddress=self.address,
                                        registerAddress=[GYRO_CONFIG1_register],
                                        data=[gyro_config_register1[0] | TEMP_FILT_BW_5Hz])
        
        if response['result'] != self.pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name:
            print("Error: Could not initialize the device")
            exit(1)

    def _read_data(self):
        response = self.pulsar.i2c_controller_read(busId=self.i2c_bus,
                                                   targetAddress=self.address,
                                                   requestDataLength=READ_LENGTH,
                                                   registerAddress=[TEMP_DATA1_register])
        
        if response['result'] != self.pulsar.i2c_definitions.CommonResultCodes.SUCCESS.name:
            print("Error: Could not read data: ", response['result'])
            exit(1)
        
        raw_data = response['payload']

        # Convert data to signed 16-bit integers
        imu_data = [0,0,0,0,0,0,0]
        for i in range(len(imu_data)):
            imu_data[i] = ctypes.c_int16((raw_data[2*i] << 8) | raw_data[2*i + 1]).value
        
        return imu_data
    
    def calibrate(self):
        print("Calibrating...")
        sum_values = [0, 0, 0, 0, 0, 0, 0]
        accel_bias = [0, 0, 0]
        gyro_bias = [0, 0, 0]

        for i in range(128):
            # Read data
            imu_data = self._read_data()
            for j in range(len(imu_data)):          
                sum_values[j] += imu_data[j]

        accel_bias[0] = sum_values[1] * self.a_res / 128.0
        accel_bias[1] = sum_values[2] * self.a_res / 128.0
        accel_bias[2] = sum_values[3] * self.a_res / 128.0
        gyro_bias[0] = sum_values[4] * self.g_res / 128.0
        gyro_bias[1] = sum_values[5] * self.g_res / 128.0
        gyro_bias[2] = sum_values[6] * self.g_res / 128.0

        if accel_bias[0] > 0.8:
            accel_bias[0] -= 1.0  # Remove gravity from the x-axis accelerometer bias calculation
        if accel_bias[0] < -0.8:
            accel_bias[0] += 1.0  # Remove gravity from the x-axis accelerometer bias calculation
        if accel_bias[1] > 0.8:
            accel_bias[1] -= 1.0  # Remove gravity from the y-axis accelerometer bias calculation
        if accel_bias[1] < -0.8:
            accel_bias[1] += 1.0  # Remove gravity from the y-axis accelerometer bias calculation
        if accel_bias[2] > 0.8:
            accel_bias[2] -= 1.0  # Remove gravity from the z-axis accelerometer bias calculation
        if accel_bias[2] < -0.8:
            accel_bias[2] += 1.0  # Remove gravity from the z-axis accelerometer bias calculation 

        self.accel_bias = accel_bias
        self.gyro_bias = gyro_bias

        print("Calibration done")
    
    def read(self):
        imu_data = self._read_data()

        ax = imu_data[1]*self.a_res - self.accel_bias[0]
        ay = imu_data[2]*self.a_res - self.accel_bias[1]
        az = imu_data[3]*self.a_res - self.accel_bias[2]

        gx = imu_data[4]*self.g_res - self.gyro_bias[0]
        gy = imu_data[5]*self.g_res - self.gyro_bias[1]
        gz = imu_data[6]*self.g_res - self.gyro_bias[2]

        return ((ax, ay, az), (gx, gy, gz))