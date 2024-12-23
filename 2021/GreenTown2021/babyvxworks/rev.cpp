#include <stdio.h>


unsigned char checking[] = { 
                188, 10, 187, 193, 213, 134, 127, 10, 
                201, 185, 81, 78, 136, 10, 130, 185, 
                49, 141, 10, 253, 201, 199, 127, 185, 
                17, 78, 185, 232, 141, 87
            };


int main() {
    for (int cnt = 0; cnt < 30; ++cnt) {
        for (int i = 0; i < 30; ++i) {
            checking[i] -= (unsigned char)3;
            checking[i] ^= (unsigned char)0x22;
        }
    }

    for (int cnt = 0; cnt < 30; ++cnt) {
        printf("%c", checking[cnt]);
    }
    printf("\n");

    return 0;
}   
