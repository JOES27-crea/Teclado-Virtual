# Interfaz gráfica del teclado virtual usando Pygame
# Dibuja el teclado, área de texto, sugerencias y gestiona la retroalimentación sonora

import pygame
from config import *
from logica_teclado import KeyboardLogic

class KeyboardUI:
    def __init__(self):
        # Inicializa la ventana principal de Pygame con el tamaño adecuado
        self.screen = pygame.display.set_mode((KEYBOARD_WIDTH, TEXT_AREA_HEIGHT + SUGGESTIONS_HEIGHT + KEYBOARD_HEIGHT))
        # Instancia la lógica del teclado (gestión de texto, sugerencias, teclas)
        self.logic = KeyboardLogic()
        # Fuente para las teclas
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # Fuente para el área de texto
        self.text_font = pygame.font.SysFont(FONT_NAME, TEXT_FONT_SIZE)
        self.suggestion_highlight = None  # Índice de sugerencia resaltada
        self.cursor_visible = True  # Controla la visibilidad del cursor
        self.cursor_timer = 0  # Temporizador para parpadeo del cursor

    def draw(self):
        # Dibuja toda la interfaz: área de texto, sugerencias y teclado
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_text_area()
        self._draw_suggestions()
        self._draw_keyboard()
        pygame.display.flip()  # Actualiza la pantalla

    def _draw_text_area(self):
        # Dibuja el área donde aparece el texto escrito
        pygame.draw.rect(self.screen, TEXT_BG_COLOR, (0, 0, KEYBOARD_WIDTH, TEXT_AREA_HEIGHT))
        font = self.text_font
        words = self.logic.current_text.split()
        lines = []
        current_line = ""

        # Divide el texto en líneas para que no se salga del área
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] < KEYBOARD_WIDTH - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        y_offset = 10
        # Dibuja solo las dos últimas líneas (simula área de texto tipo chat)
        for line in lines[-2:]:
            text_surface = font.render(line, True, TEXT_COLOR)
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += TEXT_FONT_SIZE + 5

        # Lógica para el parpadeo del cursor
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time

        if self.cursor_visible:
            # Dibuja el cursor al final de la última línea
            cursor_x = 25 + font.size(lines[-1] if lines else "")[0]
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (cursor_x, y_offset - TEXT_FONT_SIZE - 5, 2, TEXT_FONT_SIZE)
            )

    def _draw_suggestions(self):
        # Dibuja el área de sugerencias de palabras
        pygame.draw.rect(self.screen, SUGGESTIONS_COLOR, (0, TEXT_AREA_HEIGHT, KEYBOARD_WIDTH, SUGGESTIONS_HEIGHT))
        suggestions = self.logic.get_suggestions()
        for i, suggestion in enumerate(suggestions):
            suggestion_rect = pygame.Rect(10 + i * 200, TEXT_AREA_HEIGHT + 10, 190, SUGGESTIONS_HEIGHT - 20)

            # Resalta la sugerencia si está seleccionada
            if self.suggestion_highlight == i:
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, suggestion_rect, 3)

            text = self.font.render(suggestion, True, (0, 0, 0))
            self.screen.blit(text, (suggestion_rect.x + 10, suggestion_rect.y + 10))

    def _draw_keyboard(self):
        # --- Dibuja teclado QWERTY ---
        for row_idx, row in enumerate(self.logic.key_layout):
            for col_idx, key in enumerate(row):
                rect = self.logic.key_rects[row_idx][col_idx]

                # Selecciona color según la fila
                if row_idx == 0:
                    color = KEY_COLOR1
                    text_color = (0, 0, 0)
                elif row_idx < 3:
                    color = KEY_COLOR2
                    text_color = (0, 0, 0)
                else:
                    color = KEY_COLOR3
                    text_color = (0, 0, 0)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)  # Borde gris

                # Resalta la tecla si está seleccionada
                if self.logic.selected_key == (row_idx, col_idx):
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, rect, 3)

                key_text = key
                if key == 'MAYUS':
                    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)
                    key_text = "MAYUS"
                else:
                    font = self.font
                    if self.logic.caps_lock and key.isalpha():
                        key_text = key.upper()

                text_surface = font.render(key_text, True, text_color)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)

        # --- Dibuja Num Pad ---
        for row_idx, row in enumerate(self.logic.num_pad_layout):
            for col_idx, key in enumerate(row):
                rect = self.logic.num_pad_rects[row_idx][col_idx]

                color = KEY_COLOR1  # mismo color que los números arriba
                text_color = (0, 0, 0)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

                # Resalta la tecla del num pad si está seleccionada
                if self.logic.selected_key == ('num_pad', row_idx, col_idx):
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, rect, 3)

                if key != '':
                    text_surface = self.font.render(key, True, text_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

    def check_suggestion_click(self, pos):
        # Verifica si el usuario hizo clic en alguna sugerencia
        suggestions = self.logic.get_suggestions()
        for i, suggestion in enumerate(suggestions):
            suggestion_rect = pygame.Rect(10 + i * 200, TEXT_AREA_HEIGHT + 10, 190, SUGGESTIONS_HEIGHT - 20)
            if suggestion_rect.collidepoint(pos):
                self.suggestion_highlight = i
                return True
        self.suggestion_highlight = None
        return False

    def select_key(self):
        # Llama a la lógica para procesar la tecla seleccionada (QWERTY o num pad)
        if self.logic.selected_key:
            # caso Num Pad
            if isinstance(self.logic.selected_key, tuple) and self.logic.selected_key[0] == 'num_pad':
                row_idx, col_idx = self.logic.selected_key[1], self.logic.selected_key[2]
                self.logic.select_key(self.logic.num_pad_layout[row_idx][col_idx])
            else:
                row, col = self.logic.selected_key
                self.logic.select_key(self.logic.key_layout[row][col])
            return True
        return False
