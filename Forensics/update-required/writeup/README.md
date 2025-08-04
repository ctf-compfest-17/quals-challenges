# Writeup <Update Required>

Analysis the pcap file until you found http request and than dump the executeable file. After that, reverse engineer and analyze how the binary file works. Once the executable was extracted from the HTTP request in the PCAP file, we proceeded with static analysis using disassembly and reverse engineering tools.

The binary is a Rust-based ransomware, and the execution flow is relatively straightforward and linear.
Here's the step-by-step breakdown of what happens when the binary runs:
1. encrypt_file_and_split:
this function will open the victim target file which was secret.pdf and than encrypt it using AES with the key and iv from the generate_key_iv function and than split the encrypted file into 3 parts.
2. generate_key_iv:
this function will generate each key and iv from 2 strings where the key is derived from hashing two hardcoded strings: "Mondstadt4Ever" and "KleeLovesBoom", and the IV s created by taking the MD5 hash of "KleeLovesBoom" and reversing the byte order.
3. send_parts:
send each parts to attacker from tcp connection
4. destroy_original:
delete the original file from the victim device

From our static analysis, we know that the encrypted file was split and transmitted via TCP. We use the following Wireshark filter: "ip.dst == 192.168.129.92 && tcp.port == 1337", We identify TCP streams 25 through 27, corresponding to the three encrypted parts. By dumping the data from these streams and reassembling them in the correct order, we obtain the full encrypted file.

Once the encrypted file is reassembled, we proceed to decrypt it using decrypt.py, which performs AES decryption with the correct key and IV derived from the binary. This yields a password-protected PDF. Now, we must retrieve the password to open this PDF. As stated in the challenge description, the password is the MetaMask seed phrase. However, the seed phrase is itself protected by the MetaMask vault password, which we need to recover next.

According to the challenge desc, the user once copied the MetaMask password to the clipboard. Based on this [article](https://www.inversecos.com/2022/05/how-to-perform-clipboard-forensics.html),  we examined the ActivitiesCache.db file.
There, we found a base64-encoded clipboard payload. Decoding it revealed the MetaMask password : m0ndstadtc1ty0fFr33dom .Once we recover the MetaMask password from the clipboard data, we can unlock the MetaMask vault and retrieve the seed phrase.

With the password recovered, we extracted the MetaMask vault data from the browser extension files. Following the steps outlined in this [guide](https://medium.com/coinmonks/lost-metamask-wallet-the-forensic-way-c1871c3768f3), we will get a payload in the 000003.log file :

{"data":"JPdHpmJRSorA6uK+FpStxHl4arQUMBM9RUcaicyzPy/5ZKBirApyEwoEDj+hzUOUEHMp4I/mWHvRy4LpJ4V/ViF+l5hF5PFpVl/Jza9uSvG3Asy3q5IO0yaX0he8PHrJ2A13Zgyu+21VVxKaAAZ1W+Qsmv9uXcIyzkAyYS13horUtOA1/1vpk72ja/048ht3mypgHd7FgK/GfbMlcG8LfY79Ee2lsnihkl5+T6GejPpU54CN/XGKPnFVHxgGLVsyeIy2ClwaJn25MkM5y+tEGIZ3XQpjFTaUZDdblZxCchC2gC16efPayi2yWjJbu7L0aocgJp2MBQC+fWduK11Xk/VDmPUgKRobzzGFr8LGZjEsAzC+rKdR/lT46iAmQyVS2qIY9BYBNQTLUpgjOeI6/trJR1vqzGVxFrcj+IX63PsQN101WsWADisHkRIZJJkSDPcnRigoUnvWwQH2NmG45tKjB3u6aN/vz0ytWpJK5Bs4riUNJXM/yCpzO0wn3n+kfNvp/S09u0RXxmoTXNvPytzvviaToEykyJFuT9uNUqLCPuCgckzN+rcga3AEmpZg62pDJHg+tv+/qYtRu7Ml1UVxy9DnR6cKOEQuPkYifCk/a1r+/hk7QLaT8iei0g==","iv":"RygWvnoMS5oyTq94H3KiIw==","keyMetadata":{"algorithm":"PBKDF2","params":{"iterations":600000}},"salt":"d0m0kTp3az079GbowRiRtAVORc3wHNLbXJ9llvFkTKo="} 

Using MetaMask Vault Decryptor and the recovered password, we decrypted the vault and successfully extracted the seed phrase.
With the seed phrase obtained, we can finally use it as the password to unlock the PDF and get the flag.