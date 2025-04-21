from enum import Enum

WHO_AM_I_register = 0x75
WHO_AM_I_length = 1
WHO_AM_I_value = 0x47

PWR_MGMT0_register = 0x4E
PWR_MGMT0_length = 1

class IMU14CLICK_ACCEL_MODE(Enum):
    OFF         = 0x00
    _OFF        = 0x01
    LOW_POWER   = 0x02
    LOW_NOISE   = 0x03

class IMU14CLICK_GYRO_MODE(Enum):
    OFF         = 0x00
    STANDBY     = 0x04
    RESERVED    = 0x08
    LOW_NOISE   = 0x0C

GYRO_CONFIG0_register = 0x4F
GYRO_CONFIG0_length = 1

class IMU14CLICK_GYRO_FS(Enum):
    """Gyroscope full scale values"""
    FS_2000dps  = 0x00
    FS_1000dps  = 0x20
    FS_500dps   = 0x40
    FS_250dps   = 0x60
    FS_125dps   = 0x80
    FS_62_5dps  = 0xA0
    FS_31_25dps = 0xC0
    FS_15_625dps= 0xE0

# Gyroscope full scale values in dps
IMU14CLICK_GYRO_FS_VALUES = {
    IMU14CLICK_GYRO_FS.FS_15_625dps.value: 15.625,
    IMU14CLICK_GYRO_FS.FS_31_25dps.value:  31.25,
    IMU14CLICK_GYRO_FS.FS_62_5dps.value:   62.5,
    IMU14CLICK_GYRO_FS.FS_125dps.value:  125.0,
    IMU14CLICK_GYRO_FS.FS_250dps.value:  250.0,
    IMU14CLICK_GYRO_FS.FS_500dps.value:  500.0,
    IMU14CLICK_GYRO_FS.FS_1000dps.value: 1000.0,
    IMU14CLICK_GYRO_FS.FS_2000dps.value: 2000.0
}

class IMU14CLICK_GYRO_ODR(Enum):
    """Gyroscope output data rates"""
    ODR_32kHz   = 0x01
    ODR_16kHz   = 0x02
    ODR_8kHz    = 0x03
    ODR_4kHz    = 0x04
    ODR_2kHz    = 0x05
    ODR_1kHz    = 0x06
    ODR_200Hz   = 0x07
    ODR_100Hz   = 0x08
    ODR_50Hz    = 0x09
    ODR_25Hz    = 0x0A
    ODR_12_5Hz  = 0x0B
    ODR_500Hz   = 0x0F

# Gyroscope 16 bits symmetric resolution
IMU14CLICK_GYRO_RESOLUTION = 32768.0

GYRO_CONFIG1_register = 0x51
GYRO_CONFIG1_length = 1
TEMP_FILT_BW_5Hz = 0xC0

ACCEL_CONFIG0_register = 0x50
ACCEL_CONFIG0_length = 1

class IMU14CLICK_ACCEL_FS(Enum):
    """Accelerometer full scale values"""
    FS_16g  = 0x00
    FS_8g   = 0x20
    FS_4g   = 0x40
    FS_2g   = 0x60

# Accelerometer full scale values in g
IMU14CLICK_ACCEL_FS_VALUES = {
    IMU14CLICK_ACCEL_FS.FS_2g.value:   2.0,
    IMU14CLICK_ACCEL_FS.FS_4g.value:   4.0,
    IMU14CLICK_ACCEL_FS.FS_8g.value:   8.0,
    IMU14CLICK_ACCEL_FS.FS_16g.value:  16.0
}

class IMU14CLICK_ACCEL_ODR(Enum):
    """Accelerometer output data rates"""
    ODR_32kHz   = 0x01
    ODR_16kHz   = 0x02
    ODR_8kHz    = 0x03
    ODR_4kHz    = 0x04
    ODR_2kHz    = 0x05
    ODR_1kHz    = 0x06
    ODR_200Hz   = 0x07
    ODR_100Hz   = 0x08
    ODR_50Hz    = 0x09
    ODR_25Hz    = 0x0A
    ODR_12_5Hz  = 0x0B
    ODR_6_25Hz  = 0x0C
    ODR_3_125Hz = 0x0D
    ODR_1_5625Hz= 0x0E
    ODR_500Hz   = 0x0F

# Accelerometer 16 bits symmetric resolution
IMU14CLICK_ACCEL_RESOLUTION = 32768.0

TEMP_DATA1_register = 0x1D
READ_LENGTH = 14 # 14 bytes to read all data (6 bytes for accelerometer, 6 bytes for gyroscope, 2 bytes for temperature)