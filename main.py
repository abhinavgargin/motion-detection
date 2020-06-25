from flask import Flask, render_template 
# importing datetime class from datetime library 
from datetime import datetime 
import cv2, time, pandas 
from flask_cors import CORS
app = Flask(__name__) 
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
  
@app.route("/") 
def index(): 
   static_back = None

   # List when any moving object appear 
   motion_list = [ None, None ] 

   # Time of movement 
   time = [] 

   # Initializing DataFrame, one column is start 
   # time and other column is end time 
   df = pandas.DataFrame(columns = ["Start", "End"]) 

   # Capturing video 
   video = cv2.VideoCapture('test.webm') 

   # Infinite while loop to treat stack of image as video 
   fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
   while True: 
   # Reading frame(image) from video 
      check, frame = video.read() 
      fgmask = fgbg.apply(frame)

   # Initializing motion = 0(no motion) 
      motion = 0

      thresh_frame = fgmask
      if type(thresh_frame) == type(None):
         break
# Finding contour of moving object 
      cnts,_ = cv2.findContours(thresh_frame.copy(), 
         cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

      for contour in cnts: 
         if cv2.contourArea(contour) < 10000: 
            continue
         motion = 1

         (x, y, w, h) = cv2.boundingRect(contour) 
   # making green rectangle arround the moving object 
         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 

   # Appending status of motion 
      motion_list.append(motion)
   #print(motion_list) 

      motion_list = motion_list[-2:] 
   #print(motion_list)

   # Appending Start time of motion 
      if motion_list[-1] == 1 and motion_list[-2] == 0: 
         time.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000) 
   #print("Start time: " , time)

   # Appending End time of motion 
      if motion_list[-1] == 0 and motion_list[-2] == 1: 
         time.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000) 
   #print("End time :" , time)

      #cv2.imshow("Threshold Frame", thresh_frame) 

   # Displaying color frame with contour of motion of object 
      #cv2.imshow("Color Frame", frame) 

      key = cv2.waitKey(1) 
   # if q entered whole process will stop 
      if key == ord('q'): 
   # if something is movingthen it append the end time of movement 
         if motion == 1: 
            time.append(datetime.now()) 
            print("last")
         break

   # Appending time of motion in DataFrame 
   for i in range(0, len(time), 2): 
      df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True) 

   # Creating a CSV file in which time of movements will be saved 
   df.to_csv("Time_of_movements.csv") 

   video.release() 

   # Destroying all the windows 
   cv2.destroyAllWindows()
   return df
 


if __name__ == '__main__': 
   app.run(debug = True) 