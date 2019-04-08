'''Main file
'''

from gate import Gate


def run():
    '''Main function
    '''

    gate_obj = Gate('test.mp4')
    gate_obj.read()


if __name__ == "__main__":
    run()
