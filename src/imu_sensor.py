# imu_sensor.py - IMU 센서
from config import bus
import time
from motor_control import car_turn_left, car_turn_right, car_stop, car_forward

mpu_addr = 0x68

def init_mpu():
    bus.write_byte_data(mpu_addr, 0x6B, 0)
    bus.write_byte_data(mpu_addr, 0x1B, 0x00)
    bus.write_byte_data(mpu_addr, 0x1C, 0x00)

init_mpu()

def read_word(reg):
    high = bus.read_byte_data(mpu_addr, reg)
    low = bus.read_byte_data(mpu_addr, reg+1)
    val = (high<<8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    return val

# Gyro offset 캘리브레이션
print("[IMU] 3초간 고정하세요…")
gyro_samples = []
t0 = time.time()
while time.time() - t0 < 3:
    gyro_samples.append(read_word(0x47)/131.0)
    time.sleep(0.01)

gyro_offset = sum(gyro_samples)/len(gyro_samples)
print(f"[IMU] offset = {gyro_offset:.2f}")

yaw = 0.0
gz_lpf = 0.0
last_time = time.time()
ALPHA = 0.9
DEADZONE = 0.3

def update_yaw():
    """IMU yaw 값 업데이트"""
    global yaw, gz_lpf, last_time

    now = time.time()
    dt = now - last_time
    last_time = now

    gz = read_word(0x47)/131.0
    gz_lpf = ALPHA*gz_lpf + (1-ALPHA)*gz
    gz_corrected = gz_lpf - gyro_offset

    if abs(gz_corrected) < DEADZONE:
        gz_corrected = 0

    yaw += gz_corrected * dt
    return yaw

def get_yaw():
    """현재 yaw 값 반환"""
    return yaw

def rotate_to_yaw(target_yaw, speed=80):
    """목표 각도로 회전"""

    timeout = time.time()

    while True:
        now_yaw = update_yaw()
        diff = target_yaw - now_yaw

        if diff > 0:
            car_turn_left(speed)
        else:
            car_turn_right(speed)

        if abs(diff) < 3.0:
            car_stop()
            break

        time.sleep(0.03)

        if time.time() - timeout > 20:
            car_stop()
            break
