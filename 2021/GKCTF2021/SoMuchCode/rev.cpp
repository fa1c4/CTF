#include <stdio.h> 
#include <stdint.h> 


void XXTeaDecrypt(int n, uint32_t* v, uint32_t const key[4]) { 
    uint32_t y, z, sum; 
    unsigned p, rounds, e; 
    uint32_t DELTA = 0x33445566; 
    rounds = 12; 
    sum = rounds * DELTA; 
    y = v[0];
    while (rounds--) { 
        e = (sum >> 2) & 3; 
        for (p = n - 1; p > 0; p--) {  
            z = v[p - 1]; 
            v[p] -= (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z))); 
            y = v[p];
        }
        z = v[n - 1];  
        v[0] -= (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z)));  
        y = v[0];
        sum -= DELTA; 
    }
}

int main() { 
   uint8_t enc_data[] = {0x5c, 0xab, 0x3c, 0x99, 0x29, 
                        0xe1, 0x40, 0x3f, 0xde, 0x91, 
                        0x77, 0x77, 0xa6, 0xfe, 0x7d, 
                        0x73, 0xe6, 0x59, 0xcf, 0xec, 
                        0xe3, 0x4c, 0x60, 0xc9, 0xa5, 
                        0xc0, 0x82, 0x96, 0x1e, 0x2a, 
                        0x6f, 0x55, 0}; 
   uint32_t key[] = {14000, 79894, 16, 123123}; 
 
   XXTeaDecrypt(8, (uint32_t*)enc_data, key); 
 
   printf("GKCTF{%s}", (char*)enc_data);
   return 0; 
}
