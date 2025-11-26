import sys
import os
import time
import math
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from BMI323_definitions import *
from ctypes import *

# The read method needs to read two dummy bytes before the actual data
# as specified in the BMI323 datasheet
OFFSET_FOR_DUMMY_BYTES = 2

def find_i2c_matching_item(data, target_i2c_address):
    for item in data['detected_7_bit_addresses']:
        if item == target_i2c_address:
            return item
    return None

class BMI323:
    i2c_addr = 0x69
    address = None

    # Sensor configuration
    accel_mode = BMI323_ACCEL_OP_MODES.HIGH_PERFORMANCE.value
    accel_avg_num = BMI323_ACCEL_AVG_NUM.NO_AVG.value
    accel_filter_bw = BMI323_ACCEL_FILTER_BW.ODR_4.value
    accel_fs = BMI323_ACCEL_FS.FS_2g.value
    accel_odr = BMI323_ACCEL_ODR.AODR_100Hz.value
    
    gyro_mode = BMI323_GYRO_OP_MODES.HIGH_PERFORMANCE.value
    gyro_avg_num = BMI323_GYRO_AVG_NUM.NO_AVG.value
    gyro_filter_bw = BMI323_GYRO_FILTER_BW.ODR_4.value
    gyro_fs = BMI323_GYRO_FS.FS_250dps.value
    gyro_odr = BMI323_GYRO_ODR.GODR_100Hz.value

    watermark_level = 1
    activity_detection_factor = 4
    activity_detection_thres = 2
    env_coef_down = 0xD939
    env_coef_up = 0xF1CC
    env_min_dist_down = 0x85
    env_min_dist_up = 0x131
    filter_cascade_enabled = 1
    mcr_threshold = 5
    mean_crossing_pp_enabled = 0
    mean_step_dur = 0xFD54
    mean_val_decay = 0xEAC8
    peak_duration_min_running = 0x0C
    peak_duration_min_walking = 0x0C
    reset_counter = 0
    step_buffer_size = 5
    step_counter_increment = 0x100
    step_duration_max = 0x40
    step_duration_pp_enabled = 0 # 1
    step_duration_thres = 0 # 1
    step_duration_window = 0 # 0x0A

    use_feature_step_counter = False

    # Calibration
    accel_bias = None
    gyro_bias = None

    def __init__(self, controller, bus_id):
        self.controller = controller
        self.bus_id = bus_id

        result = controller.i2cControllerScanBus(busId=self.bus_id)
        bmi_device_addr = find_i2c_matching_item(result, self.i2c_addr)

        if bmi_device_addr is None:
            print("BMI device not found in the I2C bus")
            return
        
        self.address = bmi_device_addr

    def __calculate_resolutions(self):
        '''
        Calculate the resolutions of the sensor based on the current configuration.
        Use the respective full scale values and the number of bits (16) to calculate the resolutions.
        '''
        a_res = BMI323_ACCEL_FS_VALUES[self.accel_fs] / BMI323_ACCEL_RESOLUTION
        g_res = BMI323_GYRO_FS_VALUES[self.gyro_fs] / BMI323_GYRO_RESOLUTION
        return (a_res, g_res)

    def __read_data(self):
        '''
        Read the data from the sensor. The data is read in a single transaction starting from the
        accelerometer data X register. The data is then converted to signed 16-bit integers.
        '''
        # The three components of the accelerometer and gyroscope are 2-bytes length each
        READ_LEN = 12

        # Read data
        imu_data = self.get_register(BMI323_ACCEL_DATA_X, READ_LEN)

        return imu_data
    
    
    def init_device(self):
        '''
        Initialize the sensor with the current configuration.
        '''
        # Soft reset the sensor and enable the feature engine to activate the advanced features (i.g, step counter)
        self.soft_reset()

        # Set accelerometer configuration
        BMI323_ACCEL_CONFIG_LB = self.accel_filter_bw | self.accel_fs | self.accel_odr
        BMI323_ACCEL_CONFIG_HB = self.accel_mode | self.accel_avg_num
        BMI323_ACCEL_CONFIG = [BMI323_ACCEL_CONFIG_LB, BMI323_ACCEL_CONFIG_HB]
        self.controller.i2cControllerWrite(targetAddress=self.address, busId=self.bus_id, registerAddress=[BMI323_ACCEL_CONFIG_REG], data=BMI323_ACCEL_CONFIG)
        
        # Set gyroscope configuration
        BMI323_GYRO_CONFIG_LB = self.gyro_filter_bw | self.gyro_fs | self.gyro_odr
        BMI323_GYRO_CONFIG_HB = self.gyro_mode | self.gyro_avg_num
        BMI323_GYRO_CONFIG = [BMI323_GYRO_CONFIG_LB, BMI323_GYRO_CONFIG_HB]
        self.controller.i2cControllerWrite(targetAddress=self.address, busId=self.bus_id, registerAddress=[BMI323_GYRO_CONFIG_REG], data=BMI323_GYRO_CONFIG)

        if self.use_feature_step_counter:
            
            self.config_step_counter()   

            self.select_step_counter_feature()   
            
            self.map_step_counter_interrupt()

        # Calculate resolutions
        self.accel_res, self.gyro_res = self.__calculate_resolutions()

    def calibrate(self):
        '''
        Calibrate the sensor by reading certain number of samples and calculating the average value.
        The average value is then used as the bias for the sensor.
        '''
        sum_values = [0, 0, 0, 0, 0, 0]
        accel_bias = [0, 0, 0]
        gyro_bias = [0, 0, 0]

        for i in range(CALIBRATION_SAMPLES):
            # Read data
            imu_data = self.__read_data()
            for j in range(len(imu_data)):          
                sum_values[j] += imu_data[j]

        calibration_samples_float = float(CALIBRATION_SAMPLES)
        accel_bias[0] = sum_values[0] * self.accel_res / calibration_samples_float
        accel_bias[1] = sum_values[1] * self.accel_res / calibration_samples_float
        accel_bias[2] = sum_values[2] * self.accel_res / calibration_samples_float
        gyro_bias[0] = sum_values[3] * self.gyro_res / calibration_samples_float
        gyro_bias[1] = sum_values[4] * self.gyro_res / calibration_samples_float
        gyro_bias[2] = sum_values[5] * self.gyro_res / calibration_samples_float

        if accel_bias[0] > MAX_ACCEL_BIAS:
            accel_bias[0] -= 1.0  # Remove gravity from the x-axis accelerometer bias calculation
        if accel_bias[0] < MIN_ACCEL_BIAS:
            accel_bias[0] += 1.0  # Remove gravity from the x-axis accelerometer bias calculation
        if accel_bias[1] > MAX_ACCEL_BIAS:
            accel_bias[1] -= 1.0  # Remove gravity from the y-axis accelerometer bias calculation
        if accel_bias[1] < MIN_ACCEL_BIAS:
            accel_bias[1] += 1.0  # Remove gravity from the y-axis accelerometer bias calculation
        if accel_bias[2] > MAX_ACCEL_BIAS:
            accel_bias[2] -= 1.0  # Remove gravity from the z-axis accelerometer bias calculation
        if accel_bias[2] < MIN_ACCEL_BIAS:
            accel_bias[2] += 1.0  # Remove gravity from the z-axis accelerometer bias calculation 

        self.accel_bias = accel_bias
        self.gyro_bias = gyro_bias

    def get_register(self, register_address, len):
        '''
        Get register values in a list of signed 16-bit integers.
        '''
        result = self.controller.i2cControllerRead(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[register_address], 
            requestDataLength=OFFSET_FOR_DUMMY_BYTES + len
        )
        
        data = np.zeros(math.ceil(len/2), dtype=int)
        if result['result'] == 'SUCCESS':
            raw_data = result['payload']
            
            # Convert data to signed 16-bit integers
            for i in range(math.ceil(len/2)):
                data[i] = c_int16(
                    (raw_data[OFFSET_FOR_DUMMY_BYTES + 2*i + 1] << 8) 
                    | raw_data[OFFSET_FOR_DUMMY_BYTES + 2*i]
                ).value
        else:
            raise RuntimeError(f"Error reading register: {result}")

        return data

    def read(self):
        '''
        Read the data from the sensor and convert it to the correct units.
        '''
        # Read imu data
        imu_data = self.__read_data()
        
        # Convert data to correct units
        ax = imu_data[0]*self.accel_res - self.accel_bias[0]
        ay = imu_data[1]*self.accel_res - self.accel_bias[1]
        az = imu_data[2]*self.accel_res - self.accel_bias[2]

        gx = imu_data[3]*self.gyro_res - self.gyro_bias[0]
        gy = imu_data[4]*self.gyro_res - self.gyro_bias[1]
        gz = imu_data[5]*self.gyro_res - self.gyro_bias[2]

        return ((ax, ay, az), (gx, gy, gz))
    
    def soft_reset(self):
        '''
        Perform a soft reset and enable the feature engine.
        '''
        # Variable to store feature data array
        feature_data = [0x2c, 0x01]

        # Variable to enable feature engine bit
        feature_engine_en = [Feature.ENABLE.value, 0]

        # Array variable to store feature IO status
        feature_io_status = [Feature.ENABLE.value, 0]

        # Reset bmi3 device
        BMI3_CMD_SOFT_RESET_LB = Command.SOFT_RESET.value & 0x00FF
        BMI3_CMD_SOFT_RESET_HB = (Command.SOFT_RESET.value & 0xFF00) >> 8
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_CMD], 
            data=[BMI3_CMD_SOFT_RESET_LB, BMI3_CMD_SOFT_RESET_HB]
        )
        time.sleep(0.0015)
        
        # Performing a dummy read after a soft-reset
        self.get_register(BMI323_REG_CHIP_ID,2)

        # Enabling Feature engine
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_IO2], 
            data=feature_data
        )

        # Enabling feature status bit
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_IO_STATUS], 
            data=feature_io_status
        )

        # Enable feature engine bit
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_CTRL], 
            data=feature_engine_en
        )

        # Checking the status bit for feature engine enable
        loop = 1
        while (loop <= 100):
            time.sleep(0.100)

            reg_data = self.get_register(BMI323_REG_FEATURE_IO1,2)
            if (reg_data[0] & FEATURE_ENGINE_ENABLE_MASK):
                rslt = 0
                break
            else:
                rslt = -1

            loop+=1

        return rslt


    def config_step_counter(self):
        '''
        Configure the sensor for step counter usage.
        '''
        # Set the feature data address to step counter's base address
        BMI323_FEATURE_DATA_LB = BMI323_BASE_ADDR.STEP_CNT.value
        BMI323_FEATURE_DATA_HB = 0x00
        BMI323_FEATURE_DATA = [BMI323_FEATURE_DATA_LB, BMI323_FEATURE_DATA_HB]
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_DATA_ADDR], 
            data=BMI323_FEATURE_DATA
        )


        step_config = np.zeros(24, dtype=np.uint8)
        # Set water-mark for lsb 8 bits
        step_config[0] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[0], 
                BMI323_SC_REGISTER.WATERMARK_MASK, 
                self.watermark_level
            ) & 0xFF
        )

        watermark = (np.uint8(step_config[1] << 8))

        # Set water-mark for msb 8 bits
        step_config[1] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                watermark, 
                BMI323_SC_REGISTER.WATERMARK_MASK, 
                self.watermark_level
            ) & BMI323_SC_REGISTER.WATERMARK_MASK
        ) >> 8

        reset_counter = (np.uint16(step_config[1] << 8))

        # Set reset counter
        step_config[1] |= (
            BMI323_SC_REGISTER.SET_BITS(
                reset_counter, 
                BMI323_SC_REGISTER.RESET_COUNTER_MASK, 
                BMI323_SC_REGISTER.RESET_COUNTER_POS, 
                self.reset_counter
            ) & BMI323_SC_REGISTER.RESET_COUNTER_MASK
        ) >> 8

        # Set env_min_dist_up for lsb 8 bits
        step_config[2] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[2],
                BMI323_SC_REGISTER.ENV_MIN_DIST_UP_MASK,
                self.env_min_dist_up
            ) & 0xFF
        )

        env_min_dist_up = (np.uint16(step_config[3] << 8))

        # Set env_min_dist_up for msb 8 bits
        step_config[3] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                env_min_dist_up, 
                BMI323_SC_REGISTER.ENV_MIN_DIST_UP_MASK, 
                self.env_min_dist_up
            ) & BMI323_SC_REGISTER.ENV_MIN_DIST_UP_MASK
        ) >> 8

        # Set env_coef_up for lsb 8 bits
        step_config[4] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[4], 
                BMI323_SC_REGISTER.ENV_COEF_UP_MASK, 
                self.env_coef_up
            ) & 0xFF
        )

        env_coef_up = (np.uint16(step_config[5] << 8))

        # Set env_coef_up for msb 8 bits
        step_config[5] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                env_coef_up,
                BMI323_SC_REGISTER.ENV_COEF_UP_MASK,
                self.env_coef_up
            ) & BMI323_SC_REGISTER.ENV_COEF_UP_MASK
        ) >> 8

        # Set env_min_dist_down for lsb 8 bits
        step_config[6] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[6], 
                BMI323_SC_REGISTER.ENV_MIN_DIST_DOWN_MASK, 
                self.env_min_dist_down
            ) & 0xFF
        )

        env_min_dist_down = (np.uint16(step_config[7] << 8))

        # Set env_min_dist_down for msb 8 bits
        step_config[7] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                env_min_dist_down, 
                BMI323_SC_REGISTER.ENV_MIN_DIST_DOWN_MASK, 
                self.env_min_dist_down
            ) & BMI323_SC_REGISTER.ENV_MIN_DIST_DOWN_MASK
        ) >> 8

        # Set env_coef_down for lsb 8 bits
        step_config[8] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[8], 
                BMI323_SC_REGISTER.ENV_COEF_DOWN_MASK, 
                self.env_coef_down
            ) & 0xFF
        )

        env_coef_down = (np.uint16(step_config[9] << 8))

        # Set env_coef_down for msb 8 bits
        step_config[9] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                env_coef_down, 
                BMI323_SC_REGISTER.ENV_COEF_DOWN_MASK, 
                self.env_coef_down
            ) & BMI323_SC_REGISTER.ENV_COEF_DOWN_MASK
        ) >> 8

        # Set mean_val_decay for lsb 8 bits
        step_config[10] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[10], 
                BMI323_SC_REGISTER.MEAN_VAL_DECAY_MASK, 
                self.mean_val_decay
            ) & 0xFF
        )

        mean_val_decay = (np.uint16(step_config[11] << 8))

        # Set mean_val_decay for msb 8 bits
        step_config[11] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                mean_val_decay, 
                BMI323_SC_REGISTER.MEAN_VAL_DECAY_MASK, 
                self.mean_val_decay
            ) & BMI323_SC_REGISTER.MEAN_VAL_DECAY_MASK
        ) >> 8

        # Set mean_step_dur for lsb 8 bits
        step_config[12] = np.uint8(
            BMI323_SC_REGISTER.SET_BIT_POS0(
                step_config[12], 
                BMI323_SC_REGISTER.MEAN_STEP_DUR_MASK, 
                self.mean_step_dur
            ) & 0xFF
        )

        mean_step_dur = (np.uint16(step_config[13] << 8))

        # Set mean_step_dur for msb 8 bits
        step_config[13] = (
            BMI323_SC_REGISTER.SET_BIT_POS0(
                mean_step_dur, 
                BMI323_SC_REGISTER.MEAN_STEP_DUR_MASK, 
                self.mean_step_dur
            ) & BMI323_SC_REGISTER.MEAN_STEP_DUR_MASK
        ) >> 8

        # Set step buffer size
        step_config[14] = BMI323_SC_REGISTER.SET_BIT_POS0(
            step_config[14], 
            BMI323_SC_REGISTER.BUFFER_SIZE_MASK, 
            self.step_buffer_size
        )

        # Set filter cascade
        step_config[14] |= BMI323_SC_REGISTER.SET_BITS(
            step_config[14], 
            BMI323_SC_REGISTER.FILTER_CASCADE_ENABLED_MASK,
            BMI323_SC_REGISTER.FILTER_CASCADE_ENABLED_POS, 
            self.filter_cascade_enabled
        )

        # Set step_counter_increment for lsb 8 bits
        step_config[14] |= np.uint8(
            BMI323_SC_REGISTER.SET_BITS(
                step_config[14], 
                BMI323_SC_REGISTER.COUNTER_INCREMENT_MASK, 
                BMI323_SC_REGISTER.COUNTER_INCREMENT_POS, 
                self.step_counter_increment
            ) & 0xFF
        )

        step_counter_increment = (np.uint16(step_config[15] << 8))

        # Set step_counter_increment for msb 8 bits
        step_config[15] = (
            BMI323_SC_REGISTER.SET_BITS(
                step_counter_increment, 
                BMI323_SC_REGISTER.COUNTER_INCREMENT_MASK, 
                BMI323_SC_REGISTER.COUNTER_INCREMENT_POS, 
                self.step_counter_increment
            ) & BMI323_SC_REGISTER.COUNTER_INCREMENT_MASK
        ) >> 8

        # Set peak_duration_min_walking for lsb 8 bits
        step_config[16] = BMI323_SC_REGISTER.SET_BIT_POS0(
            step_config[16], 
            BMI323_SC_REGISTER.PEAK_DURATION_MIN_WALKING_MASK, 
            self.peak_duration_min_walking
        )

        peak_duration_min_running = (np.uint16(step_config[17] << 8))

        # Set peak_duration_min_walking for msb 8 bits
        step_config[17] = (
            BMI323_SC_REGISTER.SET_BITS(
                peak_duration_min_running, 
                BMI323_SC_REGISTER.PEAK_DURATION_MIN_RUNNING_MASK,
                BMI323_SC_REGISTER.PEAK_DURATION_MIN_RUNNING_POS, 
                self.peak_duration_min_running
            ) & BMI323_SC_REGISTER.PEAK_DURATION_MIN_RUNNING_MASK
        ) >> 8

        # Set activity detection fsctor
        step_config[18] = BMI323_SC_REGISTER.SET_BIT_POS0(
            step_config[18], 
            BMI323_SC_REGISTER.ACTIVITY_DETECTION_FACTOR_MASK, 
            self.activity_detection_factor
        )

        # Set activity_detection_threshold for lsb 8 bits
        step_config[18] |= np.uint8(
            BMI323_SC_REGISTER.SET_BITS(
                step_config[18], 
                BMI323_SC_REGISTER.ACTIVITY_DETECTION_THRESHOLD_MASK, 
                BMI323_SC_REGISTER.ACTIVITY_DETECTION_THRESHOLD_POS, 
                self.activity_detection_thres
            ) & 0xFF
        )

        activity_detection_threshold = (np.uint16(step_config[19] << 8))

        # Set activity_detection_threshold for msb 8 bits
        step_config[19] = (
            BMI323_SC_REGISTER.SET_BITS(
                activity_detection_threshold, 
                BMI323_SC_REGISTER.ACTIVITY_DETECTION_THRESHOLD_MASK, 
                BMI323_SC_REGISTER.ACTIVITY_DETECTION_THRESHOLD_POS, 
                self.activity_detection_thres
            ) & BMI323_SC_REGISTER.ACTIVITY_DETECTION_THRESHOLD_MASK
        ) >> 8

        # Set maximum step duration
        step_config[20] = BMI323_SC_REGISTER.SET_BIT_POS0(
            step_config[20], 
            BMI323_SC_REGISTER.DURATION_MAX_MASK, 
            self.step_duration_max
        )

        step_duration_window = (np.uint16(step_config[21] << 8))

        # Set step duration window
        step_config[21] = (
            BMI323_SC_REGISTER.SET_BITS(
                step_duration_window, 
                BMI323_SC_REGISTER.DURATION_WINDOW_MASK, 
                BMI323_SC_REGISTER.DURATION_WINDOW_POS, 
                self.step_duration_window
            ) & BMI323_SC_REGISTER.DURATION_WINDOW_MASK
        ) >> 8

        step_config[22] = BMI323_SC_REGISTER.SET_BIT_POS0(
            step_config[22], 
            BMI323_SC_REGISTER.DURATION_PP_ENABLED_MASK, 
            self.step_duration_pp_enabled
        )

        step_config[22] |= BMI323_SC_REGISTER.SET_BITS(
            step_config[22], 
            BMI323_SC_REGISTER.DURATION_THRESHOLD_MASK, 
            BMI323_SC_REGISTER.DURATION_THRESHOLD_POS, 
            self.step_duration_thres
        )

        step_config[22] |= BMI323_SC_REGISTER.SET_BITS(
            step_config[22], 
            BMI323_SC_REGISTER.MEAN_CROSSING_PP_ENABLED_MASK, 
            BMI323_SC_REGISTER.MEAN_CROSSING_PP_ENABLED_POS, 
            self.mean_crossing_pp_enabled
            )

        # Set mcr_threshold for lsb 8 bits
        step_config[22] |= np.uint8(
            BMI323_SC_REGISTER.SET_BITS(
                step_config[22], 
                BMI323_SC_REGISTER.MCR_THRESHOLD_MASK, 
                BMI323_SC_REGISTER.MCR_THRESHOLD_POS, 
                self.mcr_threshold
            ) & 0xFF
        )

        mcr_threshold = (np.uint16(step_config[23] << 8))

        # Set mcr_threshold for msb 8 bits
        step_config[23] = (
            BMI323_SC_REGISTER.SET_BITS(
                mcr_threshold, 
                BMI323_SC_REGISTER.MCR_THRESHOLD_MASK, 
                BMI323_SC_REGISTER.MCR_THRESHOLD_POS, 
                self.mcr_threshold
            ) & BMI323_SC_REGISTER.MCR_THRESHOLD_MASK
        ) >> 8

        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_DATA_TX], 
            data=step_config.tolist()
        )


    def select_step_counter_feature(self, ):
        '''
        Update Feature Engine configuration to use step counter
        '''

        feature = self.get_register(BMI323_REG_FEATURE_IO0, 2)

        # feature[0] = uint8_t)(BMI3_SET_BIT_POS0(get_feature[0], BMI3_NO_MOTION_X_EN,
        #                                 enable->no_motion_x_en) & BMI3_NO_MOTION_X_EN_MASK);
        # feature[0] |=
        #     (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_NO_MOTION_Y_EN,
        #                             enable->no_motion_y_en) & BMI3_NO_MOTION_Y_EN_MASK);
        # feature[0] |=
        #     (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_NO_MOTION_Z_EN,
        #                             enable->no_motion_z_en) & BMI3_NO_MOTION_Z_EN_MASK);
        # feature[0] |=
        #     (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_ANY_MOTION_X_EN,
        #                             enable->any_motion_x_en) & BMI3_ANY_MOTION_X_EN_MASK);
        # feature[0] |=
        #     (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_ANY_MOTION_Y_EN,
        #                             enable->any_motion_y_en) & BMI3_ANY_MOTION_Y_EN_MASK);
        # feature[0] |=
        #     (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_ANY_MOTION_Z_EN,
        #                             enable->any_motion_z_en) & BMI3_ANY_MOTION_Z_EN_MASK);
        # feature[0] |= (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_FLAT_EN, enable->flat_en) & BMI3_FLAT_EN_MASK);
        # feature[0] |=
        #     (uint8_t)(BMI3_SET_BITS(get_feature[0], BMI3_ORIENTATION_EN,
        #                             enable->orientation_en) & BMI3_ORIENTATION_EN_MASK);

        # feature[1] =
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_STEP_DETECTOR_EN,
        #                                 enable->step_detector_en) & BMI3_STEP_DETECTOR_EN_MASK) >> 8);
        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_STEP_COUNTER_EN,
        #                                 enable->step_counter_en) & BMI3_STEP_COUNTER_EN_MASK) >> 8);
        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_SIG_MOTION_EN,
        #                                 enable->sig_motion_en) & BMI3_SIG_MOTION_EN_MASK) >> 8);

        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_TILT_EN, enable->tilt_en) & BMI3_TILT_EN_MASK) >> 8);

        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_TAP_DETECTOR_S_TAP_EN,
        #                                 enable->tap_detector_s_tap_en) & BMI3_TAP_DETECTOR_S_TAP_EN_MASK) >> 8);

        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_TAP_DETECTOR_D_TAP_EN,
        #                                 enable->tap_detector_d_tap_en) & BMI3_TAP_DETECTOR_D_TAP_EN_MASK) >> 8);

        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_TAP_DETECTOR_T_TAP_EN,
        #                                 enable->tap_detector_t_tap_en) & BMI3_TAP_DETECTOR_T_TAP_EN_MASK) >> 8);

        # feature[1] |=
        #     (uint8_t)((BMI3_SET_BITS(get_feature[1], BMI3_I3C_SYNC_EN,
        #                                 enable->i3c_sync_en) & BMI3_I3C_SYNC_EN_MASK) >> 8);

        #sacar set bits a otra clase general
        
        feature[0] = (
            BMI323_SC_REGISTER.SET_BITS(
                (feature & 0xFF00)>>8, 
                BMI323_SC_REGISTER.STEP_COUNTER_EN_MASK, 
                BMI323_SC_REGISTER.STEP_COUNTER_EN_POS, 
                Feature.ENABLE.value
            ) & BMI323_SC_REGISTER.STEP_COUNTER_EN_MASK
        ) | (feature & 0x00FF) 
        feature_write = [int(feature[0] & 0x00FF), int((feature[0] & 0xFF00)>>8)]
        
        # Reset the register before updating new values
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_IO0], 
            data=[0, 0]
        )
        
        # Set the updated configuration           
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_IO0], 
            data=feature_write
        )
        
        # Trigger the feature engine to apply the newly written configuration
        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_FEATURE_IO_STATUS], 
            data=[1, 0]
        )
        

    def map_step_counter_interrupt(self):
        '''
        Map step counter interruption
        '''
        # Read interrupt map1 and map2 and register
        reg_data = self.get_register(BMI323_REG_INT_MAP1, 4)

        # Map to Int1
        temp_value = np.uint8(((reg_data[0]) & 0xFF00)>>8)
        temp_value = BMI323_SC_REGISTER.SET_BITS(
            temp_value, 
            BMI323_SC_REGISTER.STEP_COUNTER_OUT_MASK, 
            BMI323_SC_REGISTER.STEP_COUNTER_OUT_POS, 
            HwIntPin.INT1.value
        )

        reg_data[0] = temp_value | (reg_data[0] & 0x00FF)
        reg_data_write = [
            int(reg_data[0] & 0x00FF), 
            int((reg_data[0] & 0xFF00)>>8), 
            int(reg_data[1] & 0x00FF), 
            int((reg_data[1] & 0xFF00)>>8)
        ]

        self.controller.i2cControllerWrite(
            targetAddress=self.address, 
            busId=self.bus_id, 
            registerAddress=[BMI323_REG_INT_MAP1], 
            data=reg_data_write
        )