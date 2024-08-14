# babyvxworks

32bits x86 arch, drag into IDA, search the string
xref from "Plz Input Flag: ".
found the main function is started from 0x3D0, then read the asm code and patched obfuscating instruction "E8"
delete un-reasoning function start, set the the end of function 0x3D0 at 0x8ED 
F5 then we got

```cpp
int sub_3D0()
{
  int v0; // ebx
  int v1; // eax
  const char *v2; // ebx
  int v4; // [esp+14h] [ebp-C4h]
  int v5; // [esp+18h] [ebp-C0h]
  int v6; // [esp+1Ch] [ebp-BCh]
  int v7[2]; // [esp+20h] [ebp-B8h] BYREF
  char v8[52]; // [esp+28h] [ebp-B0h] BYREF
  char v9[124]; // [esp+5Ch] [ebp-7Ch] BYREF

  sub_32B0(v8, 0, 48);
  sub_32B0(v9, 0, 120);
  v7[0] = 0;
  sub_2BF0(v7, v8, 48);
  sub_2BF0(v7, v9, 120);
  v5 = 0;
  qmemcpy(v8, dword_126F8, 0x30u);
  sub_32D0("Plz Input Flag: ");
  sub_33C0("%s", v8);
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 0, 4) = 188;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 4, 4) = 10;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 8, 4) = 187;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 12, 4) = 193;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 16, 4) = 213;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 20, 4) = 134;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 24, 4) = 127;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 28, 4) = 10;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 32, 4) = 201;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 36, 4) = 185;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 40, 4) = 81;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 44, 4) = 78;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 48, 4) = 136;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 52, 4) = 10;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 56, 4) = 130;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 60, 4) = 185;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 64, 4) = 49;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 68, 4) = 141;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 72, 4) = 10;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 76, 4) = 253;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 80, 4) = 201;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 84, 4) = 199;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 88, 4) = 127;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 92, 4) = 185;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 96, 4) = 17;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 100, 4) = 78;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 104, 4) = 185;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 108, 4) = 232;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 112, 4) = 141;
  *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 21, v9, 116, 4) = 87;
  v4 = sub_34C0(v8);
  v0 = 0;
  if ( v4 <= 0 )
    goto LABEL_7;
  do
  {
    v1 = sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 24, v8, v0, 0);
    ((void (__cdecl *)(int, int))loc_330)(v1, v4);
    v6 = *(unsigned __int8 *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 26, v8, v0, 1);
    if ( *(_DWORD *)sub_2450("C:/WindRiver/workspace/helloworld/helloworld.c", 26, v9, 4 * v0, 4) == v6 )
      ++v5;
    ++v0;
  }
  while ( v0 < v4 );
  if ( v5 == 30 )
    v2 = "Success";
  else
LABEL_7:
    v2 = "Try Again";
  sub_3350(v2);
  sub_2930(v7);
  return 0;
}
```

`sub_2450` function returns the `v9 + 4*n` data reference, so the matching data array is
```c
int array[] = { 
                188, 10, 187, 193, 213, 134, 127, 10, 
                201, 185, 81, 78, 136, 10, 130, 185, 
                49, 141, 10, 253, 201, 199, 127, 185, 
                17, 78, 185, 232, 141, 87
            };
```

`sub_330` is recursive encryption function with iteration number 30 (`if ( v5 == 30 )`)
```cpp
int __cdecl start(unsigned int a1, unsigned int a2, int a3, int a4)
{
  int v4; // eax
  bool v6; // zf
  unsigned int v7; // eax
  int v8; // eax
  int v9; // [esp-8h] [ebp-18h] BYREF
  int v10; // [esp-4h] [ebp-14h]
  _BYTE *v11; // [esp+0h] [ebp-10h]
  _BYTE *v12; // [esp+4h] [ebp-Ch]
  int v13; // [esp+8h] [ebp-8h]
  _DWORD *savedregs; // [esp+10h] [ebp+0h] BYREF

  sub_80(a1, a2, a3, a4);
  sub_13FC0();
  sub_B0();
  sub_1A0(a1, a2);
  sub_D0(a3);
  sub_4CF0(a4);
  v4 = sub_3D0();
  sub_3250(v4);
  while ( 1 )
  {
    savedregs = &savedregs;
    v13 = 0;
    if ( !a2 )
      return 1;
    v12 = (_BYTE *)sub_2450((int)"C:/WindRiver/workspace/helloworld/helloworld.c", 10, a1, 0, 1, v10);
    *v12 ^= 0x22u;
    v11 = (_BYTE *)sub_2450((int)"C:/WindRiver/workspace/helloworld/helloworld.c", 11, a1, 0, 1, v10);
    v6 = *v11 == 0xFD;
    *v11 += 3;
    if ( v6 || !v6 )
      goto LABEL_8;
    v7 = (unsigned int)&v9 ^ 0x22;
    if ( ((unsigned int)&v9 ^ 0x22) != v10 )
    {
      v8 = ((int (*)(void))((char *)&loc_3D3 + 2))();
      if ( v6 )
        goto LABEL_10;
LABEL_8:
      v7 = a2;
    }
    v8 = v7 - 1;
LABEL_10:
    v9 = v8;
  }
}
```

flag_data related operation is `^= 0x22` and `+= 3`
so the whole logic of flag process is 
- for each byte in flag
-   byte ^= 0x22
-   byte += 3
-   comparing with array bytes

write the reverse, see `rev.cpp`
