"""
Exemplos de detecção de gestos para o GestIQ
Este arquivo mostra como adicionar novos gestos ao sistema
"""

import numpy as np

class GestureExamples:
    """
    Exemplos de funções de detecção de gestos
    """
    
    def detect_peace_sign(self, hand_landmarks):
        """
        Detecta o gesto de paz (✌️)
        - Indicador e médio estendidos
        - Outros dedos fechados
        """
        if not hand_landmarks:
            return False
            
        landmarks = hand_landmarks.landmark
        
        # Pontos dos dedos
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        thumb_tip = landmarks[4]
        
        # Verificar se indicador e médio estão estendidos
        index_extended = index_tip.y < landmarks[6].y
        middle_extended = middle_tip.y < landmarks[10].y
        
        # Verificar se outros dedos estão fechados
        ring_closed = ring_tip.y > landmarks[14].y
        pinky_closed = pinky_tip.y > landmarks[18].y
        thumb_closed = thumb_tip.y > landmarks[3].y
        
        return (index_extended and middle_extended and 
                ring_closed and pinky_closed and thumb_closed)
    
    def detect_fist(self, hand_landmarks):
        """
        Detecta o gesto de punho fechado (👊)
        - Todos os dedos fechados
        """
        if not hand_landmarks:
            return False
            
        landmarks = hand_landmarks.landmark
        
        # Pontos dos dedos
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Verificar se todos os dedos estão fechados
        thumb_closed = thumb_tip.y > landmarks[3].y
        index_closed = index_tip.y > landmarks[6].y
        middle_closed = middle_tip.y > landmarks[10].y
        ring_closed = ring_tip.y > landmarks[14].y
        pinky_closed = pinky_tip.y > landmarks[18].y
        
        return (thumb_closed and index_closed and 
                middle_closed and ring_closed and pinky_closed)
    
    def detect_open_hand(self, hand_landmarks):
        """
        Detecta mão aberta (🖐️)
        - Todos os dedos estendidos
        """
        if not hand_landmarks:
            return False
            
        landmarks = hand_landmarks.landmark
        
        # Pontos dos dedos
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Verificar se todos os dedos estão estendidos
        thumb_extended = thumb_tip.y < landmarks[3].y
        index_extended = index_tip.y < landmarks[6].y
        middle_extended = middle_tip.y < landmarks[10].y
        ring_extended = ring_tip.y < landmarks[14].y
        pinky_extended = pinky_tip.y < landmarks[18].y
        
        return (thumb_extended and index_extended and 
                middle_extended and ring_extended and pinky_extended)
    
    def detect_pointing(self, hand_landmarks):
        """
        Detecta gesto de apontar (👆)
        - Apenas indicador estendido
        - Outros dedos fechados
        """
        if not hand_landmarks:
            return False
            
        landmarks = hand_landmarks.landmark
        
        # Pontos dos dedos
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Verificar se apenas o indicador está estendido
        index_extended = index_tip.y < landmarks[6].y
        
        # Verificar se outros dedos estão fechados
        thumb_closed = thumb_tip.y > landmarks[3].y
        middle_closed = middle_tip.y > landmarks[10].y
        ring_closed = ring_tip.y > landmarks[14].y
        pinky_closed = pinky_tip.y > landmarks[18].y
        
        return (index_extended and thumb_closed and 
                middle_closed and ring_closed and pinky_closed)
    
    def detect_rock_on(self, hand_landmarks):
        """
        Detecta gesto rock on (🤘)
        - Indicador e mindinho estendidos
        - Outros dedos fechados
        """
        if not hand_landmarks:
            return False
            
        landmarks = hand_landmarks.landmark
        
        # Pontos dos dedos
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Verificar se indicador e mindinho estão estendidos
        index_extended = index_tip.y < landmarks[6].y
        pinky_extended = pinky_tip.y < landmarks[18].y
        
        # Verificar se outros dedos estão fechados
        thumb_closed = thumb_tip.y > landmarks[3].y
        middle_closed = middle_tip.y > landmarks[10].y
        ring_closed = ring_tip.y > landmarks[14].y
        
        return (index_extended and pinky_extended and 
                thumb_closed and middle_closed and ring_closed)
    
    def detect_number_gestures(self, hand_landmarks):
        """
        Detecta gestos de números (1-5)
        Retorna o número de dedos estendidos
        """
        if not hand_landmarks:
            return 0
            
        landmarks = hand_landmarks.landmark
        
        # Pontos dos dedos
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Contar dedos estendidos
        extended_fingers = 0
        
        if thumb_tip.y < landmarks[3].y:
            extended_fingers += 1
        if index_tip.y < landmarks[6].y:
            extended_fingers += 1
        if middle_tip.y < landmarks[10].y:
            extended_fingers += 1
        if ring_tip.y < landmarks[14].y:
            extended_fingers += 1
        if pinky_tip.y < landmarks[18].y:
            extended_fingers += 1
            
        return extended_fingers

# Exemplo de como integrar novos gestos no GestureController
def integrate_new_gestures(controller):
    """
    Exemplo de como adicionar novos gestos ao controller principal
    """
    examples = GestureExamples()
    
    # No método run() do GestureController, adicione:
    """
    # Detectar novos gestos
    elif examples.detect_peace_sign(hand_landmarks):
        cv2.putText(frame, "PEACE SIGN", (10, 30), 
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        if not self.gesture_detected:
            self.execute_action("PEACE_SIGN")
            self.gesture_detected = True
            
    elif examples.detect_fist(hand_landmarks):
        cv2.putText(frame, "FIST", (10, 30), 
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        if not self.gesture_detected:
            self.execute_action("FIST")
            self.gesture_detected = True
    """
    
    # No método execute_action(), adicione:
    """
    elif gesture_type == "PEACE_SIGN":
        print("✌️ Gesto de paz detectado!")
        # Sua ação aqui
        
    elif gesture_type == "FIST":
        print("👊 Punho detectado!")
        # Sua ação aqui
    """

if __name__ == "__main__":
    print("📚 Exemplos de gestos para o GestIQ")
    print("Use estas funções como referência para adicionar novos gestos!") 