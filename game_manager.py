"""
Game Manager - Gestor principal del juego
"""
import pygame
import math
from config import *
from base import Base
from player import Player
from enemy import Enemy, EnemySpawner
from resource import ResourceManager
from upgrade import UpgradeMenu
from day_night import DayNightCycle
from screens import MenuScreen, VictoryScreen, DefeatScreen

class GameManager:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Estados del juego: "menu", "playing", "victory", "defeat"
        self.game_state = "menu"
        
        # Pantallas
        self.menu_screen = MenuScreen(screen_width, screen_height)
        self.victory_screen = VictoryScreen(screen_width, screen_height)
        self.defeat_screen = DefeatScreen(screen_width, screen_height)
        
        # Variables de juego
        self.base = None
        self.player = None
        self.enemies = []
        self.enemy_spawner = None
        self.resource_manager = None
        self.upgrade_menu = None
        self.day_night_cycle = None
        self.resources = 0
        self.enemies_spawned = 0
        self.defeat_reason = ""
        
    def start_game(self):
        """Inicia una nueva partida"""
        # Crear la base en el centro
        self.base = Base(self.screen_width // 2, self.screen_height // 2)
        
        # Crear el jugador cerca de la base
        self.player = Player(self.screen_width // 2 - 100, self.screen_height // 2)
        
        # Inicializar sistemas
        self.enemies = []
        self.enemy_spawner = EnemySpawner(self.screen_width, self.screen_height, self.base)
        self.resource_manager = ResourceManager(self.screen_width, self.screen_height)
        self.upgrade_menu = UpgradeMenu(self.screen_width, self.screen_height)
        self.day_night_cycle = DayNightCycle()
        
        # Inicializar recursos
        self.resources = 50  # Recursos iniciales
        self.enemies_spawned = 0
        
        # Comenzar el ciclo día/noche
        self.day_night_cycle.start_game()
        
        # Generar recursos para el primer día
        self.resource_manager.spawn_resources(self.base.x, self.base.y)
        
        # Cambiar estado
        self.game_state = "playing"
    
    def handle_event(self, event):
        """Maneja los eventos del juego"""
        if event.type == pygame.KEYDOWN:
            if self.game_state == "menu":
                self.handle_menu_input(event)
            elif self.game_state == "playing":
                self.handle_playing_input(event)
            elif self.game_state == "victory" or self.game_state == "defeat":
                self.handle_end_screen_input(event)
    
    def handle_menu_input(self, event):
        """Maneja la entrada en el menú principal"""
        if event.key == pygame.K_UP:
            self.menu_screen.navigate_up()
        elif event.key == pygame.K_DOWN:
            self.menu_screen.navigate_down()
        elif event.key == pygame.K_RETURN:
            option = self.menu_screen.get_selected_option()
            if option == "Iniciar Juego":
                self.start_game()
            elif option == "Salir":
                pygame.quit()
                exit()
    
    def handle_playing_input(self, event):
        """Maneja la entrada durante el juego"""
        if self.day_night_cycle.is_day():
            if event.key == pygame.K_SPACE or event.key == pygame.K_m:
                self.upgrade_menu.toggle()
            elif self.upgrade_menu.visible:
                if event.key == pygame.K_UP:
                    self.upgrade_menu.navigate_up()
                elif event.key == pygame.K_DOWN:
                    self.upgrade_menu.navigate_down()
                elif event.key == pygame.K_RETURN:
                    self.try_purchase_upgrade()
                elif event.key == pygame.K_ESCAPE:
                    self.upgrade_menu.hide()
    
    def handle_end_screen_input(self, event):
        """Maneja la entrada en las pantallas finales"""
        if event.key == pygame.K_RETURN:
            self.game_state = "menu"
    
    def try_purchase_upgrade(self):
        """Intenta comprar una mejora"""
        upgrade = self.upgrade_menu.get_selected_upgrade()
        if self.resources >= upgrade["cost"]:
            success = self.upgrade_menu.apply_upgrade(upgrade["id"], self.player, self.base)
            if success:
                self.resources -= upgrade["cost"]
    
    def update(self, dt):
        """Actualiza el estado del juego"""
        if self.game_state == "playing":
            self.update_playing(dt)
    
    def update_playing(self, dt):
        """Actualiza la lógica del juego durante la partida"""
        # Guardar fase anterior para detectar cambios
        previous_phase = self.day_night_cycle.phase if self.day_night_cycle else "day"
        
        # Actualizar ciclo día/noche
        self.day_night_cycle.update(dt)
        
        # Detectar transición de NOCHE a DÍA
        if previous_phase == "night" and self.day_night_cycle.phase == "day":
            # Limpiar enemigos restantes
            self.enemies.clear()
            self.enemies_spawned = 0
            
            # Generar nuevos recursos
            self.resource_manager.spawn_resources(self.base.x, self.base.y)
        
        # Actualizar jugador
        if not self.upgrade_menu.visible:
            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1
            
            # Pasar el rectángulo de la base como obstáculo
            self.player.move(dx, dy, dt, self.screen_width, self.screen_height, [self.base.get_rect()])
        
        self.player.update(dt)
        
        if self.day_night_cycle.is_day():
            self.update_day_phase(dt)
        else:
            self.update_night_phase(dt)
        
        # Verificar condiciones de victoria/derrota
        self.check_game_over()
    
    def update_day_phase(self, dt):
        """Actualiza la fase de día"""
        # Recolectar recursos
        collected = self.resource_manager.update(self.player)
        if collected > 0:
            self.resources += collected
    
    def update_night_phase(self, dt):
        """Actualiza la fase de noche"""
        # Generar enemigos
        config = NIGHT_CONFIG[self.day_night_cycle.night_number]
        max_enemies = config["enemy_count"]
        
        spawned = self.enemy_spawner.update(dt, self.enemies, 
                                           self.day_night_cycle.night_number, 
                                           self.enemies_spawned, max_enemies)
        self.enemies_spawned += spawned
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player)
            
            # Verificar colisión con la base
            if enemy.get_rect().colliderect(self.base.get_rect()):
                enemy.attack_target(self.base)
            
            # Verificar colisión con el jugador
            if enemy.get_rect().colliderect(self.player.get_rect()):
                enemy.attack_target(self.player)
        
        # El jugador ataca automáticamente
        if keys := pygame.key.get_pressed():
            if keys[pygame.K_SPACE] or keys[pygame.K_e]:
                self.player.attack(self.enemies)
        else:
            # Auto-ataque si hay enemigos en rango
            self.player.attack(self.enemies)
    
    def check_game_over(self):
        """Verifica las condiciones de victoria o derrota"""
        # Verificar derrota
        if not self.player.is_alive():
            self.game_state = "defeat"
            self.defeat_reason = "player"
        elif not self.base.is_alive():
            self.game_state = "defeat"
            self.defeat_reason = "base"
        # Verificar victoria (completar 5 noches)
        elif self.day_night_cycle.night_number > 5 and self.day_night_cycle.is_day():
            self.game_state = "victory"
    
    def render(self):
        """Renderiza el juego"""
        if self.game_state == "menu":
            self.menu_screen.render(self.screen)
        elif self.game_state == "playing":
            self.render_playing()
        elif self.game_state == "victory":
            self.victory_screen.render(self.screen, self.base.health, 
                                      self.resource_manager.total_collected)
        elif self.game_state == "defeat":
            self.defeat_screen.render(self.screen, self.day_night_cycle.night_number, 
                                     self.defeat_reason)
    
    def render_playing(self):
        """Renderiza el juego durante la partida"""
        # Fondo según fase
        self.day_night_cycle.render_background(self.screen, self.screen_width, self.screen_height)
        
        # Renderizar recursos (solo en día)
        if self.day_night_cycle.is_day():
            self.resource_manager.render(self.screen)
        
        # Renderizar base
        self.base.render(self.screen)
        
        # Renderizar jugador
        self.player.render(self.screen)
        
        # Renderizar enemigos
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        # UI del ciclo día/noche
        self.day_night_cycle.render_ui(self.screen, self.screen_width, self.screen_height)
        
        # UI de recursos
        self.render_resources_ui()
        
        # UI de estado del jugador
        self.render_player_stats()
        
        # Menú de mejoras
        self.upgrade_menu.render(self.screen, self.resources)
        
        # Indicador de teclas
        if self.day_night_cycle.is_day() and not self.upgrade_menu.visible:
            font_help = pygame.font.Font(None, 24)
            help_text = font_help.render("Presiona ESPACIO para abrir el menú de mejoras", True, WHITE)
            self.screen.blit(help_text, (self.screen_width // 2 - help_text.get_width() // 2, 
                                        self.screen_height - 30))
    
    def render_resources_ui(self):
        """Renderiza la UI de recursos"""
        # Panel de recursos (Estilo Pergamino pequeño)
        panel_rect = pygame.Rect(20, self.screen_height - 60, 200, 40)
        pygame.draw.rect(self.screen, UI_BG, panel_rect)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, 3)
        
        font = pygame.font.Font(None, 32)
        resources_text = font.render(f"Oro: {self.resources}", True, YELLOW)
        text_rect = resources_text.get_rect(midleft=(35, self.screen_height - 40))
        self.screen.blit(resources_text, text_rect)
    
    def render_player_stats(self):
        """Renderiza las estadísticas del jugador"""
        panel_rect = pygame.Rect(20, self.screen_height - 180, 200, 110)
        pygame.draw.rect(self.screen, UI_BG, panel_rect)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, 3)
        
        font = pygame.font.Font(None, 24)
        font_bold = pygame.font.Font(None, 28)
        
        y_offset = self.screen_height - 165
        
        # Título
        title = font_bold.render("CABALLERO", True, UI_TEXT)
        self.screen.blit(title, (35, y_offset))
        y_offset += 30
        
        # Stats
        stats = [
            f"Salud: {int(self.player.health)}/{int(self.player.max_health)}",
            f"Fuerza: {int(self.player.damage)}",
            f"Velocidad: {int(self.player.speed)}"
        ]
        
        for stat in stats:
            stat_text = font.render(stat, True, WHITE)
            self.screen.blit(stat_text, (35, y_offset))
            y_offset += 25
