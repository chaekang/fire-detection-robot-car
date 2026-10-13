# fire_detection.py - 원래 코드 그대로 클래스로만 감쌈
import socket
import cv2
import struct
import pickle
from picamera2 import Picamera2
import time

class FireDetector:
    def __init__(self):
        self.SERVER_IP = "192.168.1.8"
        self.SERVER_PORT = 8000
        self.sock = None
        self.picam2 = None

    def connect_to_server(self):
        """서버 연결"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[PI] 서버 연결 시도...")
        self.sock.connect((self.SERVER_IP, self.SERVER_PORT))
        print("[PI] 서버 연결 성공!")
        return True

    def init_camera(self):
        """카메라 설정"""
        self.picam2 = Picamera2()
        config = self.picam2.create_video_configuration(main={"size": (640, 480)})
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)
        print("[PI] 카메라 시작됨.")
        return True

    def check_fire(self):
        """불 감지 (원래 while True 안의 코드)"""
        frame = self.picam2.capture_array()               # numpy 이미지
        _, jpeg = cv2.imencode(".jpg", frame)             # JPEG 변환
        data = pickle.dumps(jpeg, protocol=pickle.HIGHEST_PROTOCOL)
        length = struct.pack(">L", len(data))             # 4바이트 길이

        # ==== PC로 영상 송신 ====
        self.sock.sendall(length + data)

        # ==== PC로부터 YOLO 결과 수신 ====
        result = self.sock.recv(2).decode()

        if (result == "1"):
            print("Fire detected!")
            return True
        else:
            print("No fire")
            return False

    def close(self):
        """종료"""
        self.picam2.stop()
        self.sock.close()
        print("종료됨.")
