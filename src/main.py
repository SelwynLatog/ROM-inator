#main.py
#testing opencvcam & displaying frames atm
import cv2
import time

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not detected.")
        exit()
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap

def resize_frame(frame):
    return cv2.resize(frame, (640, 480))

def calculate_fps(prev_time):
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    return fps, curr_time

def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

def main():
    cap = open_camera()
    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame = resize_frame(frame)
        fps, prev_time = calculate_fps(prev_time)
        frame = draw_fps(frame, fps)

        cv2.imshow("ROM-inator Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()