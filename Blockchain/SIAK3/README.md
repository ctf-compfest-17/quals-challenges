# SIAK3

by xymbol

---

## Flag

```
COMPFEST17{makanya_bikin_tanda_tangan_jangan_ngasal_ntar_bisa_dicontek_ama_orang_8dca2abe7a}
```

## Description
Next version of SIAK-NG! SIAK3!
Bob paid his previous tuition fees using SIAK3,
but he seems to have forgotten his privkey.
Accidentally, his wallet has a bug that creates a vulnerable signature for his previous payments.
He only remembers that his privkey contains the keyword 'cafe'.
Can you help him retrieve his privkey and pay his tuition?

## Difficulty
Tingkat kesulitan soal: medium-hard

## Hints
* 

## Tags
Solidity

## Deployment
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    cd src && cd images && ./build.sh && cd .. && cd challenge-eth && docker compose -p siak3 up --build -d
    ```
- Stop the container using:
    ```
    cd src && docker compose -p siak3 down --volumes
    ```

## Notes
Tambahan informasi untuk soal, deployment, atau serangan yang mungkin terjadi pada service soal
