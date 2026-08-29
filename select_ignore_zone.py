"""
select_ignore_zone.py

Utility for selecting an Ignore Zone using the mouse.

Usage:
    python select_ignore_zone.py
"""

import cv2
from src.config import VIDEO_PATH

points = []


def mouse_callback(event, x, y, flags, param):
    """
    Store two mouse clicks.
    """

    global points

    if event == cv2.EVENT_LBUTTONDOWN:

        points.append((x, y))

        print(f"Point {len(points)} : ({x}, {y})")


def main():

    cap = cv2.VideoCapture(VIDEO_PATH)

    success, frame = cap.read()

    cap.release()

    if not success:
        print("Cannot read video.")
        return

    clone = frame.copy()

    cv2.namedWindow("Select Ignore Zone")

    cv2.setMouseCallback(
        "Select Ignore Zone",
        mouse_callback
    )

    print("=" * 50)
    print("Click TOP-LEFT corner of the pole")
    print("Then click BOTTOM-RIGHT corner")
    print("=" * 50)

    while True:

        display = clone.copy()

        if len(points) == 1:

            cv2.circle(display, points[0], 5, (0, 0, 255), -1)

        elif len(points) == 2:

            cv2.rectangle(
                display,
                points[0],
                points[1],
                (0, 255, 0),
                2
            )

        cv2.imshow("Select Ignore Zone", display)

        key = cv2.waitKey(20)

        if key == 27:      # ESC
            break

        if len(points) == 2:

            print("\nIgnore Zone Coordinates")
            print("-----------------------")
            print(f"TOP_LEFT     = {points[0]}")
            print(f"BOTTOM_RIGHT = {points[1]}")

            cv2.waitKey(0)
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()