#!/usr/local/bin/python3

def header():
    print('Welcome to "Build Your Own Jail!"')
    print("Here, you can create your own jail to escape out of")
    print("All you need to do is provide some characters you want to be whitelisted")


if __name__ == "__main__":
    header()
    secret = __import__("os").urandom(32).hex()
    invalid = set(chr(i) for i in range(128))
    whitelist = input("Enter your whitelist: ")
    
    if not whitelist.isascii():
        print("And... what are you supposed to do with those?")
        exit()
    
    whitelist = set(whitelist)
    if len(whitelist) > 32:
        print("Surely you don't need that many")
        exit()

    invalid -= whitelist
    
    print("Now enter your code to escape the jail")
    code = input("Enter code: ")
    if not all(c not in invalid for c in code):
        print("Oops, you inputted a blacklisted character!")
        exit()
    
    if len(code) > 200:
        print("That's too long")
        exit()
    
    __import__("sys").modules['os'] = None
    __import__("sys").modules['posix'] = None
    __import__("sys").modules['ctypes'] = None
    
    interp = __import__("concurrent.interpreters").interpreters.create()
    interp.prepare_main(secret=secret)
    safe = {"__builtins__": {}}
    out = interp.call(eval, res, globals=safe, locals=safe)
    interp.close()
    
    if out != secret:
        print("No flag for you")
        exit()
    
    print("Congrats, you escaped your own jail! Here is a flag for your efforts")
    with open("/flag.txt") as f:
        print(f.read())
