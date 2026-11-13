# src/detector.py
from ultralytics import YOLO
from src.config import MODEL_PATH, CONFIDENCE_THRESHOLD

class PersonTracker:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def detect_and_track(self, frame):
        """
        Detecta personas (clase 0 en COCO) y mantiene sus IDs entre frames.
        Retorna una lista de diccionarios con id, bbox y punto base (pies).
        """
        results = self.model.track(
            frame,
            persist=True,
            classes=[0],  # 0 = person
            conf=CONFIDENCE_THRESHOLD,
            tracker="bytetrack.yaml",
            verbose=False
        )

        detections = []
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = map(int, box)
                # Punto de referencia: centro inferior del bounding box (posición en el piso)
                foot_x = int((x1 + x2) / 2)
                foot_y = int(y2)

                detections.append({
                    "id": track_id,
                    "bbox": (x1, y1, x2, y2),
                    "anchor": (foot_x, foot_y)
                })

        return detections