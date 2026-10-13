# led_control.py - 단일 RGB LED 제어
import RPi.GPIO as GPIO
import time
import threading

class LEDController:
    def __init__(self, led_pin):
        self.led_pin = led_pin
        self.blinking = False
        self.blink_thread = None

        GPIO.setup(self.led_pin, GPIO.OUT, initial=GPIO.LOW)

        print("✓ LED 컨트롤러 초기화 완료")

    def start_blink(self, interval=0.3):
        """LED 깜빡임 시작"""
        self.stop_blink()  # 기존 깜빡임 중

        self.blinking = True

        def blink_loop():
            while self.blinking:
                GPIO.output(self.led_pin, GPIO.HIGH)
                time.sleep(interval)
                GPIO.output(self.led_pin, GPIO.LOW)
                time.sleep(interval)

        self.blink_thread = threading.Thread(target=blink_loop, daemon=True)
        self.blink_thread.start()
        print(f"✓ LED 깜빡임 시작 (간격: {interval}초)")

    def stop_blink(self):
        """LED 깜빡임 중지"""
        if self.blinking:
            self.blinking = False
            if self.blink_thread:
                self.blink_thread.join(timeout=1)
            GPIO.output(self.led_pin, GPIO.LOW)
            print("✓ LED 깜빡임 중지")
