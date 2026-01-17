# 🦈 Baby Shark

영유아(7개월 전후)를 위한 인터랙티브 게임입니다. 웹캠 손 추적 기술을 활용하여 아기의 손 움직임을 화면 속 귀여운 상어가 따라다니며, 손과 눈의 협응력과 인과관계 이해력 발달에 도움을 줍니다.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 주요 기능

- **실시간 손 추적**: Google MediaPipe를 사용한 정확한 손바닥 인식
- **부드러운 애니메이션**: 꼬리가 헤엄치듯 움직이는 스프라이트 애니메이션
- **동적 움직임**: 상어가 이동 방향을 향해 자연스럽게 회전
- **속도 기반 애니메이션**: 빠르게 움직일수록 꼬리가 빠르게 흔들림
- **전체 화면**: 몰입감 있는 테두리 없는 최대화 창
- **고화질 카메라**: 1920x1080 해상도 지원

## 🎮 작동 방식

1. 게임이 웹캠 영상을 배경으로 표시합니다
2. 카메라 앞에서 손을 움직여보세요
3. 상어가 손의 움직임을 따라갑니다
4. 상어가 빨리 헤엄칠수록 꼬리가 빠르게 움직입니다

## 📋 요구 사항

- Python 3.8 - 3.11 (Python 3.12 이상은 호환성 문제가 있을 수 있음)
- 웹캠
- Windows / macOS / Linux

## 🚀 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/x3r0s/babyshark-game.git
cd babyshark-game
```

### 2. Python 환경 설정 (권장: Python 3.10)

```bash
# pyenv 사용 시 (권장)
pyenv install 3.10.11
pyenv local 3.10.11

# 또는 시스템 Python이 3.8-3.11이면 그대로 사용
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 게임 실행

```bash
python main.py
```

**ESC** 키를 눌러 게임을 종료합니다.

## 📁 프로젝트 구조

```
babyshark-game/
├── main.py              # 진입점 - 게임 루프
├── requirements.txt     # Python 의존성
├── game/                # 게임 모듈
│   ├── __init__.py      # 패키지 초기화
│   ├── config.py        # 설정 상수
│   ├── camera.py        # 웹캠 캡처 및 처리
│   ├── hand_tracking.py # MediaPipe 손 인식
│   └── shark.py         # 상어 엔티티 및 AI, 애니메이션
└── assets/              # 게임 에셋
    ├── shark-left.png   # 꼬리 왼쪽 프레임
    ├── shark-middle.png # 꼬리 중앙 프레임
    └── shark-right.png  # 꼬리 오른쪽 프레임
```

## ⚙️ 설정

`game/config.py`를 수정하여 게임을 커스터마이징할 수 있습니다:

### 화면 설정
| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DEFAULT_WIDTH` | 1200 | 기본 창 너비 |
| `DEFAULT_HEIGHT` | 800 | 기본 창 높이 |
| `GAME_TITLE` | "Baby Shark" | 창 제목 |

### 상어 설정
| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SHARK_SIZE` | 200 | 상어 스프라이트 너비 (픽셀) |
| `MAX_SPEED` | 10 | 최대 이동 속도 |
| `ACCEL` | 0.5 | 가속도 |
| `DAMPING` | 0.95 | 속도 감쇠 (마찰) |

### 손 추적
| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MIN_DETECTION_CONFIDENCE` | 0.7 | 손 인식 민감도 |
| `MIN_TRACKING_CONFIDENCE` | 0.5 | 추적 정확도 임계값 |

## 🎨 커스텀 에셋

나만의 상어 이미지를 사용하려면:

1. 꼬리 애니메이션용 PNG 이미지 3개 생성:
   - `shark-left.png` - 꼬리가 왼쪽을 향함
   - `shark-middle.png` - 꼬리가 중앙
   - `shark-right.png` - 꼬리가 오른쪽을 향함

2. `assets/` 폴더에 배치

3. 이미지는 상어 머리가 위(12시 방향)를 향하도록 제작

## 🔧 문제 해결

### "No module named 'cv2'" 또는 MediaPipe 오류
```bash
# Python 3.10 사용 (최신 버전 대신)
pyenv local 3.10.11
pip install -r requirements.txt
```

### 카메라가 감지되지 않음
- 다른 앱이 웹캠을 사용 중인지 확인
- `game/camera.py`에서 `camera_index=0`을 `camera_index=1`로 변경 시도

### 프레임 레이트가 낮음
- 다른 앱 종료
- `game/camera.py`에서 카메라 해상도 낮추기
- 손 인식을 위한 충분한 조명 확보

## 🧑‍💻 개발

### 테스트 실행
```bash
python test_imports.py
```

### 새 기능 추가
모듈화된 구조로 쉽게 확장 가능:
- `game/`에 새 엔티티 추가
- `shark.py`에서 AI 동작 수정
- `config.py`에서 물리 조정

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE) 하에 오픈 소스로 제공됩니다.

## 🙏 감사의 말

- [MediaPipe](https://mediapipe.dev/) - Google의 손 추적 솔루션
- [Pygame](https://www.pygame.org/) - 게임 개발 라이브러리
- [OpenCV](https://opencv.org/) - 카메라 캡처 및 이미지 처리

## 👨‍👩‍👧 부모님께

**안전 수칙:**
- 영아의 화면 시간을 제한하세요 (AAP는 18개월 미만 아동의 화면 시간을 최소화할 것을 권장)
- 적절한 화면 밝기 유지
- 화면과 적절한 거리 유지
- 수동적 시청이 아닌 상호작용적 유대 활동으로 활용하세요

---

Made with ❤️ for babies everywhere 🦈
