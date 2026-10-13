# buzzer_control.py
import RPi.GPIO as GPIO
import time

# BUZZER 핀 설정
BUZZER = 32  # Pin 32

def init_buzzer():
    """버저 초기화"""
    GPIO.setup(BUZZER, GPIO.OUT)
    global buzzer_pwm
    buzzer_pwm = GPIO.PWM(BUZZER, 440)

def play_obstacle_sound():
    """장애물 감지 시 도레미파솔라 재생"""
    frequencies = [262, 330, 392, 523, 659, 784]  # 도레미파솔라

    for freq in frequencies:
        buzzer_pwm.start(50)
        buzzer_pwm.ChangeFrequency(freq)
        time.sleep(0.2)  # 0.5초에서 0.2초로 짧게
        buzzer_pwm.stop()
        time.sleep(0.05)  # 0.1초에서 0.05초로 짧게

def play_finish_sound():
    """불 진화 시 라솔파미레도 재생"""
    frequencies = [784, 659, 523, 392, 330, 262] # 라솔파미레도
    for freq in frequencies:
        buzzer_pwm.start(50)
        buzzer_pwm.ChangeFrequency(freq)
        time.sleep(0.2)  # 0.5초에서 0.2초로 짧게
        buzzer_pwm.stop()
        time.sleep(0.05)  # 0.1초에서 0.05초로 짧게

def cleanup_buzzer():
    """버저 정리"""
    buzzer_pwm.stop()
