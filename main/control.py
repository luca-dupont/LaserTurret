import cv2
import sys
import os
import serial
import pygame as pg
import json

class Test :
    def __init__(self, use_serial : bool, recalibrate : bool = False, W=680,H=680) :
        self.use_serial = use_serial
        self.serial_port = '/dev/cu.usbmodem1101'
        self.baud_rate = 9600
        self.ser = None  # Initialize ser variable

        cv2.namedWindow("WebCam")
        self.vc = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if use_serial :
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
            if self.vc.isOpened(): # try to get the first frame
                self.rval, self.frame = self.vc.read()
            else:
                self.rval = False

        # Calibration sequence
        if not os.stat("settings.json").st_size or recalibrate:
            pg.init()
            pg.font.init()

            screen = pg.display.set_mode((W, H))
            clock = pg.time.Clock()
            font = pg.font.Font(None, 30)
            running = True
            q = 0

            counter = 0

            jdata = {}

            while running :
                self.rval, self.frame = self.vc.read()
                cv2.imshow("WebCam", cv2.flip(self.frame,1))

                ev = pg.event.get()

                for event in ev :
                    if event.type == pg.QUIT :
                        pg.quit()
                        running=False
                        break

                screen.fill((0,0,0))
                mousepos = pg.mouse.get_pos()
                
                match counter :
                    case 0 :
                        text = font.render("Place laser a top left of screen, ", True, (255,255,255))
                        screen.blit(text, (10,40))
                    case 1 :
                        text = font.render("Place laser a bottom right of screen, ", True, (255,255,255))
                        screen.blit(text, (10,40))
                    case 2 :
                        with open("settings.json", "w") as f :
                            json.dump(jdata, f, indent=2)
                        pg.quit()
                        running = False
                        break

                key = cv2.waitKey(40)
                if key == 32 :
                    if counter == 0 :
                        jdata["XMIN"], jdata["YMIN"] = xval, yval
                    else :
                        jdata["XMAX"], jdata["YMAX"] = xval, yval
                    counter += 1

                screen.blit(font.render("Press SPACE", True, (255,255,255)), (10, 70))
                pg.draw.rect(screen,'blue',(0,mousepos[1]-1,W,3))
                pg.draw.rect(screen,'blue',(mousepos[0]-1,0,3,H))
                pg.draw.circle(screen, 'red', mousepos, 6)

                text = font.render(f"{counter}/2 positions taken", True, (255,255,255))
                screen.blit(text, (10,10))

                xval = int(mousepos[0]*(180/W))
                yval = int(mousepos[1]*(180/H))

                if use_serial :
                    data = f"X{xval}Y{yval}"
                    self.ser.write(data.encode())

                pg.display.flip()

                clock.tick(120)
                q += 1

        self.data = "" 

        self.faces = [(0,0)]

        self.X,self.Y,self.W,self.H = (0,0,0,0)

        self.c = 1

    def convert_val(self,newMinX,newMaxX,newMinY,newMaxY, pos) :
        NewX = (((pos[0]) * (newMaxX - newMinX)) / (self.W)) + newMinX
        NewY = (((pos[1]) * (newMaxY - newMinY)) / (self.H)) + newMinY
        return [180-int(NewX),int(NewY)]

    
    def detect_faces(self, frame):
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect faces in the image
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            self.faces.append((x+(w//2),y))

        return frame

    def update(self) :
        # print(self.XMIN,self.XMAX,self.YMIN,self.YMAX)
        self.rval, self.frame = self.vc.read()

        frame_with_faces = self.detect_faces(self.frame)

        # Show the frame with face detection
        cv2.imshow("WebCam", cv2.flip(frame_with_faces,1))
        
        self.X,self.Y,self.W,self.H = cv2.getWindowImageRect("WebCam")

        with open("settings.json", "r") as f :
            dic = json.load(f)
            p = self.convert_val(dic["XMIN"], dic["XMAX"], dic["YMIN"],dic["YMAX"], (self.faces[-1][0], self.faces[-1][1]))
        self.data = f"X{p[0]}Y{p[1]-20}"

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
        self.ser.write(self.data.encode())
    

    def run(self) :
        self.update()
        if self.use_serial :
            self.send_serial_pos()
