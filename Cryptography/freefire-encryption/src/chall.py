from sage.all import *
from functools import reduce
import os

class FFEncryption:
    def __init__(self):
        self.p = 2**127 - 1
        self.k = 64
        self.F = GF((self.p, self.k), "x")
        self.key = self.gen_key()
    
    def gen_key(self):
        return [self.F.random_element() for _ in range(17)]

    def to_lst(self, el):
        return el.list()

    def to_el(self, lst):
        return self.F(list(lst))
    
    def encrypt(self, pt):
        k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, k16, k17 = self.key
        x, y = reduce(lambda acc, i: ((acc[0]*acc[1]*k2*k7, acc[1]**2) if i%4==0 else (acc[0]**2, acc[1]*acc[0]*k3*k8) if i%4==1 else (acc[0]*acc[1]*k4*k9, acc[1]**2) if i%4==2 else (acc[0]**2, acc[1]*acc[0]*k2*k10))[::-1], range(127), (k1, pt))
        z = k5 * x + k6 * y * pt + k11
        return k12 * z**2 + k13 * z + k14 * k15 * k16 * k17

def main():
    FF = FFEncryption()
    rnd = os.urandom(FF.k)
    key = os.urandom(FF.k)
    count = 0
    
    print("Welcome to FF Encryption System!")
    print("This super secure system uses 17 keys for encryption!!!")
    
    while (count < 1700):
        inp = input("> ").encode()
        
        if inp == b'done':
            print("That's quick!")
            break
        
        if len(inp) != FF.k or inp == rnd:
            print("Invalid input")
            return
        
        enc = FF.encrypt(FF.to_el(inp))
        print(f"Encrypted: {FF.to_lst(enc)}")
        count += 1
    
    print("Now, you should be able to guess the encrypted random!")
    print(f'Random: {rnd.hex()}')
    
    inp = input("Guess the random: ")
    inp_list = [int(x) for x in inp.split(",")]
    
    if inp_list != FF.to_lst(FF.encrypt(FF.to_el(rnd))):
        print("Wrong guess!")
        return
    
    print("Damn, truly a cryptomaster! Now, let's see if you can guess the key!")
    print(f'Encrypted key: {FF.to_lst(FF.encrypt(FF.to_el(key)))}')
    guess = input("Guess the key: ")
    if guess == key.hex():
        with open("flag.txt", "r") as f:
            print(f.read())
    else:
        print('Wrong key!')
        print("Better luck next time!")
        return

if __name__ == "__main__":
    main()