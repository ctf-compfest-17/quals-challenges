# Writeup Starwalker

Beda kayak pycjail biasa, di chall ini kita gak bisa specify `co_const` ato `co_names` tapi kita masi bisa recover builtins sama masih bisa dapetin function yang kita mau tanpa harus pake `co_const`.
Di python versi 3.12, `LOAD_FAST` dan `STORE_FAST` ga ada bounds checkingnya (saking cepetnya wkkwkwkw). Dengan ini, kita bisa magically ngambil builtins.

# Chosen Bytes

Ini bisa coba coba dan eksplorasi buat opcodes yang ASCII printable (ingat nyari opcode pake `dis._all_opmap` karena `dis.opmap` tidak lengkap), but in my case:

**Opcodes**
> `LOAD_FAST`, `RETURN_VALUE`,`SWAP`, `UNPACK_EX`, `MATCH_KEYS`, 
> `PUSH_EXC_INFO`, `POP_EXCEPT`, `BUILD_TUPLE`

**Operands**
> 40 (`__builtins__.__dict__` index), 59 (ini dummy number bisa literally anything), 
> 120, 121, 109 (`breakpoint` index)

# Steps

1. Load builtins dengan `LOAD_FAST` index 40 dua kali (ini nanti buat `MATCH_KEYS`)
2. Unpack 120 values pake `UNPACK_EX`
3. Pindah stack[-121] ke atas trus POP (karena pop di-ban kita bisa push exception pake `PUSH_EXC_INFO` trus `POP_EXCEPT` 2 kali) 
4. Bikin tuple 120 keys.
5. MATCH_KEYS agar bisa dapet original dict (ini agak crazy dawg)
> **MATCH_KEYS**
> 
> `STACK[-1]` is a tuple of mapping keys, and `STACK[-2]` is the match subject. If `STACK[-2]` contains all of the keys in `STACK[-1]`, push a tuple containing the corresponding values. Otherwise, push `None`.
6. `UNPACK_EX` lagi dan sekarang kita punya builtins di stack urutan kebalik.
7. Switch pake `SWAP` biar naro `breakpoint()` di TOS.
8. Now we have Pdb tinggal shell/open('./flag.txt').

# Further Reading

1. https://docs.python.org/3.12/library/dis.html#python-bytecode-instructions
2. https://docs.google.com/presentation/d/13ZiJPzQrNVC5azJPlryfrPtHulCvohts0rZJFepTmis/edit?slide=id.g2738aae40d1_0_435#slide=id.g2738aae40d1_0_435
3. https://github.com/tamuctf/tamuctf-2025/tree/main/misc/pycjailplusplus