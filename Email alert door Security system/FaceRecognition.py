import cv2
import numpy as np;
#import xlwrite
#import firebase_admin
#import firebase as Firebase;
#import firebase.firebase_ini as fire;
#import firebase_ini
import time
import sys
# from playsound import playsound

# import mysql.connector
# mydb = mysql.connector.connect(host = "localhost",user ="root",password ="Abhishetty1719", database = "attendance")
# mycursor = mydb.cursor()
try:
    time.sleep(1)
    start = time.time()
    period = 15
    face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0);
    recognizer = cv2.face.LBPHFaceRecognizer_create();
    recognizer.read('trainer.yml');
    flag = 0;
    uknwn = 0;
    counter = 0;
    id = 0;
    filename = 'filename';
    dict = {
        'item1': 1
    }
    #font = cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 5, 1, 0, 1, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        
        ret, img = cap.read();
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        faces = face_cas.detectMultiScale(gray, 1.3, 7);
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2);
            id, conf = recognizer.predict(roi_gray)
            if (conf < 50):
                if (id == 1):
                    id = 'Debashis'
                    print ("D1one")
                    cap.release();
                    cv2.destroyAllWindows();
                    
                    
                    if ((str(id)) not in dict):
                        # filename = xlwrite.output('attendance', 'class1', 1, id, 'yes');
                        # dict[str(id)] = str(id);
                        # mycursor.execute('INSERT INTO persons(PersonID, \
                        #         LastName,FirstName, Address )' \
                        #         'VALUES(1, "Shetty", "AAA", "Mangal ore")')
                        # mydb.commit()
                        # mycursor.close()
                        print ("D1one")
                        

                elif (id == 2):
                    id = 'Bipodtaran'
                    # if ((str(id)) not in dict):
                    #     # # filename = xlwrite.output('attendance', 'class1', 2, id, 'yes');
                    #     # # dict[str(id)] = str(id);
                    #     # mycursor.execute('INSERT INTO persons(PersonID, \
                    #     #         LastName,FirstName, Address )' \
                    #     #         'VALUES(1, "boss", "vickas", "Mangalore")')
                    #     # mydb.commit()
                    #     # mycursor.close()
                    #     print ("Done")

                elif (id == 3):
                    id = 'Chandana'
                    # if ((str(id)) not in dict):
                    #     # filename = xlwrite.output('attendance', 'class1', 3, id, 'yes');
                    #     # dict[str(id)] = str(id)
                    #     # mycursor.execute('INSERT INTO persons(PersonID, \
                    #     #         LastName,FirstName, Address )' \
                    #     #         'VALUES(1, "kutty", "Dhanraj", "Mangalore")')
                    #     # mydb.commit()
                    #     # mycursor.close()
                    #     print ("Done")
                
            else:
                id = 'Unknown, can not recognize'
                flag = flag + 1
                print("inknown")
                uknwn = uknwn + 1
                if uknwn == 2:
                    print("hello")
                     #mail function and message is unknown face detetcted
               
                
            print("bcjhdh")
            cv2.putText(img, str(id) + " " + str(conf), (x, y - 10), font, 0.55, (120, 255, 120), 1)
            # cv2.cv.PutText(cv2.cv.fromarray(img),str(id),(x,y+h),font,(0,0,255));
        counter = counter + 1;
        time.sleep(1)
        # print (counter)
        cv2.imshow('frame', img);
        # cv2.imshow('gray',gray);
        # if flag == 10:
        #     playsound('transactionSound.mp3')
        #     print("Transaction Blocked")
        #     break;

        if time.time() > start + period:
            break;
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break;
        if counter == 10:
            #mail send function
            print("counter is done")
            #mail function and message is no face detetcted
            break;
    cap.release();
    cv2.destroyAllWindows();
except:
    KeyboardInterrupt()