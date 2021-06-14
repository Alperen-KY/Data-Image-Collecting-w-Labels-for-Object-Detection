from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

#------------------------------------------------------------------------------------------------------------------------------------
# Below code does the authentication
# part of the code
gauth = GoogleAuth()
print(GoogleDrive)
# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)


path = r"/home/pi/Pictures"

folder_id = '1Fml8hWKmOpCjQcS7k5T4rNW8Nmbp0iy7'

os.listdir(path)

# def uplooda():
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

veri = list()
veri.append('<annotation>\n')#0
veri.append('\t<folder>drive</folder>\n')#1
veri.append('\t<filename>2.30 M Genislik 75.png</filename>\n')#2
veri.append('\t<path>YOUR PATH.png</path>\n')#3
veri.append('\t<source>\n')#4
veri.append('\t\t<database>Unknown</database>\n')#5
veri.append('\t</source>\n')#6
veri.append('\t<size>\n')#7
veri.append('\t\t<width>32</width>\n')#8
veri.append('\t\t<height>32</height>\n')#9
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

def label_xml(detections,width,height,xmin,ymin,xmax,ymax):
    det = detections
    if(det['detection_scores'][0] >= 0.50 ):
        with open(r'C:\Users\KAYA\Desktop\yeni_deneme\Resim_kaydetme\{}'.format(det['detection_classes'][0]) + '.xml', "w") as f:
            f.seek(0)
            veri[2] = '\t<filename>{}.png</filename>\n'.format(detections['detection_classes'][0])
            veri[3] = '\t<path>YOUR PATH{}.png</path>\n'.format(detections['detection_classes'][0])
            veri[8] = '\t\t<width>{}</width>\n'.format(width)
            veri[9] = '\t\t<height>{}</height>\n'.format(height)
            veri[14] = '\t\t<name>{}</name>\n'.format(detections['detection_classes'][0])
            veri[19] = '\t\t\t<xmin>{}</xmin>\n'.format(xmin)
            veri[20] = '\t\t\t<ymin>{}</ymin>\n'.format(ymin)
            veri[21] = '\t\t\t<xmax>{}</xmax>\n'.format(xmax)
            veri[22] = '\t\t\t<ymax>{}</ymax>\n'.format(ymax)
            f.writelines(veri)
            f.close()
#---------------------------------------------------------------------------------------------------------------------------------
def detec_alp(detections):
    det_alp = detections
    alper = 0
    if(det_alp['detection_scores'][0] >= 0.50):
        return_value,frame = videostream.read()# İlk fotğrafı al
        cv2.imwrite('C:\\Users\\KAYA\\Desktop\\yeni_deneme\\Resim_kaydetme\\{}_{}.jpg'.format(det_alp['detection_classes'][0], alper),frame)#Kaydet
        alper =+ 1
        print("işliyor,  accuracy = ", det_alp['detection_scores'][0], "   ", det_alp['detection_classes'][0])
        uplooda()

    
#---------------------------------------------------------------------------------------------------------------------------------
        
        
        
        

