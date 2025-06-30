#!/usr/local/bin/python3.12
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

%s, This jail is Pissing me off...           
"""

def good(x: str):
    return all(32 <= ord(c) <= 126 for c in x) and all([y in allowed for y in x]) and len(x) < 30

name = input('OK desu ka? ')
allowed = set(name)

if not name.isprintable() or len(name) > 15:
    print('☠⚐🏱☜')
    exit()
    
print(banner % (name))

inp = input('>>> ')

def f():
    pass

if good(inp):
    f.__code__ = f.__code__.replace(
        co_names=(), 
        co_consts=(), 
        co_code=inp.encode())
    f()()
else:
    print('These characters are Pissing me off...')
