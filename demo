import cv2
from gaze_tracking import GazeTracking
from datetime import datetime

def main():
    gaze = GazeTracking()
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise RuntimeError("Could not open webcam.")

    while True:
        ok, frame = cam.read()
        if not ok:
            break

        gaze.refresh(frame)
        annotated = gaze.annotated_frame()

        ts = datetime.utcnow().isoformat()

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        if gaze.is_blinking():
            status = "BLINKING"
        elif gaze.is_right():
            status = "LOOKING RIGHT"
        elif gaze.is_left():
            status = "LOOKING LEFT"
        elif gaze.is_center():
            status = "LOOKING CENTER"
        else:
            status = "UNKNOWN"

        cv2.putText(annotated, f"{ts} | {status}", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if left_pupil:
            cv2.putText(annotated, f"L pupil: {left_pupil}", (20, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        if right_pupil:
            cv2.putText(annotated, f"R pupil: {right_pupil}", (20, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Eye Tracking (GazeTracking)", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
