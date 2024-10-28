from heapq import heappush, heappop, heapify

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
    for byte in data:
        freq_dict[byte] = freq_dict.get(byte, 0) + 1
    return freq_dict

def build_huffman_tree(freq_dict):
    priority_queue = [Node(byte, frequency) for byte, frequency in freq_dict.items()]
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

def pack_bits_to_bytes(bits):
    packed_bytes = bytearray()
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        byte_str = ''.join(byte_bits)
        packed_byte = int(byte_str, 2)
        packed_bytes.append(packed_byte)
    return packed_bytes

def encode_data(data, codes):
    compressed_data = ""
    for byte in data:
        compressed_data += codes[byte]
    return compressed_data

def decode_data(encoded_data, huffman_tree):
    decoded_data = bytearray()
    current_node = huffman_tree

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.symbol is not None:
            decoded_data.append(current_node.symbol)
            current_node = huffman_tree

    return decoded_data

if __name__ == "__main__":
    
    # Leer archivo a comprimir
    file_path = 'example_image.jpg'  # Ruta del archivo JPG a comprimir
    with open(file_path, 'rb') as file:
        input_data = file.read()
    
    # Frecuencias, Arbol y Tabla
    freq_dict = count_frequencies(input_data)
    print(freq_dict)
    huffman_tree = build_huffman_tree(freq_dict)
    codes = generate_codes(huffman_tree, "", {})

    # Mostrar tabla de codificacion
    print("\nTabla de Codificación:")
    for byte, code in codes.items():
        print(f"{byte}: {code}")

    # Codificar datos a comprimir
    compressed_data = encode_data(input_data, codes)

    # Convertir la cadena a bytes
    packed_compressed_data = pack_bits_to_bytes(compressed_data)
    
    # Mostrar los bits originales
    #print("\nBits Originales:")
    #for byte in input_data:
    #    print(format(byte, '08b'), end=' ')
        
    # Mostrar los bits originales y comprimidos
    #print("\nBits Comprimidos:")
    #for byte in compressed_data:
    #    print(format(byte, '08b'), end='')

    # Guardar bits comprimidos
    compressed_file_path = 'compressed_image.bin'
    with open('compressed_image.bin', 'wb') as output_file:
        output_file.write(packed_compressed_data)

    # Leer archivo comprimido
    with open(compressed_file_path, 'rb') as compressed_file:
        compressed_data = compressed_file.read()
        
    # Convertir los bytes del archivo comprimido a una cadena de bits
    compressed_data_bits = ''.join(format(byte, '08b') for byte in compressed_data)

    # Decodificar los datos comprimidos
    decoded_data = decode_data(compressed_data_bits, huffman_tree)
    
    # Guardar archivo descomprimido
    with open('decompressed_image.jpg', 'wb') as output_file:
        output_file.write(decoded_data)

    print("\nArchivo comprimido guardado como 'compressed_image.bin'")
    print("Archivo descomprimido guardado como 'decompressed_image.jpg'")
    
    # Mostrar el tamaño del archivo original y comprimido
    original_size = len(input_data)
    compressed_size = len(packed_compressed_data)
    print(f"\nTamaño del archivo original: {original_size} bytes")
    print(f"Tamaño del archivo comprimido: {compressed_size} bytes")

    # Calcular la tasa de compresión
    compression_ratio = original_size / compressed_size
    print(f"Tasa de compresión: {compression_ratio:.3f}")