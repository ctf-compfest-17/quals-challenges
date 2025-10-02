from md5 import *
from binascii import unhexlify
from rand import *

rng = Random()

def xor(a: bytes, b: bytes) -> bytes:
    max_len = max(len(a), len(b))
    a_padded = a.ljust(max_len, b"\x00")
    b_padded = b.ljust(max_len, b"\x00")
    return bytes(x ^ y for x, y in zip(a_padded, b_padded))

class OpenCommitment:
    color_hash = None

    def __init__(self, commitment):
        self.commitment = commitment

    def open(self, key_bytes):
        key_hash = hash(key_bytes)
        self.color_hash = xor(self.commitment, key_hash)
        return self.color_hash

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def get_random_edge(self):
        return self.edges[rng.randint(len(self.edges))]

class Verifier:
    valid_colors = {
        hash(b'red'):b"red",
        hash(b'green'):b"green",
        hash(b'blue'):b"blue"
    }
    def __init__(self, graph):
        self.graph = graph


    def verify_commitment(self, oc1, oc2, key_a, key_b):
        color1_hash = oc1.open(key_a)
        print(color1_hash)
        color2_hash = oc2.open(key_b)
        print(color2_hash)

        color1 = self.valid_colors.get(color1_hash, None)
        color2 = self.valid_colors.get(color2_hash, None)
        
        if color1 == None or color2 == None:
            print("Invalid color detected")
            return False
        elif color1 == color2:
            print(f"Adjacent vertices have the same color: {color1}")
            return False
        
        return True


    def interact(self, iterations):
        try:
            for i in range(iterations):
                print(f"\n--- Iteration {i+1} ---")

                commitments = {}
                for vertex in self.graph.vertices:
                    commitment_input = input(f"Enter commitment for vertex {vertex}: ")
                    if (len(commitment_input) != 32):
                        print("Invalid commitment length")
                        exit(1)
                    commitment_input = unhexlify(commitment_input)
                    commitments[vertex] = OpenCommitment(commitment_input)


                edge = self.graph.get_random_edge()
                print(f"Verifier selected edge: {edge}")

                key_a = unhexlify(input(f"Enter key for vertex {edge[0]}: "))
                key_b = unhexlify(input(f"Enter key for vertex {edge[1]}: "))

                if (key_a == b"red" or key_a == b"green" or key_a == b"blue" or
                    key_b == b"red" or key_b == b"green" or key_b == b"blue"):
                    print("Keys cannot be the same as colors")
                    exit(1)

                oc1 = commitments[edge[0]]
                oc2 = commitments[edge[1]]
                

                if not self.verify_commitment(oc1, oc2, key_a, key_b):
                    print("Are you lying to me 😡 ")
                    exit(1)
        except Exception as e:
            print(f"Something went wrong: {e}")
            exit(1)
        
def print_flag():
    print("\nAlright, it seems that you can be trusted. Here's the secret: ")
    flag = "REDACTED"
    print(flag)

def main():
    print("I have a secret but I will only share it to those who can be trusted. Can you be trusted? I've created this game to test if you are")
    print("\nHere's a warm-up round so you know how this works")
    graph1 = Graph(
    vertices=[1, 2, 3, 4, 5, 6, 7, 8],
    edges=[
        (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
        (2, 3), (2, 4), (2, 5), (2, 6), (3, 7),
        (3, 8), (4, 7), (4, 8), (5, 7), (5, 8),
        (6, 7)
        ]
    )
    verifier = Verifier(graph1)
    verifier.interact(30)

    print("\nNow for the real challenge...")
    graph2 = Graph(
        vertices=[1, 2, 3, 4, 5, 6, 7],
        edges=[
            (1, 2), (1, 3), (1, 4), (1, 5), (2, 3),
            (2, 4), (2, 5), (3, 4), (3, 5), (4, 5),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
            (6, 7)
        ]
    )
    verifier = Verifier(graph2)
    verifier.interact(100) 
    print_flag()

if __name__ == "__main__":
    main()