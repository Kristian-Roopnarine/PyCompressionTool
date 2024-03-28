import os
import sys
import priority_queue

ENCODE_DIR = "files_to_compress"
DECODE_DIR = "compressed_files"


class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other_node):
        return self.freq < other_node.freq

    def __gt__(self, other_node):
        return self.freq > other_node.freq


def gen_freq_and_contents(file_path):
    char_freq = dict()
    contents = ""
    with open(file_path, "r", encoding="utf-8") as f:
        while True:
            # f.read() will return the number of CHARACTERS specifed
            # need to read in binary mode to get the correct number of bytes
            char = f.read(1)
            if char == "":
                break
            if char not in char_freq:
                char_freq[char] = {"freq": 0, "bit_string": ""}
            char_freq[char]["freq"] += 1
            contents += char
    return char_freq, contents


def build_huffman(q):
    while len(q) != 1:
        l = priority_queue.deque(q)
        r = priority_queue.deque(q)
        internal = HuffmanNode(None, l.freq + r.freq, l, r)
        priority_queue.enqueue(internal, q)
    # huffman node will be only element in list
    return q[0]


def build_bit_str(freq_table, node, bit_str):
    if not (node.left and node.right):
        freq_table[node.char]["bit_string"] = bit_str
        return
    if node.left:
        build_bit_str(freq_table, node.left, bit_str + "0")
    if node.right:
        build_bit_str(freq_table, node.right, bit_str + "1")


def build_prefix_table(freq_table, huffman_node):
    build_bit_str(freq_table, huffman_node, "")
    return


def build_header(freq):
    output = ""
    for c, data in freq.items():
        output += f"{ord(c)},{data['freq']};"
    return output[:-1]


def compress(freq, contents):
    compressed_out = ""
    for char in contents:
        compressed_out += freq[char]["bit_string"]
    return compressed_out


def decompress(bin_str, huffman_root):
    output = ""
    curr_node = huffman_root
    for char in bin_str:
        if char == "0":
            curr_node = curr_node.left
        if char == "1":
            curr_node = curr_node.right
        if not (curr_node.left and curr_node.right):
            output += curr_node.char
            curr_node = huffman_root
    return output


def gen_nodes_from_header(header):
    q = []
    frequencies = header.split(";")
    for data in frequencies:
        char, freq = data.split(",")
        node = HuffmanNode(chr(int(char)), int(freq))
        q.append(node)
    return q


def encode(file_name):
    file_path = f"{os.getcwd()}/{ENCODE_DIR}/{file_name}"
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Could not find file : {file_name}")
        sys.exit(1)
    freq, contents = gen_freq_and_contents(file_path)
    q = []
    for c, data in freq.items():
        node = HuffmanNode(c, data["freq"])
        q.append(node)
    priority_queue.build(q)
    if not priority_queue.is_valid(q):
        print("Min heap is not valid")
        sys.exit(1)
    huffman_root = build_huffman(q)
    build_prefix_table(freq, huffman_root)
    header = build_header(freq)
    compressed_out = compress(freq, contents)
    compressed_bytes = int(compressed_out, 2).to_bytes(
        (len(compressed_out) + 7) // 8, byteorder="big"
    )
    with open(f"{DECODE_DIR}/{file_name}.bin", "wb+") as w:
        w.write(header.encode())
        w.write(b"\n")
        w.write(compressed_bytes)


def decode(file_name):
    file_path = f"{os.getcwd()}/{DECODE_DIR}/{file_name}"
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Could not find file : {file_name}")
        sys.exit(1)
    f = open(file_path, "rb")
    header = f.readline().decode()
    q = gen_nodes_from_header(header)
    priority_queue.build(q)
    huffman_root = build_huffman(q)
    output = f.read()
    f.close()
    binary_str = bin(int.from_bytes(output, byteorder="big")).replace("0b", "")
    decompressed_contents = decompress(binary_str, huffman_root)
    with open(f"{file_name}_decompressed.txt", "w") as w:
        w.write(decompressed_contents)
