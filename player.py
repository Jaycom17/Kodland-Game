"""
Clase del jugador
"""
import pygame
import math
from config import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.damage = PLAYER_DAMAGE
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.attack_range = PLAYER_ATTACK_RANGE
        self.attack_timer = 0
        self.color = GREEN
        
    def move(self, dx, dy, dt, screen_width, screen_height, obstacles=None):
        """Mueve al jugador con colisiones"""
        if obstacles is None:
            obstacles = []

        # Normalizar el vector de movimiento
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
        
        # Calcular movimiento propuesto en X
        new_x = self.x + dx * self.speed * dt
        # Validar colisión en X
        rect_x = pygame.Rect(new_x - self.size//2, self.y - self.size//2, self.size, self.size)
        collided_x = False
        for obstacle in obstacles:
            if rect_x.colliderect(obstacle):
                collided_x = True
                break
        
        # Aplicar movimiento X si no hay colisión y está dentro de pantalla
        if not collided_x:
            self.x = max(self.size, min(screen_width - self.size, new_x))

        # Calcular movimiento propuesto en Y
        new_y = self.y + dy * self.speed * dt
        # Validar colisión en Y
        rect_y = pygame.Rect(self.x - self.size//2, new_y - self.size//2, self.size, self.size)
        collided_y = False
        for obstacle in obstacles:
            if rect_y.colliderect(obstacle):
                collided_y = True
                break
        
        # Aplicar movimiento Y si no hay colisión y está dentro de pantalla
        if not collided_y:
            self.y = max(self.size, min(screen_height - self.size, new_y))
    
    def update(self, dt):
        """Actualiza el estado del jugador"""
        if self.attack_timer > 0:
            self.attack_timer -= dt
    
    def take_damage(self, damage):
        """El jugador recibe daño"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        """Cura al jugador"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def increase_max_health(self, amount):
        """Aumenta la vida máxima del jugador"""
        self.max_health += amount
        self.health += amount
    
    def increase_damage(self, amount):
        """Aumenta el daño del jugador"""
        self.damage += amount
    
    def increase_speed(self, amount):
        """Aumenta la velocidad del jugador"""
        self.speed += amount
    
    def can_attack(self):
        """Verifica si el jugador puede atacar"""
        return self.attack_timer <= 0
    
    def attack(self, enemies):
        """Ataca a los enemigos en rango"""
        if not self.can_attack():
            return 0
        
        killed = 0
        for enemy in enemies[:]:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.attack_range:
                enemy.take_damage(self.damage)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    killed += 1
        
        if killed > 0:
            self.attack_timer = self.attack_cooldown
        
        return killed
    
    def is_alive(self):
        """Verifica si el jugador sigue vivo"""
        return self.health > 0
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def render(self, screen):
        """Dibuja al jugador en pantalla"""
        # Círculo de rango de ataque (más sutil)
        if self.can_attack():
            range_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (255, 255, 255, 15), 
                             (self.attack_range, self.attack_range), self.attack_range)
            pygame.draw.circle(range_surface, (255, 255, 255, 40), 
                             (self.attack_range, self.attack_range), self.attack_range, 1)
            screen.blit(range_surface, (int(self.x - self.attack_range), int(self.y - self.attack_range)))

        # Dibujar al jugador (Caballero)
        # Capa / Cuerpo
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size//2)
        
        # Casco (Plateado/Gris)
        helmet_color = (200, 200, 200)
        pygame.draw.circle(screen, helmet_color, (int(self.x), int(self.y)), self.size//3)
        
        # Visera del casco (Cruz)
        pygame.draw.line(screen, BLACK, (self.x - 5, self.y), (self.x + 5, self.y), 2)
        pygame.draw.line(screen, BLACK, (self.x, self.y - 5), (self.x, self.y + 5), 2)
            
        # Barra de vida flotante
        bar_width = self.size + 10
        bar_height = 4
        bar_x = self.x - bar_width//2
        bar_y = self.y - self.size - 5
        
        # Fondo de la barra
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de vida actual
        health_pct = self.health / self.max_health
        health_color = GREEN if health_pct > 0.4 else RED
        health_width = int(bar_width * health_pct)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
