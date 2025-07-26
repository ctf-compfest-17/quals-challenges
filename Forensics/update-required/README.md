# Update Required

by jay

---

## Flag

```
COMPFEST17{c0ngr@tulat1on_you_hav3_found_the_s3cret_and_here_is_y0ur_r3ward} 
```

## Description
A researcher in Mondstadt’s tech division received an urgent-looking HTML file, claiming to be a critical security patch. Trusting its source, they executed antivirus.exe — and moments later, a secret PDF file disappeared.

The PDF contained a confidential override PIN tied to the Vision Distribution Network. To secure it, the researcher encrypted the file using their MetaMask seed phrase, joined with an underscore (_) as the PDF password.

Although the MetaMask vault remains on disk, the password to unlock it is missing. Fortunately, there's a chance: the researcher had once copied the vault password to clipboard.

Zip password : soalinigasusahkokxixixixi

## Difficulty
Tingkat kesulitan soal: medium-hard

## Hints
* hint 1
* hint 2
* hint dst.

## Tags
Tags dari soal pisahkan koma (e.g: tags1, tags2, tags3)

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
