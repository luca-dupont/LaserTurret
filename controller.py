import pygame as pg
import serial
import sys

class Controller :
    def __init__(self, use_serial, W=680,H=680) :
        self.use_serial = use_serial

        pg.init()
        pg.font.init()

        self.serial_port = '/dev/cu.usbmodem1101'
        self.baud_rate = 9600
        self.ser = None  # Initialize ser variable

        if use_serial :
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")

        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 30)

        self.W = self.screen.get_width()
        self.H = self.screen.get_height()

        self.pos = (0,0)
        
        self.c=0
        self.data = ""


    def events(self) :
        self.pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
    
    def display(self) :
        self.screen.fill('black')

        pg.draw.rect(self.screen,'blue',(0,self.pos[1]-1,self.W,3))
        pg.draw.rect(self.screen,'blue',(self.pos[0]-1,0,3,self.H))
        pg.draw.circle(self.screen, 'red', self.pos, 6)

        text = self.font.render(
            self.data, True, (255,255,255)
        )    

        self.screen.blit(text, (10, 10))

        pg.display.flip()

    def update(self) :

        self.data = f"X{180-int(self.pos[0]*(180/self.W))}Y{int(self.pos[1]*(180/self.H))}"

        self.clock.tick(120)
    
    def send_serial_pos(self) :
        if self.c%2 :    
            self.ser.write(self.data.encode())
        self.c += 1
        
    def quit(self) :
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
        pg.quit()
        sys.exit()

    def run(self) :
        self.events()
        self.display()
        if self.use_serial :
            self.send_serial_pos()
        self.update()
