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

# Take this traveller
def gadget(f, *args):
    f(args[0])

def good(x: str):
    return all(32 <= ord(c) <= 126 for c in x) and all([y in allowed for y in x]) and len(x) <= 1000

name = input('OK desu ka? ')
allowed = set(name)
what_is_this = [{}]

if not name.isprintable() or len(name) > 50:
    print('☠⚐🏱☜')
    exit()
    
print(banner % (name))
inp = input('>>> ')

def f():
    pass

if good(inp):
    f.__code__ = f.__code__.replace(
        co_names=(),
        co_code=inp.encode())
    f()
else:
    print('These characters are Pissing me off...')
