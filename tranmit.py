import os
import pytesseract
import moviepy
import cv2


# Input file path
input_file_path = r'D:\CDP\download.jpg'

# Output file path
output_file_path = r'D:\CDP\output.txt'

# Get the file extension
file_extension = os.path.splitext(input_file_path)[1]
print(file_extension)


# Read the input file and convert to text
if file_extension == ".txt":
    with open(input_file_path, "r") as input_file:
        text = input_file.read()

elif file_extension in [".jpg", ".png", ".bmp"]:
    pytesseract.pytesseract.tesseract_cmd = r'C:\users\lasit\appdata\local\programs\python\python311\lib\site-packages'
    img = cv2.imread(input_file_path)
    text = pytesseract.image_to_string(img)
    print(text)

elif file_extension in [".mp4", ".avi", ".mov"]:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    video = VideoFileClip(input_file_path)
    audio = video.audio
    audio.write_audiofile("temp.wav")
    text = pytesseract.image_to_string("temp.wav")

# Write the output file
with open(output_file_path, "w") as output_file:
    output_file.write(text)