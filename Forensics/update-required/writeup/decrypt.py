from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

def generate_key_iv():
    base = b'KleeLovesBoom'
    salt = b'Mondstadt4Ever'

    key_full = hashlib.sha256(base + salt).digest()
    key = key_full[:16]

    iv = bytearray(hashlib.md5(base).digest())
    iv.reverse()
    return bytes(key), bytes(iv)

def decrypt_file(input_path, output_path):
    key, iv = generate_key_iv()

    with open(input_path, 'rb') as f:
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_path, 'wb') as f:
        f.write(plaintext)

if __name__ == '__main__':
    decrypt_file('full_payload.bin', 'decrypted_output.pdf')
    print("Decryption complete: decrypted_output.pdf")