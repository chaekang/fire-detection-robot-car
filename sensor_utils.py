import RPi.GPIO as GPIO
import time
from config import TRACKING_LEFT1, TRACKING_LEFT2, TRACKING_RIGHT1, TRACKING_RIGHT2
from config import TRIG, ECHO
from config import IR_LEFT, IR_RIGHT

# 라인트래킹 센서 읽기
def read_line_sensors():
    L1 = GPIO.input(TRACKING_LEFT1)
    L2 = GPIO.input(TRACKING_LEFT2)
    R1 = GPIO.input(TRACKING_RIGHT1)
    R2 = GPIO.input(TRACKING_RIGHT2)
    return (L1, L2, R1, R2)

# 검은 선 개수 세기
def count_black(L1, L2, R1, R2):
    return 4 - (L1 + L2 + R1 + R2)

# 라인 방향 판단
def get_direction(L1, L2, R1, R2):
    left_black = 2 - (L1 + L2)
    right_black = 2 - (R1 + R2)
    if left_black > right_black:
        return "left"
    if right_black > left_black:
        return "right"
    return "center"

# 초음파 센서로 거리 확인
def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    start = time.time()
    pulse_start = start
    pulse_end = start

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start - start > 0.1:
            return 999

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > 0.1:
            return 999

    return round((pulse_end - pulse_start) * 17150, 2)

    """
    IR 센서 읽기
    Returns: (left_blocked, right_blocked)
        False = 장애물 없음 (HIGH)
        True = 장애물 있음 (LOW)
    """
# IR 센서 읽기
def read_ir_sensors():
    left_blocked = not GPIO.input(IR_LEFT)   # LOW = 장애물
    right_blocked = not GPIO.input(IR_RIGHT)
    return left_blocked, right_blocked
