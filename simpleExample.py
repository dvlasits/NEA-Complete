from time import sleep
def main():
    for i in range(10):
        s1()
        sleep(1)
    sleep(2)
    s2()
def s1():
    sleep(6)
    s2()
def s2():
    sleep(4)
    s3()
def s3():
    sleep(11)
    pass
main()
