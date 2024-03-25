import os
import sys

ENCODE_DIR = "files_to_compress"
DECODE_DIR = "compressed"


def encode(file_name):
    file_path = f"{os.getcwd()}/{ENCODE_DIR}/{file_name}"
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Could not find file : {file_name}")
        sys.exit(1)
    # read file
    # generate character frequency
    # crete huffman node for each character frequency
    # create priority queue
    # build huffman_tree
    # build prefix table
    # build_header
    # compress data using prefix table
    # pack into bytes
    # save compressed file output


def decode(file_name):
    file_path = f"{os.getcwd()}/{DECODE_DIR}/{file_name}"
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Could not find file : {file_name}")
        sys.exit(1)
