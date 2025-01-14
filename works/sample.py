from __future__ import annotations


def main():
    i = 3

    def v1(a):
        print(i)
        i += 1

    v1(5)
    print(i)


main()
