"""
tracker.py

YOLO11 + ByteTrack tracker.
"""

from ultralytics import YOLO

from src.config import (
    YOLO_MODEL,
    TRACKER,
    CONFIDENCE,
    PERSON_CLASS,
    IGNORE_TOP_LEFT,
    IGNORE_BOTTOM_RIGHT
)


class PersonTracker:
    """
    Multi-object tracker using YOLO11 and ByteTrack.
    """

    def __init__(self):

        # Load YOLO model
        self.model = YOLO(YOLO_MODEL)

    def is_in_ignore_zone(self, bbox):
        """
        Check whether the center of the bounding box
        is inside the configured Ignore Zone.
        """

        x1, y1, x2, y2 = bbox

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        return (
            IGNORE_TOP_LEFT[0] <= center_x <= IGNORE_BOTTOM_RIGHT[0]
            and
            IGNORE_TOP_LEFT[1] <= center_y <= IGNORE_BOTTOM_RIGHT[1]
        )
    
    def track(self, frame):
        """
        Perform person detection and tracking.

        Returns
        -------
        list

        [
            {
                "id": 5,
                "bbox": (x1,y1,x2,y2),
                "conf":0.91
            },
            ...
        ]
        """

        tracks = []

        results = self.model.track(

            frame,

            persist=True,

            tracker=TRACKER,

            conf=CONFIDENCE,

            imgsz=960,

            verbose=False

        )

        result = results[0]

        # No detections
        if result.boxes.id is None:
            return tracks

        ids = result.boxes.id.int().tolist()

        boxes = result.boxes.xyxy.cpu().numpy()

        classes = result.boxes.cls.cpu().numpy()

        scores = result.boxes.conf.cpu().numpy()

        for track_id, box, cls, score in zip(
            ids,
            boxes,
            classes,
            scores,
        ):

            if int(cls) != PERSON_CLASS:
                continue

            x1, y1, x2, y2 = map(int, box)

            # Ignore detections inside Ignore Zone
            if self.is_in_ignore_zone((x1, y1, x2, y2)):
                continue

            tracks.append(
                {
                    "id": track_id,
                    "bbox": (x1, y1, x2, y2),
                    "conf": float(score),
                    "center": (
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2)
                    ),
                }
            )
        return tracks