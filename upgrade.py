"""
Sistema de mejoras del jugador y la base
"""
import pygame
from config import *

class UpgradeMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False
        self.upgrades = [
            {"id": "daño", "name": "Aumentar Daño", "cost": UPGRADES["daño"]["cost"], "increment": UPGRADES["daño"]["increment"]},
            {"id": "velocidad", "name": "Aumentar Velocidad", "cost": UPGRADES["velocidad"]["cost"], "increment": UPGRADES["velocidad"]["increment"]},
            {"id": "vida_jugador", "name": "Aumentar Vida", "cost": UPGRADES["vida_jugador"]["cost"], "increment": UPGRADES["vida_jugador"]["increment"]},
            {"id": "reparar_base", "name": "Reparar Base", "cost": UPGRADES["reparar_base"]["cost"], "increment": UPGRADES["reparar_base"]["increment"]},
            {"id": "resistencia_base", "name": "Resistencia Base", "cost": UPGRADES["resistencia_base"]["cost"], "increment": UPGRADES["resistencia_base"]["increment"]}
        ]
        self.selected_index = 0
        
        # Dimensiones del menú
        self.menu_width = 400
        self.menu_height = 450
        self.menu_x = (screen_width - self.menu_width) // 2
        self.menu_y = (screen_height - self.menu_height) // 2
    
    def toggle(self):
        """Muestra u oculta el menú"""
        self.visible = not self.visible
    
    def show(self):
        """Muestra el menú"""
        self.visible = True
    
    def hide(self):
        """Oculta el menú"""
        self.visible = False
    
    def navigate_up(self):
        """Navega hacia arriba en el menú"""
        if self.selected_index > 0:
            self.selected_index -= 1
    
    def navigate_down(self):
        """Navega hacia abajo en el menú"""
        if self.selected_index < len(self.upgrades) - 1:
            self.selected_index += 1
    
    def get_selected_upgrade(self):
        """Obtiene la mejora seleccionada"""
        return self.upgrades[self.selected_index]
    
    def apply_upgrade(self, upgrade_id, player, base):
        """Aplica una mejora al jugador o la base"""
        if upgrade_id == "daño":
            player.increase_damage(UPGRADES["daño"]["increment"])
            return True
        elif upgrade_id == "velocidad":
            player.increase_speed(UPGRADES["velocidad"]["increment"])
            return True
        elif upgrade_id == "vida_jugador":
            player.increase_max_health(UPGRADES["vida_jugador"]["increment"])
            return True
        elif upgrade_id == "reparar_base":
            base.repair(UPGRADES["reparar_base"]["increment"])
            return True
        elif upgrade_id == "resistencia_base":
            base.increase_max_health(UPGRADES["resistencia_base"]["increment"])
            return True
        return False
    
    def render(self, screen, resources):
        """Dibuja el menú de mejoras"""
        if not self.visible:
            return
        
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Panel del menú (Estilo libro antiguo / pergamino)
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(screen, UI_BG, menu_rect)
        pygame.draw.rect(screen, UI_BORDER, menu_rect, 5)
        
        # Título
        font_title = pygame.font.Font(None, 48)
        title_text = font_title.render("ARMERÍA REAL", True, YELLOW)
        title_rect = title_text.get_rect(center=(self.menu_x + self.menu_width//2, self.menu_y + 40))
        screen.blit(title_text, title_rect)
        
        # Recursos disponibles
        font_resources = pygame.font.Font(None, 32)
        resources_text = font_resources.render(f"Oro disponible: {resources}", True, WHITE)
        resources_rect = resources_text.get_rect(center=(self.menu_x + self.menu_width//2, self.menu_y + 80))
        screen.blit(resources_text, resources_rect)
        
        # Lista de mejoras
        font_upgrade = pygame.font.Font(None, 28)
        y_offset = self.menu_y + 120
        
        for i, upgrade in enumerate(self.upgrades):
            # Fondo de la opción
            option_rect = pygame.Rect(self.menu_x + 20, y_offset, self.menu_width - 40, 50)
            
            if i == self.selected_index:
                pygame.draw.rect(screen, (80, 60, 40), option_rect) # Selección marrón claro
                pygame.draw.rect(screen, YELLOW, option_rect, 2)
            else:
                pygame.draw.rect(screen, (50, 40, 30), option_rect) # Deseleccionado oscuro
                pygame.draw.rect(screen, BLACK, option_rect, 1)
            
            # Texto de la mejora
            can_afford = resources >= upgrade["cost"]
            color = WHITE if can_afford else (150, 50, 50) # Rojo oscuro si no alcanza
            
            upgrade_text = font_upgrade.render(f"{upgrade['name']} - {upgrade['cost']} Oro", True, color)
            text_rect = upgrade_text.get_rect(left=option_rect.left + 15, centery=option_rect.centery)
            screen.blit(upgrade_text, text_rect)
            
            y_offset += 60
        
        # Instrucciones
        font_instructions = pygame.font.Font(None, 24)
        instructions = [
            "ARRIBA/ABAJO: Navegar",
            "ENTER: Comprar mejora",
            "ESC: Cerrar menú"
        ]
        
        y_offset = self.menu_y + self.menu_height - 80
        for instruction in instructions:
            inst_text = font_instructions.render(instruction, True, (200, 200, 200))
            inst_rect = inst_text.get_rect(center=(self.menu_x + self.menu_width//2, y_offset))
            screen.blit(inst_text, inst_rect)
            y_offset += 25
