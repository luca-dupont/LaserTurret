from controller import Controller
from faceRec import CamWindow

def main():
        # controller = Controller()
        camWindow = CamWindow()

        while True:
            camWindow.run()
            # controller.run()

if __name__ == '__main__':
    main()
