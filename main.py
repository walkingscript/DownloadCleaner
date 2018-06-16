import os
import sys

from mutagen.easyid3 import EasyID3

def main():
    for item in sys.argv:
        song = EasyID3(item)
        print(song)
    input()

if __name__ == '__main__':
    main()