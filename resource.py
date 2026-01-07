"""
Sistema de recursos para recolectar durante el día
"""
import pygame
import random
from config import *

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = RESOURCE_SIZE
        self.value = RESOURCE_VALUE
        self.color = YELLOW
        self.collected = False
        
    def check_collection(self, player):
        """Verifica si el jugador recolecta el recurso"""
        if self.collected:
            return False
        
        dist_x = player.x - self.x
        dist_y = player.y - self.y
        distance = (dist_x**2 + dist_y**2) ** 0.5
        
        if distance < player.size + self.size:
            self.collected = True
            return True
        return False
    
    def render(self, screen):
        """Dibuja el recurso en pantalla (Moneda de Oro)"""
        if not self.collected:
            # Moneda dorada
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, (184, 134, 11), (int(self.x), int(self.y)), self.size, 2)
            
            # Brillo moneda
            pygame.draw.circle(screen, (255, 255, 200), (int(self.x - 3), int(self.y - 3)), 3)
            
            # Símbolo '$' rústico
            font = pygame.font.Font(None, 24)
            # text = font.render("$", True, (184, 134, 11))
            # screen.blit(text, (self.x - 5, self.y - 8))


class ResourceManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.resources = []
        self.total_collected = 0
    
    def spawn_resources(self, base_x, base_y):
        """Genera recursos aleatoriamente en el mapa"""
        self.resources.clear()
        
        for _ in range(RESOURCE_SPAWN_COUNT):
            # Generar posición aleatoria evitando la base
            while True:
                x = random.randint(50, self.screen_width - 50)
                y = random.randint(50, self.screen_height - 50)
                
                # Verificar que no esté muy cerca de la base
                dist = ((x - base_x)**2 + (y - base_y)**2) ** 0.5
                if dist > 100:
                    break
            
            self.resources.append(Resource(x, y))
    
    def update(self, player):
        """Actualiza los recursos y verifica recolección"""
        collected_value = 0
        
        for resource in self.resources:
            if resource.check_collection(player):
                collected_value += resource.value
                self.total_collected += resource.value
        
        return collected_value
    
    def clear_resources(self):
        """Elimina todos los recursos"""
        self.resources.clear()
    
    def render(self, screen):
        """Dibuja todos los recursos"""
        for resource in self.resources:
            resource.render(screen)
