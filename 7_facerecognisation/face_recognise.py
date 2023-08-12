import cv2,numpy,os
dataset='dataset'
haar_file='haarcascade_frontalface_default.xml'
face_cascade=cv2.CascadeClassifier(haar_file)
print('training....')
(images,labels,name,id)=([],[],{},0)
for (subdirs,dirs,files) in os.walk(dataset):
    for subdir in dirs:
        name[id]=subdir
        subjectpath=os.path.join(dataset,subdir)
        for filename in os.listdir(subjectpath):
            path=subjectpath+'/'+filename
            label=id
            images.append(cv2.imread(path,0))
            labels.append(int(label))
        id+=1
(images,labels)=[numpy.array(lis)for lis in [images,labels]]
print(images,labels)
(width,height)=(130,100)

# recongnisation classifier
model=cv2.face.LBPHFaceRecognizer_create()
#model=cv2.face.FisherFaceRecognizer_create()
model.train(images,labels)

#camera processing
webcam = cv2.VideoCapture(0)
cnt=0
while True:
    (_,img)=webcam.read()
    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayImg,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        face = grayImg[y:y+h,x:x+w]
        face_resize=cv2.resize(face,(width,height))
        
        prediction =model.predict(face_resize)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        if prediction[1]<800:
            cv2.putText(img,'%s - %0f' % (name[prediction[0]],prediction[1]),(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255))
            print(name[prediction[0]])
            cnt=0
        else:
            cnt+=1
            cv2.putText(img,'unknown',(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255) ,2 )
            if (cnt>100):
                print('unknown person')
                cv2.imwrite('unknown.jpg',img)
                cnt=0
    cv2.imshow('FaceRecongnition',img)
    key = cv2.waitKey(10)
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()

        
                
            
        
        
    
 
