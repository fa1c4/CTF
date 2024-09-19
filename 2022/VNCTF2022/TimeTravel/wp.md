# Time Travel

Two phases:
### First Phase
check the date
```c
  sub_4019F7();
  printf(&Format);
  scanf("%s", input_date);
  processing_date(processed_date, input_date);
  for ( i = 0; i <= 3; ++i )
  {
    if ( dword_404040[i] != processed_date[i + 28] )
    {
      i = 2;
      v7 = 0;
      while ( i <= 3 )
      {
        for ( j = 1; j <= 4; ++j )
          *((_BYTE *)&unk_4040E0 + 6 * i + j) = input_date[v7++];
        ++i;
      }
      sub_40188E();
      printf(&byte_405120);
      exit(0);
    }
  }
  sub_401CAA(input_date);
```

we have `processed_date` data, then reverse `processing_date` function
```c
__int64 __fastcall processing_date(__int64 a1, unsigned int *a2)
{
  __int64 result; // rax
  int v3; // esi
  int v4; // ebx
  int v5[36]; // [rsp+20h] [rbp-B0h]
  unsigned int v6; // [rsp+B0h] [rbp-20h]
  unsigned int v7; // [rsp+B4h] [rbp-1Ch]
  unsigned int v8; // [rsp+B8h] [rbp-18h]
  unsigned int v9; // [rsp+BCh] [rbp-14h]
  int i; // [rsp+CCh] [rbp-4h]

  v6 = _byteswap_ulong(*a2);
  v7 = _byteswap_ulong(a2[1]);
  v8 = _byteswap_ulong(a2[2]);
  v9 = _byteswap_ulong(a2[3]);
  v5[0] = v6 ^ 0xA3B1BAC6;
  v5[1] = v7 ^ 0x56AA3350;
  v5[2] = v8 ^ 0x677D9197;
  result = v9 ^ 0xB27022DC;
  v5[3] = v9 ^ 0xB27022DC;
  for ( i = 0; i <= 31; ++i )
  {
    v3 = i + 4;
    v4 = v5[i];
    v5[v3] = sub_401A3B(v5[i + 3] ^ v5[i + 2] ^ (unsigned int)v5[i + 1] ^ dword_405040[i]) ^ v4;
    result = (unsigned int)v5[i + 4];
    *(_DWORD *)(a1 + 4i64 * i) = result;
  }
  return result;
}
```

we have `dword_405040` then reverse `sub_401A3B`
```c
__int64 __fastcall sub_401A3B(int a1)
{
  return a1 ^ (unsigned int)(__ROL4__(a1, 13) ^ __ROR4__(a1, 9));
}
```

we can the the date is `20211205`

### Second Phase 
```c
  printf(&byte_405144);                         // song of fulai
  scanf("%s", input_song);
  processing_song(processed_song, input_song);
  for ( i = 0; i <= 5; ++i )
  {
    v4[4 * i] = (unsigned __int8)processed_song[i + 60];
    v4[4 * i + 1] = (unsigned __int8)BYTE1(processed_song[i + 60]);
    v4[4 * i + 2] = (unsigned __int8)BYTE2(processed_song[i + 60]);
    v4[4 * i + 3] = HIBYTE(processed_song[i + 60]);
  }
  for ( i = 1; i <= 23; ++i )
    v4[i - 1] ^= (v4[i - 1] % 0x12u + v4[i] + 5) ^ 0x41;
  for ( i = 0; i <= 23; ++i )
  {
    if ( v4[i] != dword_404080[i] )
    {
      for ( i = 0; i <= 5; ++i )
      {
        for ( j = 0; j <= 5; ++j )
          *((_BYTE *)&unk_4040E0 + 6 * i + j) = 14;
      }
      sub_40188E();
      printf(&byte_405158);
      exit(0);
    }
  }
  sub_402193(input_song);
```
input the correct date, then extract correct `dword_404080` while debugging

the process below is not reversible
```c
  for ( i = 1; i <= 23; ++i )
    v4[i - 1] ^= (v4[i - 1] % 0x12u + v4[i] + 5) ^ 0x41;
```
we need DFS to traverse all possibilities
then, reverse the `processing_song`
```c
void __fastcall processing_song(__int64 processed_song, __int64 input_song)
{
  int v2; // esi
  unsigned int v3; // [rsp+28h] [rbp-8h]
  int i; // [rsp+2Ch] [rbp-4h]
  int idx; // [rsp+2Ch] [rbp-4h]

  for ( i = 0; i <= 5; ++i )
    *(_DWORD *)(4i64 * i + processed_song) = char2int((char *)(4 * i + input_song));
  idx = 6;
  v3 = 0;
  while ( idx <= 65 )
  {
    if ( idx % 6 )
    {
      *(_DWORD *)(4i64 * idx + processed_song) = *(_DWORD *)(4i64 * idx - 24 + processed_song) ^ *(_DWORD *)(4i64 * idx - 4 + processed_song);
    }
    else
    {
      v2 = *(_DWORD *)(4i64 * idx - 24 + processed_song);
      *(_DWORD *)(4i64 * idx + processed_song) = v2 ^ subproc(*(unsigned int *)(4i64 * idx - 4 + processed_song), v3++);
    }
    ++idx;
  }
}
```
we need `processed_song[60-65]`, write the formula of process above
```python
if idx % 6 != 0:
    song[idx] = song[idx-6] ^ song[idx-1]
else:
    song[idx] = song[idx-6] ^ subproc(song[idx-1])
```

reverse the `subproc`
```c
__int64 __fastcall subproc(unsigned int a1, int pnum)
{
  char num_arr[28]; // [rsp+20h] [rbp-20h] BYREF
  unsigned int v4; // [rsp+3Ch] [rbp-4h]

  sub_401EFB(a1, num_arr);
  sub_401F67(num_arr, 1i64);
  v4 = sub_401EA7(num_arr);
  return v4 ^ dword_4050C0[pnum];
}

__int64 __fastcall sub_401F67(__int64 num_arr, int shift_bit)
{
  __int64 result; // rax
  int v3[6]; // [rsp+0h] [rbp-20h]
  int v4; // [rsp+18h] [rbp-8h]
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 3; ++i )
    v3[i] = *(_DWORD *)(4i64 * i + num_arr);    // 0 1 2 3
  result = (unsigned int)shift_bit;
  v4 = shift_bit;
  for ( i = 0; i <= 3; ++i )
  {
    *(_DWORD *)(num_arr + 4i64 * i) = v3[v4++]; // 1 2 3 0
    result = (unsigned int)(v4 % 4);
    v4 %= 4;
  }
  return result;
}
```

left rotate shift the num_arr(4 bytes) number by byte 

DFS get the possible `v4`, then compute the `processed_song[0-59]`
reverse to the input_song, get the second phase input

finally, input two phases correct texts, get the flag.
