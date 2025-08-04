# Writeup Free Fire Encryption
I just modify this challenge
https://github.com/maple3142/My-CTF-Challenges/tree/master/AlpacaHack%20Round%209/ffmac

We're using the alternative solver since the oracle is not enough to recover the c1, c2, and c3.
I modified it to be polynomial of degree 2 instead of linear one, so we just need to adjust abit the A matrix and b vector, then adjust the key finding scheme.