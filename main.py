#! /usr/bin/python2

from gate import Gate


def run(name='test.avi'):
    gate_obj = Gate(name)
    gate_obj.read()


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        run()
