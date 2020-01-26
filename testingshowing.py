from time import sleep
def main():
    sleep(2)
    s1()
    sleep(3)
def s1():
    s2()
    sleep(4)
def s2():
    sleep(3)
main()
