"""
main.py

People Counter using:
- YOLO11
- ByteTrack
- Virtual Fence
- Event Manager

Outputs
-------
1. Annotated Video
2. CSV Events
3. JSON Events
4. Performance Report
"""

import time
import cv2

from src.config import (
    VIDEO_PATH,
    TOP_LEFT,
    BOTTOM_RIGHT
)

from src.tracker import PersonTracker
from src.fence import VirtualFence
from src.event_manager import EventManager
from src.logger import EventLogger
from src.performance import PerformanceReport


def main():

    # -------------------------------------------------
    # Initialize modules
    # -------------------------------------------------

    tracker = PersonTracker()

    fence = VirtualFence(
        TOP_LEFT,
        BOTTOM_RIGHT
    )

    event_manager = EventManager()

    logger = EventLogger()

    report = PerformanceReport()

    # -------------------------------------------------
    # Open Video
    # -------------------------------------------------

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():

        print("Cannot open video.")

        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # -------------------------------------------------
    # Output Video
    # -------------------------------------------------

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video_writer = cv2.VideoWriter(

        "outputs/output.mp4",

        fourcc,

        fps,

        (width, height)

    )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    frame_number = 0

    enter_count = 0

    exit_count = 0

    max_occupancy = 0

    latencies = []

    program_start = time.perf_counter()

    # -------------------------------------------------
    # Main Loop
    # -------------------------------------------------

    while True:

        frame_start = time.perf_counter()

        success, frame = cap.read()

        if not success:

            break

        frame_number += 1

        # ---------------------------------------------
        # Draw Fence
        # ---------------------------------------------

        cv2.rectangle(

            frame,

            TOP_LEFT,

            BOTTOM_RIGHT,

            (0, 0, 255),

            2

        )

        # ---------------------------------------------
        # Tracking
        # ---------------------------------------------

        tracks = tracker.track(frame)

        cv2.putText(

            frame,

            f"Active Tracks : {len(tracks)}",

            (25, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (0, 255, 255),

            2

        )

        # ---------------------------------------------
        # Process Tracks
        # ---------------------------------------------

        for obj in tracks:

            x1, y1, x2, y2 = obj["bbox"]

            track_id = obj["id"]

            inside = fence.is_inside(obj["bbox"])

            event = event_manager.update(

                track_id,

                inside,

                frame_number

            )

            # -----------------------------------------
            # Event occurred
            # -----------------------------------------

            if event is not None:

                if event == "ENTER":

                    enter_count += 1

                elif event == "EXIT":

                    exit_count += 1

                seconds = frame_number / fps

                hours = int(seconds // 3600)

                minutes = int((seconds % 3600) // 60)

                secs = seconds % 60

                timestamp = f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

                logger.log(

                    timestamp,

                    frame_number,

                    track_id,

                    event,

                    event_manager.get_count()

                )

                print(

                    f"{timestamp} | "

                    f"Frame {frame_number} | "

                    f"Track {track_id} | "

                    f"{event}"

                )

            # -----------------------------------------
            # Visualization
            # -----------------------------------------

            if inside:

                color = (0, 255, 0)

                status = "INSIDE"

            else:

                color = (0, 0, 255)

                status = "OUTSIDE"

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                color,

                2

            )

            cv2.putText(

                frame,

                f"ID {track_id}",

                (x1, y1 - 10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                color,

                2

            )

            foot = fence.foot_point(obj["bbox"])

            cv2.circle(

                frame,

                foot,

                5,

                (255, 0, 0),

                -1

            )

            cv2.putText(

                frame,

                status,

                (x1, y2 + 20),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                color,

                2

            )

        # ---------------------------------------------
        # Cleanup
        # ---------------------------------------------

        event_manager.cleanup(frame_number)

        current_occ = event_manager.get_count()

        max_occupancy = max(

            max_occupancy,

            current_occ

        )

        cv2.putText(

            frame,

            f"Occupancy : {current_occ}",

            (25, 20),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (0, 255, 255),

            2

        )

        # ---------------------------------------------
        # Latency
        # ---------------------------------------------

        frame_end = time.perf_counter()

        latency = frame_end - frame_start

        latencies.append(latency)

        # ---------------------------------------------
        # Save & Show
        # ---------------------------------------------

        video_writer.write(frame)

        cv2.imshow(

            "People Counter",

            frame

        )

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

    # -------------------------------------------------
    # Final Statistics
    # -------------------------------------------------

    program_end = time.perf_counter()

    total_time = program_end - program_start

    average_latency = sum(latencies) / len(latencies)

    processing_fps = frame_number / total_time

    # -------------------------------------------------
    # Save Performance Report
    # -------------------------------------------------

    report.save(

    filename="outputs/performance_report.txt",

    total_frames=frame_number,

    video_fps=fps,

    processing_fps=processing_fps,

    total_time=total_time,

    latencies=latencies,

    enter_events=enter_count,

    exit_events=exit_count,

    max_occupancy=max_occupancy,

    final_occupancy=event_manager.get_count()

    )

    # -------------------------------------------------
    # Release Resources
    # -------------------------------------------------

    cap.release()

    video_writer.release()

    cv2.destroyAllWindows()

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    print("\n========== Processing Finished ==========")

    print("Output Video        : outputs/output.mp4")

    print("CSV Events          : outputs/events.csv")

    print("JSON Events         : outputs/events.json")

    print("Performance Report  : outputs/performance_report.txt")

    print(f"Average FPS         : {processing_fps:.2f}")

    print(f"Average Latency     : {average_latency*1000:.2f} ms")


if __name__ == "__main__":

    main()