#include <stdio.h>

int main() {
    for (int i = 46; i <= 90; ++i) {
        if ( i > 90 || i <= 47 || i > 57 && i <= 64 )
            continue;
        printf("%c ", i);
    }
    return 0;
}
