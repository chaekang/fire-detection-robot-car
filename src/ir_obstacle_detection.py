# obstacle_avoidance.py - 라인 변경 방식으로 수정
import time
import RPi.GPIO as GPIO
from config import LED_RGB
from sensor_utils import get_distance, read_ir_sensors, read_line_sensors, get_direction
from motor_control import (car_forward, car_stop,
                           rotate_left, rotate_right, car_turn_right, car_turn_left)
from imu_sensor import get_yaw, update_yaw, rotate_to_yaw
from display_control import DisplayController
from led_control import LEDController
from buzzer_control import play_finish_sound, play_obstacle_sound

def wait_until_fire_disappears(fire_detector):
    """
    불이 시야에서 사라질 때까지 대기 (제한시간 없음!)
    """
    print("\n화재 모니터링 중... (불이 사라질 때까지 계속 대기)")

    display = DisplayController()
    display.show_face("alert")

    led_controller = LEDController(LED_RGB)
    led_controller.start_blink(interval=0.2)

    no_fire_count = 0
    required_count = 3

    while True:  # 제한시간 제거!
        if fire_detector.check_fire():
            print("여전히 불 감지 중...")
            no_fire_count = 0
        else:
            no_fire_count += 1
            print(f"불 미감지 ({no_fire_count}/{required_count})")

            if no_fire_count >= required_count:
                print("\n불이 시야에서 사라짐!")

                led_controller.stop_blink()
                display.show_face("normal")

                return True

        time.sleep(0.1)


def celebrate_fire_extinguished(display, led_controller):
    """
    화재 진압 완료 축하 시퀀스
    """
    print("\n화재 진압 완료")

    # 표정: 행복
    display.show_face("happy")

    # LED: 느린 깜빡임
    led_controller.start_blink(interval=0.5)

    play_finish_sound()

    # 3초 대기
    time.sleep(3)

    # LED 중지
    led_controller.stop_blink()

    # 표정: 기본으로
    display.show_face("normal")

    print("✓ 기본 상태로 복귀\n")


def check_obstacle_is_fire(fire_detector):
    """현재 전방 장애물이 불인지 확인"""
    print("장애물이 불인지 확인 중...")

    fire_count = 0
    check_count = 3

    for i in range(check_count):
        if fire_detector.check_fire():
            fire_count += 1
            print(f"    {i+1}/{check_count}: O")
        else:
            print(f"    {i+1}/{check_count}: O")
        time.sleep(0.15)

    is_fire = fire_count >= 2

    if is_fire:
        print(f"화재 장애물 ({fire_count}/{check_count})")
    else:
        print(f"일반 장애물 ({fire_count}/{check_count})")

    return is_fire

def count_black(L1, L2, R1, R2):
    """검은색 센서 개수 세기"""
    return (1 if L1 == 0 else 0) + (1 if L2 == 0 else 0) + \
           (1 if R1 == 0 else 0) + (1 if R2 == 0 else 0)


def avoid_obstacle_and_change_line(result):
    """라인 변경 방식으로 장애물 회피"""
    print("장애물 감지 → 라인 변경 회피 시작")
    car_stop()

    # LED 깜빡임으로 알림
    play_obstacle_sound()
    GPIO.output(LED_RGB, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(LED_RGB, GPIO.LOW)

    # [1단계] 기존 라인 벗어나기
    print("[1단계] 기존 라인 벗어나기")
    update_yaw()
    yaw_start = get_yaw()
    if (result == "left"):
        print(f"[1단계] 목표 각도: {yaw_start + 40:.2f}도로 회전")
        rotate_to_yaw(yaw_start + 40)
    else:
        print(f"[1단계] 목표 각도: {yaw_start - 40:.2f}도로 회전")
        rotate_to_yaw(yaw_start - 40)

    car_stop()
    time.sleep(0.2)

    # [2단계] 오른쪽으로 회전하며 전진 (라인 벗어나기)
    print("[2단계] 전진하며 장애물 벗어나기")
    avoid_start = time.time()

    while time.time() - avoid_start < 1.5:
        car_forward(60)

    car_stop()
    time.sleep(0.2)

    if (result == "left"):
        print(f"[3단계] 목표 각도: {yaw_start:.2f}도로 회전")
        rotate_to_yaw(yaw_start)
    else:
        print(f"[3단계] 목표 각도: {yaw_start:.2f}도로 회전")
        rotate_to_yaw(yaw_start)

    car_stop()
    time.sleep(0.2)

    # [4단계] 오른쪽으로 회전하며 전진 (라인 벗어나기)
    print("[4단계] 오른쪽으로 회전하며 라인 벗어나기")

    while True:
        car_forward(30)

        L1, L2, R1, R2 = read_line_sensors()
        if count_black(L1, L2, R1, R2) >= 2:
            print("라인 찾음")
            break

    car_stop()
    time.sleep(0.2)

    # [5단계] IMU 기반 정면 복원
    print("[5단계] IMU 기반 정면 복원")
    rotate_to_yaw(target_yaw=yaw_start)

    print("장애물 회피 완료\n")
    return True


def handle_obstacle_detection(fire_detector):
    """장애물 감지 및 처리 통합 함수"""
    dist = get_distance()

    if dist < 0 or dist > 30:
        return None, None

    print(f"\n장애물 감지! 거리: {dist:.1f}cm")

    car_stop()

    # LED 깜빡임으로 경고
    GPIO.output(LED_RGB, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(LED_RGB, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(LED_RGB, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(LED_RGB, GPIO.LOW)

    is_fire = check_obstacle_is_fire(fire_detector)

    if is_fire:
        success = wait_until_fire_disappears(fire_detector)
        play_obstacle_sound()
        return "fire", success
    else:
        direction=determine_avoidance_direction()
        success = avoid_obstacle_and_change_line(direction)
        return "normal", success

def determine_avoidance_direction():
    """IR 센서로 회피 방향 결정"""
    print("회피 방향 결정 중...")

    left_clear, right_clear = read_ir_sensors()

    # 둘 다 clear하면 왼쪽 우선
    if left_clear and right_clear:
        print("    → 양쪽 모두 여유 있음, 왼쪽 선택")
        return "left"
    elif left_clear:
        print("    → 오른쪽만 여유 있음")
        return "right"
    elif right_clear:
        print("    → 왼쪽만 여유 있음")
        return "left"
    else:
        # 둘 다 막혀있으면 오른쪽 (기본값)
        print("    → 양쪽 모두 막힘, 오른쪽 선택 (기본)")
        return "right"
