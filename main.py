'''Main file
'''

from gate import gate


def run():
    '''Main function
    '''

    gateObj = gate('test.mp4')
    gateObj.read()


if __name__ == "__main__":
    run()
