import time
from sensor_utils import read_line_sensors, count_black, get_direction
from motor_control import car_forward, car_turn_left, car_turn_right, car_stop, motor_control
from imu_sensor import update_yaw, get_yaw, rotate_to_yaw

# 기본 라인트래킹
def basic_line_tracking():
    update_yaw()

    L1, L2, R1, R2 = read_line_sensors()
    black = count_black(L1, L2, R1, R2)
    direction = get_direction(L1, L2, R1, R2)

    print(f"L1:{L1} L2:{L2} | R1:{R1} R2:{R2} | black={black}")

    if black == 3:
        print("교차점 감지 - 90도 회전 시퀀스 시작")

        # 1단계: 정지
        print("[1단계] 정지")
        car_stop()
        time.sleep(0.3)

        # 2단계: 방향에 따라 90도 회전
        print(f"[2단계] {direction} 방향으로 90도 회전")

        if direction == "left":
            print(f"  왼쪽 90도 회전 시작")
            rotate_to_yaw(45)  # 제자리 좌회전
            time.sleep(1.0)
            car_stop()
        elif direction == "right":
            print(f"  오른쪽 90도 회전 시작")
            rotate_to_yaw(-45)  # 제자리 우회전
            time.sleep(1.0)
            car_stop()
        else:
            print(f"  중앙 감지 - 직진 유지")
            car_forward(50)
            time.sleep(0.5)

        car_stop()
        time.sleep(0.2)

    elif black == 2:
        if direction == "left":
            car_turn_left(50)
        elif direction == "right":
            car_turn_right(50)
        else:
            car_forward(40)

    elif black == 1:
        yaw_before = get_yaw()

        if L1 == 0:
            rotate_to_yaw(yaw_before + 5)
            print("와리가리 왼쪽")
        elif L2 == 0:
            rotate_to_yaw(yaw_before + 5)
            print("와리가리 왼쪽")
        elif R1 == 0:
            rotate_to_yaw(yaw_before - 5)
            print("와리가리 오쪽")
        elif R2 == 0:
            rotate_to_yaw(yaw_before - 5)
            print("와리가리 오쪽")

    else:
        if black == 0:
            search_lost_line()
        else: # black == 4
            car_forward(40)
            time.sleep(0.2)

# 라인 놓쳤을 때 재탐색
def search_lost_line():
    print("라인 완전 놓침 -> 좌우 탐색")

    # 왼쪽부터 탐색
    print("왼쪽 탐색 중...")
    rotate_start = time.time()
    while time.time() - rotate_start < 1.0:
        car_turn_left(55)
        L1, L2, R1, R2 = read_line_sensors()
        if count_black(L1, L2, R1, R2) >= 1:  # 라인 찾으면
            print("왼쪽에서 라인 발견!")
            car_stop() # 더 가지 말고 멈추기
            return
        time.sleep(0.05)

    car_stop()
    time.sleep(0.1)

    # 다음으로 오른쪽 탐색
    L1, L2, R1, R2 = read_line_sensors()
    if count_black(L1, L2, R1, R2) == 0:
        print("오른쪽 탐색 중...")
        rotate_start = time.time()
        while time.time() - rotate_start < 2.0:
            car_turn_right(55)
            L1, L2, R1, R2 = read_line_sensors()
            if count_black(L1, L2, R1, R2) >= 1:  # 라인 찾으면
                print("오른쪽에서 라인 발견!")
                car_stop()  # 더 가지 말고 멈추기
                return
            time.sleep(0.05)

    car_stop()
