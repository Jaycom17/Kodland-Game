import pygame
import random
import math
from .settings import *

def generar_fondo_pasto(ancho, alto):
    superficie = pygame.Surface((ancho, alto))

    # 1. Gradiente base: Verde oscuro y profundo, sobrio
    color_top = (30, 50, 25)      # Verde bosque muy oscuro
    color_bottom = (45, 75, 35)   # Verde oliva oscuro
    
    for y in range(alto):
        factor = y / alto
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * factor)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * factor)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * factor)
        pygame.draw.line(superficie, (r, g, b), (0, y), (ancho, y))

    # 2. Textura sutil (ruido suave) para romper la uniformidad
    for _ in range(800):
        cx = random.randint(0, ancho - 1)
        cy = random.randint(0, alto - 1)
        radio = random.randint(15, 40)
        variacion = random.randint(-8, 8) 
        
        try:
            color_base = superficie.get_at((cx, cy))
            r = max(0, min(255, color_base.r + variacion))
            g = max(0, min(255, color_base.g + variacion))
            b = max(0, min(255, color_base.b + variacion))
            
            s_parche = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
            pygame.draw.circle(s_parche, (r, g, b, 40), (radio, radio), radio)
            superficie.blit(s_parche, (cx-radio, cy-radio))
        except IndexError:
            pass

    # 3. Zonas de tierra (grandes y difusas, no caminos ruidosos)
    for _ in range(12): 
        cx = random.randint(0, ancho)
        cy = random.randint(0, alto)
        rx = random.randint(80, 200)
        ry = random.randint(60, 150)
        
        s_tierra = pygame.Surface((rx*2, ry*2), pygame.SRCALPHA)
        # Marrón tierra oscuro, baja opacidad
        color_tierra = (65, 50, 35, 90) 
        pygame.draw.ellipse(s_tierra, color_tierra, (0, 0, rx*2, ry*2))
        superficie.blit(s_tierra, (cx-rx, cy-ry))

    # 4. Detalles muy escasos (pequeños matojos)
    for _ in range(150):
        cx = random.randint(0, ancho)
        cy = random.randint(0, alto)
        color_matojo = (55, 85, 45) # Un poco más claro que el fondo
        
        # Pequeño grupo de 3 lineas
        for i in range(-1, 2):
            pygame.draw.line(superficie, color_matojo, (cx, cy), (cx + i*4, cy - 6), 1)

    return superficie

def generar_fondo_muro(ancho, alto):
    superficie = pygame.Surface((ancho, alto))
    superficie.fill((30, 30, 35)) # Gris base oscuro
    
    # Patrón de ladrillos
    ancho_ladrillo = 60
    alto_ladrillo = 30
    
    for y in range(0, alto, alto_ladrillo):
        desplazamiento = 0 if (y // alto_ladrillo) % 2 == 0 else ancho_ladrillo // 2
        for x in range(-30, ancho, ancho_ladrillo):
            # Variación de color para realismo
            val = random.randint(40, 60)
            color = (val, val, val + 5)
            
            rect = pygame.Rect(x + desplazamiento, y, ancho_ladrillo, alto_ladrillo)
            pygame.draw.rect(superficie, color, rect)
            pygame.draw.rect(superficie, (20, 20, 25), rect, 1) # Borde oscuro
            
    return superficie
