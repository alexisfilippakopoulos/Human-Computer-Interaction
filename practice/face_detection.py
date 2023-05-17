import numpy as np
import cv2
import cv2.data

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
detected_counter = 0
not_detected_counter = 0
patience = 100
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (fx, fy, fw, fh) in faces:
        roi_gray = gray[fy:fy+fw, fx:fx+fw]
        roi_color = frame[fy:fy+fh, fx:fx+fw]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
    
    if len(faces) >= 1 and len(eyes) >= 2:

        for (ex, ey , ew, eh) in eyes:
            #cv2.putText(frame, f"{len(faces)}, {len(eyes)}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            detected_counter += 1
            if detected_counter > 20:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 5)
                cv2.putText(frame, f"Frames: {detected_counter}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    else:
        not_detected_counter += 1
        if not_detected_counter > patience:
            detected_counter = 0
    

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()