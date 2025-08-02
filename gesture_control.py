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
import pyautogui
from typing import Tuple, Dict, Any

# Importar configurações centralizadas
try:
    from config import (
        CAMERA_CONFIG, MEDIAPIPE_CONFIG, GESTURE_CONFIG,
        COLORS, ACTIONS, DEBUG_CONFIG, PERFORMANCE_CONFIG
    )
    print("✅ Configurações carregadas do config.py")
except ImportError:
    print("⚠️  Arquivo config.py não encontrado. Usando configurações padrão.")
    CAMERA_CONFIG = {'width': 640, 'height': 480, 'fps': 30}
    MEDIAPIPE_CONFIG = {
        'static_image_mode': False,
        'max_num_hands': 1,
        'min_detection_confidence': 0.7,
        'min_tracking_confidence': 0.5
    }
    GESTURE_CONFIG = {
        'ok_distance': 0.05,
        'action_cooldown': 2.0,
        'min_gesture_duration': 0.5
    }
    COLORS = {
        'ok_gesture': (0, 255, 0),
        'thumbs_up': (255, 0, 0),
        'text': (255, 255, 255)
    }
    ACTIONS = {
        "OK": {"app": "notepad.exe", "description": "Abre o Notepad"},
        "THUMBS_UP": {"app": "calc.exe", "description": "Abre a Calculadora"}
    }
    DEBUG_CONFIG = {'show_landmarks': True, 'show_fps': True, 'show_gesture_info': True}
    PERFORMANCE_CONFIG = {'max_fps': 30, 'frame_skip': 1, 'enable_gpu': False}

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
            static_image_mode=MEDIAPIPE_CONFIG['static_image_mode'],
            max_num_hands=MEDIAPIPE_CONFIG['max_num_hands'],
            min_detection_confidence=MEDIAPIPE_CONFIG['min_detection_confidence'],
            min_tracking_confidence=MEDIAPIPE_CONFIG['min_tracking_confidence']
        )
    
    def _setup_camera(self) -> None:
        """Configura a captura de vídeo da câmera."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("❌ Não foi possível acessar a câmera")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['height'])
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
    
    def _setup_controls(self) -> None:
        """Configura variáveis de controle."""
        self.last_action_time = 0
        self.action_cooldown = GESTURE_CONFIG['action_cooldown']
        self.gesture_detected = False
        self.running = True
        
        # Configurações de debug e performance
        self.show_landmarks = DEBUG_CONFIG['show_landmarks']
        self.show_fps = DEBUG_CONFIG['show_fps']
        self.show_gesture_info = DEBUG_CONFIG['show_gesture_info']
        self.max_fps = PERFORMANCE_CONFIG['max_fps']
        self.frame_skip = PERFORMANCE_CONFIG['frame_skip']
        self.frame_count = 0
        
        # Controle direto de janela
        self.direct_control_active = False
        self.last_hand_position = None
        self.window_initial_position = None
        self.last_window_move_time = 0  # Cooldown para movimentos de janela
    
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
        
        return thumb_index_distance < GESTURE_CONFIG['ok_distance'] and other_fingers_extended
    
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
    
    def detect_copy_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de copiar (indicador e médio estendidos, outros fechados).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto de copiar for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se indicador e médio estão estendidos (com tolerância)
        index_extended = points['index_tip'].y < points['index_pip'].y - 0.02
        middle_extended = points['middle_tip'].y < points['middle_pip'].y - 0.02
        
        # Verificar se outros dedos estão fechados (com tolerância)
        thumb_closed = points['thumb_tip'].y > points['thumb_ip'].y - 0.01
        ring_closed = points['ring_tip'].y > points['ring_pip'].y - 0.01
        pinky_closed = points['pinky_tip'].y > points['pinky_pip'].y - 0.01
        
        # Debug: imprimir valores para verificar
        if DEBUG_CONFIG.get('log_level', 'INFO') == 'DEBUG':
            print(f"Copy Debug - Index: {index_extended}, Middle: {middle_extended}")
            print(f"Thumb: {thumb_closed}, Ring: {ring_closed}, Pinky: {pinky_closed}")
        
        return (index_extended and middle_extended and 
                thumb_closed and ring_closed and pinky_closed)
    
    def detect_paste_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de colar (polegar e indicador em V, outros fechados).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto de colar for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se polegar e indicador estão estendidos (formando V)
        thumb_extended = points['thumb_tip'].y < points['thumb_ip'].y - 0.02
        index_extended = points['index_tip'].y < points['index_pip'].y - 0.02
        
        # Verificar se outros dedos estão fechados
        middle_closed = points['middle_tip'].y > points['middle_pip'].y - 0.01
        ring_closed = points['ring_tip'].y > points['ring_pip'].y - 0.01
        pinky_closed = points['pinky_tip'].y > points['pinky_pip'].y - 0.01
        
        # Debug: imprimir valores para verificar
        if DEBUG_CONFIG.get('log_level', 'INFO') == 'DEBUG':
            print(f"Paste Debug - Thumb: {thumb_extended}, Index: {index_extended}")
            print(f"Middle: {middle_closed}, Ring: {ring_closed}, Pinky: {pinky_closed}")
        
        return (thumb_extended and index_extended and 
                middle_closed and ring_closed and pinky_closed)
    
    def detect_move_window_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de mover janela (indicador, médio e anelar estendidos).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto de mover janela for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se indicador, médio e anelar estão estendidos
        index_extended = points['index_tip'].y < points['index_pip'].y - 0.02
        middle_extended = points['middle_tip'].y < points['middle_pip'].y - 0.02
        ring_extended = points['ring_tip'].y < points['ring_pip'].y - 0.02
        
        # Verificar se outros dedos estão fechados
        thumb_closed = points['thumb_tip'].y > points['thumb_ip'].y - 0.01
        pinky_closed = points['pinky_tip'].y > points['pinky_pip'].y - 0.01
        
        return (index_extended and middle_extended and ring_extended and 
                thumb_closed and pinky_closed)
    
    def detect_resize_window_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de redimensionar janela (polegar, indicador e médio estendidos).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto de redimensionar for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se polegar, indicador e médio estão estendidos
        thumb_extended = points['thumb_tip'].y < points['thumb_ip'].y - 0.02
        index_extended = points['index_tip'].y < points['index_pip'].y - 0.02
        middle_extended = points['middle_tip'].y < points['middle_pip'].y - 0.02
        
        # Verificar se outros dedos estão fechados
        ring_closed = points['ring_tip'].y > points['ring_pip'].y - 0.01
        pinky_closed = points['pinky_tip'].y > points['pinky_pip'].y - 0.01
        
        return (thumb_extended and index_extended and middle_extended and 
                ring_closed and pinky_closed)
    
    def detect_minimize_window_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de minimizar janela (polegar para baixo, outros fechados).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto de minimizar for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se o polegar está para baixo
        thumb_down = (points['thumb_tip'].y > points['thumb_ip'].y > 
                     points['thumb_mcp'].y)
        
        # Verificar se outros dedos estão fechados
        other_fingers_closed = (
            points['index_tip'].y > points['index_pip'].y and
            points['middle_tip'].y > points['middle_pip'].y and
            points['ring_tip'].y > points['ring_pip'].y and
            points['pinky_tip'].y > points['pinky_pip'].y
        )
        
        return thumb_down and other_fingers_closed
    
    def detect_direct_window_control_gesture(self, hand_landmarks) -> bool:
        """
        Detecta o gesto de controle direto de janela (mão aberta).
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            
        Returns:
            True se o gesto de controle direto for detectado, False caso contrário
        """
        if not hand_landmarks:
            return False
        
        points = self._get_landmark_points(hand_landmarks.landmark)
        
        # Verificar se todos os dedos estão estendidos (mão aberta)
        thumb_extended = points['thumb_tip'].y < points['thumb_ip'].y - 0.02
        index_extended = points['index_tip'].y < points['index_pip'].y - 0.02
        middle_extended = points['middle_tip'].y < points['middle_pip'].y - 0.02
        ring_extended = points['ring_tip'].y < points['ring_pip'].y - 0.02
        pinky_extended = points['pinky_tip'].y < points['pinky_pip'].y - 0.02
        
        return (thumb_extended and index_extended and middle_extended and 
                ring_extended and pinky_extended)
    
    def _process_direct_window_control(self, hand_landmarks, frame: np.ndarray) -> None:
        """
        Processa controle direto de janela baseado na posição da mão.
        
        Args:
            hand_landmarks: Landmarks da mão
            frame: Frame da câmera
        """
        if not self.direct_control_active:
            return
        
        # Obter posição atual da mão (usar o ponto médio da palma)
        palm_center_x = hand_landmarks.landmark[9].x  # Ponto médio da palma
        palm_center_y = hand_landmarks.landmark[9].y
        
        # Converter para coordenadas da tela
        screen_width, screen_height = pyautogui.size()
        screen_x = int(palm_center_x * screen_width)
        screen_y = int(palm_center_y * screen_height)
        
        # Calcular movimento relativo
        if self.last_hand_position is not None:
            delta_x = screen_x - self.last_hand_position[0]
            delta_y = screen_y - self.last_hand_position[1]
            
            # Mover janela ativa usando Win+Setas (muito mais confiável!)
            try:
                current_time = time.time()
                # Cooldown de 1.0 segundo entre movimentos (muito mais controlado)
                if current_time - self.last_window_move_time < 1.0:
                    return
                
                # Mover a janela usando Win+Setas
                if abs(delta_x) > 30:  # Limiar muito aumentado para controle preciso
                    if delta_x > 0:
                        pyautogui.hotkey('win', 'right')  # Mover para direita
                        time.sleep(0.5)  # Pausa maior para evitar movimentos rápidos
                    else:
                        pyautogui.hotkey('win', 'left')   # Mover para esquerda
                        time.sleep(0.5)
                    self.last_window_move_time = current_time
                
                if abs(delta_y) > 30:  # Limiar muito aumentado para controle preciso
                    if delta_y > 0:
                        pyautogui.hotkey('win', 'down')    # Mover para baixo
                        time.sleep(0.5)
                    else:
                        pyautogui.hotkey('win', 'up')      # Mover para cima
                        time.sleep(0.5)
                    self.last_window_move_time = current_time
                
                # Desenhar indicador visual
                cv2.putText(frame, f"MOVING WINDOW: ({delta_x}, {delta_y})", 
                           (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['direct_control'], 2)
                
            except Exception as e:
                print(f"❌ Erro ao mover janela: {e}")
        
        self.last_hand_position = (screen_x, screen_y)
    
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
            action_config = ACTIONS[gesture_type]
            description = action_config.get('description', 'Ação personalizada')
            print(f"🎯 Gesto {gesture_type} detectado! {description}...")
            
            try:
                # Verificar se é uma ação de aplicação ou de teclado
                if 'app' in action_config:
                    app_name = action_config['app']
                    subprocess.Popen([app_name], shell=True)
                elif 'action' in action_config:
                    action_type = action_config['action']
                    if action_type == 'copy':
                        pyautogui.hotkey('ctrl', 'c')
                        print("📋 Texto copiado!")
                    elif action_type == 'paste':
                        pyautogui.hotkey('ctrl', 'v')
                        print("📋 Texto colado!")
                    elif action_type == 'move_window':
                        # Ativar modo de mover janela
                        pyautogui.hotkey('alt', 'space')
                        time.sleep(0.1)
                        pyautogui.press('m')
                        print("🖼️  Modo mover janela ativado!")
                    elif action_type == 'resize_window':
                        # Ativar modo de redimensionar janela
                        pyautogui.hotkey('alt', 'space')
                        time.sleep(0.1)
                        pyautogui.press('s')
                        print("📐 Modo redimensionar janela ativado!")
                    elif action_type == 'minimize_window':
                        # Minimizar janela ativa
                        pyautogui.hotkey('alt', 'space')
                        time.sleep(0.1)
                        pyautogui.press('n')
                        print("📉 Janela minimizada!")
                    elif action_type == 'direct_window_control':
                        # Ativar controle direto de janela
                        if not self.direct_control_active:
                            self.direct_control_active = True
                            self.window_initial_position = pyautogui.position()
                            self.last_hand_position = None  # Resetar posição
                            self.move_mode_activated = False  # Resetar modo
                            print("🎯 Controle direto de janela ativado! Mova a mão para controlar.")
                        else:
                            self.direct_control_active = False
                            # Limpar variável de controle
                            if hasattr(self, 'move_mode_activated'):
                                delattr(self, 'move_mode_activated')
                            print("🎯 Controle direto de janela desativado!")
            except Exception as e:
                print(f"❌ Erro ao executar ação: {e}")
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
            color = ACTIONS.get("OK", {}).get("color", COLORS['ok_gesture'])
            self._draw_gesture_text(frame, "OK GESTURE", color)
            if not self.gesture_detected:
                self.execute_action("OK")
                self.gesture_detected = True
                
        elif self.detect_thumbs_up(hand_landmarks):
            color = ACTIONS.get("THUMBS_UP", {}).get("color", COLORS['thumbs_up'])
            self._draw_gesture_text(frame, "THUMBS UP", color)
            if not self.gesture_detected:
                self.execute_action("THUMBS_UP")
                self.gesture_detected = True
                
        elif self.detect_copy_gesture(hand_landmarks):
            color = ACTIONS.get("COPY_GESTURE", {}).get("color", COLORS['copy'])
            self._draw_gesture_text(frame, "COPY", color)
            if not self.gesture_detected:
                self.execute_action("COPY_GESTURE")
                self.gesture_detected = True
                
        elif self.detect_paste_gesture(hand_landmarks):
            color = ACTIONS.get("PASTE_GESTURE", {}).get("color", COLORS['paste'])
            self._draw_gesture_text(frame, "PASTE", color)
            if not self.gesture_detected:
                self.execute_action("PASTE_GESTURE")
                self.gesture_detected = True
                
        elif self.detect_move_window_gesture(hand_landmarks):
            color = ACTIONS.get("MOVE_WINDOW", {}).get("color", COLORS['move'])
            self._draw_gesture_text(frame, "MOVE WINDOW", color)
            if not self.gesture_detected:
                self.execute_action("MOVE_WINDOW")
                self.gesture_detected = True
                
        elif self.detect_resize_window_gesture(hand_landmarks):
            color = ACTIONS.get("RESIZE_WINDOW", {}).get("color", COLORS['resize'])
            self._draw_gesture_text(frame, "RESIZE WINDOW", color)
            if not self.gesture_detected:
                self.execute_action("RESIZE_WINDOW")
                self.gesture_detected = True
                
        elif self.detect_minimize_window_gesture(hand_landmarks):
            color = ACTIONS.get("MINIMIZE_WINDOW", {}).get("color", COLORS['minimize'])
            self._draw_gesture_text(frame, "MINIMIZE", color)
            if not self.gesture_detected:
                self.execute_action("MINIMIZE_WINDOW")
                self.gesture_detected = True
                
        elif self.detect_direct_window_control_gesture(hand_landmarks):
            color = ACTIONS.get("DIRECT_WINDOW_CONTROL", {}).get("color", COLORS['direct_control'])
            self._draw_gesture_text(frame, "DIRECT CONTROL", color)
            if not self.gesture_detected:
                self.execute_action("DIRECT_WINDOW_CONTROL")
                self.gesture_detected = True
            
            # Processar controle direto se ativo
            if self.direct_control_active:
                self._process_direct_window_control(hand_landmarks, frame)
        else:
            self.gesture_detected = False
    
    def _print_instructions(self) -> None:
        """Imprime instruções de uso do programa."""
        print("🚀 Iniciando Sistema de Controle por Gestos")
        print("📋 Comandos disponíveis:")
        print("   👌 Gesto OK → Abre o Notepad")
        print("   👍 Joinha → Abre a Calculadora")
        print("   ✌️  Copiar → Copia texto (Ctrl+C) - 2 dedos")
        print("   🤟 Colar → Cola texto (Ctrl+V) - V com polegar")
        print("   🖐️  Mover Janela → Ativa modo mover (3 dedos)")
        print("   🤏 Redimensionar → Ativa modo redimensionar (3 dedos + polegar)")
        print("   👎 Minimizar → Minimiza janela (polegar para baixo)")
        print("   🖐️  Controle Direto → Mova janela com a mão (mão aberta)")
        print("   🖐️  Mão aberta → Para o programa")
        print("\nPressione 'q' para sair")
    
    def run(self) -> None:
        """Loop principal do programa."""
        self._print_instructions()
        
        # Configurar callback para fechamento da janela
        cv2.namedWindow("Controle por Gestos - GestIQ", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Controle por Gestos - GestIQ", cv2.WND_PROP_TOPMOST, 1)
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Erro ao acessar câmera")
                    break
                
                # Controle de FPS e frame skip
                self.frame_count += 1
                if self.frame_count % self.frame_skip != 0:
                    continue
                
                # Converter BGR para RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                # Processar landmarks das mãos
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Mostrar landmarks apenas se configurado
                        if self.show_landmarks:
                            self.mp_drawing.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                            )
                        self._process_gestures(hand_landmarks, frame)
                else:
                    self.gesture_detected = False
                
                # Mostrar informações de debug
                if self.show_fps:
                    fps_text = f"FPS: {self.max_fps}"
                    cv2.putText(frame, fps_text, (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['text'], 1)
                
                if self.show_gesture_info:
                    info_text = f"Frame: {self.frame_count}"
                    cv2.putText(frame, info_text, (10, 80), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['text'], 1)
                
                # Mostrar frame
                cv2.imshow("Controle por Gestos - GestIQ", frame)
                
                # Verificar tecla de saída ou fechamento da janela
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
                # Verificar se a janela foi fechada
                if cv2.getWindowProperty("Controle por Gestos - GestIQ", cv2.WND_PROP_VISIBLE) < 1:
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