# motor_control.py - 모터 제어
import time
from config import bus, STM8_ADDR

# 기본 모터 제어
def motor_control(left_speed, right_speed):
    try:
        left_dir = 0x01 if left_speed >= 0 else 0x02
        right_dir = 0x01 if right_speed >= 0 else 0x02
        left_speed = abs(left_speed) & 0xFF
        right_speed = abs(right_speed) & 0xFF
        bus.write_i2c_block_data(STM8_ADDR, 0x01,
                                 [left_dir, left_speed, right_dir, right_speed])
    except Exception as e:
        print(f"I2C 모터 오류: {e}")

# 서보 제어
def servo_control(num, angle):
    try:
        bus.write_i2c_block_data(STM8_ADDR, 0x03, [num, angle])
    except Exception as e:
        print(f"I2C 서보 오류: {e}")


# 기본 동작
def car_forward(speed=40):
    motor_control(speed, speed)

def car_turn_left(speed=70):
    motor_control(int(speed * 0.25), speed)

def car_turn_right(speed=70):
    motor_control(speed, int(speed * 0.0006))

def rotate_left(speed=60):
    motor_control(-speed, speed)

def rotate_right(speed=60):
    motor_control(speed, -speed)

def car_stop():
    motor_control(0, 0)
