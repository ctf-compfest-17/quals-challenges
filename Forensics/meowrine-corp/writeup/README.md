# Writeup Meowrine Corp


> The first step rely on the description of the challenge, so if you think the description is not clear enough or is making it too obvious, let me know and I'll change it





## Step 1:

From the description, we know that the admiral's computer got hacked and that the hacker managed to get access to it. The most common way a hacker gain access to a machine is via a reverse shell. In a reverse shell, the hacker will do all the commands via powershell termimal. A quick google search or asking a LLM would show that powershell commands are logged by the powershell script block logging, where the logs could be found at `Microsoft-Windows-PowerShell%4Operational.evtx`


## Step 2:

Looking at the logs, we see that the hacker is adding some registry key with their values set to a really long string. We also see a log which show the attacker making a powershell script which collects the value of the registry keys, combine them, base64 decode them, then run them with iex. The registry keys are not added in order so we could determine the correct order from the powershell script.

## Step 3:


After decoding the base64, we see that it is a powershell script which is still obfuscated. However, the script is deobfuscating itself, so you could just print the variable (this is intended). After we deobfuscate it, we will finally get the readable powershell script.

## Step 4:

After analyzing the script, we learn that the script compresses all the files inside the Documents folder, generate a key and iv, encrypt the zip file with aes through `[System.Security.Cryptography.Aes]::Create()`. The default setting is aes cbc. It then appends the key to the start of the zip file and the iv to the end. With that knowledge, we could make a decrypt script

## Step 5:

We could export objects -> http, then export the data from the pcapng file. Then using the decrypt script we made in step 4, deecrypt that into a zip file, unzip it, then find the flag in `Hexpaws.pdf`


