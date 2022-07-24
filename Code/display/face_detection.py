import cv2

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def face_detected(image, detector):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detected_faces = detector.detectMultiScale(gray)
    return len(detected_faces) > 0
