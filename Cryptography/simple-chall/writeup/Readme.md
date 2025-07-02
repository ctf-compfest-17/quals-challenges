# Writeup Simple Chall

- Challenge ini merupakan implementasi dari knapsack, multiple modular subset sum problem dengan sedikit modifikasi untuk total. Solvernya dapat dilihat dari sini https://github.com/josephsurin/lattice-based-cryptanalysis/blob/main/lbc_toolkit/problems/knapsack.sage 

- Untuk modifikasi pada bagian total dapat kita selesaikan dengan mengonstruksi sebuah matriks M dan mereduksinya dengan gaussian. 

f_i ≡ total_i^-1 * g_i (% mod)

f_i * total_i ≡ g_i (% mod)

f_i * total_i = g_i + mod * k, k ∈ Z

g_i = f_i * total_i - mod * k, k ∈ Z

Kemudian kita dapat menyusun matrix M yang terdiri atas vektor (1, f_i) (0, mod)
Dengan kedua vektor tersebut, kita dapat membuat lattice dari kedua vektor diatas.
L = {x(1, f_i) + y(0, mod) | x, y ∈ Z}
L = {(x, x * f_i + y * mod) | x, y ∈ Z}
Singkatnya jika kita reduksi matriks M dengan gaussian, kita akan mendapatkan vektor (total_i, g_i).
Sehingga, kita dapat membentuk M = [[1, total_i], [0, mod]] kemudian direduksi dengan gaussian.

Dengan demikian kita akan mendapatkan total_i nya dan dapat kita masukkan ke dalam solver.
Sumber : https://blog.csdn.net/u010883831/article/details/122660103 nomor 6