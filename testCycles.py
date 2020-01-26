def main():
    def add1(a):
        b = [892347598347573**0.5 for i in range(100000)]
        a += 1
        if a == 100:
            return a
        return add2(a)

    def add2(a):
        b = [892347598347573**0.5 for i in range(100000)]
        a += 1
        if a == 100:
            return a
        return add1(a)

    add1(1)

main()
