# Imports
import cv2
import time
import mediapipe as mp

# Create Mediapipe hands and drawing objects
mp_hands = mp.solutions.hands.Hands()
mp_drawing = mp.solutions.drawing_utils

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

def detect_hand_landmarks(frame):
    # Convert the frame to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    results = mp_hands.process(frame_rgb)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmark_points = []
            # Iterate through each hand landmark
            for landmark in hand_landmarks.landmark:
                # Extract the landmark coordinates
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                landmark_points.append((x, y))

                # Draw a circle on the landmark position
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

           # Draw bone structure lines
            connections = [[0, 1], [1, 2], [2, 3], [3, 4],  # Thumb
                           [0, 5], [5, 6], [6, 7], [7, 8],  # Index finger
                           [0, 9], [9, 10], [10, 11], [11, 12],  # Middle finger
                           [0, 13], [13, 14], [14, 15], [15, 16],  # Ring finger
                           [0, 17], [17, 18], [18, 19], [19, 20], # Pinkie finger
                           [5, 9], [9, 13], [13, 17]] # Knuckle line

            for connection in connections:
                start_index, end_index = connection
                start_point = landmark_points[start_index]
                end_point = landmark_points[end_index]
                cv2.line(frame, start_point, end_point, (0, 0, 255), 2)
    return frame

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

        frame_landmarks = detect_hand_landmarks(frame)

        # Display FPS counter on the stream window
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display Esc exit button text
        cv2.putText(frame, 'Press Esc to exit', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the video frame
        cv2.imshow('Camera Stream', frame_landmarks)

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
    
