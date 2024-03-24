import sys
import os
import time


INPUT_DIR="files_to_compress"
HEADER_BEGIN="HEADER_BEGIN"
HEADER_END="HEADER_END"

class HuffmanNode:

    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        self.bit_str = ""

    def set_bit_str(self, bit_str):
        self.bit_str = bit_str

    def get_bit_string(self):
        return 

    def get_header_string(self):
        return f"{ord(self.char)},{self.freq}"

    def __str__(self):
        return f"Character: {'Internal Node' if self.char is None else self.char} Frequency: {self.freq}"

def get_file_name(argv):
    return argv[1]

# used dictionary at first but reading in utf-8 gave wrong file size
def gen_char_freq(file_path):
    char_frequency = [0] * 256
    f = open(file_path, 'rb')
    while True:
        char = f.read(1)
        if char == b'':
            break
        char_frequency[ord(char)] += 1
    f.close()
    return char_frequency

def left(i):
    return (i * 2) + 1

def right(i):
    return (i * 2) + 2

def parent(i):
    return (i - 1) // 2

def min_heapify(queue, i):
    min = i
    l = left(i)
    r = right(i)
    if l < len(queue) and queue[l].freq < queue[min].freq:
        min = l
    if r < len(queue) and queue[r].freq < queue[min].freq:
        min = r

    if min != i:
        queue[min], queue[i] = queue[i], queue[min]
        min_heapify(queue, min)

def build_min_heap(queue):
    for i in range(len(queue)//2, 0, -1):
        min_heapify(queue, i)

# how do I remove an item from the min heap?
def extract_min(q):
    if len(q) == 0:
        raise Exception("No items left in queue")
    # swap min with last element
    q[0], q[len(q) - 1] = q[len(q) - 1], q[0]
    # decrement the heap size and save reference
    min = q.pop()
    # min_heapify the top element
    min_heapify(q, 0)
    # return min element
    return min

def insert(q, node):
    # increase size of q
    # insert value at the end of the queue
    # compare with parents and move up into place
    q.append(node)
    i = len(q) - 1
    while i >= 0 and q[parent(i)].freq < q[i].freq:
        q[parent(i)], q[i] = q[parent(i)], q[i]
        i = parent(i)

def build_huffman_tree(q):
    while len(q) != 1:
        l = extract_min(q)
        r = extract_min(q)
        new_node = HuffmanNode(None, l.freq + r.freq, l, r)
        insert(q, new_node)

def walk_huffman(node,prefix_table, bitStr):
    if not (node.left and node.right):
        prefix_table[ord(node.char)] = bitStr
        return
    if node.left:
        walk_huffman(node.left, prefix_table, bitStr + '0')
    if node.right:
        walk_huffman(node.right,prefix_table, bitStr + '1')

def gen_prefix_table(huffman_node):
    prefix_table = [0] * 256
    walk_huffman(huffman_node, prefix_table, "")
    return prefix_table

def is_valid_min_heap(q):
    for node in q:
        if node.left and node.freq > node.left.freq:
            return False
        if node.right and node.freq > node.right.freq:
            return False
    return True

def _header_builder(node, header_arr):
    if not (node.left and node.right):
        header_arr.append(node.get_header_string())
        return 
    if node.left:
        _header_builder(node.left, header_arr)
    if node.right:
        _header_builder(node.right, header_arr)


def _traverse(node):
    if not node:
        return 0
    if not (node.left and node.right):
        return len(bin(int(node.bit_str, 2))) * node.freq
    return _traverse(node.left) + _traverse(node.right)

def test_compressed_bit_length(node):
    _sum = _traverse(node)
    print(_sum)

def build_header(huffman_tree):
    header_arr = [HEADER_BEGIN]
    node = huffman_tree 
    _header_builder(node, header_arr)
    header_arr.append(HEADER_END)
    header_arr.append("\n")
    return "\n".join(header_arr)


def compress_file(prefix_table, file_name):
    f_handler = open(file_name, "rb")
    output = ""
    while True:
        char = f_handler.read(1)
        if char == b'':
            break
        try:
            output += prefix_table[ord(char.decode())]
        except:
            continue
    f_handler.close()
    print('exit function')
    return output

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
    q = []
    for idx, freq in enumerate(freq):
        if freq == 0:
            continue
        node = HuffmanNode(chr(idx), freq)
        q.append(node)

    build_min_heap(q)
    if is_valid_min_heap(q):
        print("Min heap is valid")
    else:
        print("Min heap is not valid")

    build_huffman_tree(q)
    huffman_tree_head = q[0]
    prefix_table = gen_prefix_table(huffman_tree_head)
    header = build_header(huffman_tree_head)
    compressed_output = compress_file(prefix_table, f'{INPUT_DIR}/{file_name}')
    compressed_output_len = len(compressed_output) + 7
    divided_by_8 = compressed_output_len // 8
    compressed_bytes = int(compressed_output, 2).to_bytes(divided_by_8, byteorder="big")
    with open(f"output_{divided_by_8}.bin", "wb") as w:
        w.write(header.encode())
        w.write(compressed_bytes)


