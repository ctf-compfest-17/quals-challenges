#!/usr/local/bin/python3

def header():
    print('Welcome to "Build Your Own Jail!"')
    print("Here, you can create your own jail to escape out of")
    print("All you need to do is provide some characters you want to be whitelisted")


if __name__ == "__main__":
    header()
    secret = __import__("os").urandom(32).hex()
    fname = __import__("os").getenv("FLAG_FILENAME", None)
    if fname is None:
        print("[ERROR] FLAG_FILENAME not found! Please double check the Dockerfile and docker-compose.yml or contact admins if this happened in remote")
        exit()
    
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
    
    tmp = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    choice = __import__("random").choice
    new_main = "".join(choice(tmp) for _ in range(64))
    
    __import__("sys").modules['os'] = None
    __import__("sys").modules['posix'] = None
    __import__("sys").modules['ctypes'] = None
    
    interp = __import__("concurrent.interpreters").interpreters.create()
    interp.prepare_main(secret=secret)
    interp.exec(f"__import__('sys').modules['{new_main}'] = __import__('sys').modules['__main__']\n__import__('sys').modules['__main__'] = None")
    safe = {"__builtins__": {}}
    
    try:
        out = interp.call(eval, code, globals=safe, locals=safe)
        interp.close()
    
        if out != secret:
            print("No flag for you")
            exit()
    
        print("Congrats, you escaped your own jail! Here is a flag for your efforts")
        with open(f"/{fname}") as f:
            print(f.read())
    
    except Exception:
        print("No flag for you")
