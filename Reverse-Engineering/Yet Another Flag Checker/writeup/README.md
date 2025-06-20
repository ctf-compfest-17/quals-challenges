# Writeup <Yet Another Flag Checker>

Checker berbentuk suatu binary tree dibuat dari functions dan if clauses.  
Karena dalam binary tree untuk tiap node hanya ada satu path, maka kita bisa iterasi ke tiap node (jumlahnya node kecil) untuk mencari checksum yang tepat.

Conditionals yang ada pada setiap fungsi sebenarnya cuma ada 3 bentuk:
- `v[x] == y`
- `v[x] + v[y] == z`
- `(v[x] | v[y]) - (v[x] & v[y])) == z`

Langkah-langkah:
1. Scrape decompilation dari setiap fungsi.
2. Modelkan fungsi-fungsi sebagai binary tree.
3. Iterasi tiap path node sampai dapet checksum yang bener.
4. Scrape conditionals untuk path. 
5. z3.
