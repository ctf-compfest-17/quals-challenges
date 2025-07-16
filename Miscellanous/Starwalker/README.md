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
* Some specialized opcodes need caching. You can check for this yourself by dissasembling a function with a specialized opcode with `dis.dis` and turning on `show_caches`. Most of the time, this will fix crashes.

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
