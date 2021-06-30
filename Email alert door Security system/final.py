import face_recognition
# from PIL import Image, ImageDraw
import cv2
import numpy as np
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
import time
try:
    def mailsend():       
        subject = "An email with attachment from Python"
        body = "This is an email with attachment sent from Python"
        sender_email = "abhilashshetty1719@gmail.com"
        receiver_email = "theecstudent1719@gmail.com"
        password = "*************"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = "ram.jpg"  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)


    def facedetect():
        video_capture = cv2.VideoCapture(0)

        # Load a sample picture and learn how to recognize it.
        sanjay_image = face_recognition.load_image_file("shetty.jpg")
        sanjay_face_encoding = face_recognition.face_encodings(sanjay_image)[0]
        counter = 0
        lock = 0
        # # Load a second sample picture and learn how to recognize it.
        # rishab_image = face_recognition.load_image_file("Rishab.jpg")
        # rishab_face_encoding = face_recognition.face_encodings(rishab_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            sanjay_face_encoding
        ]
        known_face_names = [
            "Sanjay",
            # "Rishab"
        ]

        while True:
            ret, frame = video_capture.read()
            rgb_frame = frame[:, :, ::-1]
        # Find all the faces and face encodings in the unknown image
            face_locations = face_recognition.face_locations(rgb_frame) # Find all the faces and face encodings in the current frame of video. face_locations = face_recognition.face_locations
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # pil_image = Image.fromarray(unknown_image)
            # draw = ImageDraw.Draw(pil_image)

            # Loop through each face found in the unknown image
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "randoName"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255),cv2.FILLED)
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255),1)
                if name != "randoName":
                    print(name, "was there")
                    video_capture.release()
                    cv2.destroyAllWindows() 
                    
                else:
                    print("random guy")
                    cv2.imwrite("ram.jpg",frame)
                    lock = lock+1
                    if lock == 3:
                        mailsend()
                        video_capture.release()
                        cv2.destroyAllWindows() 



            cv2.imshow('video', frame)
            counter = counter + 1
            if counter == 100:
                print("no face detected")
                cv2.imwrite("ram.jpg",frame)
                mailsend()
                break

            print(counter)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()   
            # # Draw a box around the face using the Pillow module
            # draw.rectangle(((left, top), (right, bottom)), outline=(48, 63, 159)) 

            # # Draw a label with a name below the face
            # text_width, text_height = draw.textsize(name)
            # draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(48, 63, 159), outline=(48, 63, 159))
            # draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 0))


        # Remove the drawing library from memory as per the Pillow docs
        # del draw

        # pil_image.show()

        # You can also save a copy of the new image to disk if you want by uncommenting this line
        # pil_image.save("image_with_boxes.jpg")
############################### Motion detection code ######################################
    cap = cv2.VideoCapture(0)
    frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    # x = datetime.datetime.now()
    out = cv2.VideoWriter(('outrer.avi'), fourcc, 5.0, (1280,720))


    while True:
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        print(frame1.shape)
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=0)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 900:
                continue
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)

            ret,frame3 = cap.read()
            
            cv2.imshow("My cam video", frame3)
            facedetect()
            break
            # output.write(frame3)
            
        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        # image = cv2.resize(frame3, (1280,720))
        # out.write(image)
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(1) &0XFF == ord('x'):
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()
except:    
    print("done")
