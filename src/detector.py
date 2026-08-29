"""
detector.py

Person detector using YOLO11.
"""

from ultralytics import YOLO

from src.config import YOLO_MODEL
from src.config import PERSON_CLASS
from src.config import CONFIDENCE


class PersonDetector:
    """
    Wrapper class around YOLO11.

    This class only detects people.
    """

    def __init__(self):

        # Load YOLO model
        self.model = YOLO(YOLO_MODEL)

    def detect(self, frame):
        """
        Detect people in a frame.

        Parameters
        ----------
        frame : ndarray

        Returns
        -------
        detections : list
            [(x1,y1,x2,y2,conf), ...]
        """

        detections = []

        # Run inference
        results = self.model.predict(
            frame,
            conf=CONFIDENCE,
            verbose=False
        )

        result = results[0]

        # Iterate over detections
        for box in result.boxes:

            cls = int(box.cls.item())

            # Ignore non-person objects
            if cls != PERSON_CLASS:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            confidence = float(box.conf.item())

            detections.append(
                (
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2),
                    confidence
                )
            )

        return detections