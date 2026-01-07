"""
Configuración global del juego
"""

# Colores - MEDIEVAL PALETTE
BLACK = (25, 20, 15)
WHITE = (235, 230, 220)       # Hueso/Pergamino claro
RED = (160, 30, 30)           # Rojo sangre
GREEN = (60, 120, 60)         # Verde bosque
BLUE = (40, 70, 140)          # Azul estandarte real
YELLOW = (218, 165, 32)       # Oro
ORANGE = (210, 105, 30)       # Fuego / Cobre
DARK_BLUE = (20, 25, 40)      # Noche
LIGHT_BLUE = (100, 149, 237)  # Cielo heráldico (se usará poco, preferimos cesped)
GRAY = (128, 128, 128)        # Cota de malla
DARK_GRAY = (60, 60, 60)      # Piedra de castillo
PURPLE = (75, 0, 130)         # Magia oscura
CYAN = (175, 238, 238)        # Cristal mágico (Pale Turquoise)
MIDNIGHT = (15, 10, 20)       # Noche profunda
BROWN = (101, 67, 33)         # Madera
GRASS = (85, 107, 47)         # Olive Drab / Césped

# Colores de UI
UI_BG = (70, 50, 30)          # Madera oscura
UI_BORDER = (184, 134, 11)    # Oro oscuro
UI_TEXT = (250, 240, 200)     # Pergamino

# Configuración de la base
BASE_MAX_HEALTH = 500
BASE_SIZE = 130 # Aumentado para mayor presencia
BASE_COLOR = DARK_GRAY        # Castillo

# Configuración del jugador
PLAYER_MAX_HEALTH = 100
PLAYER_SIZE = 30
PLAYER_SPEED = 250
PLAYER_DAMAGE = 20
PLAYER_ATTACK_COOLDOWN = 0.5
PLAYER_ATTACK_RANGE = 100
PLAYER_COLOR = BLUE           # Caballero

# Configuración de enemigos
ENEMY_SPAWN_MARGIN = 50

# Tipos de enemigos: [velocidad, vida, daño, color, tamaño]
ENEMY_TYPES = {
    "lento": {
        "speed": 40,
        "health": 120,
        "damage": 15,
        "color": (45, 55, 30),    # Verde Pantano Oscuro
        "size": 30
    },
    "rapido": {
        "speed": 130,
        "health": 40,
        "damage": 8,
        "color": (90, 40, 10),    # Marrón Óxido
        "size": 18
    },
    "balanceado": {
        "speed": 80,
        "health": 70,
        "damage": 10,
        "color": (70, 10, 10),    # Rojo Sangre Sangre Oscura
        "size": 24
    }
}

# Configuración de dificultad por noche
NIGHT_CONFIG = {
    1: {"duration": 45, "enemy_count": 8, "spawn_interval": 3.0, "types": ["lento", "rapido"]},
    2: {"duration": 50, "enemy_count": 12, "spawn_interval": 2.5, "types": ["lento", "rapido", "balanceado"]},
    3: {"duration": 55, "enemy_count": 16, "spawn_interval": 2.0, "types": ["lento", "rapido", "balanceado"]},
    4: {"duration": 60, "enemy_count": 20, "spawn_interval": 1.8, "types": ["lento", "rapido", "balanceado"]},
    5: {"duration": 70, "enemy_count": 25, "spawn_interval": 1.5, "types": ["lento", "rapido", "balanceado"]}
}

# Configuración de fase de día
DAY_DURATION = 30  # segundos
RESOURCE_SPAWN_COUNT = 15
RESOURCE_SIZE = 15
RESOURCE_VALUE = 10

# Configuración de mejoras (nombre: [costo, incremento])
UPGRADES = {
    "daño": {"cost": 50, "increment": 10},
    "velocidad": {"cost": 40, "increment": 30},
    "vida_jugador": {"cost": 60, "increment": 30},
    "reparar_base": {"cost": 80, "increment": 100},
    "resistencia_base": {"cost": 100, "increment": 50}
}
