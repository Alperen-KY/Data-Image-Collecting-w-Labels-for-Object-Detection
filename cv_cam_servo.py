import cv2
import time
import serial
import numpy as np

ser = serial.Serial('/dev/ttyACM3', 9600, timeout = 5)

ser.write(b"90")

cap = cv2.VideoCapture(0)
# Set camera resolution
cap.set(3, 1920)
cap.set(4, 1080)
_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
center = int(cols / 2)
position = 90 # degrees

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x + w) / 2)
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)        
        
        break
    
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    # Move servo motor
    if x_medium < center -30:
        position += 1
        pos2 = str(position)
#        ser.write(bytes(pos2, encoding="utf-8"))
#         time.sleep(0.5)
        ser.write(b"0")

        
    elif x_medium > center + 30:
        position -= 1
        pos2 = str(position)
#         ser.write(bytes(pos2, encoding="utf-8"))
#         time.sleep(0.5)
        ser.write(b"180")

    
    
    
    
    
    cv2.imshow("red_mask", red_mask)
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(60)
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()














