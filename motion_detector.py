import cv2 , time
from datetime import datetime
import pandas

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=['Start','End'])

video=cv2.VideoCapture(0) #which camera to access,we have only 1 webcam

while True:
    check , frame = video.read()
    status=0

    #print(check) #boolean : checking if the video is working or not
    #print(frame) #numpy array : first image that the video captures

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0) #to remove noise and increase accuracy,(21,21):parameters of blurriness,0 standard deviation

    if first_frame is None :
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray) #Absolute difference between first frame and current frame

    thresh_frame=cv2.threshold(delta_frame, 30 , 255 , cv2.THRESH_BINARY)[1]#for threshold binary we need only second which is the frame #method:cv.THRESH_BINARY  #value more than 30 will get 255 i.e white color
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)  #smooth threshold frame

    (cnts,_)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 15000:
            continue
        status=1

        (x,y,w,h)= cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y) , (x+w , y+h) , (255,0,0) , 3)

    status_list.append(status) #starts with zero as first value is always zero

    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0: #-1:last item,-2=second last item #changed from 1 to 0
        times.append(datetime.now())

    if status_list[-1]==0 and status_list[-2]==1: #changed from 0 to 1
        times.append(datetime.now())



    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)

    #print(gray)
    #print(delta_frame)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

#print(status_list)
print(times)

for i in range(0,len(times),2): #step of 2
    df=df.append({'Start':times[i], 'End':times[i+1]} , ignore_index= True)

df.to_csv("Times.csv")    #exporting dataframe to csv file

video.release()
cv2.destroyAllWindows()
