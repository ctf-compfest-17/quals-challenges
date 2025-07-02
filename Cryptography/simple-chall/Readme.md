# Simple Chall

by fele

---

## Flag

```
COMPFEST17{MuLt1pl3_m0du14r_5uB53t_5uM_w1th_4_l1ttl3_b1t_0f_m0d1f1c4t10n_3badbfd552}
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
lattice, multiple modular subset sum, knapsack, cvp

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
