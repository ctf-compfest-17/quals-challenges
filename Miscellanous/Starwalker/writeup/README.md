# Writeup Starwalker

Beda kayak pycjail biasa, di chall ini kita gak bisa specify `co_const` ato `co_names` tapi kita masi bisa recover builtins sama masih bisa dapetin function yang kita mau tanpa harus pake `co_const`.
Opcode `LOAD_FAST` dan `STORE_FAST` ga ada bounds checkingnya. Dengan ini, kita bisa magically ngambil builtins sama globals.
Di challenge juga ada function `gadget` yang bisa membantu untuk call function karena minimal 32 arguments.

# Chosen Bytes

Ini bisa coba coba dan eksplorasi buat opcodes yang ASCII printable (ingat nyari opcode pake `dis._all_opmap` karena `dis.opmap` tidak lengkap), but in my case:

**Opcodes**
> `LOAD_FAST`, `RETURN_VALUE`,`SWAP`, `UNPACK_EX`, `MATCH_KEYS`, 
> `PUSH_EXC_INFO`, `POP_EXCEPT`, `BUILD_TUPLE`, `STORE_FAST`
> `LOAD_ASSERTION_ERROR`, `STORE_SUBSCR`, `CALL_NO_KW_BUILTIN_FAST`

# General Solution Idea

Basically, kita harus mendapatkan shell dengan cara menggunakan `eval` dan fungsi helper `gadget`. Argument untuk fungsi tersebut kita bisa emplace di dalam `name` jadi untuk allowed bytesnya dia dalem bentuk `<executed code>#<payload>` (for me `breakpoint()#<payload>`).

Karena kita sebenarnya tidak bisa mengakses `builtins` dan `globals` kita bisa memanfaatkan OOB dalam instruksi `LOAD_FAST` dan `STORE_FAST` ( `builtins` ada di 60 dan `globals` ada di `STACK[-100]` setelah spraying `LOAD_FAST`). 


# Steps
1. Load `__builtins__.__dict__` menggunakan `LOAD_FAST 60` dua kali (soalnya buat `MATCH_KEYS` biar dapet valuenya doang). Nanti tinggal pake `SWAP` untuk cari fungsi yang kita mau (gausah pake `STORE_FAST`).
2. Load `globals()` dengan ngespam `LOAD_FAST` OOB 30 kali. 
3. Load `builtins` lagi buat mengisi dict `globals()` karena itemsnya masih kurang dari 32 (`MATCH_KEYS` minimal 32 items).
4. Prepare `eval`, `name` dan `gadget` di stack.
5. Call `gadget` (buat arguments yang gak penting tinggal pake `LOAD_ASSERTION_ERROR`)
6. `import os; os.system('sh')`

# Further Reading

1. https://docs.python.org/3.12/library/dis.html#python-bytecode-instructions
2. https://docs.google.com/presentation/d/13ZiJPzQrNVC5azJPlryfrPtHulCvohts0rZJFepTmis/edit?slide=id.g2738aae40d1_0_435#slide=id.g2738aae40d1_0_435
3. https://github.com/tamuctf/tamuctf-2025/tree/main/misc/pycjailplusplus