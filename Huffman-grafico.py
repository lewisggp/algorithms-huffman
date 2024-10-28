from heapq import heappush, heappop, heapify
import matplotlib.pyplot as plt

def plot_huffman_tree(node, ax=None, x=0, y=0, step_x=1, step_y=2, parent_direction="Root"):
    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 10))
    
    if node is not None:
        connection_label = "Root" if parent_direction == "Root" else "0" if parent_direction == "Left" else "1"
        ax.text(x, y, f"{node.symbol}\n(freq: {node.frequency})\n{connection_label}", ha="center", va="center", bbox=dict(boxstyle="round", facecolor="lightgray"))
        if node.left is not None:
            ax.plot([x, x - step_x], [y, y - step_y], color='black')
            plot_huffman_tree(node.left, ax, x - step_x, y - step_y, step_x / 2, step_y, parent_direction="Left")
        if node.right is not None:
            ax.plot([x, x + step_x], [y, y - step_y], color='black')
            plot_huffman_tree(node.right, ax, x + step_x, y - step_y, step_x / 2, step_y, parent_direction="Right")


class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def count_frequencies(data):
    freq_dict = {}
    for symbol in data:
        freq_dict[symbol] = freq_dict.get(symbol, 0) + 1
    return freq_dict

def build_huffman_tree(freq_dict):
    priority_queue = [Node(symbol, frequency) for symbol, frequency in freq_dict.items()]
    heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left_child = heappop(priority_queue)
        right_child = heappop(priority_queue)
        combined_frequency = left_child.frequency + right_child.frequency
        parent_node = Node(None, combined_frequency)
        parent_node.left = left_child
        parent_node.right = right_child
        heappush(priority_queue, parent_node)
    
    return priority_queue[0]

def generate_codes(root, current_code, codes):
    if root is None:
        return

    if root.symbol is not None:
        codes[root.symbol] = current_code
        return

    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)
    
    return codes

def encode_data(data, codes):
    compressed_data = ""
    for symbol in data:
        compressed_data += codes[symbol]
    return compressed_data

def decode_data(encoded_data, huffman_tree):
    decoded_data = ""
    current_node = huffman_tree

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.symbol is not None:
            decoded_data += current_node.symbol
            current_node = huffman_tree

    return decoded_data

if __name__ == "__main__":
    input_text = 'Codigo de huffman'

    binary_representations = []
    for symbol in input_text:
        binary_representation = bin(ord(symbol))[2:].zfill(8)
        binary_representations.append(binary_representation)

    print("\nMensaje Original (bits):")
    print("".join(binary_representations))  # Imprimir los bits uno al lado del otro

    freq_dict = count_frequencies(input_text)
    huffman_tree = build_huffman_tree(freq_dict)
    codes = generate_codes(huffman_tree, "", {})

    print("\nTabla de Codificación:")
    for symbol, code in codes.items():
        print(f"{symbol}: {code}")

    compressed_data = encode_data(input_text, codes)
    print("\nTexto Codificado:")
    print(compressed_data)
    
    decoded_data = decode_data(compressed_data, huffman_tree)
    print("\nTexto Decodificado:")
    print(decoded_data)

    # Mostrar el árbol de Huffman
    plot_huffman_tree(huffman_tree)
    plt.axis('off')
    plt.title("Árbol de Huffman")
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()