#include <stdio.h>


int main() {
    int v7 = 0;
    for (int i = 0; i < 32768 * 2; ++i) {
        if (i % 1000 == 0) printf("%dtimes: %d\n", i, v7);
        v7 += 0x10000;
    }
    // printf("v7 + 0x10000 * (32767 + 1): %d\n", v7);
    printf("v7 + 0x10000 * 65,536: %d\n", v7);

    short int v3 = 0;
    scanf("%hd", &v3);
    printf("v3: %d\n", v3);
}
