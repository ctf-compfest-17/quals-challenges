# Build Your Own Jail

by Zanark

---

## Flag

```
COMPFEST17{h0w_d1d_y0u_g3t_h3re?_w3ll_gr4tz_44157bcbb6}
```

Mirror
```
COMPFEST17{c0ngr4ts_y0u_f0uNd_th3_s3crE7!_98f4e10bec}
```

## Description
Create your own pyjail by just providing characters to be whitelisted!

Note: The remote server enforces a Proof-of-Work to mitigate bruteforcing attempts. All you have to do to get access is to what you are told in the terminal.

Note2: The remote server does not have internet access.

`nc <ip>:<port>`

## Difficulty
Tingkat kesulitan soal: hard

## Hints
* hint 1

## Tags
pyjail

## Deployment
Make sure env variable `FILENAME` ada pas mau deploy pake docker compose, kalo mau gampang bisa pake build.sh nya, otherwise kalo gk mau pake docker compose tinggal di edit biar pake docker build trus di pass `--build-arg filename=<filename>`. Tolong juga make sure containernya gk bisa create out-going request, if possible coba block egressnya, di `docker-compose.yml` cuma masukin invalid DNS address jadi kalo masukin nama domain gk bakal ke resolve, tapi kalo masukin ip masih memungkinkan ke resolve (selama hal itu allowed dari yg megang ip nya). Alternatively maybe jalanin 2 container? 1 proxy buat ke container internal, 1 ya container challenge yg networknya internal.
