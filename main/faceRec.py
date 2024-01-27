import cv2
import sys
import serial
from math import sin,cos

class FaceRec :
    def __init__(self, use_serial : bool) :
        self.use_serial = use_serial

        cv2.namedWindow("WebCam")
        self.vc = cv2.VideoCapture(0)

        self.data = "" 

        self.serial_port = '/dev/cu.usbmodem1101'
        self.baud_rate = 9600
        self.ser = None  # Initialize ser variable

        if use_serial :
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")

            if self.vc.isOpened(): # try to get the first frame
                self.rval, self.frame = self.vc.read()
            else:
                self.rval = False

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.faces = [(0,0)]

        self.c = 1
        self.x, self.y, self.W, self.H = (0,0,0,0)
    
    def detect_faces(self, frame):
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect faces in the image
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            self.faces.append((x,y))

        return frame

    def update(self) :
        self.rval, self.frame = self.vc.read()

        frame_with_faces = self.detect_faces(self.frame)

        # Show the frame with face detection
        cv2.imshow("WebCam", cv2.flip(frame_with_faces,1))
        
        self.X,self.Y,self.W,self.H = cv2.getWindowImageRect("WebCam")

        self.data = f"X{158-int(self.faces[-1][0]*(180/self.W))}Y{int(self.faces[-1][1]*(180/(self.Y+self.H)))+20}"
        key = cv2.waitKey(20)
        if key == 27 :
            self.quit()

    def quit(self) :
        if self.ser is not None and self.ser.is_open:
            self.ser.close()

        self.vc.release()

        cv2.destroyWindow("WebCam")
        cv2.waitKey(1)
        sys.exit()
    
    def send_serial_pos(self) :
        # if not self.c%3 :    
            self.ser.write(self.data.encode())
        # self.c += 1
    
    def rotate(self) :
        d = f"X{abs(180*sin(self.c))}Y{abs(180*cos(self.c))}"
        # print(d)
        self.ser.write(d.encode())
        self.c += 0.1

    def run(self) :
        self.update()
        if self.use_serial :
            self.send_serial_pos()
            # self.rotate()
