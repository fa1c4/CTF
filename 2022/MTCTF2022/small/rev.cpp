#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


void decrypt(uint32_t* v, uint32_t* k) {
	uint32_t v0 = v[0], v1 = v[1], sum = 0x67452301 * 35, i;
	uint32_t delta = 0x67452301;
	uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];
	for (i = 0; i < 35; i++) {
		v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
		v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
		sum -= delta;
	}
	v[0] = v0; v[1] = v1;
}


int main() {
	int i ,j;
	uint32_t v[8] = {0xde087143, 0xc4f91bd2, 0xdaf6dadc, 0x6d9ed54c, 
                    0x75eb4ee7, 0x5d1ddc04, 0x511b0fd9, 0x51dc88fb};	
    uint32_t k[4] = {0x1, 0x23, 0x45, 0x67};
	int n = sizeof(v) / sizeof(uint32_t);
	
    for (i = 0; i < 4; ++i) {
        decrypt(&v[2*i], k);
        printf("data decrypted: 0x%x 0x%x\n", v[2*i+0], v[2*i+1]);
    }

    printf("flag{");
	for ( i = 0; i < n; i++) {
		for ( j = 0; j < sizeof(uint32_t) / sizeof(uint8_t); j++) {
			printf("%c", (v[i] >> (j * 8)) & 0xFF);
		}
	}
	printf("}\n");
	
    return 0;
}

// ./small 327a6c4304ad5938eaf0efb6cc3e53dc
// good
