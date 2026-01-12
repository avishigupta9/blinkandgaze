import cv2
import csv
import time
import json
import socket
import numpy as np
import mediapipe as mp

# ---------- Streaming config ----------
UDP_HOST = "127.0.0.1"
UDP_PORT = 5055

# ---------- MediaPipe ----------
mp_face_mesh = mp.solutions.face_mesh

# FaceMesh eye landmarks (practical subset for EAR-like metric)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def euclid(p1, p2):
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))

def eye_aspect_ratio(pts):
    # EAR = (||p2-p6|| + ||p3-p5||) / (2*||p1-p4||)
    p1, p2, p3, p4, p5, p6 = pts
    return (euclid(p2, p6) + euclid(p3, p5)) / (2.0 * euclid(p1, p4) + 1e-9)

def idxs_to_xy(landmarks, w, h, idxs):
    return [(landmarks[i].x * w, landmarks[i].y * h) for i in idxs]

def main():
    # Install deps:
    # pip install opencv-python mediapipe numpy
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    # ---- Tunables (calibrate per camera/user) ----
    EAR_THRESHOLD = 0.21
    MIN_CONSEC_FRAMES = 2

    blink_count = 0
    closed_frames = 0

    csv_path = f"blink_raw_{int(time.time())}.csv"
    print(f"[producer] logging raw data to: {csv_path}")
    print(f"[producer] streaming UDP to {UDP_HOST}:{UDP_PORT}")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ts", "ear_left", "ear_right", "ear_avg",
            "is_closed", "blink_event", "blink_count"
        ])
        writer.writeheader()

        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as mesh:

            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                h, w = frame.shape[:2]
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = mesh.process(rgb)

                ts = time.time()

                # default payload (also useful when face not detected)
                payload = {
                    "ts": ts,
                    "ear_left": None,
                    "ear_right": None,
                    "ear_avg": None,
                    "is_closed": None,
                    "blink_event": 0,
                    "blink_count": blink_count,
                }

                if res.multi_face_landmarks:
                    lm = res.multi_face_landmarks[0].landmark

                    left_pts = idxs_to_xy(lm, w, h, LEFT_EYE)
                    right_pts = idxs_to_xy(lm, w, h, RIGHT_EYE)

                    ear_left = eye_aspect_ratio(left_pts)
                    ear_right = eye_aspect_ratio(right_pts)
                    ear_avg = (ear_left + ear_right) / 2.0

                    is_closed = int(ear_avg < EAR_THRESHOLD)

                    blink_event = 0
                    if is_closed:
                        closed_frames += 1
                    else:
                        if closed_frames >= MIN_CONSEC_FRAMES:
                            blink_count += 1
                            blink_event = 1
                        closed_frames = 0

                    payload.update({
                        "ear_left": ear_left,
                        "ear_right": ear_right,
                        "ear_avg": ear_avg,
                        "is_closed": is_closed,
                        "blink_event": blink_event,
                        "blink_count": blink_count,
                    })

                # 1) log raw data row
                writer.writerow(payload)

                # 2) stream JSON to listener
                sock.sendto(json.dumps(payload).encode("utf-8"), (UDP_HOST, UDP_PORT))

                # minimal debug overlay
                cv2.putText(frame, f"blinks={blink_count}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                cv2.imshow("Blink Producer (press q)", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
