import dis
opmap = dis._all_opmap

def op(opcode):
    return opmap[opcode]

SIZE = 100
index = 40
def f():
    pass
code = bytes([
    op('LOAD_FAST'), index,
    # op('LOAD_FAST'), index,
    op('LOAD_FAST'), 53,
    # op('SWAP'), SIZE+10,
    # op('POP_TOP'), 99,
    # op('BUILD_TUPLE'), SIZE,
    # op('MATCH_KEYS'), 99,
    # op('UNPACK_EX'), 99,
    # op('SWAP'), 89,
    # op('PUSH_NULL'), 99

])

code += bytes([
        op('RETURN_VALUE'), 99,
])
f.__code__ = f.__code__.replace(co_consts=(), co_names=(), co_code=code)

print(code)
print('Output: ', repr(f()))