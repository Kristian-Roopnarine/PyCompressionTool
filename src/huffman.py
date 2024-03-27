import os
import sys
import priority_queue

ENCODE_DIR = "files_to_compress"
DECODE_DIR = "compressed"


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
    # huffman node will be last element in list
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
        output += f"{c},{data['freq']};"
    return output


def compress(freq, contents):
    compressed_out = ""
    for char in contents:
        compressed_out += freq[char]["bit_string"]
    return compressed_out


def encode(file_name):
    file_path = f"{os.getcwd()}/{ENCODE_DIR}/{file_name}"
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Could not find file : {file_name}")
        sys.exit(1)
    # this may actually encode all the characters properly
    freq, contents = gen_freq_and_contents(file_path)
    # crete huffman node for each character frequency
    q = []
    for c, data in freq.items():
        node = HuffmanNode(c, data["freq"])
        q.append(node)
    # create priority queue
    priority_queue.build(q)
    if not priority_queue.is_valid(q):
        print("Min heap is not valid")
        sys.exit(1)
    # build huffman_tree
    huffman_root = build_huffman(q)
    # build prefix table
    build_prefix_table(freq, huffman_root)
    # build_header
    header = build_header(freq)
    # compress data using prefix table
    compressed_out = compress(freq, contents)
    # pack into bytes
    compressed_bytes = int(compressed_out, 2).to_bytes(
        (len(compressed_out) + 7) // 8, byteorder="big"
    )
    # save compressed file output
    with open(f"{file_name}.bin", "wb") as w:
        w.write(header.encode())
        w.write(b"\n")
        w.write(compressed_bytes)


def decode(file_name):
    file_path = f"{os.getcwd()}/{DECODE_DIR}/{file_name}"
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Could not find file : {file_name}")
        sys.exit(1)
