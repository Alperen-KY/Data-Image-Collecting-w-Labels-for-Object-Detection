import os
import cv2
import time
import serial
import string
import random
import numpy as np
import importlib.util
from threading import Thread
import random_name_generator as rng
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tflite_runtime.interpreter import Interpreter


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

os.mkdir(r'/home/pi/Pictures/dataset_deneme')
#------------------------------------------------------------------------------------------------------------------------------------
# Below code does the authentication
# part of the code
gauth = GoogleAuth()
print(GoogleDrive)
# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)



path = r"/home/pi/Pictures/dataset_deneme"

folder_id = '1Fml8hWKmOpCjQcS7k5T4rNW8Nmbp0iy7'

os.listdir(path)


def uplooda():
    # iterating thought all the files/folder
    # of the desired directory
    for x in os.listdir(path):
        sub_direc = path + '/' + x
        file5 = drive.CreateFile({'title': x,
                                "parents" : [{"kind" : "drive#fileLink", "id" : '1Fml8hWKmOpCjQcS7k5T4rNW8Nmbp0iy7'}]})
        file5.SetContentFile(sub_direc)
        file5.Upload()
    file5 = None
    
#-----------------------------------------------------------------------------------------------------------------------------------




#arduino initializing
# ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 5)
# pos = 90
# pos2 = str(pos)
# ser.write(bytes(pos2, encoding="ascii"))
#-----------------------------------------------------------------------------------------------------------------------------------
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#-----------------------------------------------------------------------------------------------------------------------------------
veri = list()
veri.append('<annotation>\n')#0
veri.append('\t<folder>drive</folder>\n')#1
veri.append('\t<filename>2.30 M Genislik 75.png</filename>\n')#2
veri.append('\t<path>YOUR PATH.png</path>\n')#3
veri.append('\t<source>\n')#4
veri.append('\t\t<database>Epsilon</database>\n')#5
veri.append('\t</source>\n')#6
veri.append('\t<size>\n')#7
veri.append('\t\t<width>640</width>\n')#8
veri.append('\t\t<height>480</height>\n')#9
veri.append('\t\t<depth>3</depth>\n')#10
veri.append('\t</size>\n')#11
veri.append('\t<segmented>0</segmented>\n')#12
veri.append('\t<object>\n')#13
veri.append('\t\t<name>2.30 M Genislik</name>\n')#14
veri.append('\t\t<pose>Unspecified</pose>\n')#15
veri.append('\t\t<truncated>1</truncated>\n')#16
veri.append('\t\t<difficult>0</difficult>\n')#17
veri.append('\t\t<bndbox>\n')#18
veri.append('\t\t\t<xmin>1</xmin>\n')#19
veri.append('\t\t\t<ymin>1</ymin>\n')#20
veri.append('\t\t\t<xmax>32</xmax>\n')#21
veri.append('\t\t\t<ymax>32</ymax>\n')#22
veri.append('\t\t</bndbox>\n')#23
veri.append('\t</object>\n')#24
veri.append('</annotation>\n')#25

def label_xml(detections,width,height,xmin,ymin,xmax,ymax,name):
    label = detections
    
    with open(r'/home/pi/Pictures/dataset_deneme/{}'.format(name) + '.xml', "w+") as f:
        f.seek(0)
        veri[2] = '\t<filename>{}.png</filename>\n'.format(label)
        veri[3] = '\t<path>YOUR PATH{}.png</path>\n'.format(label)
        veri[8] = '\t\t<width>{}</width>\n'.format(width)
        veri[9] = '\t\t<height>{}</height>\n'.format(height)
        veri[14] = '\t\t<name>{}</name>\n'.format(label)
        veri[19] = '\t\t\t<xmin>{}</xmin>\n'.format(xmin)
        veri[20] = '\t\t\t<ymin>{}</ymin>\n'.format(ymin)
        veri[21] = '\t\t\t<xmax>{}</xmax>\n'.format(xmax)
        veri[22] = '\t\t\t<ymax>{}</ymax>\n'.format(ymax)
        f.writelines(veri)
        f.close()
#---------------------------------------------------------------------------------------------------------------------------------



cap = cv2.VideoCapture(1)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



MODEL_NAME = 'my_tflite_model'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'
min_conf_threshold = 0.6
imW, imH = 640, 480
use_TPU = 'store_true'

input_mean = 127.5
input_std = 127.5

# Get path to current working directory
CWD_PATH = os.getcwd()
# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)
# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

if labels[0] == '???':
    del(labels[0])
    
# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

#print(input_details[:])
print(output_details[0]['index'])
print(interpreter.get_tensor(output_details[0]['index'])[0][0], '\n')

print(output_details[1]['index'])
print(interpreter.get_tensor(output_details[1]['index'])[0][0], '\n')

print(output_details[2], '\n')


floating_model = (input_details[0]['dtype'] == np.float32)



# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()



ymin = 0
xmin = 0
ymax = 0
xmax = 0

med_hght = imH / 2
med_wdth = imW / 2

while True:
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()
    
    # Grab frame from video stream
    ret, frame = cap.read()
    
    # Resize frame to expected shape [1xHxWx3]
    frame_resized = cv2.resize(frame, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)
    
    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std
    
    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()
    
    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0][0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0][0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0][0] # Confidence of detected objects
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
    
    
    

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    if ((scores > min_conf_threshold) and (scores <= 1.0)):
        
        # Get bounding box coordinates and draw box
        # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
        ymin = int(max(1,(boxes[0] * imH)))
        xmin = int(max(1,(boxes[1] * imW)))
        ymax = int(min(imH,(boxes[2] * imH)))
        xmax = int(min(imW,(boxes[3] * imW)))
        
#------------------------------------------------------------------------------------------------------------------
        #Dataset her dosya için random isim olusturma
        rand_name_file = id_generator()
        #dataset icin label dosyası olusturma ve kaydetme _______  /home/pi/Pictures/dataset_deneme
        label_xml(labels[int(classes)],640,480,xmin,ymin,xmax,ymax,rand_name_file)
        #dataset icin foto kaydetme _______  /home/pi/Pictures/dataset_deneme
        cv2.imwrite(r"/home/pi/Pictures/dataset_deneme/{}.png".format(rand_name_file), frame)
        print('\n',labels[int(classes)])
        
#------------------------------------------------------------------------------------------------------------------


        
        
        cv2.line(frame, (int((xmax-xmin)/2)+xmin, 0), (int((xmax-xmin)/2)+xmin, 480), (0, 255, 0), 2)
        cv2.line(frame, (640, int((ymax-ymin)/2)+ymin), (0, int((ymax-ymin)/2)+ymin), (0, 255, 0), 2)
            
            
        cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
        
        
            
            # Draw label
        object_name = labels[int(classes)] # Look up object name from "labels" array using class index
        label = '%s: %d%%' % (object_name, int(scores*100)) # Example: 'person: 72%'
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
        label_ymin = max(ymin, labelSize[0]) # Make sure not to draw label too close to top of window
        cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
        cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
        
        
        

    # Draw framerate in corner of frame
    cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
         
    
    #frame = cv2.resize(frame, None, None, fx=1.2, fy=1.2)
    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('object detection', frame)


    
    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1 
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break


uplooda()

import shutil
shutil.rmtree("/home/pi/Pictures/dataset_deneme")
    


    
    
