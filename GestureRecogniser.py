import mediapipe as mp
import cv2
import ctypes
import time

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

video = cv2.VideoCapture(0)

last_action = None
no_gesture_detected = False

print('1 Finger: Pause/Play | 2 Fingers: Skip | Thumbs Up: Increase Volume | Thumbs Down: Decrease Volume')

def control_media(last_action):
    if last_action == "Pointing_Up":
        # Pause media
        print('1 Finger detected, pausing media...')
        ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
    elif last_action == "Victory":
        # Resume media
        print('2 Fingers detected, skipping...')
        ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
    elif last_action == "Thumb_Up":
        print('Increasing volume...')
        for _ in range(10):
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
        #time.sleep(5)
        #ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0) #release volume up key
        #print('Increased volume')

    elif last_action == "Thumb_Down":
        print('Decreasing volume...')
        for _ in range(10):
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0) #press volume down key
        #time.sleep(5)
        #ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0) #release volume down key
        #print('Decreased volume')
        

    

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):

    global last_action
    global no_gesture_detected

    if result.gestures != []:

        recognised_gesture = result.gestures[0][0].category_name

        #if gesture is not the same as the previous, update it and print the new gesture
        if recognised_gesture != last_action:

            #new gesture was detected
            last_action = recognised_gesture
            
            control_media(last_action)

            print(last_action)
            no_gesture_detected = False

    else:
        if not no_gesture_detected:
            print('No known gesture detected')
            no_gesture_detected = True

    #print(result.gestures)
    #if result.gestures == []:
    #    print('No gesture recognised')
    #else:
    #    category_name = result.gestures[0][0].category_name

    #    print(category_name)


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:

    while video.isOpened(): 
        #capture video stream frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        #send video stream data to perform gesture recognition
        recognizer.recognize_async(mp_image, timestamp)

        if cv2.waitKey(1) == 27:  # 27 is the ASCII value for Esc (currently doesnt work)
            break

video.release()
cv2.destroyAllWindows()