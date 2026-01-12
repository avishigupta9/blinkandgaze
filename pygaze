import time
import csv
from pygaze.display import Display
from pygaze.eyetracker import EyeTracker
from pygaze.libtime import clock
from pygaze.libinput import Mouse

def main():
    # Dummy eye tracker behaves like a mouse pointer for gaze.
    disp = Display()
    tracker = EyeTracker(disp, trackertype="dummy")
    mouse = Mouse()

    csv_path = f"pygaze_dummy_gaze_{int(time.time())}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["t_ms", "x", "y"])
        writer.writeheader()

        tracker.calibrate()

        start = clock.get_time()
        while True:
            t_ms = clock.get_time() - start
            x, y = mouse.get_pos()

            writer.writerow({"t_ms": t_ms, "x": x, "y": y})
            disp.fill()
            disp.show()

            # ESC to quit
            keys = mouse.get_pressed()
            # (simple exit condition: right click)
            if keys[2]:
                break

    disp.close()
    print(f"Saved to {csv_path}")

if __name__ == "__main__":
    main()
