from control import Test

def main():
    control = Test(False, 400, 400)

    while True:
        control.run()

if __name__ == "__main__":
    main()
