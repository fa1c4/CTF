# asm

2024, we use IDApro-9.0 to decompile the asm binary program (IDApro-8.xx cant decompile, need to read asm code)

find the key function `sub_101A6`
```c
__int64 sub_101A6()
{
  char v1[104]; // [sp+190h] [-80h] BYREF
  int v2; // [sp+1F8h] [-18h]
  int i; // [sp+1FCh] [-14h]
  __int64 vars0; // [sp+200h] [-10h] BYREF

  sub_104D6("flag plz");
  sub_104E0("%80s", v1);
  v2 = sub_1052C(v1);
  for ( i = 0; i < (__int64)v2; ++i )
    *((_DWORD *)&vars0 + i - 128) = (97 * i % 256) ^ (unsigned __int8)(*((_BYTE *)&vars0 + (i + 1) % 31 - 112) ^ *((_BYTE *)&vars0 + i - 112));
  for ( i = 0; i < (__int64)v2; ++i )
  {
    if ( *((_DWORD *)&vars0 + i - 128) != (__int64)dword_1EBA0[i] )
      return 0LL;
  }
  sub_104D6("OK");
  return 0LL;
}
```

checking logic:
```python
flag[0] ^ flag[1] ^ (97 * 0 % 256) == dword_1EBA0[0]
flag[1] ^ flag[2] ^ (97 * 1 % 256) == dword_1EBA0[1]
flag[2] ^ flag[3] ^ (97 * 2 % 256) == dword_1EBA0[2]
...
flag[30] ^ flag[0] ^ (97 * 30 % 256) == dword_1EBA0[30]
```

export the check data, xor back to the flag
```c
int dword_1EBA0[32] = {
    17, 118, 208, 30, 153, 182, 44, 145,
    18, 69, 251, 42, 151, 198, 99, 184,
    20, 124, 225, 30, 131, 230, 69, 160,
    25, 99, 221, 50, 164, 223, 113, 0
};
```
