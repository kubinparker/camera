import cv2
import socketio
sio = socketio.Client()
sio.connect('http://localhost:8000')

video_capture = cv2.VideoCapture(0)
ret, frame1 = video_capture.read()
ret, frame2 = video_capture.read()
i = 0
top_left, bottom_right = (330, 50), (450, 280)

while True:
    # Grab a single frame of video
    diff = cv2.absdiff(frame1, frame2)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.rectangle(frame1, top_left, bottom_right, (0, 255, 0), 2)
    for contour in contours:
        
        if cv2.contourArea(contour) < 900:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        center_x = x + w / 2
        center_y = y + h / 2
        logic = top_left[0] < center_x < bottom_right[0] and top_left[1] < center_y < bottom_right[1]
        if logic:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            sio.emit('notification', {'status': f'Moving-{i}'})
            i+=1

    cv2.imshow("Video", frame1)
    frame1 = frame2
    ret, frame2 = video_capture.read()

    if cv2.waitKey(50) == 27:
        sio.disconnect()
        break

video_capture.release()
cv2.destroyAllWindows()

