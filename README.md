#  SmartCafé Analytics

Sistema inteligente de monitoreo y análisis operativo para cafeterías y establecimientos gastronómicos mediante **Visión Artificial**. Desarrollado en **Python**, **OpenCV** y **YOLOv8 (ByteTrack)** para medir el flujo de clientes, cronometrar tiempos de atención en barra y alertar demoras en tiempo real.

---

##  Funcionalidades Principales

* **Detección y Conteo de Flujo de Clientes:** Identificación continua de personas en el establecimiento mediante aprendizaje profundo (YOLOv8) y asignación de IDs persistentes entre fotogramas.
* **Cronometraje Individual en Barra:** Regiones de interés (ROI) configuradas en el mostrador que inician automáticamente un cronómetro cuando un cliente ingresa a la zona de pedidos y registran el tiempo total al retirarse.
* **Dashboard HUD en Tiempo Real:** Interfaz gráfica superpuesta sobre el flujo de video con métricas clave (flujo total, clientes en espera, clientes en barra, tiempo promedio de atención y contador de pedidos completados).
* **Sistema de Alertas Visuales:** Cambio dinámico de color en las zonas de interés y notificación visual en pantalla cuando un cliente supera el tiempo límite de espera establecido.

---

##  Arquitectura del Proyecto

```text
smartcafe-analytics/
├── data/                      # Videos de prueba (.mp4)
├── src/
│   ├── __init__.py            # Inicializador del paquete
│   ├── config.py              # Coordenadas ROI, umbrales de tiempo y paleta de colores
│   ├── detector.py            # Motor de detección y tracking (YOLOv8 + ByteTrack)
│   ├── roi_manager.py         # Lógica de cronómetros, conteo en zonas y cálculo de promedios
│   └── dashboard.py           # Renderizado del panel HUD, cajas delimitadoras y alertas
├── main.py                    # Punto de entrada principal y bucle de procesamiento de video
├── requirements.txt           # Lista de dependencias del proyecto
└── README.md                  # Documentación técnica


---

## Guía de Calibración de Regiones de Interés (ROI)
El sistema estandariza todos los fotogramas de entrada a una resolución de 1280x720 píxeles para mantener consistencia en las coordenadas. Dependiendo del ángulo de tu cámara o video de prueba, puedes ajustar las zonas de monitoreo siguiendo estos pasos:

1. Entender el sistema de coordenadas
En OpenCV, el origen (0, 0) se ubica en la esquina superior izquierda:

x: Desplazamiento horizontal de izquierda (0) a derecha (1280).

y: Desplazamiento vertical de arriba (0) a abajo (720).

Cada región de interés se define mediante una lista de 4 valores: [x1, y1, x2, y2], donde (x1, y1) es la esquina superior izquierda del rectángulo y (x2, y2) es la esquina inferior derecha.

2. Punto de anclaje de detección
Para evitar falsos positivos cuando alguien camina por detrás del mostrador, el sistema evalúa el centro inferior del cuadro delimitador (posición de los pies) de cada persona (anchor = (foot_x, foot_y)). Asegúrate de que los rectángulos ROI cubran el área del piso donde se paran los clientes.