"""
Testes unitários para o GestIQ
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import sys
import os

# Adicionar o diretório atual ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gesture_control import GestureController


class TestGestureController(unittest.TestCase):
    """Testes para a classe GestureController."""
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        # Mock da câmera para evitar dependência real
        with patch('cv2.VideoCapture') as mock_camera:
            mock_camera.return_value.isOpened.return_value = True
            self.controller = GestureController()
    
    def tearDown(self):
        """Limpeza após cada teste."""
        if hasattr(self.controller, 'cap'):
            self.controller.cap.release()
    
    def test_initialization(self):
        """Testa se o controlador é inicializado corretamente."""
        self.assertIsNotNone(self.controller.hands)
        self.assertIsNotNone(self.controller.cap)
        self.assertEqual(self.controller.action_cooldown, 2.0)
        self.assertFalse(self.controller.gesture_detected)
    
    def test_get_landmark_points(self):
        """Testa a extração de pontos-chave dos landmarks."""
        # Criar landmarks mock
        mock_landmarks = []
        for i in range(21):
            mock_landmark = Mock()
            mock_landmark.x = i * 0.1
            mock_landmark.y = i * 0.1
            mock_landmarks.append(mock_landmark)
        
        points = self.controller._get_landmark_points(mock_landmarks)
        
        # Verificar se todos os pontos foram extraídos
        expected_keys = [
            'thumb_tip', 'thumb_ip', 'thumb_mcp',
            'index_tip', 'index_pip',
            'middle_tip', 'middle_pip',
            'ring_tip', 'ring_pip',
            'pinky_tip', 'pinky_pip'
        ]
        
        for key in expected_keys:
            self.assertIn(key, points)
    
    def test_detect_ok_gesture_valid(self):
        """Testa detecção do gesto OK com dados válidos."""
        # Criar landmarks que simulam gesto OK
        mock_landmarks = Mock()
        mock_landmarks.landmark = self._create_ok_gesture_landmarks()
        
        result = self.controller.detect_ok_gesture(mock_landmarks)
        self.assertTrue(result)
    
    def test_detect_ok_gesture_invalid(self):
        """Testa detecção do gesto OK com dados inválidos."""
        # Criar landmarks que não simulam gesto OK
        mock_landmarks = Mock()
        mock_landmarks.landmark = self._create_invalid_gesture_landmarks()
        
        result = self.controller.detect_ok_gesture(mock_landmarks)
        self.assertFalse(result)
    
    def test_detect_thumbs_up_valid(self):
        """Testa detecção do joinha com dados válidos."""
        # Criar landmarks que simulam joinha
        mock_landmarks = Mock()
        mock_landmarks.landmark = self._create_thumbs_up_landmarks()
        
        result = self.controller.detect_thumbs_up(mock_landmarks)
        self.assertTrue(result)
    
    def test_detect_thumbs_up_invalid(self):
        """Testa detecção do joinha com dados inválidos."""
        # Criar landmarks que não simulam joinha
        mock_landmarks = Mock()
        mock_landmarks.landmark = self._create_invalid_gesture_landmarks()
        
        result = self.controller.detect_thumbs_up(mock_landmarks)
        self.assertFalse(result)
    
    def test_execute_action_with_cooldown(self):
        """Testa se o cooldown impede ações repetidas."""
        # Simular ação recente
        self.controller.last_action_time = 1000.0
        
        with patch('time.time', return_value=1001.0):  # 1 segundo depois
            with patch('subprocess.Popen') as mock_subprocess:
                self.controller.execute_action("OK")
                mock_subprocess.assert_not_called()
    
    def test_execute_action_valid(self):
        """Testa execução de ação válida."""
        with patch('time.time', return_value=1000.0):
            with patch('subprocess.Popen') as mock_subprocess:
                self.controller.execute_action("OK")
                mock_subprocess.assert_called_once()
    
    def test_execute_action_invalid(self):
        """Testa execução de ação inválida."""
        with patch('time.time', return_value=1000.0):
            with patch('builtins.print') as mock_print:
                self.controller.execute_action("INVALID_GESTURE")
                mock_print.assert_called_with("⚠️  Ação não definida para gesto: INVALID_GESTURE")
    
    def _create_ok_gesture_landmarks(self):
        """Cria landmarks que simulam gesto OK."""
        landmarks = []
        for i in range(21):
            landmark = Mock()
            if i == 4:  # thumb_tip
                landmark.x, landmark.y = 0.5, 0.5
            elif i == 8:  # index_tip
                landmark.x, landmark.y = 0.52, 0.52  # Próximo ao polegar
            elif i in [12, 16, 20]:  # Outros dedos estendidos
                landmark.y = 0.3
            elif i in [11, 15, 19]:  # Pontas dos outros dedos
                landmark.y = 0.4
            else:
                landmark.x, landmark.y = i * 0.1, i * 0.1
            landmarks.append(landmark)
        return landmarks
    
    def _create_thumbs_up_landmarks(self):
        """Cria landmarks que simulam joinha."""
        landmarks = []
        for i in range(21):
            landmark = Mock()
            if i == 4:  # thumb_tip
                landmark.y = 0.2  # Para cima
            elif i == 3:  # thumb_ip
                landmark.y = 0.3
            elif i == 2:  # thumb_mcp
                landmark.y = 0.4
            elif i in [8, 12, 16, 20]:  # Outros dedos fechados
                landmark.y = 0.6
            elif i in [6, 10, 14, 18]:  # Pontas dos outros dedos
                landmark.y = 0.5
            else:
                landmark.x, landmark.y = i * 0.1, i * 0.1
            landmarks.append(landmark)
        return landmarks
    
    def _create_invalid_gesture_landmarks(self):
        """Cria landmarks que não simulam nenhum gesto."""
        landmarks = []
        for i in range(21):
            landmark = Mock()
            landmark.x, landmark.y = i * 0.1, i * 0.1
            landmarks.append(landmark)
        return landmarks


class TestConfig(unittest.TestCase):
    """Testes para configurações."""
    
    def test_config_import(self):
        """Testa se o arquivo de configuração pode ser importado."""
        try:
            import config
            self.assertIsNotNone(config.ACTIONS)
            self.assertIsNotNone(config.COLORS)
        except ImportError:
            self.fail("Não foi possível importar o arquivo de configuração")


if __name__ == '__main__':
    # Executar testes
    unittest.main(verbosity=2) 