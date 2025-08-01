"""
GestIQ - Sistema de Controle por Gestos
Controla aplicações do computador através de gestos das mãos usando OpenCV e MediaPipe.
"""

import cv2
import mediapipe as mp
import numpy as np
import subprocess
import time
import os
from typing import Optional, Tuple, Dict, Any

# Constantes de configuração
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
ACTION_COOLDOWN = 2.0  # segundos entre ações
OK_GESTURE_DISTANCE = 0.05  # distância máxima para gesto OK
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5

# Configurações de cores para interface
COLORS = {
    'ok_gesture': (0, 255, 0),    # Verde
    'thumbs_up': (255, 0, 0),     # Vermelho
    'text': (255, 255, 255)       # Branco
}

# Ações disponíveis
ACTIONS = {
    "OK": "notepad.exe",
    "THUMBS_UP": "calc.exe"
}


class GestureController:
    """
    Controlador principal para detecção e execução de gestos.
    
    Atributos:
        mp_hands: Configuração do MediaPipe para detecção de mãos
        mp_drawing: Utilitários de desenho do MediaPipe
        hands: Instância do detector de mãos
        cap: Captura de vídeo da câmera
        last_action_time: Timestamp da última ação executada
        action_cooldown: Tempo mínimo entre ações
        gesture_detected: Flag indicando se um gesto foi detectado
    """
    
    def __init__(self) -> None:
        """Inicializa o controlador de gestos."""
        self._setup_mediapipe()
        self._setup_camera()
        self._setup_controls()
    
    def _setup_mediapipe(self) -> None:
        """Configura o MediaPipe para detecção de mãos."""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
    
    def _setup_camera(self) -> None:
        """Configura a captura de vídeo da câmera."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("❌ Não foi possível acessar a câmera")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    def _setup_controls(self) -> None:
        """Configura variáveis de controle."""
        self.last_action_time = 0
        self.action_cooldown = ACTION_COOLDOWN
        self.gesture_detected = False
    
    def _get_landmark_points(self, landmarks) -> Dict[str, Any]:
        """
        Extrai pontos-chave dos landmarks da mão.
        
        Args:
            landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            Dicionário com os pontos-chave dos dedos
        """
        return {
            'thumb_tip': landmarks[4],
            'thumb_ip': landmarks[3],
            'thumb_mcp': landmarks[2],
            'index_tip': landmarks[8],
            'index_pip': landmarks[6],
            'middle_tip': landmarks[12],
            'middle_pip': landmarks[10],
            'ring_tip': landmarks[16],
            'ring_pip': landmarks[14],
            'pinky_tip': landmarks[20],
            'pinky_pip': landmarks[18]
        }
    
    def detect_ok_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de OK (polegar e indicador formando um círculo).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto OK for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Calcular distância entre polegar e indicador
        thumb_index_distance = np.sqrt(
            (points['thumb_tip'].x - points['index_tip'].x)**2 + 
            (points['thumb_tip'].y - points['index_tip'].y)**2
        )
        
        # Verificar se outros dedos estão estendidos
        other_fingers_extended = (
            points['middle_tip'].y < points['middle_pip'].y and
            points['ring_tip'].y < points['ring_pip'].y and
            points['pinky_tip'].y < points['pinky_pip'].y
        )
        
        return thumb_index_distance < OK_GESTURE_DISTANCE and other_fingers_extended
    
    def detect_thumbs_up(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de joinha (polegar para cima).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o joinha for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se o polegar está para cima
        thumb_up = (points['thumb_tip'].y < points['thumb_ip'].y < 
                   points['thumb_mcp'].y)
        
        # Verificar se outros dedos estão fechados
        other_fingers_closed = (
            points['index_tip'].y > points['index_pip'].y and
            points['middle_tip'].y > points['middle_pip'].y and
            points['ring_tip'].y > points['ring_pip'].y and
            points['pinky_tip'].y > points['pinky_pip'].y
        )
        
        return thumb_up and other_fingers_closed
    
    def execute_action(self, gesture_type: str) -> None:
        """
        Executa ações baseadas no gesto detectado.
        
        Args:
            gesture_type: Tipo do gesto detectado
        """
        current_time = time.time()
        
        # Evitar ações repetidas em sequência
        if current_time - self.last_action_time < self.action_cooldown:
            return
        
        self.last_action_time = current_time
        
        if gesture_type in ACTIONS:
            app_name = ACTIONS[gesture_type]
            print(f"🎯 Gesto {gesture_type} detectado! Abrindo {app_name}...")
            
            try:
                subprocess.Popen([app_name], shell=True)
            except Exception as e:
                print(f"❌ Erro ao abrir {app_name}: {e}")
        else:
            print(f"⚠️  Ação não definida para gesto: {gesture_type}")
    
    def _draw_gesture_text(self, frame: np.ndarray, text: str, color: Tuple[int, int, int]) -> None:
        """
        Desenha texto do gesto detectado no frame.
        
        Args:
            frame: Frame da câmera
            text: Texto a ser desenhado
            color: Cor do texto (B, G, R)
        """
        cv2.putText(frame, text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    def _process_gestures(self, hand_landmarks, frame: np.ndarray) -> None:
        """
        Processa gestos detectados e executa ações correspondentes.
        
        Args:
            hand_landmarks: Landmarks da mão
            frame: Frame da câmera
        """
        if self.detect_ok_gesture(hand_landmarks):
            self._draw_gesture_text(frame, "OK GESTURE", COLORS['ok_gesture'])
            if not self.gesture_detected:
                self.execute_action("OK")
                self.gesture_detected = True
                
        elif self.detect_thumbs_up(hand_landmarks):
            self._draw_gesture_text(frame, "THUMBS UP", COLORS['thumbs_up'])
            if not self.gesture_detected:
                self.execute_action("THUMBS_UP")
                self.gesture_detected = True
        else:
            self.gesture_detected = False
    
    def _print_instructions(self) -> None:
        """Imprime instruções de uso do programa."""
        print("🚀 Iniciando Sistema de Controle por Gestos")
        print("📋 Comandos disponíveis:")
        print("   👌 Gesto OK → Abre o Notepad")
        print("   👍 Joinha → Abre a Calculadora")
        print("   🖐️  Mão aberta → Para o programa")
        print("\nPressione 'q' para sair")
    
    def run(self) -> None:
        """Loop principal do programa."""
        self._print_instructions()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Erro ao acessar câmera")
                    break
                
                # Converter BGR para RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                # Processar landmarks das mãos
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                        )
                        self._process_gestures(hand_landmarks, frame)
                else:
                    self.gesture_detected = False
                
                # Mostrar frame
                cv2.imshow("Controle por Gestos - GestIQ", frame)
                
                # Verificar tecla de saída
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Programa interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
        finally:
            self._cleanup()
    
    def _cleanup(self) -> None:
        """Limpa recursos do programa."""
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()
        print("👋 Programa finalizado!")


def main() -> None:
    """Função principal do programa."""
    try:
        controller = GestureController()
        controller.run()
    except Exception as e:
        print(f"❌ Erro ao inicializar programa: {e}")


if __name__ == "__main__":
    main() 