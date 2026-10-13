# camera_control.py - 카메라 서보 제어
import time
from config import CAMERA_SERVO,bus

STM8_ADDR = 0x16

# 서보 제어
def servo_control(servo_num, angle):
    bus.write_i2c_block_data(STM8_ADDR, 0x03, [servo_num, angle])

def camera_scan_left_right():
    print("카메라 스캔 시작")

    # 왼쪽
    servo_control(CAMERA_SERVO, 0)
    print("카메라 왼쪽")
    time.sleep(2)

    # 중앙
    servo_control(CAMERA_SERVO, 15)
    print("카메라 중앙")
    time.sleep(0.3)

    print("카메라 스캔 완료")

def camera_center():
    servo_control(CAMERA_SERVO, 15)
