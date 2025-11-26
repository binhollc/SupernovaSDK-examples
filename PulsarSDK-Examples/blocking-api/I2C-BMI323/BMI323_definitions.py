from enum import Enum
import numpy as np

# Number of samples to be used for calibration
CALIBRATION_SAMPLES = 180

# Address of the BMI323 Accelerometer Configuration Register
BMI323_ACCEL_CONFIG_REG = 0x20

class BMI323_ACCEL_OP_MODES(Enum):
    """Accelerometer operating modes"""
    SUSPEND          = 0x00
    LOW_POWER_MODE   = 0x30
    HIGH_PERFORMANCE = 0x40
    NORMAL           = 0x70

class BMI323_ACCEL_AVG_NUM(Enum):
    """Accelerometer averaging numbers"""
    NO_AVG = 0x00
    AVG_2  = 0x01
    AVG_4  = 0x02
    AVG_8  = 0x03
    AVG_16 = 0x04
    AVG_32 = 0x05
    AVG_64 = 0x06

class BMI323_ACCEL_FILTER_BW(Enum):
    """Accelerometer filter bandwidths"""
    ODR_2  = 0x00
    ODR_4  = 0x80

class BMI323_ACCEL_FS(Enum):
    """Accelerometer full scale values"""
    FS_2g   = 0x00
    FS_4g   = 0x10
    FS_8g   = 0x20
    FS_16g  = 0x30

# Accelerometer full scale values in g
BMI323_ACCEL_FS_VALUES = {
    BMI323_ACCEL_FS.FS_2g.value:   2.0,
    BMI323_ACCEL_FS.FS_4g.value:   4.0,
    BMI323_ACCEL_FS.FS_8g.value:   8.0,
    BMI323_ACCEL_FS.FS_16g.value:  16.0
}

class BMI323_ACCEL_ODR(Enum):
    """Accelerometer output data rates"""
    AODR_0_78125Hz  = 0x01
    AODR_1_5625Hz   = 0x02
    AODR_3_125Hz    = 0x03
    AODR_6_25Hz     = 0x04
    AODR_12_5Hz     = 0x05
    AODR_25Hz       = 0x06
    AODR_50Hz       = 0x07
    AODR_100Hz      = 0x08
    AODR_200Hz      = 0x09
    AODR_400Hz      = 0x0A
    AODR_800Hz      = 0x0B
    AODR_1_6kHz     = 0x0C
    AODR_3_2kHz     = 0x0D
    AODR_6_4kHz     = 0x0E

# Accelerometer 16 bits symmetric resolution
BMI323_ACCEL_RESOLUTION = 32768.0

# Accelerometer bias limits in g
MAX_ACCEL_BIAS = 0.8
MIN_ACCEL_BIAS = -0.8

# Chip id address
BMI323_REG_CHIP_ID = 0x00

# Accelerometer data X register address
BMI323_ACCEL_DATA_X = 0x03

# Address of the BMI323 Gyroscope Configuration Register
BMI323_GYRO_CONFIG_REG = 0x21

# Address of the BMI323 Feature Engine Control Register
BMI323_REG_FEATURE_CTRL = 0x40

# Address of the BMI323 Feature Data Address Register
BMI323_REG_FEATURE_DATA_ADDR = 0x41

# Address of the BMI323 I/O port for the data values of the feature engine
BMI323_REG_FEATURE_DATA_TX = 0x42

# Address of the BMI323 feature engine configuration, before setting/changing an active configuration the register must be cleared (set to 0)
BMI323_REG_FEATURE_IO0 = 0x10

# Address of the BMI323 Feature engine I/O register 0
BMI323_REG_FEATURE_IO1 = 0x11

# Address of the BMI323 Feature engine I/O register 1
BMI323_REG_FEATURE_IO2 = 0x12

# Address of the BMI323 feature I/O synchronization status and trigger
BMI323_REG_FEATURE_IO_STATUS = 0x14

# Address of the BMI323 mapping of feature engine interrupts to outputs
BMI323_REG_INT_MAP1 = 0x3A

# Address of the BMI323 INT1 Status Register
BMI323_REG_INT_STATUS_INT1 = 0x0D

# Address of the BMI323 Command Register
BMI323_REG_CMD = 0x7E



FEATURE_ENGINE_ENABLE_MASK = 0x0001


class BMI323_GYRO_OP_MODES(Enum):
    """Gyroscope operating modes"""
    SUSPEND          = 0x00
    DRIVER_ONLY      = 0x10
    LOW_POWER_MODE   = 0x30
    HIGH_PERFORMANCE = 0x40
    NORMAL           = 0x70

class BMI323_GYRO_AVG_NUM(Enum):
    """Gyroscope averaging numbers"""
    NO_AVG = 0x00
    AVG_2  = 0x01
    AVG_4  = 0x02
    AVG_8  = 0x03
    AVG_16 = 0x04
    AVG_32 = 0x05
    AVG_64 = 0x06

class BMI323_GYRO_FILTER_BW(Enum):
    """Gyroscope filter bandwidths"""
    ODR_2  = 0x00
    ODR_4  = 0x80

class BMI323_GYRO_FS(Enum):
    """Gyroscope full scale values"""
    FS_125dps   = 0x00
    FS_250dps   = 0x10
    FS_500dps   = 0x20
    FS_1000dps  = 0x30
    FS_2000dps  = 0x40

# Gyroscope full scale values in dps
BMI323_GYRO_FS_VALUES = {
    BMI323_GYRO_FS.FS_125dps.value:  125.0,
    BMI323_GYRO_FS.FS_250dps.value:  250.0,
    BMI323_GYRO_FS.FS_500dps.value:  500.0,
    BMI323_GYRO_FS.FS_1000dps.value: 1000.0,
    BMI323_GYRO_FS.FS_2000dps.value: 2000.0
}

class BMI323_GYRO_ODR(Enum):
    """Gyroscope output data rates"""
    GODR_0_78125Hz  = 0x01
    GODR_1_5625Hz   = 0x02
    GODR_3_125Hz    = 0x03
    GODR_6_25Hz     = 0x04
    GODR_12_5Hz     = 0x05
    GODR_25Hz       = 0x06
    GODR_50Hz       = 0x07
    GODR_100Hz      = 0x08
    GODR_200Hz      = 0x09
    GODR_400Hz      = 0x0A
    GODR_800Hz      = 0x0B
    GODR_1_6kHz     = 0x0C
    GODR_3_2kHz     = 0x0D
    GODR_6_4kHz     = 0x0E

# Gyroscope 16 bits symmetric resolution
BMI323_GYRO_RESOLUTION = 32768.0

class BMI323_BASE_ADDR(Enum):
    """Feature interrupts base address"""
    CONFIG_VERSION              = 0x00
    AXIS_REMAP                  = 0x03
    ANY_MOTION                  = 0x05
    NO_MOTION                   = 0x08
    FLAT                        = 0x0B
    SIG_MOTION                  = 0x0D
    STEP_CNT                    = 0x10
    ORIENT                      = 0x1C
    TAP                         = 0x1E
    TILT                        = 0x21
    ALT_AUTO_CONFIG             = 0X23
    ST_RESULT                   = 0x24
    ST_SELECT                   = 0x25
    GYRO_SC_SELECT              = 0x26
    GYRO_SC_ST_CONF             = 0x27
    GYRO_SC_ST_COEFFICIENTS     = 0x28
    I3C_SYNC                    = 0x36
    I3C_SYNC_ACC                = 0x37
    I3C_SYNC_GYR                = 0x3A
    I3C_SYNC_TEMP               = 0x3D
    I3C_SYNC_TIME               = 0x3E
    ACC_GYR_OFFSET_GAIN_RESET   = 0x3F
    ACC_OFFSET_GAIN             = 0x40
    GYRO_OFFSET_GAIN            = 0x46

class BMI323_SC_REGISTER:
    """Bit position definitions for step counter feature configuration"""
    WATERMARK_MASK                     = 0x3FF

    RESET_COUNTER_MASK                 = 0x0400
    RESET_COUNTER_POS                  = 10

    ENV_MIN_DIST_UP_MASK               = 0xFFFF

    ENV_COEF_UP_MASK                   = 0xFFFF

    ENV_MIN_DIST_DOWN_MASK             = 0xFFFF

    ENV_COEF_DOWN_MASK                 = 0xFFFF

    MEAN_VAL_DECAY_MASK                = 0xFFFF

    MEAN_STEP_DUR_MASK                 = 0xFFFF

    BUFFER_SIZE_MASK                   = 0x000F

    FILTER_CASCADE_ENABLED_MASK        = 0x0010
    FILTER_CASCADE_ENABLED_POS         = 4

    COUNTER_INCREMENT_MASK             = 0xFFE0
    COUNTER_INCREMENT_POS              = 5

    PEAK_DURATION_MIN_WALKING_MASK     = 0x00FF

    PEAK_DURATION_MIN_RUNNING_MASK     = 0xFF00
    PEAK_DURATION_MIN_RUNNING_POS      = 8

    ACTIVITY_DETECTION_FACTOR_MASK     = 0x000F

    ACTIVITY_DETECTION_THRESHOLD_MASK  = 0xFFF0
    ACTIVITY_DETECTION_THRESHOLD_POS   = 4

    DURATION_MAX_MASK                  = 0x00FF

    DURATION_WINDOW_MASK               = 0xFF00
    DURATION_WINDOW_POS                = 8

    DURATION_PP_ENABLED_MASK           = 0x0001

    DURATION_THRESHOLD_MASK            = 0x000E
    DURATION_THRESHOLD_POS             = 1

    MEAN_CROSSING_PP_ENABLED_MASK      = 0x0010
    MEAN_CROSSING_PP_ENABLED_POS       = 4

    MCR_THRESHOLD_MASK                 = 0x03E0
    MCR_THRESHOLD_POS                  = 5

    STEP_COUNTER_EN_MASK               = 0x0200
    STEP_COUNTER_EN_POS                = 9

    STEP_COUNTER_OUT_MASK              = 0x0C00
    STEP_COUNTER_OUT_POS               = 10

    INT_STATUS_STEP_COUNTER            = 0x0020

    @staticmethod
    def SET_BIT_POS0(reg_data, mask, data):
        reg_data = np.uint8(reg_data)
        mask = np.uint16(mask)
        data = np.uint16(data)
        return (reg_data & (~mask & 0xFFFF)) | (data & mask)

    @staticmethod
    def SET_BITS(reg_data, mask, pos, data):
        reg_data = np.uint8(reg_data)
        mask = np.uint16(mask)
        data = np.uint16(data)
        pos = np.uint8(pos)
        return (reg_data & (~mask & 0xFFFF)) | ((data << pos) & mask)
    

class HwIntPin (Enum):
    """Enum to define interrupt lines"""
    INT_NONE       = 0
    INT1           = 1
    INT2           = 2
    I3C_INT        = 3
    INT_PIN_MAX    = 4

class Feature(Enum):
    """For enable and disable"""
    ENABLE  = 1
    DISABLE = 0

class Command(Enum):
    SELF_TEST_TRIGGER   = 0x0100
    SELF_CALIB_TRIGGER  = 0x0101
    SELF_CALIB_ABORT    = 0x0200
    I3C_TCSYNC_UPDATE   = 0x0201
    AXIS_MAP_UPDATE     = 0x0300
    _1                   = 0x64AD
    _2                   = 0xD3AC
    SOFT_RESET          = 0xDEAF



class feature_enable():
    # Enables no-motion feature for X-axis
    no_motion_x_en = Feature.DISABLE

    # Enables no-motion feature for Y-axis
    no_motion_y_en = Feature.DISABLE

    # Enables no-motion feature for Z-axis
    no_motion_z_en = Feature.DISABLE

    # Enables any-motion feature for X-axis
    any_motion_x_en = Feature.DISABLE

    # Enables any-motion feature for Y-axis
    any_motion_y_en = Feature.DISABLE

    # Enables any-motion feature for Z-axis
    any_motion_z_en = Feature.DISABLE

    # Enables flat feature
    flat_en = Feature.DISABLE

    # Enables orientation feature
    orientation_en = Feature.DISABLE

    # Enables step detector feature
    step_detector_en = Feature.DISABLE

    # Enables step counter feature
    step_counter_en = Feature.DISABLE

    # Enables significant motion feature
    sig_motion_en = Feature.DISABLE

    # Enables tilt feature
    tilt_en = Feature.DISABLE

    # Enables single tap feature
    tap_detector_s_tap_en = Feature.DISABLE

    # Enables double tap feature
    tap_detector_d_tap_en = Feature.DISABLE

    # Enables triple tap feature
    tap_detector_t_tap_en = Feature.DISABLE

    # Enables I3C TC-sync feature
    i3c_sync_en = Feature.DISABLE