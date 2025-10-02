
## Vuln 1</br >
randomnya predictable karena itu cuman lcg yg ditruncated sbnyk n lsb. Solvernya makek hnp tapi mungkin aja ada cara lain </br >
Solver : `solve_rand.sage`</br >

Nb : Ada chance gagal predict tapi harusnya kecil kemungkinannya</br >

## Vuln 2</br >
rounds dari md5 hashnya gak lengkap, jadi kita bisa cari first preimage dari hashnya</br >
POC : `crack_hash.py`</br >
Test : `test_hash.py`</br >
Solver : `solve_hash.py`</br >


Ref : </br >
https://ctftime.org/writeup/38725</br >
https://github.com/oranav/ctf-writeups/blob/master/36c3/md15/solve.py </br >
