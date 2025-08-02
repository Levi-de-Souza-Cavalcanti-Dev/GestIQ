"""
Configurações centralizadas para o GestIQ
"""

# Configurações da câmera
CAMERA_CONFIG = {
    'width': 1280,
    'height': 720,
    'fps': 60
}

# Configurações do MediaPipe
MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'max_num_hands': 1,
    'min_detection_confidence': 0.9,
    'min_tracking_confidence': 0.7
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
    'copy': (255, 0, 255),          # Magenta
    'paste': (0, 255, 255),         # Ciano
    'move': (255, 165, 0),          # Laranja
    'resize': (128, 0, 128),        # Roxo
    'minimize': (255, 20, 147),     # Rosa
    'direct_control': (0, 128, 0),  # Verde escuro
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
    },
    "COPY_GESTURE": {
        "action": "copy",
        "description": "Copia texto selecionado (Ctrl+C)",
        "color": COLORS['copy']
    },
    "PASTE_GESTURE": {
        "action": "paste",
        "description": "Cola texto (Ctrl+V)",
        "color": COLORS['paste']
    },
    "MOVE_WINDOW": {
        "action": "move_window",
        "description": "Move janela ativa",
        "color": COLORS['move']
    },
    "RESIZE_WINDOW": {
        "action": "resize_window", 
        "description": "Redimensiona janela ativa",
        "color": COLORS['resize']
    },
    "MINIMIZE_WINDOW": {
        "action": "minimize_window",
        "description": "Minimiza janela ativa",
        "color": COLORS['minimize']
    },
    "DIRECT_WINDOW_CONTROL": {
        "action": "direct_window_control",
        "description": "Controle direto de janela com mão",
        "color": COLORS['direct_control']
    }
}

# Configurações de debug
DEBUG_CONFIG = {
    'show_landmarks': True,
    'show_fps': True,
    'show_gesture_info': True,
    'log_level': 'ERROR'
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'max_fps': 30,
    'frame_skip': 1,
    'enable_gpu': False
} 