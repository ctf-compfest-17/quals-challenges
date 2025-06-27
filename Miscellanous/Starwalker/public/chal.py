
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
    return all([y in allowed for y in x])

name = input('OK desu ka? ')
allowed = set(name)

if not name.isprintable() or len(name) > 15:
    print('☠⚐🏱☜')
    exit()
    
print(banner % (name))

inp = input('>>> ')

def f():
    pass

if all([y in allowed for y in inp]) and len(inp) < 30 and inp.isprintable():
    f.__code__ = f.__code__.replace(
        co_names=(), 
        co_consts=(), 
        co_code=inp.encode())
    f()()
else:
    print('These characters are Pissing me off...')
