# Burhansweeper

by AdamRayyan

---

## Flag

```
COMPFEST17{i_m4y_h4v3_4_s3v3r3_4dd1c710n_to_b4l4tr0_5a021a3917}
```

## Description
bur bur bur bur burhanpedia


## Difficulty
Tingkat kesulitan soal: easy

## Hints
* hint 1
* hint 2
* hint dst.

## Tags
game, lua

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
