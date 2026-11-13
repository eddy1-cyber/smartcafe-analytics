# ☕ SmartCafé Analytics

Sistema inteligente de monitoreo y análisis operativo para cafeterías y establecimientos gastronómicos mediante **Visión Artificial**. Desarrollado en **Python**, **OpenCV** y **YOLOv8 (ByteTrack)** para medir el flujo de clientes, cronometrar tiempos de atención en barra y alertar demoras en tiempo real.

---

## 🎯 Funcionalidades Principales

* **Detección y Conteo de Flujo de Clientes:** Identificación continua de personas en el establecimiento mediante aprendizaje profundo (YOLOv8) y asignación de IDs persistentes entre fotogramas.
* **Cronometraje Individual en Barra:** Regiones de interés (ROI) configuradas en el mostrador que inician automáticamente un cronómetro cuando un cliente ingresa a la zona de pedidos y registran el tiempo total al retirarse.
* **Dashboard HUD en Tiempo Real:** Interfaz gráfica superpuesta sobre el flujo de video con métricas clave (flujo total, clientes en espera, clientes en barra, tiempo promedio de atención y contador de pedidos completados).
* **Sistema de Alertas Visuales:** Cambio dinámico de color en las zonas de interés y notificación visual en pantalla cuando un cliente supera el tiempo límite de espera establecido.

---

## 📁 Arquitectura del Proyecto

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