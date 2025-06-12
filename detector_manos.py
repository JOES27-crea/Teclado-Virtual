import os
# Suprime los mensajes de advertencia de TensorFlow para mantener la consola limpia
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import warnings
warnings.filterwarnings("ignore")

import cv2  # Librería para procesamiento de imágenes y captura de video
import mediapipe as mp  # Librería para reconocimiento de manos y landmarks

class HandTracker:
    def __init__(self):
        # Inicializa el módulo de manos de MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # Procesamiento en tiempo real
            max_num_hands=1,  # Solo detecta una mano a la vez
            min_detection_confidence=0.5,  # Umbral de confianza para la detección
            model_complexity=0  # Reduce la complejidad del modelo para menos advertencias
        )
        # Utilidad para dibujar los landmarks de la mano sobre la imagen
        self.mp_drawing = mp.solutions.drawing_utils
        
    def get_finger_position(self, frame):
        # Convierte el frame de BGR (OpenCV) a RGB (MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Procesa el frame para detectar la mano y obtener landmarks
        results = self.hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibuja los landmarks y conexiones de la mano sobre el frame
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                # Obtiene la posición de la punta del dedo índice (landmark 8)
                index_finger = hand_landmarks.landmark[8]
                h, w, _ = frame.shape
                x, y = int(index_finger.x * w), int(index_finger.y * h)
                # Dibuja un círculo verde en la punta del dedo índice
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                return (x, y)  # Devuelve las coordenadas del dedo índice
        return None  # Si no se detecta mano, retorna None
    
    def is_fist(self, frame):
        # Detecta si la mano está en posición de puño cerrado (todos los dedos doblados excepto el pulgar)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # IDs de las puntas de los dedos: índice, medio, anular, meñique
                tips_ids = [8, 12, 16, 20]
                folded = 0
                for tip_id in tips_ids:
                    tip = hand_landmarks.landmark[tip_id]
                    pip = hand_landmarks.landmark[tip_id - 2]  # Articulación intermedia del dedo
                    if tip.y > pip.y:  # Si la punta está por debajo de la articulación, el dedo está doblado
                        folded += 1
                if folded == 4:
                    return True  # Todos los dedos doblados: puño cerrado
        return False  # No se detecta puño cerrado