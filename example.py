from time import sleep
def main(bool):
    sleep(2)
    if bool:
        child()
        sleep(2)
def child():
    sleep(1)
main(True)
main(False)
