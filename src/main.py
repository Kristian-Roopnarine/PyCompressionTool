import sys
import os

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
        return f"{self.char},{self.freq}"

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

def walk_huffman(node, bitStr):
    if not (node.left and node.right):
        node.set_bit_str(bitStr)
        return
    if node.left:
        walk_huffman(node.left, bitStr + '0')
    if node.right:
        walk_huffman(node.right, bitStr + '1')


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

def build_header(huffman_tree):
    header_arr = [HEADER_BEGIN]
    node = huffman_tree 
    _header_builder(node, header_arr)
    header_arr.append(HEADER_END)
    return "\n".join(header_arr)

def get_bit_string(node, char):
    if not node:
        return
    try:
        if node.char == char.decode("utf-8"):
            return node.bit_str
    except:
        pass
    return get_bit_string(node.left, char) or get_bit_string(node.right, char)

def compress_file(prefix_table, file_name):
    f_handler = open(file_name, "rb")
    output = ''
    while True:
        char = f_handler.read(1)
        if char == b'':
            break
        output += str(get_bit_string(prefix_table, char))
    f_handler.close()
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
    walk_huffman(huffman_tree_head, "")
    compressed_content = build_header(huffman_tree_head)
    compressed_content += compress_file(huffman_tree_head, f'{INPUT_DIR}/{file_name}')
    with open("output.txt", "wb") as w:
        w.write(bytes(compressed_content, "utf-8"))


