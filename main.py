"""
Juego de Defensa de Base - Ciclos Día/Noche
Objetivo: Defender la base durante 5 noches
"""
import pygame
import sys
from game_manager import GameManager

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defensa de Base - 5 Noches")

# Reloj para controlar FPS
clock = pygame.time.Clock()
FPS = 60

def main():
    """Función principal del juego"""
    game = GameManager(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time en segundos
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Actualizar
        game.update(dt)
        
        # Renderizar
        game.render()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
