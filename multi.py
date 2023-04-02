import cv2
import pytesseract
from pytesseract import Output
import concurrent.futures

import datetime

start = datetime.datetime.now()

# Replace this with the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set video file path (replace with your own path)
video_file = "video.mkv"

# Replace with the text you want to find
TARGET_TEXT = "Viktor"

# Define the region of interest (x, y, width, height)
x, y, w, h = 519, 823, 867, 182

# Open the video file
cap = cv2.VideoCapture(video_file)

# Set the video capture object to the desired time
fps = int(cap.get(cv2.CAP_PROP_FPS))

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_step = 60  # Step size to get one frame per second


def process_frame(frame):
    roi = frame[y:y + h, x:x + w]

    text_data = pytesseract.image_to_data(roi, output_type=Output.DICT, config="--psm 6")

    for text in text_data["text"]:
        if TARGET_TEXT.lower() in text.lower():
            cv2.imshow('Current Frame', frame)
            cv2.waitKey(5000)
            return True
    return False


# Read the required frames into memory
batchsize = 30
frames = []
checked_frames = 0
checked_frame = 0
for frame_index in range(0, total_frames, frame_step):
    if frame_index < 56000:
        continue
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    # print(f'Loading Frame {frame_index}')
    if not ret:
        break
    checked_frame += 1
    frames.append(frame)

    if len(frames) == batchsize:
        print(checked_frame)
        found = False
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_frame, frames)

            for frame_index, result in enumerate(results):

                if result:
                    found = True


                    print(frame_index)


                    new_frame_index = frame_index

                    print(new_frame_index)

                    frame_index = frame_index

                    found_frame = (frame_index + checked_frames) * frame_step

                    current_time = found_frame / fps
                    minutes, seconds = divmod(current_time, 60)
                    hours, minutes = divmod(minutes, 60)

                    print(f"Found '{TARGET_TEXT}' at {int(hours)}:{int(minutes)}:{int(seconds)}")


                    end = datetime.datetime.now()

                    print(end - start)

            checked_frames = checked_frames + 30
            frames = []

cap.release()

"""if found:
    current_time = found_frame / fps
    minutes, seconds = divmod(current_time, 60)
    hours, minutes = divmod(minutes, 60)

    print(f"Found '{TARGET_TEXT}' at {int(hours)}:{int(minutes)}:{int(seconds)}")"""

end = datetime.datetime.now()

print(end - start)
