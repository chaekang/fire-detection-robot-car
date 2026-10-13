import RPi.GPIO as GPIO
import time
from config import bus

# GPIO 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# IR 센서 핀 설정 (BOARD 기준)
AvoidSensorLeft = 21   # 왼쪽 IR 센서
AvoidSensorRight = 19  # 오른쪽 IR 센서
Avoid_ON = 22          # IR 센서 스위치

# GPIO 핀 모드 설정
GPIO.setup(AvoidSensorLeft, GPIO.IN)
GPIO.setup(AvoidSensorRight, GPIO.IN)
GPIO.setup(Avoid_ON, GPIO.OUT)

# IR 센서 활성화
GPIO.output(Avoid_ON, GPIO.HIGH)

# I2C 설정
# bus = smbus.SMBus(1)
STM8_ADDRESS = 0x48  # STM8의 I2C 주소

# 모터 제어 함수들
def car_run(left_speed, right_speed):
    """차량 전진"""
    try:
        bus.write_i2c_block_data(STM8_ADDRESS, 0x01, [left_speed, right_speed, 0, 0])
    except:
        pass

def car_stop():
    """차량 정지"""
    try:
        bus.write_i2c_block_data(STM8_ADDRESS, 0x02, [0, 0, 0, 0])
    except:
        pass

def car_spin_left(left_speed, right_speed):
    """제자리 좌회전"""
    try:
        bus.write_i2c_block_data(STM8_ADDRESS, 0x03, [left_speed, right_speed, 0, 0])
    except:
        pass

def car_spin_right(left_speed, right_speed):
    """제자리 우회전"""
    try:
        bus.write_i2c_block_data(STM8_ADDRESS, 0x04, [left_speed, right_speed, 0, 0])
    except:
        pass

# IR 장애물 회피 함수
def ir_avoid():
    """IR 센서를 이용한 장애물 회피"""
    # IR 센서 값 읽기 (LOW = 장애물 감지, HIGH = 장애물 없음)
    left_sensor = GPIO.input(AvoidSensorLeft)
    right_sensor = GPIO.input(AvoidSensorRight)

    # 양쪽 모두 장애물 감지
    if left_sensor == False and right_sensor == False:
        print("양쪽 장애물 감지 - 우회전")
        car_stop()
        time.sleep(0.1)
        car_spin_right(80, 80)
        time.sleep(0.5)

    # 왼쪽만 장애물 감지
    elif left_sensor == False and right_sensor == True:
        print("왼쪽 장애물 감지 - 우회전")
        car_stop()
        time.sleep(0.1)
        car_spin_right(90, 90)
        time.sleep(0.3)

    # 오른쪽만 장애물 감지
    elif left_sensor == True and right_sensor == False:
        print("오른쪽 장애물 감지 - 좌회전")
        car_stop()
        time.sleep(0.1)
        car_spin_left(90, 90)
        time.sleep(0.3)

    # 장애물 없음 - 전진
    else:
        print("장애물 없음 - 전진")
        car_run(100, 100)

# 메인 루프
try:
    print("IR 센서 장애물 회피 시작")
    print("Ctrl+C로 종료")

    while True:
        ir_avoid()
        time.sleep(0.1)  # 센서 읽기 주기

except KeyboardInterrupt:
    print("\n프로그램 종료")
    car_stop()
    GPIO.cleanup()
