import os
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter import messagebox

directories = ['TrainingImage', 'StudentDetails', 'ImagesUnknown', 'TrainingImageLabel', 'Attendance']
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
#create directories if directories are missing or not found
        
window = tk.Tk()
window.title("Face Recognition Attendance System")
window.geometry("800x600")
window.configure(background='#E1EFFF')
window.attributes('-fullscreen', False)  # Ensure windowed mode
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))  # Set window size to screen resolution


lbl_title = tk.Label(window, text="Face Recognition Attendance System", bg="#0080FF", fg="white",
                     font=('times', 24, 'bold'))
lbl_title.pack(pady=20)

frame_entries = tk.Frame(window, bg="#E1EFFF")
frame_entries.pack(pady=10)

lbl_id = tk.Label(frame_entries, text="Enter ID:", font=('times', 16), bg="#E1EFFF")
lbl_id.grid(row=0, column=0, padx=10)

txt = tk.Entry(frame_entries, width=20, font=('times', 16))
txt.grid(row=0, column=1, padx=10)

lbl_name = tk.Label(frame_entries, text="Enter Name:", font=('times', 16), bg="#E1EFFF")
lbl_name.grid(row=1, column=0, padx=10)

txt2 = tk.Entry(frame_entries, width=20, font=('times', 16))
txt2.grid(row=1, column=1, padx=10)

lbl_notification = tk.Label(window, text="Notification:", font=('times', 16), bg="#E1EFFF")
lbl_notification.pack(pady=10)

message = tk.Label(window, text="", font=('times', 16), bg="#E1EFFF", fg="red")
message.pack()

lbl_attendance = tk.Label(window, text="Attendance:", font=('times', 16), bg="#E1EFFF")
lbl_attendance.pack(pady=10)

message2 = tk.Label(window, text="", font=('times', 16), bg="#E1EFFF", fg="green")
message2.pack()
 
def clear():
        txt.delete(0, 'end')
        txt2.delete(0, 'end')
        message.config(text="")
    
def quit_application():
    answer = messagebox.askquestion("Quit", "Are you sure you want to quit?")
    if answer == "yes":
        window.destroy()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    
    # Load the CSV file to DataFrame
    csv_file_path = "StudentDetails\StudentDetails.csv"
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        messagebox.showerror("Error", "StudentDetails.csv not found!")
        return
    
    attendance = pd.DataFrame(columns=['Id', 'Name', 'Date', 'Time'])

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    save_interval = 60  # Save attendance every 60 seconds
    last_save_time = time.time()

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                # Check if Id exists in the DataFrame
                if Id in df['Id'].values:
                    aa = df.loc[df['Id'] == Id, 'Name'].values[0]
                else:
                    aa = 'Unknown'
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                aa = str(Id)

            if conf > 75:
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])

            cv2.putText(im, str(aa), (x, y + h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

        cv2.imshow('im', im)

        current_time = time.time()
        if current_time - last_save_time >= save_interval:
            # Debug print statements
            print("Saving attendance...")
            print("Attendance DataFrame:")
            print(attendance.head())

            # Save attendance to CSV file
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance\Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
            attendance.to_csv(fileName, index=False)
            print("Attendance recorded successfully!")
            last_save_time = current_time

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    res = attendance
    message2.configure(text=res)

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    
    # Load the CSV file to DataFrame
    csv_file_path = "StudentDetails\StudentDetails.csv"
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        messagebox.showerror("Error", "StudentDetails.csv not found!")
        return
    
    attendance = pd.DataFrame(columns=['Id', 'Name', 'Date', 'Time'])

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    save_interval = 60  # Save attendance every 60 seconds
    last_save_time = time.time()



    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                # Check if Id exists in the DataFrame
                if Id in df['Id'].values:
                    aa = df.loc[df['Id'] == Id, 'Name'].values[0]
                else:
                    aa = 'Unknown'
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                aa = str(Id)

            if conf > 75:
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])

            cv2.putText(im, str(aa), (x, y + h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

        cv2.imshow('im', im)

        current_time = time.time()
        if current_time - last_save_time >= save_interval:
            # Save attendance to CSV file
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance\Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
            attendance['Time'] = timeStamp  # Update the 'Time' column with current timeStamp
            attendance.to_csv(fileName, index=False)
            print("Attendance recorded successfully!")
            last_save_time = current_time


        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    res = attendance
    message2.configure(text=res)


frame_buttons = tk.Frame(window, bg="#E1EFFF")
frame_buttons.pack(pady=20)

clearButton = tk.Button(frame_buttons, text="Clear", command=clear, font=('times', 16),
                        bg="#FF4500", fg="white", width=15, height=2, activebackground="#FF6347")
clearButton.grid(row=0, column=0, padx=10)

takeImgButton = tk.Button(frame_buttons, text="Take Images", command=TakeImages, font=('times', 16),
                          bg="#008000", fg="white", width=15, height=2, activebackground="#32CD32")
takeImgButton.grid(row=1, column=0, padx=10)

trainImgButton = tk.Button(frame_buttons, text="Train Images", command=TrainImages, font=('times', 16),
                           bg="#008000", fg="white", width=15, height=2, activebackground="#32CD32")
trainImgButton.grid(row=1, column=1, padx=10)

trackImgButton = tk.Button(frame_buttons, text="Track Images", command=TrackImages, font=('times', 16),
                           bg="#008000", fg="white", width=15, height=2, activebackground="#32CD32")
trackImgButton.grid(row=1, column=2, padx=10)

quitButton = tk.Button(frame_buttons, text="Quit", command=quit_application, font=('times', 16),
                       bg="#FF4500", fg="white", width=15, height=2, activebackground="#FF6347")
quitButton.grid(row=0, column=1, padx=10)

window.mainloop()

