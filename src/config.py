# src/config.py

# Fuente de video: 0 para webcam o ruta a archivo MP4 (ej: "data/cafe_demo.mp4")
VIDEO_SOURCE = "data/bangkok_airport.mp4"

# Modelo YOLO (yolov8n.pt es ligero y rápido para tiempo real)
MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.45

# Regiones de Interés (ROI) definidas como [x1, y1, x2, y2] para resolución 1280x720
ROI_MOSTRADOR = [450, 250, 850, 650]   # Zona de atención en barra
ROI_ESPERA = [50, 250, 430, 680]       # Zona de fila / espera

# Umbrales de tiempo (en segundos)
MAX_WAIT_TIME_SEC = 15.0               # Alerta si un cliente supera este tiempo en barra

# Paleta de colores (Formato BGR para OpenCV)
COLOR_BG_HUD = (20, 20, 25)
COLOR_ACCENT = (255, 191, 0)           # Azul eléctrico / Cian
COLOR_OK = (80, 220, 100)              # Verde
COLOR_ALERT = (60, 60, 255)            # Rojo alerta
COLOR_TEXT = (245, 245, 245)