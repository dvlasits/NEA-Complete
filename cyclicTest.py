def main(bool=True):
    if bool:
        s1()
def s1():
    s2()
def s2():
    main(False)
main()
