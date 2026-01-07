import pygame

# Inicialización mínima para usar colores/constantes si fuera necesario, 
# aunque generalmente solo definimos tuplas aquí.

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
