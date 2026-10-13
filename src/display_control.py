# display_control.py - OLED 디스플레이 제어
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time
import threading

class DisplayController:
    def __init__(self):
        try:
            serial = i2c(port=1, address=0x3c)
            self.device = ssd1306(serial)

            try:
                self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 60)
            except:
                self.font = ImageFont.load_default()

            self.current_face = "normal"
            print("OLED 디스플레이 초기화 완료")
        except Exception as e:
            print(f"OLED 초기화 실패: {e}")
            self.device = None

    def show_face(self, face_type):
        """표정 표시"""
        if not self.device:
            return

        faces = {
            "normal": "◑.◑",    # 기본 상태
            "alert": "◑O◑",     # 불 감지
            "happy": "◑v◑",     # 불 소각
        }

        face = faces.get(face_type, "◑.◑")
        self.current_face = face_type

        with canvas(self.device) as draw:
            draw.text((10, 0), face, fill="white", font=self.font)

    def clear(self):
        """화면 지우기"""
        if self.device:
            self.device.clear()

    def close(self):
        """디스플레이 종료"""
        self.clear()
        print("✓ OLED 디스플레이 종료")
