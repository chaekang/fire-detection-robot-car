# config.py - 공통 설정
import RPi.GPIO as GPIO
import smbus
import threading

# I2C 설정
I2C_BUS = 1
STM8_ADDR = 0x16
bus = smbus.SMBus(I2C_BUS)
i2c_lock = threading.Lock()

# GPIO 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 라인트래킹 센서 핀
TRACKING_LEFT1 = 13
TRACKING_LEFT2 = 15
TRACKING_RIGHT1 = 11
TRACKING_RIGHT2 = 7

# 초음파 센서 핀
TRIG = 16
ECHO = 18

# IR 장애물 감지 센서 핀 (추가)
IR_LEFT = 21      # 왼쪽 IR 센서
IR_RIGHT = 19     # 오른쪽 IR 센서
IR_SWITCH = 22    # IR 센서 스위치

# LED 핀
LED_RGB = 12

# 카메라 서보 번호
CAMERA_SERVO = 4

# YOLO 서버 설정
YOLO_SERVER_IP = "192.168.1.8"
YOLO_SERVER_PORT = 8000

def init_gpio():
    """GPIO 핀 초기화"""
    # 라인트래킹 센서
    GPIO.setup(TRACKING_LEFT1, GPIO.IN)
    GPIO.setup(TRACKING_LEFT2, GPIO.IN)
    GPIO.setup(TRACKING_RIGHT1, GPIO.IN)
    GPIO.setup(TRACKING_RIGHT2, GPIO.IN)

    # 초음파
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN)

    # IR 센서 (추가)
    GPIO.setup(IR_LEFT, GPIO.IN)
    GPIO.setup(IR_RIGHT, GPIO.IN)
    GPIO.setup(IR_SWITCH, GPIO.OUT)
    GPIO.output(IR_SWITCH, GPIO.HIGH)  # IR 센서 활성화

    # LED
    GPIO.setup(LED_RGB, GPIO.OUT, initial=GPIO.LOW)

    print("✓ GPIO 초기화 완료")

def cleanup_gpio():
    """GPIO 정리"""
    GPIO.cleanup()
    print("✓ GPIO 정리 완료")
