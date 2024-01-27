from controller import Controller
from faceRec import FaceRec

def main():
        controller = Controller(True)
        # faceRec = FaceRec(use_serial=True)

        while True:
            # faceRec.run()
            controller.run()

if __name__ == '__main__':
    main()
