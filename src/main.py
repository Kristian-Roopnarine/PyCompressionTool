import sys
from huffman import encode, decode

FILES_TO_COMPRESS = "files_to_compress"


def get_file_info(args):
    file_name = args[1]
    file_ext = file_name.split(".")[-1]
    return file_name, file_ext


def main(file_name, file_ext):
    if file_ext == "txt":
        encode(file_name)
    elif file_ext == "bin":
        decode(file_name)
    else:
        raise Exception("File extension not supported.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please include a file name to either compress or bin file to decompress")
        sys.exit(1)
    file_name, file_ext = get_file_info(sys.argv)
    main(file_name, file_ext)
