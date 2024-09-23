#include <stdio.h>
#include <stdlib.h>


unsigned char dword_1EBA0[32] = {
    17, 118, 208, 30, 153, 182, 44, 145,
    18, 69, 251, 42, 151, 198, 99, 184,
    20, 124, 225, 30, 131, 230, 69, 160,
    25, 99, 221, 50, 164, 223, 113, 0
};


int main() {
    unsigned char flag[32] = {0};
    flag[0] = 'R';
    for (int i = 1; i < 31; ++i) {
        flag[i] = (unsigned char)((dword_1EBA0[i-1] ^ (97 * (i - 1) % 256)) ^ flag[i-1]);
        // printf("%d: %d\n", i, flag[i]);
    }

    printf("%s\n", flag);
}
