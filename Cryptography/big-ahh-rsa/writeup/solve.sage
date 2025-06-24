from pwn import *
from Crypto.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
from decimal import Decimal
def coppersmith_howgrave_univariate(pol, modulus, beta, mm, tt, XX):
    """
    Coppersmith revisited by Howgrave-Graham
    
    finds a solution if:
    * b|modulus, b >= modulus^beta , 0 < beta <= 1
    * |x| < XX

    # Copyright : David Wong
    # Github : https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/coppersmith.sage

    """
    #
    # init
    #
    dd = pol.degree()
    nn = dd * mm + tt

    #
    # checks
    #
    if not 0 < beta <= 1:
        raise ValueError("beta should belongs in (0, 1]")

    if not pol.is_monic():
        raise ArithmeticError("Polynomial must be monic.")

    # Coppersmith revisited algo for univariate
    # change ring of pol and x
    polZ = pol.change_ring(ZZ)
    x = polZ.parent().gen()
    # compute polynomials
    gg = []
    for ii in range(mm):
        for jj in range(dd):
            gg.append((x * XX)**jj * modulus**(mm - ii) * polZ(x * XX)**ii)
    for ii in range(tt):
        gg.append((x * XX)**ii * polZ(x * XX)**mm)
    
    # construct lattice B
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        for jj in range(ii+1):
            BB[ii, jj] = gg[ii][jj]
    # LLL
    BB = BB.LLL()
    # transform shortest vector in polynomial    
    new_pol = 0
    for ii in range(nn):
        new_pol += x**ii * BB[0, ii] / XX**ii
    # factor polynomial
    potential_roots = new_pol.roots()
    # test roots
    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = polZ(ZZ(root[0]))
            if gcd(modulus, result) >= modulus^beta:
                roots.append(ZZ(root[0]))
    return roots


def get_p(N, pa):
    """Returns a factor p of N or None given N = pq and an approximation of p."""
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL'); 
    pol = x - pa
    dd = pol.degree()
    beta = 0.5                             # we should have q >= N^beta
    epsilon = beta / 7                     # <= beta/7
    mm = ceil(beta**2 / (dd * epsilon))    # optimized
    tt = floor(dd * mm * ((1/beta) - 1))   # optimized
    XX = ceil(N**((beta**2/dd) - epsilon)) # we should have |diff| < X
    
    # Coppersmith
    
    roots = coppersmith_howgrave_univariate(pol, N, beta, mm, tt, XX)
    if roots:
        return pa - roots[0]

    
def get_approx_p_pm_q(N, e, x, y, prec=1000):
    """Returns an approximate p+q and p-q given N, e, x, y such that 

        ex - (p^4 - 1)(q^4 - 1)y = w and N=pq
     """
    # Increase the precision
    RF = RealField(prec)
    # Convert inputs to high-precision real numbers
    N, e, x, y = RF(N), RF(e), RF(x), RF(y)
    # Perform the computation with high precision
    p_plus_q = floor(sqrt(abs((N+1)**2 - (e*x)/y)))
    p_minus_q = floor(sqrt(abs((N-1)**2 - (e*x)/y)))
    return p_plus_q, p_minus_q

def factor_N(N, e, prec=None):
    """Returns the factors p, q of N or None given the public key (N, e). 
    """
    precision = prec if prec else 3*N.bit_length()
    r = (e)/(N**2 + 1 - (9/4)*N)
    cf = r.continued_fraction()
    for i, xy in enumerate(cf.convergents()[1:]):
        x = xy.denominator()
        y = xy.numerator()
        p_plus_q, p_minus_q = get_approx_p_pm_q(N, e, x, y, precision)
        pa = int((p_plus_q + p_minus_q)/2)
        p = get_p(N, pa)
        if p:
            return p, N//p 
    return None, None

if __name__ == "__main__":
    #proc = remote("localhost", 1337)
    proc = process(["python3", "../src/src.py"])
    proc.recvuntil(b"N:")
    N = int(proc.recvline().strip())
    bound = round((2*N).sqrt().sqrt())
    proc.recvuntil(b"Enter bound: ")
    print(f"Bound: {bound}")
    proc.sendline(str(bound).encode())
    proc.recvuntil(b"e:")
    e = int(proc.recvline().strip())
    proc.recvuntil(b"ct:")
    ct = int(proc.recvline().strip())
    p, q = factor_N(N, e)
    phi = (p**2 - 1) * (q**2 - 1)
    d = pow(e, -1, phi)
    m = pow(ct, d, N)
    flag = long_to_bytes(m)
    print(flag)


