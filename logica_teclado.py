# Lógica principal del teclado virtual: entrada de texto, sugerencias y procesamiento de teclas
# Integra el modelo LSTM/NLTK para autocompletar y gestiona la interacción con la interfaz

from collections import Counter
import pygame
import nltk
from nltk.corpus import cess_esp
from config import *
from modelo_palabras.sugeridor_palabras import LSTMSuggester

# KeyboardLogic: Clase principal que gestiona el estado del teclado, la entrada de texto y la selección de teclas.
class KeyboardLogic:
    def __init__(self):
        try:
            # Carga palabras del corpus cess_esp de NLTK para sugerencias por frecuencia
            palabras_es = [word.lower() for word in cess_esp.words() if word.isalpha() and 3 <= len(word) <= 10]
            self.suggestion_model = Counter(palabras_es)
        except:
            print("Error: Ejecuta nltk.download('cess_esp')")
            self.suggestion_model = Counter()

        # Inicializa el sistema de sonido y carga el sonido de clic
        pygame.mixer.init()
        self.sound_click = pygame.mixer.Sound('sounds/click.wav')
        self.current_text = ""
        self.selected_key = None
        self.caps_lock = False

        # Definición del teclado QWERTY
        self.key_layout = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', ';'],
            ['MAYUS', 'ESPACIO', 'BORRAR']
        ]

        # Definición del teclado numérico
        self.num_pad_layout = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['¿', '0', '?']
        ]

        # Calcula las posiciones de las teclas QWERTY y num pad
        self.key_rects = self._init_key_rects()
        self.num_pad_rects = self._init_num_pad_rects()

        try:
            # Intenta cargar el modelo LSTM entrenado para sugerencias inteligentes
            self.lstm_suggester = LSTMSuggester()
            self.lstm_suggester.load_model('modelo_palabras/lstm_suggester.pkl')
            self.lstm_ready = True
        except Exception as e:
            print("No se pudo cargar el modelo LSTM:", e)
            self.lstm_ready = False

    def _init_key_rects(self):
        rects = []
        key_height = KEYBOARD_HEIGHT // len(self.key_layout)
        for row_idx, row in enumerate(self.key_layout):
            row_rects = []
            key_width = (KEYBOARD_WIDTH * 0.75) // len(row)  # 75% para el QWERTY
            for col_idx in range(len(row)):
                x = col_idx * key_width
                y = TEXT_AREA_HEIGHT + SUGGESTIONS_HEIGHT + row_idx * key_height
                row_rects.append(pygame.Rect(x, y, key_width, key_height))  # Rectángulo de cada tecla
            rects.append(row_rects)
        return rects

    def _init_num_pad_rects(self):
        rects = []
        pad_key_height = KEYBOARD_HEIGHT // len(self.num_pad_layout)
        pad_key_width = (KEYBOARD_WIDTH * 0.25) // 3  # 25% para el num pad
        pad_offset_x = KEYBOARD_WIDTH * 0.75  # empieza al 75% del ancho
        pad_offset_y = TEXT_AREA_HEIGHT + SUGGESTIONS_HEIGHT

        for row_idx, row in enumerate(self.num_pad_layout):
            row_rects = []
            for col_idx in range(len(row)):
                x = pad_offset_x + col_idx * pad_key_width
                y = pad_offset_y + row_idx * pad_key_height
                row_rects.append(pygame.Rect(x, y, pad_key_width, pad_key_height))  # Rectángulo de cada tecla num pad
            rects.append(row_rects)
        return rects

    def update_selection(self, gaze_pos):
        self.selected_key = None

        # Verificar si la posición del dedo está sobre una tecla QWERTY
        for row_idx, row in enumerate(self.key_rects):
            for col_idx, rect in enumerate(row):
                if rect.collidepoint(gaze_pos):
                    self.selected_key = (row_idx, col_idx)
                    return

        # Verificar si la posición del dedo está sobre una tecla del num pad
        for row_idx, row in enumerate(self.num_pad_rects):
            for col_idx, rect in enumerate(row):
                if rect.collidepoint(gaze_pos):
                    if self.num_pad_layout[row_idx][col_idx] != '':
                        self.selected_key = ('num_pad', row_idx, col_idx)
                    return

    def select_key(self, key=None):
        self.sound_click.play()  # Reproduce sonido al seleccionar una tecla

        if key is None:
            # Si no se pasa una tecla explícita, usa la seleccionada por el dedo
            if isinstance(self.selected_key, tuple):
                if self.selected_key[0] == 'num_pad':
                    row_idx, col_idx = self.selected_key[1], self.selected_key[2]
                    key = self.num_pad_layout[row_idx][col_idx]
                else:
                    row_idx, col_idx = self.selected_key
                    key = self.key_layout[row_idx][col_idx]
            else:
                return  # Nada seleccionado

        # Procesa la tecla seleccionada
        if key == 'ESPACIO':
            self.current_text += ' '
        elif key == 'BORRAR':
            self.current_text = self.current_text[:-1]
        elif key == 'MAYUS':
            self.caps_lock = not self.caps_lock  # Activa/desactiva mayúsculas
        else:
            self.current_text += key.upper() if self.caps_lock else key.lower()

    def get_suggestions(self):
        # Si el modelo LSTM está listo y hay texto, usa LSTM para sugerencias
        if self.lstm_ready and self.current_text.strip():
            last_word = self.current_text.split()[-1].lower()
            if not last_word:
                return []
            return self.lstm_suggester.suggest_words(last_word)
        # Si no, usa sugerencias por frecuencia (NLTK)
        if not self.current_text.strip():
            return []
        last_word = self.current_text.split()[-1].lower()
        return [w for w in self.suggestion_model if w.startswith(last_word)][:3]

    def select_suggestion(self, suggestion):
        if suggestion:
            # Reemplaza la última palabra por la sugerencia seleccionada y agrega un espacio
            words = self.current_text.split()
            self.current_text = ' '.join(words[:-1]) + " " + suggestion + " "
            self.sound_click.play()  # Sonido al autocompletar