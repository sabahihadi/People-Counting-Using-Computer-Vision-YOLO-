"""
performance.py

Generate performance report for the People Counter project.

The report contains:

1. Video information
2. Pipeline performance metrics
3. Counting statistics
"""

import os
import statistics


class PerformanceReport:
    """
    Generate and save a performance report.
    """

    def save(
        self,
        filename,
        total_frames,
        video_fps,
        processing_fps,
        total_time,
        latencies,
        enter_events,
        exit_events,
        max_occupancy,
        final_occupancy
    ):
        """
        Save performance report.

        Parameters
        ----------
        filename : str
            Output report filename.

        total_frames : int
            Total processed frames.

        video_fps : float
            FPS of input video.

        processing_fps : float
            Actual FPS achieved by the system.

        total_time : float
            Total execution time (seconds).

        latencies : list[float]
            Pipeline latency for every processed frame (seconds).

        enter_events : int
            Number of ENTER events.

        exit_events : int
            Number of EXIT events.

        max_occupancy : int
            Maximum occupancy observed.

        final_occupancy : int
            Occupancy at the end of the video.
        """

        # Create output directory if needed
        os.makedirs("outputs", exist_ok=True)

        # -----------------------------
        # Pipeline latency statistics
        # -----------------------------

        average_latency = sum(latencies) / len(latencies)

        minimum_latency = min(latencies)

        maximum_latency = max(latencies)

        if len(latencies) > 1:
            std_latency = statistics.stdev(latencies)
        else:
            std_latency = 0.0

        # -----------------------------
        # Write report
        # -----------------------------

        with open(filename, "w", encoding="utf-8") as file:

            file.write("=" * 55 + "\n")
            file.write("People Counter Performance Report\n")
            file.write("=" * 55 + "\n\n")

            # ----------------------------------------
            # Video Information
            # ----------------------------------------

            file.write("VIDEO INFORMATION\n")
            file.write("-" * 55 + "\n")

            file.write(f"Input Video FPS              : {video_fps:.2f}\n")
            file.write(f"Processed Frames             : {total_frames}\n")
            file.write(f"Total Processing Time        : {total_time:.2f} sec\n\n")

            # ----------------------------------------
            # Pipeline Performance
            # ----------------------------------------

            file.write("PIPELINE PERFORMANCE\n")
            file.write("-" * 55 + "\n")

            file.write(f"Processing Throughput        : {processing_fps:.2f} FPS\n")
            file.write(f"Average Pipeline Latency     : {average_latency*1000:.2f} ms\n")
            file.write(f"Minimum Pipeline Latency     : {minimum_latency*1000:.2f} ms\n")
            file.write(f"Maximum Pipeline Latency     : {maximum_latency*1000:.2f} ms\n")
            file.write(f"Latency Standard Deviation   : {std_latency*1000:.2f} ms\n\n")

            # ----------------------------------------
            # Counting Statistics
            # ----------------------------------------

            file.write("COUNTING STATISTICS\n")
            file.write("-" * 55 + "\n")

            file.write(f"ENTER Events                : {enter_events}\n")
            file.write(f"EXIT Events                 : {exit_events}\n")
            file.write(f"Maximum Occupancy           : {max_occupancy}\n")
            file.write(f"Final Occupancy             : {final_occupancy}\n")