#!/usr/bin/env python3

import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_file(encrypted_file_path, output_file_path):
    # Hardcoded key and IV (same as PowerShell script)
    key = b"9xK#mP2$vB8nQ7zL"  # 16 bytes
    iv = b"4tR!jF6&wE3sA9hY"   # 16 bytes
    
    try:
        # Read encrypted file
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Create AES cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Write decrypted zip file
        with open(output_file_path, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"Successfully decrypted: {encrypted_file_path}")
        print(f"Output saved as: {output_file_path}")
        
    except Exception as e:
        print(f"Error during decryption: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python decrypt.py <encrypted_file> <output_zip_file>")
        print("Example: python decrypt.py file.enc decrypted.zip")
        sys.exit(1)
    
    encrypted_file = sys.argv[1]
    output_file = sys.argv[2]
    
    decrypt_file(encrypted_file, output_file)