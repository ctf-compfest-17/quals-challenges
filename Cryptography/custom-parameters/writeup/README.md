# Writeup Big Ahh RSA

This challenge is based on this paper https://eprint.iacr.org/2025/380.pdf

TL;DR the paper proves that you could use the generalized wienner attack (continued fractions + coppersmith method) against rsa/rsa-like systems with a d value that is too large.

The author of the paper provided a poc code for the exploit available here https://github.com/mseckept/generalized-wiener-attack

However, simply copy and pasting the code won't work because that code is used for phi = (p^4-1)(q^4-1) while this challenge uses 
phi = (p^2-1)(q^2-1). So we need to read the paper to find out how the code works and which part to modify

After reading the paper, it should be fairly obvious that we need to modify the get_approx_p_pm_q method and the r in factor_N method. The work for (p^2-1)(q^2-1) has already been done before on this paper https://eprint.iacr.org/2017/1076.pdf. Note that the paper provides the attack for a d value that is too small but now we know that we could use the same attack against a d value that is too large.

solve:
just run `solve.sage`

