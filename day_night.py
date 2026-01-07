"""
Gestor del ciclo día/noche
"""
import pygame
from config import *

class DayNightCycle:
    def __init__(self):
        self.phase = "day"  # "day" o "night"
        self.night_number = 1
        self.day_timer = DAY_DURATION
        self.night_timer = 0
        self.transition_alpha = 0
        self.transitioning = False
        
    def start_game(self):
        """Inicia el juego en fase de día"""
        self.phase = "day"
        self.night_number = 1
        self.day_timer = DAY_DURATION
        self.night_timer = 0
    
    def is_day(self):
        """Verifica si es de día"""
        return self.phase == "day"
    
    def is_night(self):
        """Verifica si es de noche"""
        return self.phase == "night"
    
    def get_night_duration(self):
        """Obtiene la duración de la noche actual"""
        if self.night_number in NIGHT_CONFIG:
            return NIGHT_CONFIG[self.night_number]["duration"]
        return 60
    
    def update(self, dt):
        """Actualiza el ciclo día/noche"""
        if self.phase == "day":
            self.day_timer -= dt
            if self.day_timer <= 0:
                self.start_night()
        elif self.phase == "night":
            self.night_timer -= dt
            if self.night_timer <= 0:
                self.end_night()
    
    def start_night(self):
        """Inicia la fase de noche"""
        self.phase = "night"
        self.night_timer = self.get_night_duration()
        self.transitioning = True
    
    def end_night(self):
        """Termina la fase de noche y avanza al siguiente día"""
        self.phase = "day"
        self.night_number += 1
        self.day_timer = DAY_DURATION
        self.transitioning = True
    
    def render_background(self, screen, width, height):
        """Renderiza el fondo según la fase actual"""
        color = GRASS if self.is_day() else MIDNIGHT
        screen.fill(color)
        
        # Textura de suelo simple
        tile_size = 60
        grid_color = (60, 80, 40) if self.is_day() else (20, 15, 25)
        
        # Para que draw.line acepte alpha, necesitamos una surface transparente
        grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Puntos de hierba o piedra aleatorios en lugar de grid futurista
        # Por simplicidad y rendimiento, mantenemos el grid pero con color de "suelo"
        for x in range(0, width, tile_size):
            pygame.draw.line(grid_surface, (*grid_color[:3], 40), (x, 0), (x, height))
        for y in range(0, height, tile_size):
            pygame.draw.line(grid_surface, (*grid_color[:3], 40), (0, y), (width, y))
            
        screen.blit(grid_surface, (0,0))
    
    def render_ui(self, screen, width, height):
        """Renderiza la información del ciclo día/noche"""
        font_large = pygame.font.Font(None, 40)
        font_medium = pygame.font.Font(None, 28)
        
        # Panel superior de UI (Estandarte)
        banner_rect = pygame.Rect(width//2 - 150, 0, 300, 80)
        pygame.draw.rect(screen, UI_BG, banner_rect) # Fondo madera
        pygame.draw.rect(screen, UI_BORDER, banner_rect, 3) # Borde dorado
        
        # Remaches en las esquinas
        pygame.draw.circle(screen, BLACK, (banner_rect.left + 5, banner_rect.bottom - 5), 3)
        pygame.draw.circle(screen, BLACK, (banner_rect.right - 5, banner_rect.bottom - 5), 3)
        
        if self.is_day():
            # Mostrar tiempo restante del día
            phase_text = font_large.render("DÍA - PREPARACIÓN", True, UI_TEXT)
            timer_color = RED if self.day_timer < 5 else UI_TEXT
            timer_text = font_medium.render(f"Tiempo restante: {int(self.day_timer)}s", True, timer_color)
            night_text = font_medium.render(f"Próxima oleada: {self.night_number}", True, YELLOW)
            
            screen.blit(phase_text, (width // 2 - phase_text.get_width() // 2, 10))
            screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 45))
            screen.blit(night_text, (width // 2 - night_text.get_width() // 2, 70))
        else:
            # Mostrar tiempo restante de la noche
            phase_text = font_large.render(f"⚔️ OLEADA {self.night_number} ⚔️", True, RED)
            timer_text = font_medium.render(f"Sobrevive: {int(self.night_timer)}s", True, WHITE)
            
            screen.blit(phase_text, (width // 2 - phase_text.get_width() // 2, 10))
            screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 45))
