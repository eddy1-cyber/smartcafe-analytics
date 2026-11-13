# src/roi_manager.py
import time
from src.config import ROI_MOSTRADOR, ROI_ESPERA, MAX_WAIT_TIME_SEC

class ServiceMonitor:
    def __init__(self):
        self.active_sessions = {}      # {track_id: start_timestamp}
        self.completed_times = []      # Lista de tiempos totales de atención (segundos)
        self.total_unique_clients = set()
        self.current_in_wait = 0
        self.current_at_counter = 0
        self.alert_triggered = False

    @staticmethod
    def _is_inside_roi(point, roi):
        px, py = point
        x1, y1, x2, y2 = roi
        return x1 <= px <= x2 and y1 <= py <= y2

    def update(self, detections):
        now = time.time()
        current_counter_ids = set()
        wait_count = 0
        self.alert_triggered = False

        for person in detections:
            tid = person["id"]
            anchor = person["anchor"]
            self.total_unique_clients.add(tid)

            # Verificar zona de espera
            if self._is_inside_roi(anchor, ROI_ESPERA):
                wait_count += 1

            # Verificar zona de mostrador (cronometraje de atención)
            if self._is_inside_roi(anchor, ROI_MOSTRADOR):
                current_counter_ids.add(tid)
                if tid not in self.active_sessions:
                    # El cliente acaba de acercarse al mostrador
                    self.active_sessions[tid] = now

                elapsed = now - self.active_sessions[tid]
                person["service_time"] = elapsed
                person["is_delayed"] = elapsed > MAX_WAIT_TIME_SEC

                if person["is_delayed"]:
                    self.alert_triggered = True
            else:
                person["service_time"] = None
                person["is_delayed"] = False

        # Detectar clientes que ya salieron del mostrador para registrar su tiempo final
        finished_ids = [tid for tid in self.active_sessions if tid not in current_counter_ids]
        for tid in finished_ids:
            total_duration = now - self.active_sessions.pop(tid)
            if total_duration >= 2.0:  # Filtrar cruces accidentales menores a 2 segundos
                self.completed_times.append(total_duration)

        self.current_in_wait = wait_count
        self.current_at_counter = len(current_counter_ids)

    def get_metrics(self):
        avg_time = (
            sum(self.completed_times) / len(self.completed_times)
            if self.completed_times else 0.0
        )
        return {
            "total_flow": len(self.total_unique_clients),
            "in_wait": self.current_in_wait,
            "at_counter": self.current_at_counter,
            "avg_service_time": avg_time,
            "completed_orders": len(self.completed_times),
            "alert": self.alert_triggered
        }