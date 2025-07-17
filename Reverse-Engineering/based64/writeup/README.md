# Based64 writeup

Base64 encoding tapi buat dapet karakternya kita pake Knight Tour grid 8x8 dengan starting point tournya angka-angka 6-bit hasil algo base64 sebelum di encode ke karakter dan end pointnya jadi index buat tabel transformasi yang bakal kasih index karakter ke berapa di list karakter base64.


Solvenya honestly tinggal copas algo Knight's Tournya (versi dengan Warnsdorff's Rule) dari hasil dekompilasi (harus liat method `ikt` dan `kt`) terus tinggal jalanin sekali buat tiap index buat dapetin tour-tour dan langkah ke berapa dari tour yang di decide sebagai stopping point buat tour yang mulai dari index `x`. Ini dilakuin biar 1-1 mapping, soalnya sblmnya gk pake dan gk 1-1 solusinya acak adul 1M possibilities yang harus diliat. Dapet mapping, tinggal reverse base64 nya.


Yang bikin susah disini adalah hasil kompilasi native-image GraalVM, even with debug info dan -O0, masih ada beberapa optimisasi yang dilakukan (kyk for loop yang jumlah loopnya konstan literally jadi if else panjang) dan harus ngerti juga Java pass by value and reference, soalnya hasil kompilasi ada yg di pass ke method call literally suatu angka, yang kalo gk tau bakal ngira something else, ternyata address. Pasti ada perlu dynamic analysis buat mahamin jg ini ngapain. But idk if LLMs work, saya tidak coba karena tidak ingin feed info (pas gw pake karena wajib di PPL, like di sprint 3 or 4 datanya udh masuk training gw gk kasih context yang sesuai, hasil generasi kodenya sesuai nama fungsi"nya dengan yang udah ada :v). 
