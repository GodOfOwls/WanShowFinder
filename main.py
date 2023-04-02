import cv2
import pytesseract
from pytesseract import Output
import re
import timeit
import datetime


start = datetime.datetime.now()

# Replace this with the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set video file path (replace with your own path)
video_file = "video.mkv"

# Replace with the text you want to find
TARGET_TEXT = "John"

# Define the region of interest (x, y, width, height)
x, y, w, h = 519, 823, 867, 182

# Open the video file
cap = cv2.VideoCapture(video_file)

# Set the video capture object to the desired time
fps = int(cap.get(cv2.CAP_PROP_FPS))

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_step = 60  # Step size to get one frame per second

for frame_index in range(0, total_frames, frame_step):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()

    print(f"Checking frame {frame_index}")

    if not ret:
        break

    # Display the current frame
    # cv2.imshow('Current Frame', frame)
    # cv2.waitKey(5)



    # Crop the frame to the region of interest
    roi = frame[y:y+h, x:x+w]

    # Perform OCR on the region of interest
    text_data = pytesseract.image_to_data(roi, output_type=Output.DICT, config="--psm 6")

    # Check if the target text is found
    found = False
    for text in text_data["text"]:
        if TARGET_TEXT.lower() in text.lower():
            found = True
            break

    if found:
        # Calculate the current timestamp in the video
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_time = current_frame / fps
        minutes, seconds = divmod(current_time, 60)
        hours, minutes = divmod(minutes, 60)

        # Print the timestamp and alert message
        print(f"Found '{TARGET_TEXT}' at {int(hours)}:{int(minutes)}:{int(seconds)}")
        break


end = datetime.datetime.now()

print(end - start)

# Close the window and release the video capture object
cv2.destroyAllWindows()
cap.release()
