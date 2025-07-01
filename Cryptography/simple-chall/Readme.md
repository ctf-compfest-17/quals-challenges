# Simple Chall

by fele

---

## Flag

```
COMPFEST17{1dK_bUt_5uB53t_5Um_15_345Y_r19hT_5a581d63c1}
```

## Description
It seems like there's nothing wrong.

## Difficulty
Tingkat kesulitan soal: easy-medium

## Hints
* hint 1
* hint 2
* hint dst.

## Tags
lattice, modular subset sum, knapsack, cvp

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
