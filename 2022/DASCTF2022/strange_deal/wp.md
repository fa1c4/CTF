# Strange Deal

1.UPX3.96 unpack the binary `upx.exe -d binary`
2.objcopy --dump-section pydata=pydump binary
3.`python pyinstxtractor.py pydump` using python version==3.10 (or cant extract pyz files)
4.010 editor recover the magic number of target.pyc through head 16 bytes of struct.pyc
```
6F 0D 0D 0A 00 00 00 00 70 79 69 30 01 01 00 00
```
5.pycdc target.pyc to get python source code
6.pycas to read python assembly to determine logic
7.xxTEA to decrypt data
8.RAS winner attack to decrypt data and get flag
