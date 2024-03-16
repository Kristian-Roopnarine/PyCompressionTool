import sys
import os

INPUT_DIR="files_to_compress"

def get_file_name(argv):
    return argv[1]

def gen_char_freq(file_path):
    char_frequency = {}
    f = open(file_path, 'r', encoding="utf-8")
    while True:
        char = f.read(1)
        if char == '':
            break
        if char not in char_frequency:
            char_frequency[char] = 0
        char_frequency[char] += 1
    f.close()
    return char_frequency

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please include a file name to compress")
        sys.exit(1)
    file_name = get_file_name(sys.argv)
    file_path = f'{INPUT_DIR}/{file_name}'
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print("Error finding file")
        sys.exit(1)

    freq = gen_char_freq(file_path)


