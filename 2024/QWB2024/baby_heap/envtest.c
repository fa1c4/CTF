#include <stdlib.h>
#include <stdio.h>


int main() {
    // setenv
    setenv("USER", "flag?", 1);
    printf("USER: %s\n", getenv("USER"));

    // putenv
    putenv("USER=flag?");
    printf("USER: %s\n", getenv("USER"));

    // printenv
    char *v0;
    v0 = getenv("USER");
    if (v0) printf("USER = %s\n", v0);

    return 0;
}
