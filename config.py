"""
Configurações centralizadas para o GestIQ
"""

# Configurações da câmera
CAMERA_CONFIG = {
    'width': 640,
    'height': 480,
    'fps': 30
}

# Configurações do MediaPipe
MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'max_num_hands': 1,
    'min_detection_confidence': 0.7,
    'min_tracking_confidence': 0.5
}

# Configurações de gestos
GESTURE_CONFIG = {
    'ok_distance': 0.05,  # Distância máxima para gesto OK
    'action_cooldown': 2.0,  # Segundos entre ações
    'min_gesture_duration': 0.5  # Duração mínima para confirmar gesto
}

# Cores para interface
COLORS = {
    'ok_gesture': (0, 255, 0),      # Verde
    'thumbs_up': (255, 0, 0),       # Vermelho
    'peace_sign': (0, 255, 255),    # Amarelo
    'fist': (255, 255, 0),          # Ciano
    'text': (255, 255, 255),        # Branco
    'background': (0, 0, 0)         # Preto
}

# Ações disponíveis
ACTIONS = {
    "OK": {
        "app": "notepad.exe",
        "description": "Abre o Notepad",
        "color": COLORS['ok_gesture']
    },
    "THUMBS_UP": {
        "app": "calc.exe",
        "description": "Abre a Calculadora",
        "color": COLORS['thumbs_up']
    },
    "PEACE_SIGN": {
        "app": "mspaint.exe",
        "description": "Abre o Paint",
        "color": COLORS['peace_sign']
    },
    "FIST": {
        "app": "taskmgr.exe",
        "description": "Abre o Gerenciador de Tarefas",
        "color": COLORS['fist']
    }
}

# Configurações de debug
DEBUG_CONFIG = {
    'show_landmarks': True,
    'show_fps': True,
    'show_gesture_info': True,
    'log_level': 'INFO'
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'max_fps': 30,
    'frame_skip': 1,
    'enable_gpu': False
} 