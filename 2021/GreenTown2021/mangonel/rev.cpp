/*
reverse script for mangonel in GreenTown CTF 2021
*/

#include <stdio.h>


int main() {
    unsigned long long i;
    unsigned long long tmp;
    double key;
    double v4 = 0, v2 = 0, v1 = 0;

    for (i = 0; i < 10; ++i) {
        tmp = i << 32;
        key = *(double *)(&tmp);

        printf("%p ", (i << 32));
        printf("%p ", *(double *)(&tmp));

        v4 = 149.2 * (i << 32) + (i << 32) * -27.6 * (i << 32) - 129.0;
        printf("%v4:%lf ", v4);

        v4 = 149.2 * key + key * -27.6 * key - 129.0;
        printf("%v4:%lf ", v4);

        v4 = 149.2 * key + key * -27.6 * key - 129.0;
        if ((v4 > -0.00003) && (v4 < 0.00003)) {
            printf("v4:%p %lf\n", i, v4);
        }

        v2 = key * -39.6 * key + 59.2 * key + 37.8;
        if ((v2 > -0.00002) && (v2 < 0.00002)) {
            printf("v2:%p %lf\n", i, v2);
        }

        v1 = key * -39.6 * key + 59.2 * key + 37.8;
        if ((v1 > -0.00003) && (v1 < 0.00003)) {
            printf("v1:%p %lf\n", i, v1);
        }

        printf("\n");
    }

    // printf("\nGetFlag!\nflag{454af13f-f84c-1140-1ee4-debf58a4ff3f} ");

    return 0;
}
