
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

This jail is Pissing me off...           
"""

def good(x: str):
    return x.isprintable() and [x_ch not in '5t4rw4lker' for x_ch in x.lower()]
print(banner)
inp = input('>>> ')

def f():
    pass

if not good(inp):
    print('These characters are Pissing me off...')
else:
    f.__code__ = f.__code__.replace(co_names=(), co_consts=(), co_code=inp.encode())
    f()()
    