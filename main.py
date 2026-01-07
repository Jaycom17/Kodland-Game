import pygame
import random
import sys
from src.settings import *
from src.world import generar_fondo_pasto, generar_fondo_muro
from src.entities import Jugador, generar_enemigos
from src.ui import pantalla_menu, pantalla_seleccion_arma, pantalla_juego, pantalla_fin_juego

def main():
    # Inicialización de Pygame
    pygame.init()
    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Survival Medieval Pro")
    reloj = pygame.time.Clock()
    
    estado_juego = MENU
    jugador = None
    enemigos = []
    efectos = [] # Proyectiles y visuales
    oleada_actual = 1
    enemigos_por_oleada = [15, 20, 30, 40, 50] 
    enemigos_generados = 0
    enemigos_restantes_spawn = 0
    oleada_alcanzada = 0
    timer_spawn = 0
    
    # Cargar fondo
    print("Generando mundo...")
    fondo_juego = generar_fondo_pasto(ANCHO, ALTO)
    fondo_menu = generar_fondo_muro(ANCHO, ALTO)
    
    # Configurar música
    try:
        pygame.mixer.music.load("song.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar la música ({e})")

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        tiempo_actual = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_juego == MENU:
                    button_rect = pantalla_menu(pantalla, mouse_pos, fondo_menu)
                    if button_rect.collidepoint(mouse_pos):
                        estado_juego = SELECCION_ARMA
                
                elif estado_juego == SELECCION_ARMA:
                    for boton, arma in pantalla_seleccion_arma(pantalla, mouse_pos):
                        if boton.collidepoint(mouse_pos):
                            jugador = Jugador(ANCHO//2, ALTO//2, arma)
                            enemigos = []
                            efectos = []
                            oleada_actual = 1
                            enemigos_restantes_spawn = enemigos_por_oleada[0]
                            estado_juego = JUGANDO
                            
                elif estado_juego == VICTORIA or estado_juego == GAME_OVER:
                    btn = pantalla_fin_juego(pantalla, estado_juego, oleada_alcanzada, mouse_pos, fondo_menu)
                    if btn.collidepoint(mouse_pos):
                        estado_juego = MENU

        if estado_juego == MENU:
            pantalla_menu(pantalla, mouse_pos, fondo_menu)
            
        elif estado_juego == SELECCION_ARMA:
            pantalla_seleccion_arma(pantalla, mouse_pos)
            
        elif estado_juego == JUGANDO:
            # Spawner progresivo para no saturar de golpe
            if enemigos_restantes_spawn > 0:
                timer_spawn += 1
                if timer_spawn > 30: # Spawn cada medio segundo aprox
                    cantidad = min(random.randint(1, 3), enemigos_restantes_spawn)
                    nuevos = generar_enemigos(cantidad, oleada_actual, ANCHO, ALTO)
                    enemigos.extend(nuevos)
                    enemigos_restantes_spawn -= cantidad
                    timer_spawn = 0
            
            if jugador:
                teclas = pygame.key.get_pressed()
                jugador.mover(teclas, ANCHO, ALTO)
                jugador.atacar_automatico(tiempo_actual, enemigos, efectos)
            
            # Actualizar efectos y colisones
            for efecto in efectos[:]:
                if hasattr(efecto, 'actualizar'): efecto.actualizar()
                
                quitar = False
                if hasattr(efecto, 'fuera_de_pantalla') and efecto.fuera_de_pantalla(ANCHO, ALTO):
                    quitar = True
                elif not efecto.activo:
                    quitar = True
                elif hasattr(efecto, 'verificar_colision'):
                    if efecto.verificar_colision(enemigos):
                         if efecto.tipo == "proyectil": quitar = True
                
                if quitar:
                    efectos.remove(efecto)

            # Enemigos
            for enemigo in enemigos[:]:
                if enemigo.esta_vivo():
                    if jugador:
                        enemigo.mover_hacia_jugador(jugador)
                        enemigo.atacar_jugador(jugador, tiempo_actual)
                else:
                    enemigos.remove(enemigo)
            
            # Control oleadas
            if len(enemigos) == 0 and enemigos_restantes_spawn == 0:
                oleada_actual += 1
                if oleada_actual > 5:
                    oleada_alcanzada = 5
                    estado_juego = VICTORIA
                else:
                    enemigos_restantes_spawn = enemigos_por_oleada[oleada_actual - 1]
                    # Aumentar dificultad arma
                    if jugador:
                        jugador.velocidad_ataque = max(0.2, jugador.velocidad_ataque - 0.15)
                        # Restaurar al héroe antes de la siguiente oleada
                        jugador.vida = jugador.vida_maxima

            if jugador and jugador.vida <= 0:
                oleada_alcanzada = oleada_actual
                estado_juego = GAME_OVER
            
            # Solo dibujamos el juego si seguimos jugando, si cambiamos a game over, se dibujará en el siguiente frame en el bloque correcto
            if estado_juego == JUGANDO and jugador:
                pantalla_juego(pantalla, jugador, enemigos, efectos, oleada_actual, enemigos_restantes_spawn + len(enemigos), fondo_juego)
        
        elif estado_juego == VICTORIA or estado_juego == GAME_OVER:
            pantalla_fin_juego(pantalla, estado_juego, oleada_alcanzada, mouse_pos, fondo_menu)
            
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
