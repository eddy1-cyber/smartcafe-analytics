# src/dashboard.py
import cv2
import numpy as np
from src.config import (
    ROI_MOSTRADOR, ROI_ESPERA,
    COLOR_BG_HUD, COLOR_ACCENT, COLOR_OK, COLOR_ALERT, COLOR_TEXT
)

class AnalyticsDashboard:
    def render(self, frame, detections, metrics):
        overlay = frame.copy()

        # 1. Dibujar Regiones de Interés (ROIs) semitransparentes
        counter_color = COLOR_ALERT if metrics["alert"] else COLOR_OK
        cv2.rectangle(overlay, (ROI_MOSTRADOR[0], ROI_MOSTRADOR[1]),
                      (ROI_MOSTRADOR[2], ROI_MOSTRADOR[3]), counter_color, -1)
        cv2.rectangle(overlay, (ROI_ESPERA[0], ROI_ESPERA[1]),
                      (ROI_ESPERA[2], ROI_ESPERA[3]), COLOR_ACCENT, -1)

        cv2.addWeighted(overlay, 0.18, frame, 0.82, 0, frame)

        # Bordes y etiquetas de zonas
        cv2.rectangle(frame, (ROI_MOSTRADOR[0], ROI_MOSTRADOR[1]),
                      (ROI_MOSTRADOR[2], ROI_MOSTRADOR[3]), counter_color, 2)
        cv2.putText(frame, "ZONA DE ATENCION (BARRA)", (ROI_MOSTRADOR[0] + 10, ROI_MOSTRADOR[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, counter_color, 2)

        cv2.rectangle(frame, (ROI_ESPERA[0], ROI_ESPERA[1]),
                      (ROI_ESPERA[2], ROI_ESPERA[3]), COLOR_ACCENT, 2)
        cv2.putText(frame, "ZONA DE ESPERA", (ROI_ESPERA[0] + 10, ROI_ESPERA[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_ACCENT, 2)

        # 2. Dibujar detecciones y cronómetros individuales
        for person in detections:
            x1, y1, x2, y2 = person["bbox"]
            tid = person["id"]
            service_time = person.get("service_time")
            is_delayed = person.get("is_delayed", False)

            box_color = COLOR_ALERT if is_delayed else (COLOR_OK if service_time else COLOR_ACCENT)
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.circle(frame, person["anchor"], 5, box_color, -1)

            label = f"ID #{tid}"
            if service_time is not None:
                label += f" | {service_time:.1f}s"

            cv2.rectangle(frame, (x1, y1 - 28), (x1 + len(label) * 11, y1), box_color, -1)
            cv2.putText(frame, label, (x1 + 5, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (15, 15, 15), 2)

        # 3. Panel HUD Superior
        self._draw_hud(frame, metrics)
        return frame

    def _draw_hud(self, frame, metrics):
        h, w, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (w, 85), COLOR_BG_HUD, -1)
        cv2.line(frame, (0, 85), (w, 85), COLOR_ACCENT, 2)

        # Métricas en columnas
        stats = [
            ("FLUJO TOTAL", f"{metrics['total_flow']} clientes", 30),
            ("EN ESPERA", f"{metrics['in_wait']}", 260),
            ("EN BARRA", f"{metrics['at_counter']}", 440),
            ("TIEMPO PROMEDIO", f"{metrics['avg_service_time']:.1f} s", 620),
            ("ATENDIDOS", f"{metrics['completed_orders']}", 880),
        ]

        for title, value, x_pos in stats:
            cv2.putText(frame, title, (x_pos, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (170, 170, 170), 1)
            cv2.putText(frame, value, (x_pos, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.85, COLOR_TEXT, 2)

        # Indicador de Alerta Visual
        if metrics["alert"]:
            cv2.rectangle(frame, (w - 310, 15), (w - 20, 70), COLOR_ALERT, -1)
            cv2.putText(frame, "ALERTA: DEMORA EN BARRA", (w - 295, 48),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_TEXT, 2)