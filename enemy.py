"""
Clase para los enemigos
"""
import pygame
import math
import random
from config import *

class Enemy:
    def __init__(self, x, y, enemy_type, base, night_number):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.base = base
        
        # Configuración según el tipo
        config = ENEMY_TYPES[enemy_type].copy()
        
        # Escalar dificultad según la noche
        difficulty_multiplier = 1 + (night_number - 1) * 0.15
        
        self.max_health = config["health"] * difficulty_multiplier
        self.health = self.max_health
        self.speed = config["speed"] * (1 + (night_number - 1) * 0.1)
        self.damage = config["damage"] * difficulty_multiplier
        self.color = config["color"]
        self.size = config["size"]
        self.attack_cooldown = 1.0
        self.attack_timer = 0
        
    def update(self, dt, player):
        """Actualiza el movimiento del enemigo hacia la base"""
        # Reducir timer de ataque
        if self.attack_timer > 0:
            self.attack_timer -= dt
        
        # Calcular dirección hacia la base
        dx = self.base.x - self.x
        dy = self.base.y - self.y
        
        # Si el jugador está cerca, considerar atacarlo
        player_dist = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
        if player_dist < 100:
            dx = player.x - self.x
            dy = player.y - self.y
        
        # Normalizar
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
            
            # Mover hacia el objetivo
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
    
    def take_damage(self, damage):
        """El enemigo recibe daño"""
        self.health -= damage
    
    def can_attack(self):
        """Verifica si el enemigo puede atacar"""
        return self.attack_timer <= 0
    
    def attack_target(self, target):
        """Ataca un objetivo (base o jugador)"""
        if self.can_attack():
            target.take_damage(self.damage)
            self.attack_timer = self.attack_cooldown
            return True
        return False
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def render(self, screen):
        """Dibuja al enemigo en pantalla con aspecto intimidante"""
        
        # Efecto de ojos brillantes común
        eye_color = (255, 50, 0) # Rojo anaranjado brillante
        if self.type == "rapido":
            eye_color = (255, 255, 0) # Amarillo vicioso
        
        # Dibujar forma según tipo
        if self.type == "lento":
            # --- OGRO DE GUERRA --- (Tanque)
            # Cuerpo masivo con armadura pesada
            # Hombbreras con pinchos
            spike_size = 8
            pygame.draw.polygon(screen, (30, 30, 30), [(self.x - self.size//2, self.y - self.size//2), 
                                                      (self.x - self.size//2 - spike_size, self.y - self.size//2 - spike_size), 
                                                      (self.x - self.size//2 + spike_size, self.y - self.size//2)])
            pygame.draw.polygon(screen, (30, 30, 30), [(self.x + self.size//2, self.y - self.size//2), 
                                                      (self.x + self.size//2 + spike_size, self.y - self.size//2 - spike_size), 
                                                      (self.x + self.size//2 - spike_size, self.y - self.size//2)])

            # Cuerpo principal
            pygame.draw.rect(screen, self.color, 
                           (self.x - self.size//2, self.y - self.size//2, self.size, self.size))
            # Placa de pecho de hierro oxidado
            pygame.draw.rect(screen, (60, 50, 40), 
                           (self.x - self.size//3, self.y - self.size//3, self.size//1.5, self.size//1.5))
            
            # Cara fea
            pygame.draw.circle(screen, eye_color, (int(self.x - 5), int(self.y - 8)), 2)
            pygame.draw.circle(screen, eye_color, (int(self.x + 5), int(self.y - 8)), 2)
            # Boca (cicatriz)
            pygame.draw.line(screen, (20, 20, 20), (self.x - 6, self.y + 5), (self.x + 6, self.y + 2), 2)

            # Arma: Gran Garrote con clavos
            club_len = 25
            pygame.draw.line(screen, (101, 67, 33), (self.x + self.size//2, self.y), (self.x + self.size//2 + club_len, self.y + 5), 6)
            # Clavos del garrote
            pygame.draw.circle(screen, (150, 150, 150), (int(self.x + self.size//2 + club_len), int(self.y + 5)), 3)

                           
        elif self.type == "rapido":
            # --- GOBLIN SAQUEADOR --- (Rápido)
            # Cuerpo anguloso y errático
            points = [
                (self.x, self.y + self.size//2), # Abajo centro
                (self.x - self.size//2, self.y - self.size//4), # Izq arr
                (self.x + self.size//2, self.y - self.size//4), # Der arr
                (self.x, self.y - self.size) # Cabeza arr
            ]
            pygame.draw.polygon(screen, self.color, points)
            
            # Orejas largas
            ear_l = [(self.x - 5, self.y - 10), (self.x - 15, self.y - 15), (self.x - 5, self.y - 5)]
            ear_r = [(self.x + 5, self.y - 10), (self.x + 15, self.y - 15), (self.x + 5, self.y - 5)]
            pygame.draw.polygon(screen, self.color, ear_l)
            pygame.draw.polygon(screen, self.color, ear_r)

            # Ojos brillantes grandes
            pygame.draw.circle(screen, eye_color, (int(self.x - 3), int(self.y - 12)), 2)
            pygame.draw.circle(screen, eye_color, (int(self.x + 3), int(self.y - 12)), 2)
            
            # Dagas duales
            pygame.draw.line(screen, (200, 200, 200), (self.x - 10, self.y), (self.x - 15, self.y + 10), 2)
            pygame.draw.line(screen, (200, 200, 200), (self.x + 10, self.y), (self.x + 15, self.y + 10), 2)
            
        else: # balanceado
            # --- ORCO BERSERKER --- (Equilibrado)
            # Cuerpo robusto
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size//2)
            # Casco con cuernos
            horn_color = (200, 200, 180)
            pygame.draw.polygon(screen, horn_color, [(self.x - 5, self.y - 10), (self.x - 12, self.y - 20), (self.x - 2, self.y - 10)])
            pygame.draw.polygon(screen, horn_color, [(self.x + 5, self.y - 10), (self.x + 12, self.y - 20), (self.x + 2, self.y - 10)])
            
            # Escudo de hierro negro con emblema rojo
            shield_pos = (int(self.x - 8), int(self.y + 5))
            pygame.draw.circle(screen, (20, 20, 20), shield_pos, self.size//3)
            pygame.draw.circle(screen, (100, 20, 20), shield_pos, 3) # Emblema

            # Ojos rojos furiosos
            pygame.draw.line(screen, eye_color, (self.x - 4, self.y - 2), (self.x - 1, self.y - 1), 2)
            pygame.draw.line(screen, eye_color, (self.x + 4, self.y - 2), (self.x + 1, self.y - 1), 2)
            
            # Hacha
            weapon_pos = (self.x + 10, self.y)
            pygame.draw.line(screen, (100, 50, 0), (self.x, self.y), (self.x + 15, self.y - 5), 3) # Mango
            pygame.draw.circle(screen, (180, 180, 180), (int(self.x + 15), int(self.y - 5)), 6) # Hoja
        
        # Barra de vida más minimalista y oscura
        bar_width = self.size
        bar_height = 3
        bar_x = self.x - bar_width//2
        bar_y = self.y - self.size//2 - 10
        
        # Fondo y vida
        health_pct = self.health / self.max_health
        if health_pct < 1.0: # Solo mostrar si está dañado
            pygame.draw.rect(screen, (50, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (200, 20, 20), (bar_x, bar_y, int(bar_width * health_pct), bar_height))


class EnemySpawner:
    def __init__(self, screen_width, screen_height, base):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.base = base
        self.spawn_timer = 0
    
    def spawn_enemy(self, night_number):
        """Genera un enemigo en un borde aleatorio del mapa"""
        # Configuración de la noche actual
        config = NIGHT_CONFIG[night_number]
        
        # Seleccionar tipo de enemigo aleatorio
        enemy_type = random.choice(config["types"])
        
        # Seleccionar borde aleatorio
        side = random.choice(["top", "bottom", "left", "right"])
        
        if side == "top":
            x = random.randint(ENEMY_SPAWN_MARGIN, self.screen_width - ENEMY_SPAWN_MARGIN)
            y = ENEMY_SPAWN_MARGIN
        elif side == "bottom":
            x = random.randint(ENEMY_SPAWN_MARGIN, self.screen_width - ENEMY_SPAWN_MARGIN)
            y = self.screen_height - ENEMY_SPAWN_MARGIN
        elif side == "left":
            x = ENEMY_SPAWN_MARGIN
            y = random.randint(ENEMY_SPAWN_MARGIN, self.screen_height - ENEMY_SPAWN_MARGIN)
        else:  # right
            x = self.screen_width - ENEMY_SPAWN_MARGIN
            y = random.randint(ENEMY_SPAWN_MARGIN, self.screen_height - ENEMY_SPAWN_MARGIN)
        
        return Enemy(x, y, enemy_type, self.base, night_number)
    
    def update(self, dt, enemies, night_number, current_spawned, max_spawns):
        """Actualiza el spawner y genera enemigos"""
        if current_spawned >= max_spawns:
            return 0
        
        config = NIGHT_CONFIG[night_number]
        spawn_interval = config["spawn_interval"]
        
        self.spawn_timer += dt
        
        spawned = 0
        while self.spawn_timer >= spawn_interval and current_spawned + spawned < max_spawns:
            enemy = self.spawn_enemy(night_number)
            enemies.append(enemy)
            self.spawn_timer -= spawn_interval
            spawned += 1
        
        return spawned
