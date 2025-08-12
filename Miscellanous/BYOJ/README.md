# Build Your Own Jail

by Zanark

---

## Flag

```
COMPFEST17{h0w_d1d_y0u_g3t_h3re?_w3ll_gr4tz_44157bcbb6}
```

## Description
Create your own pyjail by just providing characters to be whitelisted!

`nc <ip>:<port>`

## Difficulty
Tingkat kesulitan soal: hard

## Hints
* hint 1

## Tags
pyjail

## Deployment
Make sure env variable `FILENAME` ada pas mau deploy pake docker compose, kalo mau gampang bisa pake build.sh nya, otherwise kalo gk mau pake docker compose tinggal di edit biar pake docker build trus di pas `--build-arg filename=<filename>`
