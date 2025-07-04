# Writeup Meowrine Corp

TL;DR (Nanti dibikin lengkapnya)

check evtx log di Applications and Services Logs > Microsoft > Windows > PowerShell > Operational. Filter untuk event id 4104(script block logging) dan lihat ada command untuk menambahkan value di 4 lokasi registry yang berbeda, salah satunya adalah di HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run. lihat disitu dan lihat bahwa valuenya merupakan sebuah powershell command yg mengambil value dari 3 registry lainnya, lalu digabung dan di run.

Value yang digabungkan merupakan sebuah powershell command yang memiliki beberapa layer encoding/obfusctation yaitu base64->reverse order->base64->string building dengan regex->hex encoding

setelah di deobfuscated, bisa dilihat bahwa scriptnya ngezip semua content dari folder Documents dan di encrypt dengan aes dengan key dan iv yang di hardcode lalu dikirim ke server. Tinggal cari http requestnya di pcap, dump datanya, lalu decrypt dan unzip. Flagnya ada di salah satu pdfnya.


