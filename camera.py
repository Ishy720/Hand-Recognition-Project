# Imports

import cv2
import time

# Functions

def find_device_camera_index():
    for index in range(10):
        try:
            capture_device_port_location = cv2.VideoCapture(index)
            if capture_device_port_location.isOpened():
                #print(f"Camera device found at index {index}")
                capture_device_port_location.release()
                return index
        except cv2.error as e:
            print(f"Error occurred while opening camera at index {index}: {str(e)}")

    #print("No camera device was located on the computer")
    return None


def display_camera_stream(cam_index):

    # Open video stream from found camera device
    video_stream = cv2.VideoCapture(cam_index)

    # Get initial time to determine FPS
    start_time = time.time()
    num_frames = 0

    
    while True:
        # Read each frame from the camera stream
        ret, frame = video_stream.read()

        # Calculate FPS
        num_frames += 1
        elapsed_time = time.time() - start_time
        fps = num_frames / elapsed_time

        # Display FPS counter on the stream window
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display Esc exit button text
        cv2.putText(frame, 'Press Esc to exit', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the video frame
        cv2.imshow('Camera Stream', frame)

        # Terminate if Esc is pressed
        if cv2.waitKey(1) == 27:  # 27 is the ASCII value for Esc
            break

    # Stop using the camera and close windows
    video_stream.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    # Locate camera device on computer
    camera_device_index_location = find_device_camera_index()

    # Display video stream from camera device
    display_camera_stream(camera_device_index_location)
    
