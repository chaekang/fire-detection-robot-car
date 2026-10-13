# main.py - 메인 통합 로직 (버저 추가)
import time
from config import init_gpio, cleanup_gpio, LED_RGB
import RPi.GPIO as GPIO
from motor_control import car_stop
from line_tracking import basic_line_tracking
from ir_obstacle_detection import handle_obstacle_detection, celebrate_fire_extinguished, wait_until_fire_disappears
from fire_detection import FireDetector
from camera_control import camera_center
from display_control import DisplayController
from led_control import LEDController
from buzzer_control import init_buzzer, play_obstacle_sound, cleanup_buzzer

def main():
    """
    메인 통합 로직
    1) 라인트래킹
    2) 초음파로 장애물 감지
    3) 정지 후 불 여부 판단
    4) 불이면: 워터펌프 → 표정 행복 → 불 사라질 때까지 대기 → 주행
    """
    print("\n" + "="*50)
    print("소방 로봇 시작 (IR 장애물 회피 + 화재 진압)")
    print("="*50 + "\n")

    # GPIO 초기화
    init_gpio()

    # 버저 초기화 (추가!)
    init_buzzer()

    # 디스플레이 초기화
    display = DisplayController()
    display.show_face("normal")

    # LED 컨트롤러 초기화
    led_controller = LEDController(LED_RGB)

    # Fire Detector 초기화
    fire_detector = FireDetector()
    if not fire_detector.connect_to_server():
        print("⚠ YOLO 서버 연결 실패, 불 감지 기능 비활성화")
        print("  → 일반 장애물 회피 모드로 동작\n")
    else:
        fire_detector.init_camera()
        print("✓ YOLO 서버 연결 성공\n")

    # 카메라 중앙 정렬
    camera_center()

    fire_extinguished_count = 0  # 진압한 화재 수

    try:
        while True:
            # ===========================
            # 1. 장애물 감지 및 처리
            # ===========================
            obstacle_type, result = handle_obstacle_detection(fire_detector)

            if obstacle_type == "fire":

                # 불 난 장애물 처리
                if result:  # 접근 성공
                    print("\n" + "="*50)
                    print("화재 진압 위치 도달!")
                    print("="*50)

                    fire_extinguished_count += 1
                    print(f"\n✓ 화재 진압 완료! (누적: {fire_extinguished_count}건)")

                    celebrate_fire_extinguished(display, led_controller)

                    print("="*50 + "\n")

                    car_stop()
                    time.sleep(0.5)

                else:
                    print("화재 접근 실패\n")

            elif obstacle_type == "normal":

                # 일반 장애물 회피 완료
                avoid_dir = result

            # ===========================
            # 2. 기본 라인트래킹
            # ===========================
            basic_line_tracking()
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n\n프로그램 사용자 종료")
        print(f"총 {fire_extinguished_count}건의 화재 진압")

    finally:
        car_stop()
        fire_detector.close()
        cleanup_buzzer()  # 추가!
        cleanup_gpio()
        print("\n소방 로봇 종료 완료\n")

if __name__ == "__main__":
    main()
