#!/usr/local/bin/python3.12
import base64
import io
from contextlib import redirect_stdout
from dis import _all_opmap as op

banner = """
                            @@                               
                          @@@@@                              
                          @@  @@                             
                        @@@    @@                            
                        @@     @@@                           
                       @@        @@                          
                     @@            @@                        
                @@@@@@@@@@@@@@       @@                      
           @@@@@    @    @@@@@@@@@@@@@@@@@                   
        @@@           @       @  @@@  @@@@@@@@@@             
           @@@@         @@@@@           @    @@@@@@@@        
              @@@@@@                                @@@@@@@@@
                   @@                               @@@@@@@@@
                   @@                        @@@@@@@@        
                   @@         @@@          @@@@@             
                   @@         @@@          @@                
                 @@@        @@ @@        @@@                 
                 @@@        @@ @@       @@                   
                 @@@       @@  @@       @@                   
                @@         @@@@@      @@                     
                @@       @@  @@       @@                     
                @@      @@@  @@      @@@                     
              @@       @@    @@      @@                      
              @@      @@    @@       @@                      
             @@       @@    @@     @@                        
            @@@       @@  @@@      @@                        
   @@@@@@@@@@       @@    @@       @@                        
 @@@                @@    @@       @@                        
@@                @@@   @@       @@@@@@@@@                   
@@@@@@@@@@@@@@@@@@@@    @@               @@@                 
@@@@@@@@@@@@@@@@@@    @@                 @@@                 
                      @@@@@@@@@@@@@@@@@@@@        

These birds are Pissing me off...           
"""
banned = [
    'IMPORT_NAME', 'IMPORT_FROM', 'GET_ITER', 
    'FOR_ITER', 'FOR_ITER_LIST', 'FOR_ITER_TUPLE', 'FOR_ITER_RANGE',
    'BINARY_SUBSCR', 'STORE_SUBSCR', 'DELETE_SUBSCR',
    'EXTENDED_ARG', 'POP_TOP', 'CALL', 
    'LOAD_FAST', 'STORE_FAST', 'STORE_NAME', 'STORE_GLOBAL', 
    'STORE_FAST__STORE_FAST', 'STORE_SUBSCR_DICT', 
    'LOAD_CONST', 'LOAD_GLOBAL',
    'LOAD_CONST__LOAD_FAST', 'LOAD_FAST__LOAD_FAST',
    'STORE_FAST__LOAD_FAST', 'LOAD_FAST_AND_CLEAR',
]

def f(): pass

def get_stdout(f):
    out = io.StringIO()
    with redirect_stdout(out):
        f()
    return out.getvalue().strip()

def good(s):
    return 50 <= len(s) <= 100 and sum([x for x in s]) % 17 == 0 and all([op[i] not in s for i in banned])

def print_flag():
    with open('./flag.txt') as f:
        print(f'Heres the    flag: {f.read()}')

print(banner)

try:
    code = base64.b64decode(input('>>> '))
except:
    print('This base64 is Pissing me off...')
    exit() 
    
if not good(code):
    print('These characters are Pissing me off...')
    exit()
f.__code__ = f.__code__.replace(co_code=code, co_consts=(), co_names=())

out = get_stdout(f)

if str(out) == str(code):
    print_flag()
else:
    print('No')