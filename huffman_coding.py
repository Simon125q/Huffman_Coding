from collections import Counter

class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._heapify_down(0)

        return item

    def _heapify_up(self, index):
        parent = (index - 1) // 2

        if index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


def build_huffman_tree(symbols):
    symbol_counts = Counter(symbols)
    priority_queue = PriorityQueue()

    for symbol, count in symbol_counts.items():
        priority_queue.push(Node(symbol, count))

    while len(priority_queue.heap) > 1:
        left_node = priority_queue.pop()
        right_node = priority_queue.pop()

        merged_frequency = left_node.frequency + right_node.frequency
        merged_node = Node(None, merged_frequency)
        merged_node.left = left_node
        merged_node.right = right_node

        priority_queue.push(merged_node)

    return priority_queue.pop()


def build_huffman_code_table(root):
    code_table = {}

    def traverse(node, current_code):
        if node.symbol is not None:
            code_table[node.symbol] = current_code
            return

        traverse(node.left, current_code + "0")
        traverse(node.right, current_code + "1")

    traverse(root, "")
    return code_table


def encode_string(input_string, code_table):
    encoded_string = ""
    for symbol in input_string:
        encoded_string += code_table[symbol]
    return encoded_string


def calculate_compression_ratio(input_string, encoded_string):
    input_size = len(input_string) * 8  # Assuming 8 bits per character
    encoded_size = len(encoded_string)
    compression_ratio = input_size / encoded_size
    return compression_ratio


def huffman_coding(input_string):
    symbols = list(input_string)
    huffman_tree = build_huffman_tree(symbols)
    code_table = build_huffman_code_table(huffman_tree)
    encoded_string = encode_string(input_string, code_table)
    compression_ratio = calculate_compression_ratio(input_string, encoded_string)
    return encoded_string, code_table, compression_ratio



input_string = "I love data structures"
encoded_string, code_table, compression_ratio = huffman_coding(input_string)

print("Encoded:", encoded_string)
for symbol, code in code_table.items():
    print(symbol, ":", code)
print("Compression Ratio:", compression_ratio)
