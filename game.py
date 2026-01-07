import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Constantes de pantalla
ANCHO = 1024
ALTO = 720
FPS = 60

# Colores avanzados
NEGRO = (15, 15, 15)
BLANCO = (240, 240, 240)
ROJO_SANGRE = (180, 20, 20)
VERDE_CÉSPED = (34, 139, 34)
AZUL_MAGICO = (65, 105, 225)
GRIS_PIEDRA = (112, 128, 144)
GRIS_ACERO = (192, 192, 192)
DORADO = (218, 165, 32)
MARRON_MADERA = (139, 69, 19)
VIOLETA_OSCURO = (75, 0, 130)
NARANJA_FUEGO = (255, 69, 0)

# Estados del juego
MENU = "menu"
SELECCION_ARMA = "seleccion_arma"
JUGANDO = "jugando"
VICTORIA = "victoria"
GAME_OVER = "game_over"

# Configuración de armas
ARMAS = {
    "vara": {
        "nombre": "Vara Arcana",
        "velocidad_ataque": 0.8,
        "daño": 30,
        "rango": 800, # Todo el mapa prácticamente
        "color": AZUL_MAGICO,
        "descripcion": "Dispara proyectiles mágicos a distancia."
    },
    "espada": {
        "nombre": "Espada Real",
        "velocidad_ataque": 1.0,
        "daño": 50,
        "rango": 120, # Alcance del tajo
        "color": GRIS_ACERO,
        "descripcion": "Tajo frontal que daña a enemigos en arco."
    },
    "mazo": {
        "nombre": "Martillo de Guerra",
        "velocidad_ataque": 1.2,
        "daño": 70,
        "rango": 150, # Radio del impacto
        "color": MARRON_MADERA,
        "descripcion": "Golpe sísmico en área alrededor."
    }
}

class Jugador:
    def __init__(self, x, y, arma_tipo):
        self.x = x
        self.y = y
        self.radio = 20
        self.velocidad = 5
        self.vida_maxima = 120
        self.vida = self.vida_maxima
        self.arma = arma_tipo
        self.velocidad_ataque = ARMAS[arma_tipo]["velocidad_ataque"]
        self.daño = ARMAS[arma_tipo]["daño"]
        self.rango = ARMAS[arma_tipo]["rango"]
        self.tiempo_ultimo_ataque = 0
        self.direccion_mirada = 0 # Grados
        self.color = BLANCO
        
        # Ajustes visuales según clase
        if arma_tipo == "vara":
            self.color_cuerpo = VIOLETA_OSCURO
        elif arma_tipo == "espada":
            self.color_cuerpo = GRIS_ACERO
        else: # mazo
            self.color_cuerpo = MARRON_MADERA

    def mover(self, teclas, ancho_pantalla, alto_pantalla):
        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = self.velocidad
            
        # Normalizar movimiento diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
            
        self.x += dx
        self.y += dy
        
        # Mantener dentro de los límites
        self.x = max(self.radio, min(self.x, ancho_pantalla - self.radio))
        self.y = max(self.radio, min(self.y, alto_pantalla - self.radio))
        
        # Actualizar dirección si se mueve
        if dx != 0 or dy != 0:
            self.direccion_mirada = math.atan2(dy, dx)
    
    def atacar_automatico(self, tiempo_actual, enemigos, efectos):
        if tiempo_actual - self.tiempo_ultimo_ataque >= self.velocidad_ataque * 1000:
            atacó = False
            
            if self.arma == "vara":
                # Ataque a distancia: Busca enemigo más cercano y dispara
                if enemigos:
                    enemigo_cercano = min(enemigos, key=lambda e: 
                        math.sqrt((e.x - self.x)**2 + (e.y - self.y)**2))
                    
                    proyectil = Proyectil(self.x, self.y, enemigo_cercano.x, enemigo_cercano.y, self.daño, ARMAS[self.arma]["color"])
                    efectos.append(proyectil)
                    atacó = True

            elif self.arma == "espada":
                # Ataque Melee: Busca enemigo más cercano en rango para orientar el tajo
                enemigos_en_rango = [e for e in enemigos if math.sqrt((e.x - self.x)**2 + (e.y - self.y)**2) <= self.rango + 50]
                
                target_angle = self.direccion_mirada
                if enemigos_en_rango:
                    enemigo_cercano = min(enemigos_en_rango, key=lambda e: math.sqrt((e.x - self.x)**2 + (e.y - self.y)**2))
                    target_angle = math.atan2(enemigo_cercano.y - self.y, enemigo_cercano.x - self.x)
                    atacó = True # Ataca si hay enemigos cerca
                else:
                    # Si no hay enemigos cerca, no ataca o ataca al aire? 
                    # Digamos que ataca en la dirección de movimiento para efecto visual
                    atacó = True 

                if atacó:
                    # Crear efecto de tajo
                    tajo = EfectoTajo(self.x, self.y, target_angle, self.rango, self.daño)
                    efectos.append(tajo)
                    # Aplicar daño instantáneo a los que toque el tajo
                    for enemigo in enemigos:
                        if enemigo.esta_vivo():
                            dist = math.sqrt((enemigo.x - self.x)**2 + (enemigo.y - self.y)**2)
                            if dist <= self.rango:
                                # Comprobar ángulo
                                ang_enemigo = math.atan2(enemigo.y - self.y, enemigo.x - self.x)
                                diff = (ang_enemigo - target_angle + math.pi) % (2*math.pi) - math.pi
                                if abs(diff) < 1.0: # Un cono de ataque de aprox 110 grados
                                    enemigo.recibir_daño(self.daño)
                                    # Empuje leve con espada
                                    enemigo.x += math.cos(target_angle) * 10
                                    enemigo.y += math.sin(target_angle) * 10

            elif self.arma == "mazo":
                # Ataque Área: Golpe al suelo si hay enemigos cerca
                enemigos_en_rango = [e for e in enemigos if math.sqrt((e.x - self.x)**2 + (e.y - self.y)**2) <= self.rango]
                if enemigos_en_rango:
                    golpe = EfectoGolpeSuelo(self.x, self.y, self.rango)
                    efectos.append(golpe)
                    for enemigo in enemigos_en_rango:
                        enemigo.recibir_daño(self.daño)
                        # Gran empuje
                        angulo_empuje = math.atan2(enemigo.y - self.y, enemigo.x - self.x)
                        enemigo.x += math.cos(angulo_empuje) * 40
                        enemigo.y += math.sin(angulo_empuje) * 40
                    atacó = True

            if atacó:
                self.tiempo_ultimo_ataque = tiempo_actual
    
    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0
    
    def dibujar(self, pantalla):
        def ajustar_color(color, delta):
            return tuple(max(0, min(255, c + delta)) for c in color)

        scale = 0.8

        def w(valor):
            return max(1, int(valor * scale))

        sombra_ancho = int(80 * scale)
        sombra_alto = int(26 * scale)
        sombra = pygame.Surface((sombra_ancho, sombra_alto), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 120), (0, 0, sombra_ancho, sombra_alto))
        pantalla.blit(sombra, (self.x - sombra_ancho // 2, self.y + int(28 * scale)))

        sprite = pygame.Surface((100, 120), pygame.SRCALPHA)
        cx = sprite.get_width() // 2
        torso_color = self.color_cuerpo
        piel = (236, 204, 165)

        if self.arma == "vara":
            capa_color = ajustar_color(torso_color, -40)
            pygame.draw.polygon(sprite, capa_color, [(cx, 28), (cx - 42, 110), (cx + 42, 110)])
            pygame.draw.polygon(sprite, ajustar_color(capa_color, -30), [(cx, 36), (cx - 30, 106), (cx + 30, 106)], 3)

        pygame.draw.ellipse(sprite, torso_color, (cx - 24, 56, 48, 54))
        pygame.draw.ellipse(sprite, ajustar_color(torso_color, -25), (cx - 26, 76, 52, 26))
        pygame.draw.ellipse(sprite, ajustar_color(torso_color, 35), (cx - 22, 56, 44, 24))

        hombros_color = ajustar_color(torso_color, -30)
        pygame.draw.circle(sprite, hombros_color, (cx - 26, 74), 12)
        pygame.draw.circle(sprite, hombros_color, (cx + 26, 74), 12)
        pygame.draw.circle(sprite, ajustar_color(hombros_color, 35), (cx - 26, 72), 7)
        pygame.draw.circle(sprite, ajustar_color(hombros_color, 35), (cx + 26, 72), 7)

        brazo_color = ajustar_color(torso_color, -15)
        pygame.draw.rect(sprite, brazo_color, (cx - 38, 80, 16, 32), border_radius=6)
        pygame.draw.rect(sprite, brazo_color, (cx + 22, 80, 14, 30), border_radius=6)
        pygame.draw.circle(sprite, piel, (cx - 30, 110), 6)

        pygame.draw.rect(sprite, (75, 45, 25), (cx - 24, 88, 48, 8), border_radius=4)
        pygame.draw.rect(sprite, (160, 120, 60), (cx - 6, 88, 12, 8), border_radius=4)

        pygame.draw.rect(sprite, ajustar_color(torso_color, -45), (cx - 20, 98, 18, 24), border_radius=6)
        pygame.draw.rect(sprite, ajustar_color(torso_color, -55), (cx + 2, 98, 18, 24), border_radius=6)
        pygame.draw.rect(sprite, (58, 40, 28), (cx - 22, 118, 22, 10), border_radius=5)
        pygame.draw.rect(sprite, (58, 40, 28), (cx, 118, 22, 10), border_radius=5)

        pygame.draw.circle(sprite, piel, (cx, 44), 14)
        pygame.draw.circle(sprite, (240, 230, 220), (cx - 5, 42), 4)
        pygame.draw.circle(sprite, (240, 230, 220), (cx + 5, 42), 4)
        pygame.draw.circle(sprite, (40, 40, 40), (cx - 5, 42), 2)
        pygame.draw.circle(sprite, (40, 40, 40), (cx + 5, 42), 2)
        pygame.draw.polygon(sprite, (200, 170, 140), [(cx, 50), (cx - 3, 56), (cx + 3, 56)])
        pygame.draw.arc(sprite, ajustar_color(piel, -40), (cx - 6, 56, 12, 8), math.pi, math.pi * 1.8, 2)
        pygame.draw.line(sprite, ajustar_color(piel, -60), (cx - 8, 36), (cx - 2, 38), 2)
        pygame.draw.line(sprite, ajustar_color(piel, -60), (cx + 2, 38), (cx + 8, 36), 2)

        if self.arma == "espada":
            metal = (170, 170, 190)
            pygame.draw.rect(sprite, metal, (cx - 20, 60, 40, 40), border_radius=10)
            pygame.draw.polygon(sprite, ajustar_color(metal, -30), [(cx - 18, 90), (cx + 18, 90), (cx, 106)])
            pygame.draw.rect(sprite, (120, 95, 55), (cx - 6, 88, 12, 26), border_radius=4)
            casco = (150, 150, 170)
            pygame.draw.rect(sprite, casco, (cx - 18, 30, 36, 18), border_radius=12)
            pygame.draw.rect(sprite, ajustar_color(casco, -30), (cx - 18, 38, 36, 12), border_radius=8)
            pygame.draw.rect(sprite, (40, 40, 70), (cx - 12, 40, 24, 8), border_radius=4)
            pygame.draw.circle(sprite, ajustar_color(casco, 30), (cx - 20, 40), 4)
            pygame.draw.circle(sprite, ajustar_color(casco, 30), (cx + 20, 40), 4)
            pygame.draw.arc(sprite, ajustar_color(metal, 20), (cx - 36, 64, 24, 20), math.pi * 1.1, math.pi * 1.9, 3)
            pygame.draw.arc(sprite, ajustar_color(metal, 20), (cx + 12, 64, 24, 20), math.pi * 1.2, math.pi * 2.0, 3)
        elif self.arma == "mazo":
            metal = (130, 105, 85)
            pygame.draw.rect(sprite, metal, (cx - 24, 60, 48, 46), border_radius=12)
            pygame.draw.rect(sprite, ajustar_color(metal, -30), (cx - 24, 74, 48, 16), border_radius=10)
            pygame.draw.rect(sprite, (90, 70, 50), (cx - 30, 88, 60, 12), border_radius=6)
            pygame.draw.circle(sprite, ajustar_color(metal, 25), (cx - 28, 72), 12)
            pygame.draw.circle(sprite, ajustar_color(metal, 25), (cx + 28, 72), 12)
            pygame.draw.circle(sprite, ajustar_color(metal, -10), (cx - 28, 70), 7)
            pygame.draw.circle(sprite, ajustar_color(metal, -10), (cx + 28, 70), 7)
            casco = (110, 95, 80)
            pygame.draw.rect(sprite, casco, (cx - 18, 30, 36, 22), border_radius=10)
            pygame.draw.rect(sprite, ajustar_color(casco, -25), (cx - 18, 40, 36, 12), border_radius=6)
            pygame.draw.rect(sprite, (50, 45, 40), (cx - 12, 42, 24, 6), border_radius=3)
        else:
            capucha = ajustar_color(torso_color, -25)
            pygame.draw.circle(sprite, capucha, (cx, 42), 20, width=6)
            pygame.draw.circle(sprite, ajustar_color(capucha, -30), (cx, 42), 20, 2)
            pygame.draw.polygon(sprite, ajustar_color(capucha, -15), [(cx - 18, 60), (cx + 18, 60), (cx, 92)])
            pygame.draw.polygon(sprite, ajustar_color(capucha, -35), [(cx - 14, 62), (cx + 14, 62), (cx, 88)], 3)
            pygame.draw.circle(sprite, (190, 150, 220), (cx, 96), 6)
            pygame.draw.circle(sprite, (120, 90, 200), (cx, 96), 3)

        sprite_escalado = pygame.transform.smoothscale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
        sprite_rect = sprite_escalado.get_rect(center=(self.x, self.y + int(6 * scale)))
        pantalla.blit(sprite_escalado, sprite_rect)

        offset_arma_x = math.cos(self.direccion_mirada) * (26 * scale)
        offset_arma_y = math.sin(self.direccion_mirada) * (26 * scale)
        mano_x = self.x + offset_arma_x
        mano_y = self.y + offset_arma_y + (12 * scale)

        color_arma = ARMAS[self.arma]["color"]
        if self.arma == "vara":
            base_x = self.x - math.cos(self.direccion_mirada) * (10 * scale)
            base_y = self.y - math.sin(self.direccion_mirada) * (10 * scale) + (12 * scale)
            punta_x = mano_x + math.cos(self.direccion_mirada) * (40 * scale)
            punta_y = mano_y + math.sin(self.direccion_mirada) * (40 * scale)
            pygame.draw.line(pantalla, (95, 70, 40), (base_x, base_y), (punta_x, punta_y), w(6))
            pygame.draw.line(pantalla, (60, 45, 30), (base_x, base_y), (punta_x, punta_y), w(2))
            gema_tamaño = max(12, int(26 * scale))
            gema = pygame.Surface((gema_tamaño, gema_tamaño), pygame.SRCALPHA)
            pygame.draw.circle(gema, (*color_arma, 160), (gema.get_width() // 2, gema.get_height() // 2), gema.get_width() // 2 - 1)
            pygame.draw.circle(gema, (255, 255, 255, 180), (gema.get_width() // 2, int(gema.get_height() * 0.35)), max(2, gema.get_width() // 5))
            pantalla.blit(gema, (int(punta_x - gema.get_width() // 2), int(punta_y - gema.get_height() // 2)))
            aura_tamaño = max(30, int(40 * scale))
            aura_radio = max(12, int(18 * scale))
            aura = pygame.Surface((aura_tamaño, aura_tamaño), pygame.SRCALPHA)
            pygame.draw.circle(aura, (*color_arma, 70), (aura_tamaño // 2, aura_tamaño // 2), aura_radio, w(3))
            pantalla.blit(aura, (int(punta_x - aura_tamaño // 2), int(punta_y - aura_tamaño // 2)))
        elif self.arma == "espada":
            hoja_largo = 52 * scale
            hoja_x = mano_x + math.cos(self.direccion_mirada) * hoja_largo
            hoja_y = mano_y + math.sin(self.direccion_mirada) * hoja_largo
            base_mano_x = mano_x - math.cos(self.direccion_mirada) * (12 * scale)
            base_mano_y = mano_y - math.sin(self.direccion_mirada) * (12 * scale)
            pygame.draw.line(pantalla, (220, 220, 230), (mano_x, mano_y), (hoja_x, hoja_y), w(6))
            pygame.draw.line(pantalla, (140, 140, 160), (mano_x, mano_y), (hoja_x, hoja_y), w(2))
            punta_x = hoja_x + math.cos(self.direccion_mirada) * (8 * scale)
            punta_y = hoja_y + math.sin(self.direccion_mirada) * (8 * scale)
            pygame.draw.polygon(pantalla, (220, 220, 230), [(hoja_x, hoja_y), (punta_x, punta_y), (hoja_x + math.cos(self.direccion_mirada + 0.35) * (6 * scale), hoja_y + math.sin(self.direccion_mirada + 0.35) * (6 * scale))])
            pygame.draw.polygon(pantalla, (220, 220, 230), [(hoja_x, hoja_y), (punta_x, punta_y), (hoja_x + math.cos(self.direccion_mirada - 0.35) * (6 * scale), hoja_y + math.sin(self.direccion_mirada - 0.35) * (6 * scale))])
            perp_x = math.cos(self.direccion_mirada + math.pi / 2)
            perp_y = math.sin(self.direccion_mirada + math.pi / 2)
            pygame.draw.line(pantalla, (210, 180, 60), (mano_x + perp_x * (14 * scale), mano_y + perp_y * (14 * scale)), (mano_x - perp_x * (14 * scale), mano_y - perp_y * (14 * scale)), w(6))
            pygame.draw.line(pantalla, (150, 110, 45), (mano_x + perp_x * (10 * scale), mano_y + perp_y * (10 * scale)), (mano_x - perp_x * (10 * scale), mano_y - perp_y * (10 * scale)), w(2))
            pygame.draw.line(pantalla, (70, 50, 30), (base_mano_x, base_mano_y), (mano_x, mano_y), w(6))
            pygame.draw.line(pantalla, (45, 30, 18), (base_mano_x, base_mano_y), (mano_x, mano_y), w(2))
            pomo_x = base_mano_x - math.cos(self.direccion_mirada) * (6 * scale)
            pomo_y = base_mano_y - math.sin(self.direccion_mirada) * (6 * scale)
            pygame.draw.circle(pantalla, (210, 180, 60), (int(pomo_x), int(pomo_y)), max(2, int(4 * scale)))
        else:
            mango_largo = 36 * scale
            mango_x = mano_x + math.cos(self.direccion_mirada) * mango_largo
            mango_y = mano_y + math.sin(self.direccion_mirada) * mango_largo
            pygame.draw.line(pantalla, (110, 80, 45), (mano_x, mano_y), (mango_x, mango_y), w(7))
            pygame.draw.line(pantalla, (60, 45, 25), (mano_x, mano_y), (mango_x, mango_y), w(3))
            cabeza_radio = int(14 * scale)
            cabeza_x = mango_x + math.cos(self.direccion_mirada) * (cabeza_radio + 4 * scale)
            cabeza_y = mango_y + math.sin(self.direccion_mirada) * (cabeza_radio + 4 * scale)
            pygame.draw.circle(pantalla, color_arma, (int(cabeza_x), int(cabeza_y)), max(6, cabeza_radio))
            for ang in (0, math.pi / 2, math.pi, math.pi * 1.5):
                spike_dir = self.direccion_mirada + ang
                punta_x = cabeza_x + math.cos(spike_dir) * (cabeza_radio + 6 * scale)
                punta_y = cabeza_y + math.sin(spike_dir) * (cabeza_radio + 6 * scale)
                pygame.draw.line(pantalla, ajustar_color(color_arma, 30), (cabeza_x, cabeza_y), (punta_x, punta_y), w(3))

        mano_radio = max(3, int(6 * scale))
        pygame.draw.circle(pantalla, piel, (int(mano_x), int(mano_y)), mano_radio)
        pygame.draw.circle(pantalla, ajustar_color(piel, -40), (int(mano_x), int(mano_y)), mano_radio, 1)

        # Barra de vida
        barra_ancho = 50
        barra_alto = 6
        barra_x = self.x - barra_ancho // 2
        barra_y = self.y - self.radio - int(24 * scale)
        
        pygame.draw.rect(pantalla, ROJO_SANGRE, (barra_x, barra_y, barra_ancho, barra_alto))
        vida_ancho = int((self.vida / self.vida_maxima) * barra_ancho)
        pygame.draw.rect(pantalla, VERDE_CÉSPED, (barra_x, barra_y, vida_ancho, barra_alto))

class Enemigo:
    def __init__(self, x, y, oleada, tipo="normal"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.tiempo_ultimo_ataque = 0
        self.cooldown_ataque = 1000
        
        # Configuración según tipo
        base_hp = 40 + (oleada * 10)
        base_dmg = 5 + (oleada * 2)
        
        if tipo == "rapido":
            self.radio = 12
            self.velocidad = 2.5 + (oleada * 0.2)
            self.vida_maxima = base_hp * 0.6
            self.daño = base_dmg * 0.8
            self.color_base = (200, 200, 50) # Amarillo sucio
            self.puntos_forma = 3 # Triángulo
        elif tipo == "pesado":
            self.radio = 22
            self.velocidad = 1.0 + (oleada * 0.1)
            self.vida_maxima = base_hp * 2.0
            self.daño = base_dmg * 1.5
            self.color_base = (50, 50, 50) # Gris oscuro
            self.puntos_forma = 4 # Cuadrado
        else: # normal
            self.radio = 16
            self.velocidad = 1.8 + (oleada * 0.15)
            self.vida_maxima = base_hp
            self.daño = base_dmg
            self.color_base = (150, 0, 0) # Rojo oscuro
            self.puntos_forma = 5 # Pentágono

        self.vida = self.vida_maxima

    def mover_hacia_jugador(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        
        if distancia > 0:
            dx /= distancia
            dy /= distancia
            
            # Simple evitación de superposición entre enemigos sería costoso, 
            # así que lo dejamos simple por ahora
            self.x += dx * self.velocidad
            self.y += dy * self.velocidad
    
    def atacar_jugador(self, jugador, tiempo_actual):
        distancia = math.sqrt((self.x - jugador.x)**2 + (self.y - jugador.y)**2)
        # Colisión circulo-circulo
        if distancia < self.radio + jugador.radio:
            if tiempo_actual - self.tiempo_ultimo_ataque >= self.cooldown_ataque:
                jugador.recibir_daño(self.daño)
                self.tiempo_ultimo_ataque = tiempo_actual
    
    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        
    def esta_vivo(self):
        return self.vida > 0
    
    def dibujar(self, pantalla):
        def ajustar_color(color, delta):
            return tuple(max(0, min(255, c + delta)) for c in color)

        sombra_ancho = max(24, int(self.radio * 3.2))
        sombra_alto = max(12, int(self.radio * 1.2))
        sombra = pygame.Surface((sombra_ancho, sombra_alto), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 110), (0, 0, sombra_ancho, sombra_alto))
        pantalla.blit(sombra, (int(self.x - sombra_ancho / 2), int(self.y + self.radio - sombra_alto / 2)))

        sprite_dim = int(self.radio * 4 + 36)
        sprite = pygame.Surface((sprite_dim, sprite_dim), pygame.SRCALPHA)
        cx = sprite.get_width() // 2
        cy = sprite.get_height() // 2

        if self.tipo == "rapido":
            pelaje = (120, 120, 130)
            sombra_pelaje = ajustar_color(pelaje, -40)
            brillo_pelaje = ajustar_color(pelaje, 25)

            cuerpo_rect = pygame.Rect(int(cx - self.radio * 1.7), int(cy - self.radio * 0.6), int(self.radio * 3.4), int(self.radio * 1.6))
            pygame.draw.ellipse(sprite, pelaje, cuerpo_rect)
            pygame.draw.ellipse(sprite, brillo_pelaje, cuerpo_rect.inflate(-int(self.radio * 0.9), -int(self.radio * 0.6)))
            pygame.draw.polygon(sprite, sombra_pelaje, [
                (int(cx + self.radio * 1.6), int(cy)),
                (int(cx + self.radio * 2.0), int(cy - self.radio * 0.7)),
                (int(cx + self.radio * 1.6), int(cy + self.radio * 0.5))
            ])

            cabeza_rect = pygame.Rect(int(cx - self.radio * 2.0), int(cy - self.radio * 1.2), int(self.radio * 1.6), int(self.radio * 1.2))
            pygame.draw.ellipse(sprite, pelaje, cabeza_rect)
            pygame.draw.ellipse(sprite, sombra_pelaje, cabeza_rect.inflate(int(self.radio * -0.2), int(self.radio * -0.4)))
            pygame.draw.polygon(sprite, sombra_pelaje, [
                (int(cabeza_rect.left + self.radio * 0.3), cabeza_rect.top),
                (int(cabeza_rect.left - self.radio * 0.5), int(cabeza_rect.top - self.radio * 0.6)),
                (int(cabeza_rect.left + self.radio * 0.4), int(cabeza_rect.top - self.radio * 0.2))
            ])
            pygame.draw.polygon(sprite, sombra_pelaje, [
                (int(cabeza_rect.right - self.radio * 0.3), cabeza_rect.top),
                (int(cabeza_rect.right + self.radio * 0.5), int(cabeza_rect.top - self.radio * 0.6)),
                (int(cabeza_rect.right - self.radio * 0.4), int(cabeza_rect.top - self.radio * 0.2))
            ])
            hocico_rect = pygame.Rect(int(cabeza_rect.centerx - self.radio * 0.3), int(cabeza_rect.centery), int(self.radio * 0.9), int(self.radio * 0.5))
            pygame.draw.ellipse(sprite, ajustar_color(pelaje, -20), hocico_rect)
            ojo_radio = max(1, int(self.radio * 0.25))
            pygame.draw.circle(sprite, (220, 60, 60), (int(cabeza_rect.centerx - self.radio * 0.4), int(cabeza_rect.centery - self.radio * 0.2)), ojo_radio)
            pygame.draw.circle(sprite, (220, 60, 60), (int(cabeza_rect.centerx + self.radio * 0.4), int(cabeza_rect.centery - self.radio * 0.2)), ojo_radio)
            pygame.draw.circle(sprite, (30, 30, 30), (int(cabeza_rect.centerx + self.radio * 0.2), int(cabeza_rect.centery + self.radio * 0.2)), max(1, int(self.radio * 0.2)))

            for offset in (-self.radio * 0.9, -self.radio * 0.3, self.radio * 0.25, self.radio * 0.8):
                pata_rect = pygame.Rect(int(cx + offset), int(cy + self.radio * 0.4), int(self.radio * 0.5), int(self.radio * 1.2))
                pygame.draw.rect(sprite, sombra_pelaje, pata_rect, border_radius=6)
                pata_superior = pata_rect.copy()
                pata_superior.height = int(self.radio * 0.7)
                pygame.draw.rect(sprite, brillo_pelaje, pata_superior, border_radius=6)
                pygame.draw.rect(sprite, (30, 30, 30), (pata_rect.left, pata_rect.bottom - int(self.radio * 0.3), pata_rect.width, int(self.radio * 0.3)), border_radius=4)

        elif self.tipo == "pesado":
            roca = (92, 98, 92)
            sombra_roca = ajustar_color(roca, -35)
            brillo_roca = ajustar_color(roca, 25)

            torso_rect = pygame.Rect(int(cx - self.radio * 1.3), int(cy - self.radio * 0.5), int(self.radio * 2.6), int(self.radio * 1.9))
            pygame.draw.rect(sprite, roca, torso_rect, border_radius=12)
            pygame.draw.rect(sprite, sombra_roca, torso_rect, width=2, border_radius=12)

            superior_rect = pygame.Rect(int(cx - self.radio * 1.1), int(cy - self.radio * 1.3), int(self.radio * 2.2), int(self.radio))
            pygame.draw.rect(sprite, roca, superior_rect, border_radius=10)
            pygame.draw.rect(sprite, brillo_roca, superior_rect.inflate(-int(self.radio * 0.4), -int(self.radio * 0.3)), border_radius=8)

            cabeza_rect = pygame.Rect(int(cx - self.radio * 0.9), int(cy - self.radio * 1.6), int(self.radio * 1.8), int(self.radio * 0.8))
            pygame.draw.rect(sprite, roca, cabeza_rect, border_radius=6)
            pygame.draw.rect(sprite, sombra_roca, cabeza_rect, width=2, border_radius=6)
            visor_rect = pygame.Rect(int(cabeza_rect.left + self.radio * 0.2), int(cabeza_rect.top + self.radio * 0.25), int(self.radio * 1.4), int(self.radio * 0.25))
            pygame.draw.rect(sprite, (70, 180, 200), visor_rect, border_radius=4)
            pygame.draw.rect(sprite, (30, 60, 80), visor_rect, 2, border_radius=4)

            for offset in (-self.radio * 1.3, self.radio * 0.5):
                brazo_rect = pygame.Rect(int(cx + offset), int(cy - self.radio * 0.3), int(self.radio * 0.8), int(self.radio * 1.8))
                pygame.draw.rect(sprite, roca, brazo_rect, border_radius=10)
                pygame.draw.rect(sprite, sombra_roca, brazo_rect, width=2, border_radius=10)
                pygame.draw.rect(sprite, sombra_roca, (brazo_rect.left, brazo_rect.bottom - int(self.radio * 0.4), brazo_rect.width, int(self.radio * 0.4)), border_radius=8)

            pygame.draw.circle(sprite, (90, 140, 200), (cx, int(cy + self.radio * 0.2)), int(self.radio * 0.5))
            pygame.draw.circle(sprite, (140, 200, 240), (cx, int(cy + self.radio * 0.2)), max(2, int(self.radio * 0.25)), 2)
            pygame.draw.line(sprite, sombra_roca, (int(cx - self.radio * 0.6), int(cy + self.radio * 0.2)), (int(cx - self.radio * 0.2), int(cy + self.radio * 0.9)), 3)
            pygame.draw.line(sprite, sombra_roca, (int(cx + self.radio * 0.6), int(cy + self.radio * 0.2)), (int(cx + self.radio * 0.2), int(cy + self.radio * 0.9)), 3)

        else:
            piel = (90, 180, 90)
            sombra_piel = ajustar_color(piel, -45)
            brillo_piel = ajustar_color(piel, 35)

            torso_rect = pygame.Rect(int(cx - self.radio * 1.1), int(cy - self.radio * 0.4), int(self.radio * 2.2), int(self.radio * 1.6))
            pygame.draw.ellipse(sprite, piel, torso_rect)
            pygame.draw.ellipse(sprite, brillo_piel, torso_rect.inflate(-int(self.radio * 0.5), -int(self.radio * 0.6)))

            cabeza_rect = pygame.Rect(int(cx - self.radio * 0.9), int(cy - self.radio * 1.5), int(self.radio * 1.8), int(self.radio * 1.2))
            pygame.draw.ellipse(sprite, piel, cabeza_rect)
            pygame.draw.polygon(sprite, sombra_piel, [
                (int(cabeza_rect.left - self.radio * 0.4), int(cabeza_rect.centery - self.radio * 0.2)),
                (int(cabeza_rect.left), int(cabeza_rect.centery - self.radio * 0.5)),
                (int(cabeza_rect.left + self.radio * 0.3), int(cabeza_rect.centery - self.radio * 0.1))
            ])
            pygame.draw.polygon(sprite, sombra_piel, [
                (int(cabeza_rect.right + self.radio * 0.4), int(cabeza_rect.centery - self.radio * 0.2)),
                (int(cabeza_rect.right), int(cabeza_rect.centery - self.radio * 0.5)),
                (int(cabeza_rect.right - self.radio * 0.3), int(cabeza_rect.centery - self.radio * 0.1))
            ])

            ojo_radio = max(1, int(self.radio * 0.28))
            pygame.draw.circle(sprite, (255, 255, 140), (int(cabeza_rect.centerx - self.radio * 0.4), int(cabeza_rect.centery - self.radio * 0.1)), ojo_radio)
            pygame.draw.circle(sprite, (255, 255, 140), (int(cabeza_rect.centerx + self.radio * 0.4), int(cabeza_rect.centery - self.radio * 0.1)), ojo_radio)
            pupila_radio = max(1, int(self.radio * 0.15))
            pygame.draw.circle(sprite, (40, 40, 40), (int(cabeza_rect.centerx - self.radio * 0.38), int(cabeza_rect.centery - self.radio * 0.1)), pupila_radio)
            pygame.draw.circle(sprite, (40, 40, 40), (int(cabeza_rect.centerx + self.radio * 0.38), int(cabeza_rect.centery - self.radio * 0.1)), pupila_radio)
            pygame.draw.polygon(sprite, ajustar_color(piel, -25), [
                (int(cabeza_rect.centerx), int(cabeza_rect.centery)),
                (int(cabeza_rect.centerx - self.radio * 0.15), int(cabeza_rect.centery + self.radio * 0.4)),
                (int(cabeza_rect.centerx + self.radio * 0.15), int(cabeza_rect.centery + self.radio * 0.4))
            ])
            pygame.draw.rect(sprite, (240, 240, 240), (int(cabeza_rect.centerx - self.radio * 0.4), int(cabeza_rect.bottom - self.radio * 0.3), int(self.radio * 0.8), int(self.radio * 0.25)), border_radius=3)
            pygame.draw.line(sprite, (150, 150, 150), (int(cabeza_rect.centerx), int(cabeza_rect.bottom - self.radio * 0.3)), (int(cabeza_rect.centerx), int(cabeza_rect.bottom - self.radio * 0.05)), 1)

            peto = (80, 60, 40)
            pygame.draw.rect(sprite, peto, (int(cx - self.radio), int(cy + self.radio * 0.3), int(self.radio * 2), int(self.radio * 0.6)), border_radius=6)
            pygame.draw.rect(sprite, ajustar_color(peto, -15), (int(cx - self.radio * 0.7), int(cy + self.radio * 0.3), int(self.radio * 1.4), int(self.radio * 0.6)), border_radius=6)
            pygame.draw.rect(sprite, (120, 80, 40), (int(cx - self.radio * 0.2), int(cy + self.radio * 0.3), int(self.radio * 0.4), int(self.radio * 0.9)), border_radius=4)

            for offset in (-self.radio * 1.1, self.radio * 0.9):
                brazo_rect = pygame.Rect(int(cx + offset), int(cy - self.radio * 0.2), int(self.radio * 0.5), int(self.radio * 1.4))
                pygame.draw.rect(sprite, piel, brazo_rect, border_radius=6)
                pygame.draw.rect(sprite, sombra_piel, (brazo_rect.left, brazo_rect.bottom - int(self.radio * 0.4), brazo_rect.width, int(self.radio * 0.4)), border_radius=6)

            daga_inicio = (int(cx + self.radio * 1.1), int(cy + self.radio * 0.3))
            daga_fin = (int(daga_inicio[0] + self.radio * 0.9), int(daga_inicio[1] - self.radio * 0.8))
            pygame.draw.line(sprite, (200, 200, 200), daga_inicio, daga_fin, max(1, int(self.radio * 0.3)))
            pygame.draw.polygon(sprite, (220, 220, 220), [
                daga_fin,
                (daga_fin[0] + int(self.radio * 0.2), daga_fin[1] - int(self.radio * 0.2)),
                (daga_fin[0] - int(self.radio * 0.2), daga_fin[1] - int(self.radio * 0.2))
            ])
            pygame.draw.line(sprite, (150, 110, 45), (daga_inicio[0] - int(self.radio * 0.25), daga_inicio[1]), (daga_inicio[0] + int(self.radio * 0.25), daga_inicio[1]), max(1, int(self.radio * 0.3)))

        sprite_rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        pantalla.blit(sprite, sprite_rect)

        if self.vida < self.vida_maxima:
            barra_ancho = max(32, int(self.radio * 2.4))
            barra_alto = 5
            barra_x = int(self.x - barra_ancho / 2)
            barra_y = sprite_rect.top - 10
            pygame.draw.rect(pantalla, NEGRO, (barra_x, barra_y, barra_ancho, barra_alto))
            vida_ancho = int((self.vida / self.vida_maxima) * barra_ancho)
            pygame.draw.rect(pantalla, ROJO_SANGRE, (barra_x, barra_y, vida_ancho, barra_alto))

class Proyectil:
    def __init__(self, x, y, tx, ty, daño, color):
        self.x = x
        self.y = y
        self.radio = 6
        self.velocidad = 12
        self.daño = daño
        self.color = color
        self.activo = True
        self.tipo = "proyectil"
        
        angle = math.atan2(ty - y, tx - x)
        self.dx = math.cos(angle) * self.velocidad
        self.dy = math.sin(angle) * self.velocidad
    
    def actualizar(self):
        self.x += self.dx
        self.y += self.dy
    
    def verificar_colision(self, enemigos):
        for enemigo in enemigos:
            if enemigo.esta_vivo():
                dist = math.sqrt((self.x - enemigo.x)**2 + (self.y - enemigo.y)**2)
                if dist < self.radio + enemigo.radio:
                    enemigo.recibir_daño(self.daño)
                    self.activo = False
                    # Pequeño efecto de empuje
                    enemigo.x += self.dx * 0.5
                    enemigo.y += self.dy * 0.5
                    return True
        return False

    def fuera_de_pantalla(self, ancho, alto):
        return self.x < 0 or self.x > ancho or self.y < 0 or self.y > alto
    
    def dibujar(self, pantalla):
        # Efecto de rastro
        for i in range(3):
            alpha = 255 - (i * 80)
            offset_x = self.x - (self.dx * i * 0.5)
            offset_y = self.y - (self.dy * i * 0.5)
            surface = pygame.Surface((self.radio*2, self.radio*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (self.radio, self.radio), self.radio - i)
            pantalla.blit(surface, (offset_x - self.radio, offset_y - self.radio))

class EfectoTajo:
    def __init__(self, x, y, angulo, alcance, daño):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.alcance = alcance
        self.vida = 15 # Frames de duración
        self.activo = True
        self.tipo = "efecto"
        self.color = (200, 200, 255)
    
    def actualizar(self):
        self.vida -= 1
        if self.vida <= 0:
            self.activo = False
    
    def verificar_colision(self, enemigos):
        pass # La colisión se calcula al nacer el ataque para la espada
    
    def dibujar(self, pantalla):
        # Dibujar un arco
        rect = pygame.Rect(self.x - self.alcance, self.y - self.alcance, self.alcance*2, self.alcance*2)
        start_angle = -self.angulo - 0.5
        stop_angle = -self.angulo + 0.5
        pygame.draw.arc(pantalla, self.color, rect, start_angle, stop_angle, int(5 * (self.vida/15) + 1))
        
        # Linea de brillo central
        end_x = self.x + math.cos(self.angulo) * self.alcance
        end_y = self.y + math.sin(self.angulo) * self.alcance
        pygame.draw.line(pantalla, BLANCO, (self.x, self.y), (end_x, end_y), 2)

class EfectoGolpeSuelo:
    def __init__(self, x, y, radio_max):
        self.x = x
        self.y = y
        self.radio_max = radio_max
        self.radio_actual = 10
        self.vida = 20
        self.activo = True
        self.tipo = "efecto"
    
    def actualizar(self):
        self.radio_actual += (self.radio_max - self.radio_actual) * 0.2
        self.vida -= 1
        if self.vida <= 0:
            self.activo = False
            
    def verificar_colision(self, enemigos):
        pass # Daño instantáneo al nacer
        
    def dibujar(self, pantalla):
        alpha = int(255 * (self.vida / 20))
        surface = pygame.Surface((self.radio_max*2, self.radio_max*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (139, 69, 19, alpha), (self.radio_max, self.radio_max), int(self.radio_actual))
        pygame.draw.circle(surface, (255, 255, 255, alpha), (self.radio_max, self.radio_max), int(self.radio_actual), 2)
        pantalla.blit(surface, (self.x - self.radio_max, self.y - self.radio_max))

def generar_enemigos(cantidad, oleada, ancho_pantalla, alto_pantalla):
    enemigos = []
    tipos = ["normal", "rapido", "pesado"]
    # Probabilidades según oleada
    pesos = [70, 20, 10]
    if oleada > 2: pesos = [50, 30, 20]
    if oleada > 4: pesos = [30, 40, 30]

    for _ in range(cantidad):
        lado = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if lado == 'arriba':
            x, y = random.randint(0, ancho_pantalla), -40
        elif lado == 'abajo':
            x, y = random.randint(0, ancho_pantalla), alto_pantalla + 40
        elif lado == 'izquierda':
            x, y = -40, random.randint(0, alto_pantalla)
        else:
            x, y = ancho_pantalla + 40, random.randint(0, alto_pantalla)
            
        tipo = random.choices(tipos, weights=pesos, k=1)[0]
        enemigos.append(Enemigo(x, y, oleada, tipo))
    
    return enemigos

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

# -- Pantallas (Similares pero con mejor estilo visual) --
def pantalla_menu(pantalla, mouse_pos, fondo):
    pantalla.blit(fondo, (0, 0))
    
    # Estandarte o decoración tras el título (Ancho aumentado para evitar que el texto se salga)
    s = pygame.Surface((700, 150), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect(), border_radius=20)
    pantalla.blit(s, (ANCHO//2 - 350, 120))

    dibujar_texto(pantalla, "CRÓNICAS MEDIEVALES", 56, DORADO, ANCHO//2, 160)
    dibujar_texto(pantalla, "La Última Defensa", 36, GRIS_ACERO, ANCHO//2, 230)
    
    return dibujar_boton_medieval(pantalla, "INICIAR BATALLA", ANCHO//2, 400, 300, 70, mouse_pos)

def pantalla_seleccion_arma(pantalla, mouse_pos):
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "ELIGE TU DESTINO", 60, DORADO, ANCHO//2, 50)
    
    botones = []
    # Aumentar ancho de carta y separación
    ancho_carta = 240
    alto_carta = 400
    sep_cartas = 260
    start_x = ANCHO//2 - sep_cartas
    
    posiciones = [start_x, ANCHO//2, ANCHO//2 + sep_cartas]
    armas_lista = ["vara", "espada", "mazo"]
    
    c_y = ALTO // 2 + 30
    
    # Fuente para descripciones (cacheada para eficiencia)
    fuente_desc = pygame.font.SysFont("Arial", 18, bold=False)

    for i, arma_tipo in enumerate(armas_lista):
        arma = ARMAS[arma_tipo]
        x = posiciones[i]
        
        rect_carta = pygame.Rect(x - ancho_carta//2, c_y - alto_carta//2, ancho_carta, alto_carta)
        
        es_hover = rect_carta.collidepoint(mouse_pos)
        color_borde = DORADO if es_hover else arma["color"]
        grosor_borde = 4 if es_hover else 2
        
        # Fondo carta
        pygame.draw.rect(pantalla, (25, 25, 30), rect_carta)
        pygame.draw.rect(pantalla, color_borde, rect_carta, grosor_borde)
        
        # --- Contenido Interno ---
        
        # 1. Título (Tamaño reducido para que quepa "Martillo de Guerra")
        dibujar_texto(pantalla, arma["nombre"], 24, arma["color"], x, rect_carta.top + 40)
        
        # 2. Área de Imagen
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

        # 3. Separador
        pygame.draw.line(pantalla, (50, 50, 50), (x - 90, rect_carta.top + 190), (x + 90, rect_carta.top + 190), 2)
        
        # 4. Stats
        stats_y = rect_carta.top + 220
        dibujar_texto(pantalla, f"Velocidad: {arma['velocidad_ataque']}s", 22, BLANCO, x, stats_y)
        dibujar_texto(pantalla, f"Daño: {arma['daño']}", 22, BLANCO, x, stats_y + 30)
        
        # 5. Descripción con Wrap real (calculando píxeles)
        desc_y = stats_y + 65
        texto_desc = arma["descripcion"]
        
        palabras = texto_desc.split()
        lineas = []
        linea_act = ""
        ancho_max = ancho_carta - 30 # Margen interno seguro
        
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
    # Dibujar fondo prerenderizado
    pantalla.blit(fondo, (0, 0))
    
    for efecto in efectos:
        efecto.dibujar(pantalla)
    
    for enemigo in enemigos:
        enemigo.dibujar(pantalla)
    
    jugador.dibujar(pantalla)
    
    # UI Superpuesta (Con fondo semitransparente para leer mejor)
    ancho_ui = 300
    alto_ui = 100
    s = pygame.Surface((ancho_ui, alto_ui))
    s.set_alpha(150)
    s.fill(NEGRO)
    pantalla.blit(s, (ANCHO//2 - ancho_ui//2, 10))
    
    dibujar_texto(pantalla, f"OLEADA {oleada}/5", 40, BLANCO, ANCHO//2, 35)
    dibujar_texto(pantalla, f"Enemigos: {enemigos_totales}", 24, GRIS_ACERO, ANCHO//2, 75)

def pantalla_fin_juego(pantalla, estado, oleada_alcanzada, mouse_pos, fondo):
    # Fondo decorativo
    pantalla.blit(fondo, (0, 0))

    if estado == VICTORIA:
        color_titulo = VERDE_CÉSPED
        titulo = "¡VICTORIA GLORIOSA!"
    else:
        color_titulo = ROJO_SANGRE
        titulo = "GAME OVER"

    # Overlay semitransparente
    overlay_ancho = 820
    overlay_alto = 220
    s = pygame.Surface((overlay_ancho, overlay_alto), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect(), border_radius=24)
    pantalla.blit(s, (ANCHO//2 - overlay_ancho//2, 150))

    dibujar_texto(pantalla, titulo, 58, color_titulo, ANCHO//2, 210)
    dibujar_texto(pantalla, f"Oleada alcanzada: {oleada_alcanzada}", 32, BLANCO, ANCHO//2, 300)
    
    return dibujar_boton_medieval(pantalla, "MENU PRINCIPAL", ANCHO//2, 450, 300, 60, mouse_pos)

def main():
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
    fondo_juego = generar_fondo_pasto(ANCHO, ALTO)
    fondo_menu = generar_fondo_muro(ANCHO, ALTO)
    
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
                    if pantalla_menu(pantalla, mouse_pos, fondo_menu).collidepoint(mouse_pos):
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
                    jugador.velocidad_ataque = max(0.2, jugador.velocidad_ataque - 0.15)
                    # Restaurar al héroe antes de la siguiente oleada
                    jugador.vida = jugador.vida_maxima

            if jugador.vida <= 0:
                oleada_alcanzada = oleada_actual
                estado_juego = GAME_OVER
            
            # Solo dibujamos el juego si seguimos jugando, si cambiamos a game over, se dibujará en el siguiente frame en el bloque correcto
            if estado_juego == JUGANDO:
                pantalla_juego(pantalla, jugador, enemigos, efectos, oleada_actual, enemigos_restantes_spawn + len(enemigos), fondo_juego)
        
        elif estado_juego == VICTORIA or estado_juego == GAME_OVER:
            pantalla_fin_juego(pantalla, estado_juego, oleada_alcanzada, mouse_pos, fondo_menu)
            
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
