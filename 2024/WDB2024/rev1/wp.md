# rev1

apk reverse engine, JEB open and locate main logic at `MainActivity`
```java
package v0;

import android.view.View.OnClickListener;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;
import com.ctf.cma.Check;
import com.ctf.cma.MainActivity;

public final class b implements View.OnClickListener {
    public final MainActivity b;

    public b(MainActivity mainActivity0) {
        this.b = mainActivity0;
        super();
    }

    @Override  // android.view.View$OnClickListener
    public final void onClick(View view0) {
        String s = ((EditText)this.b.o.c).getText().toString().trim();
        if(s.isEmpty()) {
            return;
        }

        if(Check.validate(s)) {
            Toast.makeText(this.b, "Congratulations!!!", 0).show();
            return;
        }

        Toast.makeText(this.b, "Invalid flag", 0).show();
        ((EditText)this.b.o.c).getText().clear();
    }
}

package com.ctf.cma;

public class Check {
    static {
        System.loadLibrary("cma");
    }

    public static native boolean validate(String arg0) {
    }
}
```
`validate` function is from cma.so library
export all binary units using JEB, and IDApro open `easystd-export\com.ctf.cma\Libraries\x86_64\libcma.so.bin`

locate the crypto related functions
```c
char __fastcall validating(__int64 a1, __int64 a2, __int64 a3)
{
  const char *v3; // rbx
  int length; // r14d
  char *v5; // r15
  int v6; // ebp
  int v7; // ebp
  __int128 *content; // rbx
  __int64 cnt; // rax
  char v11[4]; // [rsp+8h] [rbp-B0h] BYREF
  char v12[132]; // [rsp+Ch] [rbp-ACh] BYREF
  unsigned __int64 v13; // [rsp+90h] [rbp-28h]

  v13 = __readfsqword(0x28u);
  v3 = (const char *)(*(__int64 (__fastcall **)(__int64, __int64, _QWORD))(*(_QWORD *)a1 + 0x548LL))(a1, a3, 0LL);
  key_gen(v11);                                 // origin_key == A11223574689900Z
  xmmword_3130 = 0LL;
  xmmword_3120 = 0LL;
  xmmword_3110 = 0LL;
  xmmword_3100 = 0LL;
  xmmword_30F0 = 0LL;
  xmmword_30E0 = 0LL;
  xmmword_30D0 = 0LL;
  xmmword_30C0 = 0LL;
  xmmword_30B0 = 0LL;
  xmmword_30A0 = 0LL;
  xmmword_3090 = 0LL;
  xmmword_3080 = 0LL;
  xmmword_3070 = 0LL;
  xmmword_3060 = 0LL;
  xmmword_3050 = 0LL;
  *(_OWORD *)input = 0LL;
  xmmword_3230 = 0LL;
  xmmword_3220 = 0LL;
  xmmword_3210 = 0LL;
  xmmword_3200 = 0LL;
  xmmword_31F0 = 0LL;
  xmmword_31E0 = 0LL;
  xmmword_31D0 = 0LL;
  xmmword_31C0 = 0LL;
  xmmword_31B0 = 0LL;
  xmmword_31A0 = 0LL;
  xmmword_3190 = 0LL;
  xmmword_3180 = 0LL;
  xmmword_3170 = 0LL;
  xmmword_3160 = 0LL;
  xmmword_3150 = 0LL;
  xmmword_3140 = 0LL;
  strcpy(input, v3);
  length = strlen(v3);
  if ( length == 16 )
  {
    enc_proc((__int64)v12, (unsigned __int8 *)input, &xmmword_3140);
  }
  else
  {
    v5 = input;
    v6 = (strlen(input) >> 4) + 16 - length % 16;
    if ( length % 16 < 16 )
      memset(&input[length], 0, (unsigned int)(15 - length % 16) + 1LL);
    if ( v6 )
    {
      v7 = -v6;
      content = &xmmword_3140;
      do
      {
        enc_proc((__int64)v12, (unsigned __int8 *)v5, content);
        v5 += 16;
        ++content;
        ++v7;
      }
      while ( v7 );
    }
  }
  cnt = -5LL;
  while ( byte_CB0[cnt + 5] == *((_BYTE *)&xmmword_3140 + cnt + 5)
       && byte_CB0[cnt + 6] == *((_BYTE *)&xmmword_3140 + cnt + 6)
       && byte_CB0[cnt + 7] == *((_BYTE *)&xmmword_3140 + cnt + 7)
       && byte_CB0[cnt + 8] == *((_BYTE *)&xmmword_3140 + cnt + 8)
       && byte_CB0[cnt + 9] == *((_BYTE *)&xmmword_3140 + cnt + 9) )
  {
    cnt += 5LL;
    if ( cnt >= 40 )
      return 1;                                 // success
  }
  return 0;                                     // fail
}

unsigned __int64 __fastcall sub_A30(__int64 a1, unsigned __int8 *a2, _BYTE *a3)
{
  __m128i v3; // xmm0
  __int64 i; // r9
  unsigned int v5; // ecx
  unsigned int v6; // ebx
  int v7; // esi
  int v8; // eax
  int v9; // ecx
  int v10; // esi
  unsigned __int64 v11; // rt0
  unsigned int v12; // esi
  int v13; // eax
  int v14; // eax
  int v15; // eax
  int v16; // eax
  __int128 v18[7]; // [rsp+10h] [rbp-98h] BYREF
  __int128 v19; // [rsp+80h] [rbp-28h]
  unsigned __int64 v20; // [rsp+90h] [rbp-18h]

  v20 = __readfsqword(0x28u);
  v19 = 0LL;
  memset(v18, 0, sizeof(v18));
  v3 = _mm_or_si128(
         _mm_or_si128(
           _mm_cvtepu8_epi32(_mm_insert_epi8(_mm_insert_epi8(_mm_insert_epi8(_mm_cvtsi32_si128(a2[15]), a2[11], 1), a2[7], 2), a2[3], 3)),
           _mm_slli_epi32(
             _mm_cvtepu8_epi32(
               _mm_insert_epi8(
                 _mm_insert_epi8(_mm_insert_epi8(_mm_cvtsi32_si128(a2[14]), a2[10], 1), a2[6], 2),
                 a2[2],
                 3)),
             8u)),
         _mm_or_si128(
           _mm_slli_epi32(
             _mm_cvtepu8_epi32(
               _mm_insert_epi8(
                 _mm_insert_epi8(_mm_insert_epi8(_mm_cvtsi32_si128(a2[13]), a2[9], 1), a2[5], 2),
                 a2[1],
                 3)),
             0x10u),
           _mm_slli_epi32(
             _mm_cvtepu8_epi32(_mm_insert_epi8(_mm_insert_epi8(_mm_insert_epi8(_mm_cvtsi32_si128(a2[12]), a2[8], 1), a2[4], 2), *a2, 3)),
             0x18u)));
  for ( i = 0LL; i != 32; ++i )
  {
    v5 = *(_DWORD *)(a1 + 4 * i) ^ _mm_extract_epi32(v3, 1) ^ _mm_extract_epi32(v3, 2) ^ _mm_cvtsi128_si32(v3);
    v6 = byte_D60[HIBYTE(v5)] ^ 7;
    v7 = (v6 << 24) | ((byte_D60[BYTE2(v5)] ^ 7) << 16);
    v8 = v7 | ((byte_D60[BYTE1(v5)] ^ 7) << 8);
    v9 = byte_D60[(unsigned __int8)v5] ^ 7;
    LODWORD(v11) = v7;
    HIDWORD(v11) = v8 + v9;
    v10 = v11 >> 22;
    HIDWORD(v11) = v8 + v9;
    LODWORD(v11) = v8;
    v12 = (v11 >> 14) ^ (__PAIR64__(v9, v8) >> 8) ^ (v8 + v9) ^ _mm_extract_epi32(v3, 3) ^ ((v6 >> 6) + 4 * (v8 + v9)) ^ v10;
    *((_DWORD *)v18 + i) = v12;
    v3 = _mm_blend_epi16(_mm_shuffle_epi32(v3, 144), _mm_cvtsi32_si128(v12), 3);
  }
  v13 = HIDWORD(v19);
  *a3 = HIBYTE(v19);
  a3[1] = BYTE2(v13);
  a3[2] = BYTE1(v13);
  a3[3] = v13;
  v14 = DWORD2(v19);
  a3[4] = BYTE11(v19);
  a3[5] = BYTE2(v14);
  a3[6] = BYTE1(v14);
  a3[7] = v14;
  v15 = DWORD1(v19);
  a3[8] = BYTE7(v19);
  a3[9] = BYTE2(v15);
  a3[10] = BYTE1(v15);
  a3[11] = v15;
  v16 = v19;
  a3[12] = BYTE3(v19);
  a3[13] = BYTE2(v16);
  a3[14] = BYTE1(v16);
  a3[15] = v16;
  return __readfsqword(0x28u);
}
```

search for some crypto algorithm illustration: 
https://bbs.kanxue.com/thread-265939.htm
> SM4是国密算法，由国家密码局发布。SM4是一个分组算法，分组长度为128比特，密钥长度为128比特，其结构是Fesitel网络的一个变体。

the characteristics are not like AES and DES cipher algorithm, then guess that the crypto alg is SM4-like algorithm.

find a constant string in `0x0000000000003010` which is `A11223574689900Z`
and compared with [GmSSL source code](https://github.com/guanzhi/GmSSL/blob/master/src/sm4.c)
it has huge possibility to be SM4 (with some modification)

try to decrypt it first with standard SM4 (modifying code template found online)
sm4.h
```cpp
/**
 * \file sm4.h
 */
#ifndef XYSSL_SM4_H
#define XYSSL_SM4_H
 
#define SM4_ENCRYPT     1
#define SM4_DECRYPT     0
#ifndef GET_ULONG_BE
//将字符型数组b的第i到第i+3位的二进制拼接成一个4*8=32bit的整数，存入n中
#define GET_ULONG_BE(n,b,i)                             \
{                                                       \
    (n) = ( (unsigned long) (b)[(i)    ] << 24 )        \
        | ( (unsigned long) (b)[(i) + 1] << 16 )        \
        | ( (unsigned long) (b)[(i) + 2] <<  8 )        \
        | ( (unsigned long) (b)[(i) + 3]       );       \
}
#endif
//将整数n的32位的二进制表示转换为4个char的数组，存入数组b的第i到第i+3位
#ifndef PUT_ULONG_BE
#define PUT_ULONG_BE(n,b,i)                             \
{                                                       \
    (b)[(i)    ] = (unsigned char) ( (n) >> 24 );       \
    (b)[(i) + 1] = (unsigned char) ( (n) >> 16 );       \
    (b)[(i) + 2] = (unsigned char) ( (n) >>  8 );       \
    (b)[(i) + 3] = (unsigned char) ( (n)       );       \
}
#endif
//循环左移 的巧妙实现（SHL(x,n)可以得到左移n位之后的结果，然后与右移的结果((x) >> (32 - n))逐位或来将右边空缺的n位补齐，效率比较高。） 
#define  SHL(x,n) (((x) & 0xFFFFFFFF) << n)
#define ROTL(x,n) (SHL((x),n) | ((x) >> (32 - n)))

#define SWAP(a,b) { unsigned long t = a; a = b; b = t; t = 0; }
 
/**
 * \brief          SM4 context structure
 */
typedef struct
{
    int mode;                   /*!<  encrypt/decrypt   */
    unsigned long sk[32];       /*!<  SM4 subkeys       */
}
sm4_context;
 
 
#ifdef __cplusplus
extern "C" {
#endif
 
/**
 * \brief          SM4 key schedule (128-bit, encryption)
 *
 * \param ctx      SM4 context to be initialized
 * \param key      16-byte secret key
 */
void sm4_setkey_enc( sm4_context *ctx, unsigned char key[16] );
 
/**
 * \brief          SM4 key schedule (128-bit, decryption)
 *
 * \param ctx      SM4 context to be initialized
 * \param key      16-byte secret key
 */
void sm4_setkey_dec( sm4_context *ctx, unsigned char key[16] );
 
/**
 * \brief          SM4-ECB block encryption/decryption
 * \param ctx      SM4 context
 * \param mode     SM4_ENCRYPT or SM4_DECRYPT
 * \param length   length of the input data
 * \param input    input block
 * \param output   output block
 */
void sm4_crypt_ecb( sm4_context *ctx,
				     int mode,
					 int length,
                     unsigned char *input,
                     unsigned char *output);
 
/**
 * \brief          SM4-CBC buffer encryption/decryption
 * \param ctx      SM4 context
 * \param mode     SM4_ENCRYPT or SM4_DECRYPT
 * \param length   length of the input data
 * \param iv       initialization vector (updated after use)
 * \param input    buffer holding the input data
 * \param output   buffer holding the output data
 */
void sm4_crypt_cbc( sm4_context *ctx,
                     int mode,
                     int length,
                     unsigned char iv[16],
                     unsigned char *input,
                     unsigned char *output );
 
#ifdef __cplusplus
}
#endif
 
#endif /* sm4.h */
```

sm4.cpp
```cpp
#include <iostream>
#include <string.h>
#include "sm4.h"

using namespace std;

 
//S盒 
const unsigned char Sbox[256] = {  
    0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,  
    0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,  
    0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,  
    0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,  
    0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,  
    0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,  
    0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,  
    0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,  
    0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,  
    0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,  
    0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,  
    0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,  
    0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,  
    0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,  
    0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,  
    0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48  
};
//CK为固定参数 
const unsigned int CK[32] = {  
    0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,  
    0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,  
    0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,  
    0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,  
    0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,  
    0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,  
    0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,  
    0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279 };
//FK为系统参数 
static const unsigned long FK[4] = {0xa3b1bac6,0x56aa3350,0x677d9197,0xb27022dc};

static unsigned char sm4Sbox(unsigned char inch)
{
    unsigned char *pTable = (unsigned char *)Sbox;
    unsigned char retVal = (unsigned char)(pTable[inch]);
    return retVal;
}
//已知加密密钥MK，求轮转密钥rk
static unsigned long sm4CaliRk(unsigned long ka){ //复合变换T
	unsigned long bb = 0; //unsigned long 4字节( 32bit ) 
	unsigned long rk = 0;
	unsigned char a[4];
	unsigned char b[4];
	PUT_ULONG_BE(ka,a,0)  //换转成8bit一个字符 
	b[0] = sm4Sbox(a[0]);
    b[1] = sm4Sbox(a[1]);
    b[2] = sm4Sbox(a[2]);
    b[3] = sm4Sbox(a[3]);
	GET_ULONG_BE(bb,b,0)  //将变换结果转换为32bit的整数
	//对得到的32位整数bb进行线性变换	
	rk = bb^ROTL(bb,13)^ROTL(bb,23);
	return rk;
}
static void sm4_setkey(unsigned long SK[32],unsigned char key[16]){
	unsigned long MK[4];
	unsigned long k[36];
	unsigned long i = 0;
	GET_ULONG_BE(MK[0],key,0);
	GET_ULONG_BE(MK[1],key,4);
	GET_ULONG_BE(MK[2],key,8);
	GET_ULONG_BE(MK[3],key,12);
	k[0] = MK[0]^FK[0];
	k[1] = MK[1]^FK[1];
	k[2] = MK[2]^FK[2];
	k[3] = MK[3]^FK[3];
	for(;i<32;i++){
		k[i+4] = k[i]^sm4CaliRk(k[i+1]^k[i+2]^k[i+3]^CK[i]);
		SK[i] = k[i+4];
	}	
}
void sm4_setkey_enc(sm4_context *ctx,unsigned char key[16]){
	ctx->mode = SM4_ENCRYPT;
	sm4_setkey(ctx->sk,key);
}

static unsigned long sm4Lt(unsigned long ka)
{
    unsigned long bb = 0;
    unsigned long c = 0;
    unsigned char a[4];
    unsigned char b[4];
    PUT_ULONG_BE(ka,a,0)
//    b[0] = sm4Sbox(a[0]);
//    b[1] = sm4Sbox(a[1]);
//    b[2] = sm4Sbox(a[2]);
//    b[3] = sm4Sbox(a[3]);
    b[0] = Sbox[a[0]];
    b[1] = Sbox[a[1]];
    b[2] = Sbox[a[2]];
    b[3] = Sbox[a[3]];
    GET_ULONG_BE(bb,b,0)
    c =bb^(ROTL(bb, 2))^(ROTL(bb, 10))^(ROTL(bb, 18))^(ROTL(bb, 24));
    return c;
}
//一轮加密 
static unsigned long sm4F(unsigned long x0, unsigned long x1, unsigned long x2, unsigned long x3, unsigned long rk)
{
    return (x0^sm4Lt(x1^x2^x3^rk));
}
static void sm4_one_round( unsigned long sk[32],
                    unsigned char input[16],
                    unsigned char output[16] )
{
    unsigned long i = 0;
    unsigned long ulbuf[36];

    memset(ulbuf, 0, sizeof(ulbuf));
    GET_ULONG_BE( ulbuf[0], input, 0 )
    GET_ULONG_BE( ulbuf[1], input, 4 )
    GET_ULONG_BE( ulbuf[2], input, 8 )
    GET_ULONG_BE( ulbuf[3], input, 12 )
    while(i<32)
    {
        ulbuf[i+4] = sm4F(ulbuf[i], ulbuf[i+1], ulbuf[i+2], ulbuf[i+3], sk[i]);
// #ifdef _DEBUG
//          printf("rk(%02d) = 0x%08x,  X(%02d) = 0x%08x \n",i,sk[i], i, ulbuf[i+4] );
// #endif
        i++;
    }
    PUT_ULONG_BE(ulbuf[35],output,0);
    PUT_ULONG_BE(ulbuf[34],output,4);
    PUT_ULONG_BE(ulbuf[33],output,8);
    PUT_ULONG_BE(ulbuf[32],output,12);
}
//ECB模式 
void sm4_crypt_ecb( sm4_context *ctx,
				   int mode,
				   int length,
				   unsigned char *input,
                   unsigned char *output)
{
    while( length > 0 )
    {
        sm4_one_round( ctx->sk, input, output );
        input  += 16;
        output += 16;
        length -= 16;
    }
 
}
//ECB模式解密密钥 
void sm4_setkey_dec( sm4_context *ctx, unsigned char key[16] )
{
    int i;
	ctx->mode = SM4_ENCRYPT;
    sm4_setkey( ctx->sk, key );
    for( i = 0; i < 16; i ++ )
    {
        SWAP( ctx->sk[ i ], ctx->sk[ 31-i] );
    }
}
//CBC模式加解密 
void sm4_crypt_cbc( sm4_context *ctx,
                    int mode,
                    int length,
                    unsigned char iv[16],
                    unsigned char *input,
                    unsigned char *output )
{
    int i;
    unsigned char temp[16];
 
    if( mode == SM4_ENCRYPT )
    {
        while( length > 0 )
        {
            for( i = 0; i < 16; i++ )
                output[i] = (unsigned char)( input[i] ^ iv[i] );
 
            sm4_one_round( ctx->sk, output, output );
            memcpy( iv, output, 16 );
 
            input  += 16;
            output += 16;
            length -= 16;
        }
    }
    else /* SM4_DECRYPT */
    {
        while( length > 0 )
        {
            memcpy( temp, input, 16 );
            sm4_one_round( ctx->sk, input, output );
 
            for( i = 0; i < 16; i++ )
                output[i] = (unsigned char)( output[i] ^ iv[i] );
 
            memcpy( iv, temp, 16 );
 
            input  += 16;
            output += 16;
            length -= 16;
        }
    }
} 


int main() {
	unsigned char key[16] = {0x41, 0x31, 0x31, 0x32, 0x32, 0x33, 0x35, 0x37, 0x34, 0x36, 0x38, 0x39, 0x39, 0x30, 0x30, 0x5a};
	unsigned char input[48] = {
        0x39, 0xB8, 0xF2, 0x2D, 0xD7, 0x53, 0xA5, 0x4C, 0x55, 0x84,
        0xFC, 0x72, 0xFF, 0x6C, 0xEC, 0xBF, 0xE6, 0x4E, 0x7F, 0x59,
        0xC6, 0x40, 0xC1, 0x9E, 0xEA, 0x0D, 0xE7, 0xB1, 0xAB, 0x0D,
        0xDC, 0xBF, 0xAF, 0x54, 0x51, 0xD0, 0xC6, 0xF8, 0xA2, 0x25,
        0x33, 0xEE, 0xA4, 0x36, 0xF1, 0xC3, 0x16, 0xD1
    };
	unsigned char output[48] = {0};
	sm4_context ctx;
	unsigned long i;

	//encryption
	sm4_setkey_enc(&ctx,key);
	sm4_crypt_ecb(&ctx, 1, sizeof(input), input, output);
	printf("encrypted results:\n"); 
	for(i = 0; i < sizeof(input); i++){
		printf("%02x ",output[i]);
	} 
	printf("\n");

    // decryption
	sm4_setkey_dec(&ctx,key);
	sm4_crypt_ecb(&ctx, 0, sizeof(input), input, output); 
	printf("decrypted results:\n"); 
	for(i = 0;i < sizeof(input); i++){
		printf("%02x ",output[i]);
	} 
	printf("\n");
    printf("wdflag{");
    for(i = 0;i < sizeof(input); i++){
		printf("%c",output[i]);
	} 
	printf("}\n");
	return 0;
}
```

get the flag directly

> wdflag{7314c25f-7097-483e-b745-fe96bb6a0b24}
