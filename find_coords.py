import cv2

# Mouse callback function to draw a rectangle and save the coordinates
def draw_rectangle(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x_end, y_end = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_end, y_end = x, y

# Set video file path (replace with your own path)
video_file = "video.mkv"

# Input the time in hh:mm:ss format
time_str = input("Enter the time (hh:mm:ss) to extract the frame: ")

# Convert the time string to seconds
hours, minutes, seconds = map(int, time_str.split(':'))
time_seconds = 3600 * hours + 60 * minutes + seconds

# Initialize variables for rectangle drawing
x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False

# Open the video file
cap = cv2.VideoCapture(video_file)

# Set the video capture object to the desired time
cap.set(cv2.CAP_PROP_POS_MSEC, time_seconds * 1000)

# Read the frame at the specified time
ret, frame = cap.read()

if not ret:
    print("Error reading the video file.")
    cap.release()
else:
    # Create a window and set the mouse callback function
    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", draw_rectangle)

    while True:
        # Display the frame with the rectangle drawn
        frame_with_rectangle = frame.copy()
        cv2.rectangle(frame_with_rectangle, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
        cv2.imshow("Video", frame_with_rectangle)

        # Press 'q' to exit the loop and save the coordinates
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Calculate the width and height of the selected area
    width, height = abs(x_end - x_start), abs(y_end - y_start)

    print(f"Selected area coordinates and dimensions: x={x_start}, y={y_start}, width={width}, height={height}")
