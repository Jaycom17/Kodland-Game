"""
Pantallas de menú, victoria y derrota
"""
import pygame
from config import *

class MenuScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.selected_option = 0
        self.options = ["Iniciar Juego", "Salir"]
    
    def navigate_up(self):
        if self.selected_option > 0:
            self.selected_option -= 1
    
    def navigate_down(self):
        if self.selected_option < len(self.options) - 1:
            self.selected_option += 1
    
    def get_selected_option(self):
        return self.options[self.selected_option]
    
    def render(self, screen):
        screen.fill(GRASS) # Fondo césped por defecto
        
        # Superponer pergamino gigante
        menu_bg_rect = pygame.Rect(self.screen_width//2 - 300, 50, 600, self.screen_height - 100)
        pygame.draw.rect(screen, UI_TEXT, menu_bg_rect) # Papel
        pygame.draw.rect(screen, UI_BG, menu_bg_rect, 10) # Borde madera
        
        # Título del juego (Estilo Medieval)
        font_title = pygame.font.Font(None, 80)
        title_text = font_title.render("DEFENSA DEL REINO", True, BLACK)
        
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 180))
        screen.blit(title_text, title_rect)
        
        # Subtítulo
        font_subtitle = pygame.font.Font(None, 40)
        subtitle_text = font_subtitle.render("Sobrevive el asedio nocturno", True, DARK_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú
        font_option = pygame.font.Font(None, 50)
        y_offset = 400
        
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = BLACK
                bg_color = YELLOW
                prefix = "> "
            else:
                color = DARK_GRAY
                bg_color = UI_TEXT
                prefix = "  "
            
            # Botón
            btn_rect = pygame.Rect(self.screen_width//2 - 150, y_offset - 10, 300, 50)
            if i == self.selected_option:
                pygame.draw.rect(screen, bg_color, btn_rect)
                pygame.draw.rect(screen, BLACK, btn_rect, 2)
            
            option_text = font_option.render(prefix + option, True, color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, y_offset + 15))
            screen.blit(option_text, option_rect)
            y_offset += 80
        
        # Instrucciones
        font_instructions = pygame.font.Font(None, 24)
        instructions_text = font_instructions.render("ARRIBA/ABAJO: Navegar | ENTER: Seleccionar", True, DARK_GRAY)
        instructions_rect = instructions_text.get_rect(center=(self.screen_width // 2, self.screen_height - 120))
        screen.blit(instructions_text, instructions_rect)


class VictoryScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def render(self, screen, base_health, total_resources):
        screen.fill(GRASS)
        
        # Pergamino
        bg_rect = pygame.Rect(self.screen_width//2 - 300, 100, 600, 500)
        pygame.draw.rect(screen, UI_TEXT, bg_rect)
        pygame.draw.rect(screen, YELLOW, bg_rect, 5) # Borde dorado victoria
        
        # Título de victoria
        font_title = pygame.font.Font(None, 96)
        title_text = font_title.render("¡VICTORIA!", True, GREEN)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 180))
        screen.blit(title_text, title_rect)
        
        # Mensaje
        font_message = pygame.font.Font(None, 42)
        message_text = font_message.render("El reino está a salvo", True, BLACK)
        message_rect = message_text.get_rect(center=(self.screen_width // 2, 260))
        screen.blit(message_text, message_rect)
        
        # Estadísticas - cuadro
        font_stats = pygame.font.Font(None, 40)
        y_offset = 350
        
        stats = [
            f"Noches Sobrevividas: 5/5",
            f"Integridad del Castillo: {int(base_health)}",
            f"Oro Recolectado: {total_resources}"
        ]
        
        for stat in stats:
            stat_text = font_stats.render(stat, True, DARK_BLUE)
            stat_rect = stat_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 50
        
        # Instrucción para continuar
        font_continue = pygame.font.Font(None, 32)
        continue_text = font_continue.render("Presiona ENTER para volver", True, DARK_GRAY)
        continue_rect = continue_text.get_rect(center=(self.screen_width // 2, self.screen_height - 150))
        screen.blit(continue_text, continue_rect)


class DefeatScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def render(self, screen, night_number, reason):
        screen.fill(MIDNIGHT) # Fondo oscuro derrota
        
        # Título de derrota
        font_title = pygame.font.Font(None, 96)
        title_text = font_title.render("DERROTA", True, RED)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Razón de derrota
        font_reason = pygame.font.Font(None, 45)
        if reason == "player":
            reason_text = font_reason.render("El Caballero ha caído en combate", True, WHITE)
        elif reason == "base":
            reason_text = font_reason.render("El Castillo ha sido destruido", True, WHITE)
        else:
            reason_text = font_reason.render("El reino ha caído", True, WHITE)
        
        reason_rect = reason_text.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(reason_text, reason_rect)
        
        # Estadísticas
        font_stats = pygame.font.Font(None, 36)
        
        if night_number > 1:
            nights_survived = night_number - 1
        else:
            nights_survived = 0
            
        stats_text = font_stats.render(f"Noches Sobrevividas: {nights_survived}/5", True, GRAY)
        stats_rect = stats_text.get_rect(center=(self.screen_width // 2, 350))
        screen.blit(stats_text, stats_rect)
        
        # Mensaje de ánimo
        font_message = pygame.font.Font(None, 32)
        message_text = font_message.render("¡Levántate y lucha de nuevo!", True, YELLOW)
        message_rect = message_text.get_rect(center=(self.screen_width // 2, 400))
        screen.blit(message_text, message_rect)
        
        # Instrucción para continuar
        font_continue = pygame.font.Font(None, 28)
        continue_text = font_continue.render("Presiona ENTER para volver al menú", True, WHITE)
        continue_rect = continue_text.get_rect(center=(self.screen_width // 2, self.screen_height - 80))
        screen.blit(continue_text, continue_rect)
