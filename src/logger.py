"""
logger.py

Save events to both CSV and JSON.
"""

import csv
import json
import os


class EventLogger:

    def __init__(self):

        os.makedirs("outputs", exist_ok=True)

        self.csv_path = "outputs/events.csv"
        self.json_path = "outputs/events.json"

        self.events = []

        with open(self.csv_path, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "frame",
                "track_id",
                "event",
                "current_occupancy"
            ])

    def log(
        self,
        timestamp,
        frame_number,
        track_id,
        event,
        occupancy
    ):

        # ---------- CSV ----------

        with open(self.csv_path, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                frame_number,
                track_id,
                event,
                occupancy
            ])

        # ---------- JSON ----------

        self.events.append({

            "timestamp": timestamp,

            "frame": frame_number,

            "track_id": track_id,

            "event": event,

            "current_occupancy": occupancy

        })

        with open(self.json_path, "w") as file:

            json.dump(
                self.events,
                file,
                indent=4
            )