import pygame
from .settings import *
from .utils import dibujar_texto, dibujar_boton, dibujar_boton_medieval

def pantalla_menu(pantalla, mouse_pos, fondo):
    """Renderiza menú principal con título y botón de inicio."""
    pantalla.blit(fondo, (0, 0))
    
    s = pygame.Surface((700, 150), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect(), border_radius=20)
    pantalla.blit(s, (ANCHO//2 - 350, 120))

    dibujar_texto(pantalla, "CRÓNICAS MEDIEVALES", 56, DORADO, ANCHO//2, 160)
    dibujar_texto(pantalla, "La Última Defensa", 36, GRIS_ACERO, ANCHO//2, 230)
    
    return dibujar_boton_medieval(pantalla, "INICIAR BATALLA", ANCHO//2, 400, 300, 70, mouse_pos)

def pantalla_seleccion_arma(pantalla, mouse_pos):
    """Renderiza pantalla de selección con cartas interactivas de armas y sus estadísticas."""
    
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "ELIGE TU DESTINO", 60, DORADO, ANCHO//2, 50)
    
    botones = []
    ancho_carta = 240
    alto_carta = 400
    sep_cartas = 260
    start_x = ANCHO//2 - sep_cartas
    
    posiciones = [start_x, ANCHO//2, ANCHO//2 + sep_cartas]
    armas_lista = ["vara", "espada", "mazo"]
    
    c_y = ALTO // 2 + 30
    
    fuente_desc = pygame.font.SysFont("Arial", 18, bold=False)

    for i, arma_tipo in enumerate(armas_lista):
        arma = ARMAS[arma_tipo]
        x = posiciones[i]
        
        rect_carta = pygame.Rect(x - ancho_carta//2, c_y - alto_carta//2, ancho_carta, alto_carta)
        
        es_hover = rect_carta.collidepoint(mouse_pos)
        color_borde = DORADO if es_hover else arma["color"]
        grosor_borde = 4 if es_hover else 2
        
        pygame.draw.rect(pantalla, (25, 25, 30), rect_carta)
        pygame.draw.rect(pantalla, color_borde, rect_carta, grosor_borde)
        
        dibujar_texto(pantalla, arma["nombre"], 24, arma["color"], x, rect_carta.top + 40)
        
        w_y = rect_carta.top + 120 
        
        if arma_tipo == 'vara':
            pygame.draw.line(pantalla, MARRON_MADERA, (x-25, w_y+25), (x+25, w_y-25), 5)
            pygame.draw.circle(pantalla, AZUL_MAGICO, (x+25, w_y-25), 10)
            pygame.draw.circle(pantalla, (200, 200, 255), (x+25, w_y-25), 5)
        elif arma_tipo == 'espada':
             pygame.draw.rect(pantalla, GRIS_ACERO, (x-5, w_y-50, 10, 70))
             pygame.draw.polygon(pantalla, GRIS_ACERO, [(x-5, w_y-50), (x+5, w_y-50), (x, w_y-65)])
             pygame.draw.line(pantalla, DORADO, (x-20, w_y+20), (x+20, w_y+20), 5)
             pygame.draw.line(pantalla, MARRON_MADERA, (x, w_y+20), (x, w_y+45), 5)
        else: # mazo
             pygame.draw.rect(pantalla, MARRON_MADERA, (x-4, w_y-10, 8, 60))
             pygame.draw.rect(pantalla, GRIS_PIEDRA, (x-25, w_y-35, 50, 30))
             pygame.draw.rect(pantalla, (150,150,150), (x-25, w_y-35, 50, 30), 2)

        pygame.draw.line(pantalla, (50, 50, 50), (x - 90, rect_carta.top + 190), (x + 90, rect_carta.top + 190), 2)
        
        stats_y = rect_carta.top + 220
        dibujar_texto(pantalla, f"Velocidad: {arma['velocidad_ataque']}s", 22, BLANCO, x, stats_y)
        dibujar_texto(pantalla, f"Daño: {arma['daño']}", 22, BLANCO, x, stats_y + 30)
        
      
        desc_y = stats_y + 65
        texto_desc = arma["descripcion"]
        
        palabras = texto_desc.split()
        lineas = []
        linea_act = ""
        ancho_max = ancho_carta - 30 
        
        for p in palabras:
            test = linea_act + p + " "
            w, _ = fuente_desc.size(test)
            if w < ancho_max:
                linea_act = test
            else:
                lineas.append(linea_act)
                linea_act = p + " "
        lineas.append(linea_act)
        
        for i, linea in enumerate(lineas):
            txt_surf = fuente_desc.render(linea, True, GRIS_ACERO)
            txt_rect = txt_surf.get_rect(center=(x, desc_y + i * 22))
            pantalla.blit(txt_surf, txt_rect)

        botones.append((rect_carta, arma_tipo))
    return botones

def pantalla_juego(pantalla, jugador, enemigos, efectos, oleada, enemigos_totales, fondo):
    """Renderiza la pantalla de combate: fondo, entidades, efectos y HUD superior."""
    
    pantalla.blit(fondo, (0, 0))
    
    for efecto in efectos:
        efecto.dibujar(pantalla)
    
    for enemigo in enemigos:
        enemigo.dibujar(pantalla)
    
    jugador.dibujar(pantalla)
    
    ancho_ui = 300
    alto_ui = 100
    s = pygame.Surface((ancho_ui, alto_ui))
    s.set_alpha(150)
    s.fill(NEGRO)
    pantalla.blit(s, (ANCHO//2 - ancho_ui//2, 10))
    
    dibujar_texto(pantalla, f"OLEADA {oleada}/5", 40, BLANCO, ANCHO//2, 35)
    dibujar_texto(pantalla, f"Enemigos: {enemigos_totales}", 24, GRIS_ACERO, ANCHO//2, 75)

def pantalla_fin_juego(pantalla, estado, oleada_alcanzada, mouse_pos, fondo):
    """Muestra pantalla de Victoria o Game Over con oleada alcanzada y botón de reinicio."""
    pantalla.blit(fondo, (0, 0))

    if estado == VICTORIA:
        color_titulo = VERDE_CÉSPED
        titulo = "¡VICTORIA GLORIOSA!"
    else:
        color_titulo = ROJO_SANGRE
        titulo = "GAME OVER"

    overlay_ancho = 820
    overlay_alto = 220
    s = pygame.Surface((overlay_ancho, overlay_alto), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect(), border_radius=24)
    pantalla.blit(s, (ANCHO//2 - overlay_ancho//2, 150))

    dibujar_texto(pantalla, titulo, 58, color_titulo, ANCHO//2, 210)
    dibujar_texto(pantalla, f"Oleada alcanzada: {oleada_alcanzada}", 32, BLANCO, ANCHO//2, 300)
    
    return dibujar_boton_medieval(pantalla, "MENU PRINCIPAL", ANCHO//2, 450, 300, 60, mouse_pos)
