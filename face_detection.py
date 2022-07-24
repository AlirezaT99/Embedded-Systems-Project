import cv2

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_face(image, draw_rect=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detected_faces = face_detector.detectMultiScale(gray)
    if draw_rect:
        for (column, row, width, height) in detected_faces:
            cv2.rectangle(
                image,
                (column, row),
                (column + width, row + height),
                (0, 255, 0),
                2
            )
        cv2.imshow('Image', image)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
    if len(detected_faces) > 0:
        return True
    return False


image = cv2.imread('person.jpg')
print(detect_face(image, draw_rect=True))

