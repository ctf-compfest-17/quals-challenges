# crash out writeup

1. Crash report is here: programdata/microsoft/windows/wer/reportarchive/AppCrash*/Report.wer, memory dump of the report is here: programdata/dumps/chrome_updater*.dmp
2. From the dump, you get several path leading to file.enc and 89a0b289f0221.zip and a password "whereourcrashis" (use strings https://isc.sans.edu/diary/22536)
3. users/evan/documents/89a0b*.zip unlock with "whereourcrashis" and you find script.py. reverse it
4. decrypt the file using the reversed script: users/evan/downloads/upload_queue/file.enc
5. edit the s0f0 header of jpg (after ff c0), reference: https://cyberhacktics.com/hiding-information-by-changing-an-images-height/