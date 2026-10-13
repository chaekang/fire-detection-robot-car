# 외부 의존성과 라이선스 확인 사항

확인일: 2026-10-13. 소스의 import, 원본 파일 목록과 각 프로젝트의 공개 라이선스 자료를 기준으로 정리했습니다. 실제 라즈베리파이의 설치 패키지와 버전은 확보하지 못했습니다. 따라서 아래 목록은 모든 전이 의존성을 포함한 확정된 라이선스 명세가 아닙니다.

## 저장소의 적용 범위

- `LICENSE`의 MIT 조건은 팀이 작성한 이 프로젝트의 코드에 적용합니다.
- MIT 선언은 프로젝트 작성자의 기여분에 적용합니다. 외부에서 가져온 코드가 확인되거나 추가되면 원본 저작권 표시와 라이선스를 유지하고 이 문서를 갱신해야 합니다.
- 현재 저장소에는 아래 라이브러리의 소스나 바이너리, 가상환경, OS 이미지, YOLO 서버 파일, 모델과 데이터셋을 포함하지 않습니다.
- 직접 의존성 이름과 출처를 기록하는 것만으로 모든 재배포 의무가 충족되는 것은 아닙니다. 해당 구성요소를 함께 배포할 때는 실제 버전의 라이선스 원문, 저작권 표시, NOTICE 및 필요한 소스 제공 조건을 확인해야 합니다.

## 직접 의존성

| 구성요소 | 코드에서의 사용 | 공개 라이선스 자료 |
|---|---|---|
| RPi.GPIO | GPIO 입력·출력과 PWM | [MIT / 패키지 정보](https://pypi.org/project/RPi.GPIO/) |
| smbus / python3-smbus | I2C 장치 접근 | [GPLv2 / 패키지 정보](https://pypi.org/project/smbus/) |
| OpenCV | 프레임 JPEG 인코딩 | [4.5.0 이상 Apache-2.0, 4.4.0 이하 BSD-3-Clause](https://opencv.org/license/) |
| Picamera2 | 라즈베리파이 카메라 입력 | [BSD-2-Clause / 원문](https://github.com/raspberrypi/picamera2/blob/main/LICENSE) |
| luma.core | OLED I2C 연결과 렌더링 | [MIT / 원문](https://github.com/rm-hull/luma.core/blob/main/LICENSE.rst) |
| luma.oled | SSD1306 드라이버 | [MIT / 원문](https://github.com/rm-hull/luma.oled/blob/main/LICENSE.rst) |
| Pillow | OLED 글꼴 렌더링 | [현재 원문은 MIT-CMU 표기](https://github.com/python-pillow/Pillow/blob/main/LICENSE). 설치 버전의 원문을 우선합니다. |

`time`, `threading`, `socket`, `struct`, `pickle`은 Python 표준 라이브러리입니다. Python 런타임 자체를 재배포한다면 [PSF 라이선스와 관련 조건](https://docs.python.org/3/license.html)을 확인하세요.

## smbus의 GPL 조건

`config.py`는 `smbus`를 import하고 직접 함수를 호출합니다. 공개 패키지에는 GPLv2로 표시되어 있으며, MIT로 작성한 자체 소스라는 사실만으로 결합된 프로그램을 배포할 때의 GPL 조건이 없어지지는 않습니다.

실제 사용한 패키지의 라이선스 원문과 결합·배포 범위를 확인해야 합니다. GPLv2-only인지 이후 버전 선택이 가능한지도 실제 파일로 확인하세요. GPL 조건이 적용되는 결합물을 배포한다면 해당 조건에 맞는 소스와 고지를 제공해야 합니다. 이를 확인하지 않은 채 프로젝트 전체를 GPLv3 또는 AGPLv3로 바꿔서도 안 됩니다.

참고: [GNU FAQ의 결합 프로그램과 호환 라이선스 설명](https://www.gnu.org/licenses/gpl-faq.en.html#GPLAndPlugins).

## 별도 YOLO 서버와 모델

원 프로젝트는 별도 PC에서 YOLOv8 기반 화재 판정 서버를 사용했습니다. 이 저장소의 `fire_detection.py`는 TCP로 프레임을 보내고 응답을 받는 클라이언트입니다. 원 서버 소스, `best.pt`, 모델 출처, 학습 데이터 및 사용 버전은 확보하지 못했습니다.

[Ultralytics 공식 안내](https://www.ultralytics.com/license)는 YOLO 코드와 모델에 AGPL-3.0 또는 Enterprise 조건을 제시합니다. 이후 서버나 모델을 추가하려면 원본 저장소, 모델 및 데이터의 조건을 확인하고, 해당하는 소스 제공과 고지 의무를 이행해야 합니다. MIT 파일 하나로 이 조건을 대체할 수 없습니다.

TCP로 통신한다는 사실만으로 라즈베리파이 코드 전체의 라이선스가 자동 결정되지는 않습니다. 프로그램들이 별도 저작물인지 하나의 결합물인지는 통신 내용과 결합 방식도 고려해야 합니다. 참고: [GNU FAQ의 별도 프로그램과 결합물 설명](https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation).

## 시스템 글꼴

`display_control.py`는 OS에 설치된 `DejaVuSansMono.ttf`를 참조합니다. 글꼴 파일 자체는 이 저장소에 포함하지 않습니다. 이후 글꼴을 함께 배포한다면 [DejaVu 글꼴 라이선스](https://dejavu-fonts.github.io/License.html)의 저작권 표시와 조건을 확인하세요.
