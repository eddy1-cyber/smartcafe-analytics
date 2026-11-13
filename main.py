# main.py
import cv2
from src.config import VIDEO_SOURCE
from src.detector import PersonTracker
from src.roi_manager import ServiceMonitor
from src.dashboard import AnalyticsDashboard

def main():
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir la fuente de video '{VIDEO_SOURCE}'.")
        return

    tracker = PersonTracker()
    monitor = ServiceMonitor()
    dashboard = AnalyticsDashboard()

    print("Iniciando SmartCafe Analytics... Presiona 'q' en la ventana de video para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            # Reiniciar video en bucle si es un archivo pregrabado
            if isinstance(VIDEO_SOURCE, str):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            break

        # Estandarizar resolución a 1280x720 para mantener consistencia con los ROIs
        frame = cv2.resize(frame, (1280, 720))

        # Pipeline de Visión Artificial
        detections = tracker.detect_and_track(frame)
        monitor.update(detections)
        metrics = monitor.get_metrics()
        output_frame = dashboard.render(frame, detections, metrics)

        cv2.imshow("SmartCafe Analytics - Monitoreo en Tiempo Real", output_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()