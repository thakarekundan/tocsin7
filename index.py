#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import pygame #For playing sound
import time
import cv2
import dlib
import pyautogui
import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
import datetime
def hyber():
    print("hello hyber")
    os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
def shut():
    print("hello shut")
    os.system("shutdown /s /t 1")
def create_resource(ti1,v,inac1,asleep1,fold):
    ti=int(ti1)
    
    inac=int(inac1)
    asleep=int(asleep1)
    #Initialize Pygame and load music
    ft=0
    pygame.mixer.init()
    pygame.mixer.music.load('alert1.mp3')
    
    #Minimum threshold of eye aspect ratio below which alarm is triggerd
    EYE_ASPECT_RATIO_THRESHOLD = 0.3
    
    #Minimum consecutive frames for which eye ratio is below threshold for alarm to be triggered
    EYE_ASPECT_RATIO_CONSEC_FRAMES = 50
    
    #COunts no. of consecutuve frames below threshold value
    COUNTER = 0
    c=0
    b=1
    flag1=True
    global inace
    #Load face cascade which will be used to draw a rectangle around detected faces.
    face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    
    #This function calculates and return eye aspect ratio
    def eye_aspect_ratio(eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
    
        ear = (A+B) / (2*C)
        return ear
    
    #Load face detector and predictor, uses dlib shape predictor file
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    #Extract indexes of facial landmarks for the left and right eye
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
    
    #Start webcam video capture

    
    #Give some time for camera to initialize(not required)
    #time.sleep(2)
    a=1
    while(True):
        video_capture = cv2.VideoCapture(0)
        nowt = datetime.datetime.now()
        nt1=nowt.minute
        newt = nowt + datetime.timedelta(minutes=ti)
        nt2=newt.minute
        print("***********")
        print(nowt,newt)
        print("***********")
        flagg=0
        yy=1
        while(True):

            #Read each frame and flip it, and convert to grayscale
            ret, frame = video_capture.read()
            frame = cv2.flip(frame,1)

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #Detect facial points through detector function
                faces = detector(gray, 0)

                #Detect faces through haarcascade_frontalface_default.xml
                face_rectangle = face_cascade.detectMultiScale(gray, 1.3, 5)

                #Draw rectangle around each face detected
                for (x,y,w,h) in face_rectangle:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

                #Detect facial points

                #print(type(faces))

                if len(faces)==0:
                    COUNTER = 0
                    inacs = datetime.datetime.now()
                    #print(inacs)
                    if flag1:
                        inace = inacs + datetime.timedelta(minutes=inac)
                        inace=inace.minute
                        flag1=False

                    if (inacs.minute>inace and b==1 and flag1==False):
                        pygame.mixer.music.play(-1)
                        b=0
                    print(inacs,inace)
                    if (b==0 and flag1==False and inacs.minute>(inace+1) ):
                        flag1 = True
                        b = 1
                        pygame.mixer.music.stop()
                        pic = pyautogui.screenshot()
                        sour = fold + "screenshot.png"
                        pic.save(sour)
                        ft = 1




                for face in faces:
                    if(b!=1):
                        flag1=True
                        b=1
                        pygame.mixer.music.stop()



                    shape = predictor(gray, face)
                    shape = face_utils.shape_to_np(shape)

                    #Get array of coordinates of leftEye and rightEye
                    leftEye = shape[lStart:lEnd]
                    rightEye = shape[rStart:rEnd]

                    #Calculate aspect ratio of both eyes
                    leftEyeAspectRatio = eye_aspect_ratio(leftEye)
                    rightEyeAspectRatio = eye_aspect_ratio(rightEye)

                    eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2

                    #Use hull to remove convex contour discrepencies and draw eye shape around eyes
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                    #Detect if eye aspect ratio is less than threshold
                    #print(eyeAspectRatio)
                    if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
                        COUNTER += 1
                        #If no. of frames is greater than threshold frames,
                        print(COUNTER,EYE_ASPECT_RATIO_CONSEC_FRAMES)
                        if COUNTER >= EYE_ASPECT_RATIO_CONSEC_FRAMES and COUNTER>=asleep:
                            if (a==1):
                                pygame.mixer.music.play(-1)
                                a=0
                                cv2.putText(frame, "You are Drowsy", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
                        if COUNTER >= EYE_ASPECT_RATIO_CONSEC_FRAMES and COUNTER>= (asleep+20):
                            pic = pyautogui.screenshot()
                            sour=fold+"screenshot.png"
                            pic.save(sour)
                            pygame.mixer.music.stop()
                            ft=1
                            break


                            #time.sleep(10)
                            #os.system('shutdown -s')

                    else:
                        pygame.mixer.music.stop()
                        a=1
                        COUNTER = 0
                if ft==1:
                    break

            cv2.imshow('Video', frame)

            kp = cv2.waitKey(1)
            nt1=datetime.datetime.now().minute
            if(nt2<nt1):
                break
            elif(kp & 0xFF == ord('q')):
                return
        if ft==1:
            video_capture.release()
            cv2.destroyAllWindows()
            pygame.mixer.music.stop()
            break
        else:
            video_capture.release()
            cv2.destroyAllWindows()
            pygame.mixer.music.stop()

            time.sleep(60*ti)

        """nowt = datetime.datetime.now()
            newt = nowt + datetime.timedelta(minutes=ti)
            while(nowt<=newt):
                print("&&&&&&&&&")
                print(datetime.datetime.now(),newt)
                if(cv2.waitKey(1) & 0xFF == ord('q')):
                    flagg=1
                    break """
    if ft==1:

        time.sleep(10)
        if v == "Hybernation":
            hyber()
        else:
            shut()



 #Show video feed
from pynput.keyboard import Key, Controller               
keyboard = Controller()
    #Finally when video capture is over, release the video capture and destroyAllWindows
def dest():
    keyboard.press('q')
    try:  
        if cv2.VideoCapture.isOpened():
            try:
                pygame.mixer.music.stop()
            except:    
                
                time.sleep(5)
                master.destroy()
    except:
        try:
            pygame.mixer.music.stop()     
            master.destroy()
        except:
            master.destroy()


def d_dtcn():
    keyboard.press('q')
    keyboard.release('q')
    master = tk.Tk()
    master.geometry("700x500")
    master.title('Client')
    #master.configure(background="#FBF985")


    canvas=Canvas(master,width=200,height=109)
    image=ImageTk.PhotoImage(Image.open("b1.jpg"))




    canvas.create_image(0,0,anchor=NW,image=image)


    canvas.grid(row=0, column=1,padx=10, pady=10)

    OPTIONS = [
    "Hybernation",
    "Shutdown",
    "Sleep"
    ] #etc
    tk.Label(master, text="System State:",font=("Helvetica", 12)).grid(row=2, column=0)
    variable = tk.StringVar(master)
    variable.set(OPTIONS[0]) # default value

    w = tk.OptionMenu(master, variable, *OPTIONS)
    w.grid(row=2, column=1,padx=10, pady=10)
    e1 = tk.Entry(master)
    e1.insert(END, 15)
    tk.Label(master, text="Camera Frequency(min):",font=("Helvetica", 12)).grid(row=3, column=0)

    e1.grid(row=3, column=1,padx=10, pady=10)
    e2 = tk.Entry(master)
    e2.insert(END, 5)
    tk.Label(master, text="User minimum inactive(min):",font=("Helvetica", 12)).grid(row=4, column=0)
    e2.grid(row=4, column=1,padx=10, pady=10)
    e3 = tk.Entry(master)
    e3.insert(END, 2)
    tk.Label(master, text="Allow Sleep(counter):",font=("Helvetica", 12)).grid(row=5, column=0)
    e3.grid(row=5, column=1,padx=10, pady=10)
    e4 = tk.Entry(master)
    e4.insert(END, 'C:/Users/mahe/Desktop/new/')
    tk.Label(master, text="Video Data Capture Folder:",font=("Helvetica", 12)).grid(row=6, column=0)
    e4.grid(row=6, column=1,padx=10, pady=10)
    tk.Button(master, text='Tocsin 1.o', command=lambda:create_resource(ti=int(e1.get()), v=variable.get(),inac=int(e2.get()),asleep=int(e3.get()),fold=str(e4.get()))).grid(row=7,
                                                                column=1,
                                                                sticky=tk.W,
                                                                padx=10, pady=10)

    #tk.Button(master, text='Tocsin 1.o', command=create_resource).pack(side=TOP, anchor=W, fill=X, expand=YES)
    tk.Button(master, 
            text='Quit',
            command=dest).grid(row=7,column=2,sticky=tk.W,padx=10, pady=10)
    msg = tk.Message(master, text = "Press 'q' for kill the Tocsin 1.o")
    msg.config(bg='lightgreen', font=('times', 12, 'italic'))
    msg.grid()

    """tk.Button(master, 
            text='Quit1',
            command=destt).grid(row=8,column=1,sticky=tk.W,pady=4)"""

    master.bind("<Escape>",lambda q:master.destroy())                       
    master.mainloop()

 



