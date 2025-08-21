#!/usr/local/bin/python3 -S

def header():
    print('Welcome to "Build Your Own Jail!"')
    print("Here, you can create your own jail to escape out of")
    print("All you need to do is provide some characters you want to be whitelisted")

def sanitize(interp):
    chrs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    choice = __import__("random").choice
    randint = __import__("random").randint
    ins = []
    for _ in range(randint(32, 64)):
        name = "".join(choice(chrs) for _ in range(randint(5, 20)))
        ins.append((name, "__main__ and secret :)"))
    
    idx = randint(0, len(ins)-1)
    interp.exec(f"ins = {ins}")
    interp.exec(f"__import__('sys').modules |= dict(ins)\ndel ins")
    interp.exec(f"__import__('sys').modules['{ins[idx][0]}'] = __import__('sys').modules['__main__']")
    interp.exec("__import__('sys').stdin = None")
    interp.exec("__import__('sys').stdout = None")
    interp.exec("__import__('sys').stderr = None")
    interp.exec("__import__('sys').__stdin__ = None")
    interp.exec("__import__('sys').__stdout__ = None")
    interp.exec("__import__('sys').__stderr__ = None")
    interp.exec("__import__('sys').modules['os'] = None")
    interp.exec("__import__('sys').modules['posix'] = None")
    interp.exec("__import__('sys').modules['ctypes'] = None")
    interp.exec("__import__('sys').modules['__main__'] = None")


if __name__ == "__main__":
    header()
    secret = __import__("os").urandom(32).hex()
    fname = __import__("os").getenv("FLAG_FILENAME", None)
    if fname is None:
        print("[ERROR] FLAG_FILENAME not found! Please double check the Dockerfile and docker-compose.yml or contact admins if this happened in remote")
        __import__("sys").exit()
    
    invalid = set(chr(i) for i in range(128))
    whitelist = input("Enter your whitelist: ")
    
    if not whitelist.isascii():
        print("And... what are you supposed to do with those?")
        __import__("sys").exit()
    
    whitelist = set(whitelist)
    if len(whitelist) > 30:
        print("Surely you don't need that many")
        __import__("sys").exit()

    invalid -= whitelist
    
    print("Now enter your code to escape the jail")
    code = input("Enter code: ")
    if not all(c not in invalid for c in code):
        print("Oops, you inputted a blacklisted character!")
        __import__("sys").exit()
    
    if len(code) > 115:
        print("That's too long")
        __import__("sys").exit()
    
    interp = __import__("concurrent.interpreters").interpreters.create()
    interp.prepare_main(secret=secret)
    sanitize(interp)
    safe = {"__builtins__": {}}
    
    try:
        out = interp.call(eval, code, globals=safe, locals=safe)
        interp.close()

        if out != secret:
            print("No flag for you")
            __import__("sys").exit()
    
        print("Congrats, you escaped your own jail! Here is a flag for your efforts")
        with open(f"/{fname}") as f:
            print(f.read())
    
    except Exception:
        print("No flag for you")
