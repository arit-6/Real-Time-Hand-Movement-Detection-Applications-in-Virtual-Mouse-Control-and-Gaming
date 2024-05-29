import cv2
import mediapipe as mp
import pyautogui
import numpy as np

video = cv2.VideoCapture(0)
frame_width = 1280  
frame_height = 720 
video.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

handGesture = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawingTools = mp.solutions.drawing_utils
screenWidth, screenHeight = pyautogui.size()

canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  
drawing = False  

sensitivity = 2  
scale_factor = 2  
run = True
frame_count = 0
skip_frames = 1  

while run:
    _, frame = video.read()
    frame = cv2.flip(frame, 1)
    frameHeight, frameWidth, _ = frame.shape
    
    if frame_count % skip_frames == 0:
        rgbConvertedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = handGesture.process(rgbConvertedFrame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                if not drawing:
                    canvas[:] = 0  
                drawingTools.draw_landmarks(canvas, hand, mp.solutions.hands.HAND_CONNECTIONS,
                                            landmark_drawing_spec=drawingTools.DrawingSpec(color=(255, 0, 255), thickness=5, circle_radius=1))
                landmarks = hand.landmark
                all_fingers_closed = True
                for id, landmark in enumerate(landmarks):
                    if id == 6:
                        y_base = landmark.y * frameHeight
                    elif id == 8:
                        y_tip = landmark.y * frameHeight
                        if y_tip < y_base:
                            x = int(landmark.x * frameWidth)
                            y = int(y_tip)
                            mousePositionX = screenWidth * x / (frame_width * scale_factor)
                            mousePositionY = screenHeight * y / (frame_height * scale_factor)
                            pyautogui.moveTo(mousePositionX * sensitivity, mousePositionY * sensitivity)
                        elif y_tip > y_base:
                            if all_fingers_closed:
                                pyautogui.click()
                        
    canvas_resized = cv2.resize(canvas, (frame_width, frame_height))  
    cv2.imshow('Virtual Mouse', frame + canvas_resized)  
    frame_count += 1
    
    key = cv2.waitKey(1)
    if key == ord('x'):  
        break

video.release()
cv2.destroyAllWindows()
