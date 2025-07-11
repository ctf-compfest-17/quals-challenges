# Writeup Starwalker

Challenge ini basically nyuruh kita untuk bikin [Quine](https://en.wikipedia.org/wiki/Quine_(computing)) dari Python function bytecode. Approach yang intended adalah untuk merecover `__builtins__.__dict__` dan `globals()` untuk mengeprint variable `code` jadi nanti akhirnya jadi `print(code)`.

# Recovering Builtins and Globals From Nothing

Gimana caranya kita bisa merecover builtins? Basic ideanya adalah pas awal dibikin fungsi, stacknya itu bukan kosong melainkan berisi undefined/uninitialized values. Jadi, secara kebetulan di dalam stack sudah ada `globals()` dan `__builtins__.__dict__`. 
Kalo kita coba lihat dari [source code](https://github.com/python/cpython/blob/3.12/Python/bytecodes.c) untuk `LOAD_FAST`,
```c
inst(LOAD_FAST, (-- value)) {
    value = GETLOCAL(oparg);
    assert(value != NULL);
    Py_INCREF(value);
}
```
terlihat bahwa tidak ada bounds checking sama sekali. Tetapi karena `LOAD_FAST` diban kita harus cari opsi yang lain.
Ternyata `SWAP` dan `COPY` juga tidak memiliki bounds checking,

```c
inst(SWAP, (bottom, unused[oparg-2], top --
            top, unused[oparg-2], bottom)) {
    assert(oparg >= 2);
}
```
```c
inst(COPY, (bottom, unused[oparg-1] -- bottom, unused[oparg-1], top)) {
    assert(oparg > 0);
    top = Py_NewRef(bottom);
}
```

Dengan ini, kita dapat merecover leftover builtins dan globals dengan mengakses uninitialized elements di stack.

# Steps
1. Load `__builtins__.__dict__` menggunakan `COPY 5` dan selanjutnya `COPY 6`. Builtins diload 2 kali buat setup `MATCH_KEYS` agar bisa mengambil values dari dict.
2. `UNPACK_EX` -> `BUILD_TUPLE` -> `MATCH_KEYS` -> `UNPACK_EX` basically unpack values dari dict ke stack. Setelah itu kita taro fungsi `print` di TOS dengan menggunakan `SWAP`
3. Load `globals()` menggunakan cara yang sama di step 1 dan taro isi dari variable `code` di TOS.
4. Prepare buat call `print` dengan `SWAP` dan `COPY`. Ingat, urutannya adalah `print` di paling bawah trus baru argumennya di atas.
5. Submit and get flag.

# Further Reading

1. https://docs.python.org/3.12/library/dis.html#python-bytecode-instructions
2. https://docs.google.com/presentation/d/13ZiJPzQrNVC5azJPlryfrPtHulCvohts0rZJFepTmis/edit?slide=id.g2738aae40d1_0_435#slide=id.g2738aae40d1_0_435
3. https://github.com/tamuctf/tamuctf-2025/tree/main/misc/pycjailplusplus