"""
Clase para la base que debe ser defendida
"""
import pygame
from config import *

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_health = BASE_MAX_HEALTH
        self.health = self.max_health
        self.size = BASE_SIZE
        self.color = BASE_COLOR
        
    def take_damage(self, damage):
        """La base recibe daño"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def repair(self, amount):
        """Repara la base"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def increase_max_health(self, amount):
        """Aumenta la vida máxima de la base"""
        self.max_health += amount
        self.health += amount
    
    def is_alive(self):
        """Verifica si la base sigue en pie"""
        return self.health > 0
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def render(self, screen):
        """Dibuja la torre de castillo detallada"""
        
        # --- ESTRUCTURA ---
        
        # Foso (Agua alrededor) - Opcional, da buen efecto
        moat_size = self.size + 30
        pygame.draw.rect(screen, (50, 80, 100), 
                        (self.x - moat_size//2, self.y - moat_size//2, moat_size, moat_size), 0, 15)
        
        # Puente levadizo (Marrón madera)
        bridge_width = 30
        bridge_length = 40
        pygame.draw.rect(screen, (90, 60, 30), 
                        (self.x - bridge_width//2, self.y + self.size//2, bridge_width, bridge_length))

        # Base principal de piedra (Gris oscuro)
        main_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        pygame.draw.rect(screen, DARK_GRAY, main_rect)
        
        # Textura de piedras irregulares en la base
        stone_color = (70, 70, 70)
        # Algunas piedras decorativas
        pygame.draw.rect(screen, stone_color, (self.x - 40, self.y - 40, 20, 15))
        pygame.draw.rect(screen, stone_color, (self.x + 20, self.y + 30, 25, 12))
        pygame.draw.rect(screen, stone_color, (self.x - 30, self.y + 10, 15, 20))
        pygame.draw.rect(screen, stone_color, (self.x + 30, self.y - 30, 20, 20))

        # --- TORRES EN LAS ESQUINAS ---
        # 4 Torres circulares en las esquinas para dar sensación de fortaleza
        tower_radius = 20
        corner_color = (60, 60, 60) # Un poco más oscuro
        
        # Dibujar torres
        corners = [
            (self.x - self.size//2, self.y - self.size//2),
            (self.x + self.size//2, self.y - self.size//2),
            (self.x - self.size//2, self.y + self.size//2),
            (self.x + self.size//2, self.y + self.size//2)
        ]
        
        for cx, cy in corners:
            pygame.draw.circle(screen, corner_color, (cx, cy), tower_radius)
            pygame.draw.circle(screen, (40, 40, 40), (cx, cy), tower_radius, 2) # Borde
            # Techo de la torre (conico visto desde arriba -> circulo más pequeño de otro color)
            pygame.draw.circle(screen, (40, 50, 60), (cx, cy), tower_radius - 5)

        # --- TORRE CENTRAL (KEEP) ---
        keep_size = self.size // 1.8
        pygame.draw.rect(screen, (80, 80, 80), 
                        (self.x - keep_size//2, self.y - keep_size//2, keep_size, keep_size))
        
        # Almenas de la torre central
        battlement_size = 10
        # Bordes decorativos
        pygame.draw.rect(screen, (50, 50, 50), 
                        (self.x - keep_size//2, self.y - keep_size//2, keep_size, keep_size), 3)

        # --- ESTANDARTE ---
        # Asta
        pygame.draw.line(screen, (139, 69, 19), (self.x, self.y), (self.x, self.y - 15), 3)
        # Bandera ondeando (Azul real con borde dorado)
        flag_points = [(self.x, self.y - 15), (self.x + 25, self.y - 15), (self.x + 15, self.y - 5), (self.x + 25, self.y + 5), (self.x, self.y + 5)]
        pygame.draw.polygon(screen, BLUE, flag_points)
        pygame.draw.polygon(screen, YELLOW, flag_points, 2)
        
        # --- UI DE VIDA DEL CASTILLO ---
        # Barra de vida estilizada (estilo pergamino/sangre)
        bar_width = self.size + 40
        bar_height = 8
        bar_x = self.x - bar_width//2
        bar_y = self.y - self.size//2 - 30
        
        # Fondo y borde (Madera)
        pygame.draw.rect(screen, UI_BG, (bar_x-2, bar_y-2, bar_width+4, bar_height+4))
        pygame.draw.rect(screen, UI_BORDER, (bar_x-3, bar_y-3, bar_width+6, bar_height+6), 1)
        
        # Barra de vida actual
        health_pct = self.health / self.max_health
        health_color = GREEN if health_pct > 0.5 else (YELLOW if health_pct > 0.25 else RED)
        health_width = int(bar_width * health_pct)
        if health_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Texto de vida
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"{int(self.health)}/{int(self.max_health)}", True, WHITE)
        text_rect = health_text.get_rect(midtop=(self.x, bar_y - 18))
        screen.blit(health_text, text_rect)
