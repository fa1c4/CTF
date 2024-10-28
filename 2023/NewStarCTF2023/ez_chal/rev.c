/*
1. debug to deteremine the XTEA algorithm
2. find the values
3. find the key is NewStar!NewStar!
4. decrypt values back to flag
*/
#include <stdio.h>
#include <stdint.h>

#define KEYLEN 4
#define DELTA 0x61C88747
#define rounds 64

// notice v type is unsigned int* instead of unsigned char*
void XTEA(unsigned int *v, uint32_t const key[KEYLEN]) {
    unsigned int v0 = v[0], v1 = v[1], sum = 0;
    sum = -(DELTA * rounds);
    for (size_t i = 0; i < rounds; ++i) {
        v1 -= v0 ^ (key[(sum >> 11) & 3] + sum) ^ (v0 + ((v0 >> 5) ^ (v0 << 4)));
        sum += DELTA;
        v0 -= v1 ^ (key[sum & 3] + sum) ^ (v1 + ((v1 >> 5) ^ (v1 << 4)));
    }
    v[0] = v0;
    v[1] = v1;
}


int main(void) {
    // uint32_t values[] = {0xC19EA29C, 0xDC091F87, 0x91F6E33B, 0xF69A5C7A, 
    //                     0x93529F20, 0x8A5B94E1, 0xF91D069B, 0x23B0E340};
    // notice that IDApro converted string maybe wrong after copying 
    unsigned char values[] = {0x9c, 0xa2, 0x9e, 0xc1, 0x87, 0x1f, 0x9, 0xdc, 0x3b, 
                         0xe3, 0xf6, 0x91, 0x7a, 0x5c, 0x9a, 0xf6, 0x20, 0x9f, 
                         0x52, 0x93, 0xe1, 0x94, 0x5b, 0x8a, 0x9b, 0x6, 0x1d, 
                         0xf9, 0x40, 0xe3, 0xb0, 0x23};
    uint32_t key[KEYLEN] = {0x5377654E, 0x21726174, 0x5377654E, 0x21726174};
    int i;
    unsigned int* p = (unsigned int*)values;
    
    for (i = 0; i < 8; i += 2) {
        XTEA(p + i, key);
    }
    
    for (i = 0; i < 8; i++) {
        printf("%c%c%c%c", *((char*)&p[i] + 0), *((char*)&p[i] + 1), *((char*)&p[i] + 2), *((char*)&p[i] + 3));
    }
    printf("\n");

    return 0;
}
