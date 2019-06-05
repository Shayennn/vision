#! /usr/bin/python3
import subprocess
import threading


class MultiTest(threading.Thread):
    '''Multi Testing class for Zeabus Vision mission by Phitchawat L.

    Arguments:
        filename {string} -- [File name with part to open]
    '''

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        subprocess.run(['python2 main.py ' + self.filename],
                       shell=True, check=True)


if __name__ == "__main__":
    import os
    TEST_FILES_DIR = 'test_file'
    THREADS = []
    for fn in os.listdir(TEST_FILES_DIR):
        if fn.split('.')[-1] != 'avi':
            continue
        THREADS.append(MultiTest(os.path.join(TEST_FILES_DIR, fn)))
    for thrd in THREADS:
        thrd.start()
    for thrd in THREADS:
        thrd.join()
    print('Everything is okay.')
