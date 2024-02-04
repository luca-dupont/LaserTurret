from control import Controller

def main():
    controller = Controller(True)

    while True:
        controller.run()

if __name__ == "__main__":
    main()
