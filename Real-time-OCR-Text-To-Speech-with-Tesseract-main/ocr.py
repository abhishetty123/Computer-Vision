from ast import While
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 1. Load the image
# img = cv2.imread("book_page.jpg")

cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

while True:
    ret, frame1 = cap.read()
    print(frame1.shape)
# 2. Resize the image
    frame1 = cv2.resize(frame1, None, fx=0.5, fy=0.5)

    # 3. Convert image to grayscale
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # 4. Convert image to black and white (using adaptive threshold)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

    config = "--psm 3"
    Rtext = pytesseract.image_to_string(adaptive_threshold, config=config, lang="eng")
    print(Rtext)
    if Rtext:
        tts=gTTS(text=Rtext,lang="en")
        tts.save("hello.mp3")
        os.system("start hello.mp3")

    cv2.imshow("gray", gray)
    cv2.imshow("adaptive th", adaptive_threshold)
    cv2.imshow("frame1", frame1)
    # cv2.waitKey(0)
    if cv2.waitKey(1) &0XFF == ord('x'):
        break
    
cv2.destroyAllWindows()