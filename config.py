import cv2

# Camera Settings
CAMERA_ID = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# Detection Settings
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5
PROCESS_EVERY_N_FRAMES = 2  # Optimize performance by processing every N frames

# Speech Settings
SPEECH_LANG = 'id'
SPEAK_INTERVAL = 3.0  # Seconds between repeats of same gesture
SPEECH_RATE = 1.0

# UI Settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
OVERLAY_ALPHA = 0.6  # Transparency of UI overlay

# Gesture Dictionary
# Mapping: Gesture Name -> (Speech Text, UI Color)
GESTURES = {
    "halo": {
        "text": "Halo! Senang bertemu denganmu.",
        "color": (0, 255, 0),  # Green
        "icon": "👋"
    },
    "perkenalan": {
        "text": "Perkenalkan, saya adalah Khalifa.",
        "color": (255, 255, 0),  # Cyan
        "icon": "✌️"
    },
    "salam": {
        "text": "Salam kenal ya, semoga harimu menyenangkan.",
        "color": (255, 0, 255),  # Magenta
        "icon": "🤝"
    },
    "terima": {
        "text": "Terimakasih banyak! Sampai jumpa lagi.",
        "color": (0, 165, 255),  # Orange
        "icon": "🖐️"
    },
    "baik": {
        "text": "Baik, saya mengerti. Siap dilaksanakan!",
        "color": (0, 255, 255),  # Yellow
        "icon": "👍"
    },
    "tidak": {
        "text": "Maaf, saya tidak setuju atau itu salah.",
        "color": (0, 0, 255),  # Red
        "icon": "👎"
    },
    "semangat": {
        "text": "Tetap semangat! Kamu pasti bisa!",
        "color": (0, 0, 139),  # Dark Red
        "icon": "✊"
    },
    "ok": {
        "text": "Oke sip! Semuanya aman.",
        "color": (255, 105, 180),  # Pink
        "icon": "👌"
    },
    "love": {
        "text": "I love you! Sayang kamu.",
        "color": (147, 20, 255),  # Deep Pink
        "icon": "🤟"
    },
     "diam": {
        "text": "Mohon tenang sejenak.",
        "color": (128, 128, 128),  # Gray
        "icon": "🤫"
    }
}
