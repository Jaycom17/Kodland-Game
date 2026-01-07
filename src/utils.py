import pygame
from .settings import *

def dibujar_texto(pantalla, texto, tamaño, color, x, y, centrado=True):
    fuente = pygame.font.SysFont("Arial", tamaño, bold=True)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    if centrado:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
    pantalla.blit(superficie_texto, rect_texto)
    return rect_texto

def dibujar_boton_medieval(pantalla, texto, x, y, ancho, alto, mouse_pos):
    rect_boton = pygame.Rect(x - ancho//2, y - alto//2, ancho, alto)
    hover = rect_boton.collidepoint(mouse_pos)
    
    # Colores madera
    color_madera_claro = (139, 69, 19)
    color_madera_oscuro = (101, 67, 33)
    color_base = color_madera_claro if hover else color_madera_oscuro
    
    # Forma base
    pygame.draw.rect(pantalla, color_base, rect_boton)
    
    # Marco metálico con remaches
    border_color = (255, 215, 0) if hover else (192, 192, 192) # Oro o Plata
    pygame.draw.rect(pantalla, border_color, rect_boton, 4)
    
    # Remaches en esquinas
    radio_remache = 5
    offset = 8
    puntos = [
        (rect_boton.left + offset, rect_boton.top + offset),
        (rect_boton.right - offset, rect_boton.top + offset),
        (rect_boton.left + offset, rect_boton.bottom - offset),
        (rect_boton.right - offset, rect_boton.bottom - offset)
    ]
    for p in puntos:
        pygame.draw.circle(pantalla, border_color, p, radio_remache)
        pygame.draw.circle(pantalla, (50, 50, 50), p, radio_remache-2)
    
    # Texto con sombra
    dibujar_texto(pantalla, texto, 32, (0, 0, 0), x + 2, y + 2)
    dibujar_texto(pantalla, texto, 32, (255, 255, 255), x, y)
    
    return rect_boton

def dibujar_boton(pantalla, texto, x, y, ancho, alto, color_normal, color_hover, mouse_pos):
    rect_boton = pygame.Rect(x - ancho//2, y - alto//2, ancho, alto)
    color = color_hover if rect_boton.collidepoint(mouse_pos) else color_normal
    
    # Efecto de botón 3D simple
    pygame.draw.rect(pantalla, (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40)), (rect_boton.x, rect_boton.y+4, ancho, alto))
    pygame.draw.rect(pantalla, color, rect_boton)
    pygame.draw.rect(pantalla, BLANCO, rect_boton, 2)
    dibujar_texto(pantalla, texto, 24, BLANCO, x, y)
    
    return rect_boton
