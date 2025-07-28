# Writeup ezzz jail
- Baca CVE-2025-22153 ada informasi kalo ada ExceptionGroup di older version of Restrictid Python Library
- Pake itu, tinggal trigger read flag lalu output pake error message (karena gak ada print function)