import traceback
import cv2

window_name = "livestream"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)   
capture = cv2.VideoCapture("http://192.168.1.105:3456/video")
img = cv2.imread('bg.jpg')

def check_distance() -> bool:
    '''
    check the distance to decide to show background or video feed
    if distance is short return True
    '''
    pressedKey = cv2.waitKey(1) & 0xFF # temporary for checking
    if pressedKey == 32:
        return True
    return False

while(True):
    try:
        if not check_distance():
            cv2.imshow(window_name, img)
        else:
            ret, frame = capture.read()
            cv2.putText(img=frame, text="Hello World", org=(100, 200), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 0, 0), thickness=2)
            cv2.imshow(window_name, frame)
    except Exception:
        traceback.print_exc()
        break
    
capture.release()
cv2.destroyAllWindows()