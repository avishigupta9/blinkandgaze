import json
import socket
import time

UDP_HOST = "127.0.0.1"
UDP_PORT = 5055

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_HOST, UDP_PORT))

    log_path = f"blink_listener_{int(time.time())}.log"
    print(f"[listener] listening on {UDP_HOST}:{UDP_PORT}")
    print(f"[listener] logging to: {log_path}")

    with open(log_path, "w") as f:
        while True:
            data, _addr = sock.recvfrom(65535)
            msg = json.loads(data.decode("utf-8"))

            line = (
                f"ts={msg['ts']:.3f} "
                f"ear_avg={msg['ear_avg']} "
                f"closed={msg['is_closed']} "
                f"blink_event={msg['blink_event']} "
                f"blink_count={msg['blink_count']}"
            )
            print(line)
            f.write(line + "\n")
            f.flush()

if __name__ == "__main__":
    main()
