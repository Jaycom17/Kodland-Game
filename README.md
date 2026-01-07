# Crónicas Medievales: La Última Defensa

**Crónicas Medievales** es un arcade survival ambientado en un campo de batalla medieval generado por código. Controla a un héroe que resiste oleada tras oleada combinando posicionamiento, control de área y gestión de ritmo de ataque.

---

## Tabla de Contenidos
- [Visión General](#visión-general)
- [Mecánicas de Juego](#mecánicas-de-juego)
- [Ciclo de Juego](#ciclo-de-juego)
- [Controles y HUD](#controles-y-hud)
- [Enemigos y Oleadas](#enemigos-y-oleadas)
- [Presentación Audiovisual](#presentación-audiovisual)
- [Características Técnicas Destacadas](#características-técnicas-destacadas)
- [Arquitectura Técnica](#arquitectura-técnica)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Guía de Desarrollo](#guía-de-desarrollo)
- [Créditos](#créditos)

---

## Visión General
- **Género:** Survival arcade con control top-down.
- **Motor:** Pygame 2, sin assets externos; todo se dibuja con primitivas.
- **Duración:** 5 oleadas progresivamente más difíciles.
- **Objetivo:** Sobrevivir a cada oleada, recuperando salud y mejorando la cadencia de ataque entre rondas.

---

## Mecánicas de Juego

### Clases y Armas
Cada arma define estilo de juego, alcance y efectos de control. La elección se realiza antes de la primera oleada:

| Clase | Rol | Ataque | Alcance | Detalles |
|-------|-----|--------|---------|----------|
| 🧙‍♂️ **Vara Arcana** | Control a distancia | Proyectil mágico teledirigido | Todo el mapa | Mantiene a los enemigos lejos pero depende del posicionamiento.
| ⚔️ **Espada Real** | Luchador versátil | Tajo en arco frontal con empuje | 120 px | Ideal contra grupos medianos; requiere mantener la orientación.
| 🔨 **Martillo de Guerra** | Tanque de área | Golpe sísmico circular | 150 px | Demuele grupos cerrados; lento pero con fuerte empuje.

### Recursos del Jugador
- **Salud:** 120 puntos, mostrados sobre el personaje. Se restaura por completo al finalizar cada oleada.
- **Velocidad de ataque:** El tiempo entre ataques disminuye tras superar cada oleada para compensar la dificultad creciente.
- **Movimiento:** Velocidad base homogénea con normalización al moverse en diagonal para preservar la física.

---

## Ciclo de Juego
1. **Menú Principal:** Presenta el título y botón para iniciar.
2. **Selección de Arma:** Cartas interactivas muestran estadísticas y descripción de cada estilo.
3. **Combate:**
   - Los enemigos se generan de forma progresiva (intervalos cada 0.5 s).
   - El jugador ataca automáticamente según su arma y objetivos en rango.
   - Los efectos visuales (tajos, ondas de choque, proyectiles) se gestionan como entidades temporales.
4. **Transición de Oleada:** Al eliminar todos los enemigos y spawns pendientes:
   - Se incrementa el número objetivo de enemigos.
   - Se ajusta la velocidad de ataque del jugador.
   - Se restaura salud.
5. **Fin de Partida:**
   - Al superar la oleada 5: pantalla de Victoria.
   - Al caer en combate: pantalla de Game Over con la oleada alcanzada.

---

## Controles y HUD
- **Movimiento:** Flechas o WASD.
- **Selección de menús:** Ratón.
- **Ataque:** Automático, orientado hacia el objetivo prioritario.
- **HUD superior:** Panel semitransparente con número de oleada y enemigos restantes.
- **Indicadores in-game:** Barra de salud encima del héroe y barras de vida individuales sobre cada enemigo que ha recibido daño.

---

## Enemigos y Oleadas

| Tipo | Apariencia | Velocidad | Salud | Daño | Comportamiento |
|------|------------|-----------|-------|------|----------------|
| **Normal** | Humanoide rojo | Media | Media | Media | Persigue directamente; base del balance.
| **Rápido** | Bestia amarilla | Alta | Baja | Media-baja | Flanquea velozmente; usa sprites tipo lobo.
| **Pesado** | Golem de piedra | Baja | Alta | Alta | Avanza implacable; castiga dejarlo acercarse.

**Escalado de oleadas:**
- Oleadas 1-5 tienen cuotas específicas (15, 20, 30, 40, 50 enemigos).
- Las proporciones de tipos se reconfiguran en las oleadas avanzadas para introducir más rápidos y pesados.

---

## Presentación Audiovisual
- **Entorno:** Fondo de césped sobrio generado con gradientes, ruido suave y manchas de tierra para un ambiente medieval sin distracciones.
- **Personajes:** Sprites procedurales con sombreado pseudo-volumétrico, capas de ropa y armas dinámicas.
- **UI:** Estética medieval consistente entre menú, selección, victoria y derrota.
- **Audio:** `song.mp3` se reproduce en bucle al 50% de volumen como música ambiente durante la partida.
- **Apoyo creativo:** Herramientas de inteligencia artificial aceleraron la iteración visual de enemigos, protagonista y armamento.

---

## Características Técnicas Destacadas

### 🎨 Renderizado 100% Procedural
Todo el contenido visual se genera en tiempo real mediante código Python y primitivas de Pygame:
- **Sin dependencias externas:** No se utilizan imágenes, sprites o tilesets precargados.
- **Sprites dinámicos:** Personajes y enemigos se construyen capa por capa con efectos de sombreado, permitiendo variaciones sin almacenar múltiples assets.
- **Escalado suave:** Aplicación de `pygame.transform.smoothscale` para mantener calidad visual en sprites generados proceduralmente.

### ⚡ Optimización de Rendimiento
- **Superficies estáticas reutilizables:** El fondo del campo de batalla se genera una sola vez al inicio y se reutiliza en cada frame.
- **Gestión eficiente de entidades:** Sistema de listas para proyectiles y efectos visuales con limpieza automática de objetos fuera de pantalla o completados.
- **Normalización vectorial:** Movimiento diagonal corregido matemáticamente para evitar velocidades mayores que el desplazamiento en un solo eje.

### 🎮 Sistemas de Combate Avanzados
- **Targeting inteligente:** El jugador ataca automáticamente al enemigo más cercano dentro del alcance de su arma.
- **Efectos de empuje (knockback):** Cada tipo de arma aplica fuerzas de retroceso diferenciadas, permitiendo control de multitudes.
- **Gestión de cooldowns:** Sistema de temporización preciso para la cadencia de ataque, con progresión dinámica entre oleadas.

### 🏗️ Arquitectura Modular y Escalable
- **Separación clara de responsabilidades:** Lógica de juego, renderizado, UI y configuración distribuidos en módulos independientes.
- **Configuración centralizada:** Todas las constantes de balance (daño, salud, velocidades) en `settings.py` para ajustes rápidos sin tocar código de lógica.
- **Sistema de estados:** Máquina de estados limpia (MENU, SELECCION, JUEGO, etc.) que facilita agregar nuevas pantallas o modos.

### 🧪 Física y Colisiones Precisas
- **Detección por distancia euclidiana:** Cálculo matemático preciso de rangos de ataque y colisiones jugador-enemigo.
- **Áreas de efecto circulares:** El Martillo de Guerra utiliza geometría circular real para determinar qué enemigos reciben daño.
- **Proyectiles teledirigidos:** La Vara Arcana implementa seguimiento de objetivo con interpolación suave de rotación.

### 📊 Balance Dinámico
- **Escalado progresivo:** Cada oleada incrementa el número de enemigos y ajusta las proporciones de tipos (normal/rápido/pesado).
- **Compensación de dificultad:** La velocidad de ataque del jugador mejora automáticamente tras superar cada oleada.
- **Restauración estratégica:** Salud completa entre oleadas para mantener un ritmo de juego equilibrado.

---

## Arquitectura Técnica

```
Kodland-Game/
├── main.py          # Bucle principal: estados, entradas, timing y ciclo de render.
└── src/
    ├── __init__.py  # Marca el paquete.
    ├── settings.py  # Constantes globales, colores, configuraciones de armas y estados.
    ├── entities.py  # Jugador, Enemigo, Proyectil, efectos visuales y spawner.
    ├── world.py     # Generadores de fondo: pradera y muralla del menú.
    ├── ui.py        # Pantallas de menú, selección, HUD y fin de partida.
    └── utils.py     # Utilidades de renderizado de texto y botones.
```

### Interacciones Clave
- `main.py` orquesta los estados y delega render y lógica específica a `ui.py` y `entities.py`.
- `entities.py` encapsula el comportamiento de los objetos activos con métodos `mover`, `atacar`, `dibujar` y `actualizar`.
- `world.py` genera superficies estáticas reutilizadas para evitar costes por frame.
- `settings.py` centraliza constantes para facilitar ajustes rápidos de balance.

### Generación Procedural
- **Sprites:** Construidos con `Surface` intermedias, permitiendo aplicar escalado suave (`smoothscale`) y efectos de sombra manuales.
- **Terreno:** El fondo utiliza gradientes verticales, manchas de ruido controlado y áreas de tierra con alfa bajo, para una estética sobria.
- **UI:** Componentes reutilizables como `dibujar_boton_medieval` aportan consistencia visual.

---

## Instalación y Ejecución

### Requisitos Previos
- Python 3.10 o superior.
- Pygame 2.6.1 (o compatible).

### Pasos
```bash
# Instalar dependencias
pip install pygame

# Ejecutar el juego
python3 main.py
```

> Consejo: usa un entorno virtual (`python -m venv venv` y luego `source venv/bin/activate`) para aislar dependencias.

---

## Guía de Desarrollo
- **Estructura modular:** Cada módulo cubre una responsabilidad clara. Para añadir nuevas armas o enemigos, edita `settings.py` y extiende las clases en `entities.py`.
- **Recarga rápida:** El fondo se genera una vez al inicio. Puedes ajustar parámetros en `world.py` sin penalizar el rendimiento en tiempo de ejecución.
- **Depuración:** Ejecuta `python -m pygame.docs` para revisar documentación oficial, o añade `print` controlados en el bucle principal para inspeccionar estados.
- **Música:** Reemplaza `song.mp3` respetando el nombre del archivo para mantener la carga automática.

