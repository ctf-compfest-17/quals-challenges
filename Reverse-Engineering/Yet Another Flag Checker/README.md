# Yet Another Flag Checker

by AdamRayyan

---

## Flag

```
COMPFEST17{it5_sm4r7_bu7_als0_v3ry_d4ng3r0u5_ccb390b346}
```

## Description
Is it really a CTF without a flag checker challenge?
> Note: password matches the following regex: 
> ```regex
> ^[A-Za-z0-9]+$
> ```
## Difficulty
Tingkat kesulitan soal: medium-hard

## Hints
-

## Tags
c++, flag checker

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
Tambahan informasi untuk soal, deployment, atau serangan yang mungkin terjadi pada service soal
