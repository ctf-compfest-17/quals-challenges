# Writeup Neutral Evil

## Vulnerability
- Missing null byte (info leak).
- Protected (somewhat) stack overflow.

## Limitations
- Cannot overwrite saved return address.
- The "win" function checks for 16 byte alignment.
- Stack space of `encounter` gets cleared.
- 10 Second timeout at `encounter`.

## Exploit Flow
- Leak rbp at `start`.
- Overwrite saved rbp at `encounter` to point at `start` buffer data.
- Also overwrite buffer data at `start` to create a fake stack frame.
- Return address of the fake stack frame is the `read_log` function.
- Flag printed.


## Notes
This is what the stack layout looks like on `encounter` after inputting "Jhonny" and "I cast fireball":
```
0x00007fffffffe3f0│+0x0000: "I cast fireball\n"	← $rsp
0x00007fffffffe3f8│+0x0008: "ireball\n"
0x00007fffffffe400│+0x0010: 0x0000000000000000
0x00007fffffffe408│+0x0018: 0x00007ffff7ffe310  →  0x0000000000000000
0x00007fffffffe410│+0x0020: 0x00007fffffffe440  →  0x00007fffffffe460  →  0x00007fffffffe500  →  0x00007fffffffe560  →  0x0000000000000000	← $rbp
0x00007fffffffe418│+0x0028: 0x0000000000401473  →  <start+0048> call 0x401378 <cleaner>
0x00007fffffffe420│+0x0030: "Jhonny\n"
0x00007fffffffe428│+0x0038: 0x0000000000000000
0x00007fffffffe430│+0x0040: 0x0000000000000000
0x00007fffffffe438│+0x0048: 0x0000000000000000
0x00007fffffffe440│+0x0050: 0x00007fffffffe460  →  0x00007fffffffe500  →  0x00007fffffffe560  →  0x0000000000000000
0x00007fffffffe448│+0x0058: 0x000000000040149c  →  <main+0021> mov edi, 0x4021f8
```
Basically we leak +0x50, then overwrite +0x20 to point to +0x30 which at +0x38 contains the `read_log+1` address.
Plus one is to avoid `push rbp` which make the stack unaligned, alternatively you can also put the return address at +0x30 and point rbp at +0x28 instead

That's about it, I wanted to make it more annoying (e.g. making the read ridiculously huge without benefit to throw off anyone relying on piping/simple non pwntools IO) but I couldn't really make it work.
