# gumshoe writeup

[Reference](https://youtu.be/aF1Yw_wu2cM?si=8tmBGfX8JWnrmK2q)

Soal ini more or less nge implement compression algorithm yang dipake Gen 1 Pokemon games, cuma dengan versi lebih "modern", as in dibanding nge compress 2 bpp images, ini nge compress 24 bpp images. Raw 24 bpp imagenya basically pake BMP bagian pixel array datanya dan dari 3 color plane (RGB) di pecah jadi plane masing-masing, trus digabung jadi 1. 