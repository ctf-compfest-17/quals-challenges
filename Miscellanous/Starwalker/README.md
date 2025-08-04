# Starwalker

by AdamRayyan

---

## Flag

```
COMPFEST17{I_4m_th3_0rIg1n4L______St4rW4lk3R_ce7428eba6}
```

## Description
These birds are Pissing me off...           

## Difficulty
Tingkat kesulitan soal: medium-hard

## Hints
> ~~Note: Hint 1 langsung dirilis, hint selainnya jangan.~~ Actually jangan deh, I wanna see where this goes. Ini hint buat jaga jaga saja
* Some specialized opcodes need caching. You can check for this yourself by dissasembling a function with a specialized opcode with `dis.dis` and turning on `show_caches`. Most of the time, this will fix crashes.
Example code:
```python
from dis import dis, _all_opmap as opmap
from opcode import _specialized_instructions as si, _specializations as sz

# Which instruction family does it belong to?
def family(op_s):
    for k, v in sz.items():
        if op_s in v:
            return k
    return None

def f(): pass

for op in si:
    print('-'*80)
    print(f'{op:<50} | {family(op):^16} | {opmap[op]} ')
    print('-'*80 + '\n')
    dis(bytes([opmap[op], 0]), adaptive=True, show_caches=True)
```
* There are many `POP` instructions other than `POP_TOP`. Most of them devolve to regular `POP` if the conditions aren't met. 

## Tags
pycjail

## Deployment
Penjelasan cara menjalankan service yang dibutuhkan serta requirementsnya.

#### Contoh 1
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    docker-compose up --build --detach
    ```

#### Contoh 2
- How to compile:
    ```
    gcc soal.c -o soal -O2 -D\_FORTIFY\_SOURCE=2 -fstack-protector-all -Wl,-z,now,-z,relro -Wall -no-pie
    ```
- Jalankan:
    ```
    ./soal
    ```
- Workdir di `/home/...`
- Gunakan libc 2.31 ketika sudah keluar. Alias Ubuntu 20.04.

## Notes

Hint selain yang pertama jangan ada yang dirilis dulu. Ini gw tulis disini biar gak lupa aja :v
