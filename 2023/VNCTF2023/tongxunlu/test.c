#include <stdio.h>
#include <stdlib.h>
#include <errno.h>


int main() {
    const char *str1 = "1234";        // Decimal string
    const char *str2 = "101010";      // Binary string
    const char *str3 = "1A3F";        // Hexadecimal string
    const char *str4 = "invalid123";  // Invalid string
    const char *str5 = "59/bin/sh\x00"; // test for /bin/sh

    char *endptr;
    long value;

    // Example 1: Convert decimal string
    errno = 0; // Clear errno
    value = strtol(str1, &endptr, 10);
    if (errno == 0 && *endptr == '\0') {
        printf("The decimal value of '%s' is %ld\n", str1, value);
    } else {
        printf("Conversion failed for '%s'\n", str1);
    }

    // Example 2: Convert binary string
    errno = 0;
    value = strtol(str2, &endptr, 2);
    if (errno == 0 && *endptr == '\0') {
        printf("The binary value '%s' as decimal is %ld\n", str2, value);
    } else {
        printf("Conversion failed for '%s'\n", str2);
    }

    // Example 3: Convert hexadecimal string
    errno = 0;
    value = strtol(str3, &endptr, 16);
    if (errno == 0 && *endptr == '\0') {
        printf("The hexadecimal value '%s' as decimal is %ld\n", str3, value);
    } else {
        printf("Conversion failed for '%s'\n", str3);
    }

    // Example 4: Convert invalid string
    errno = 0;
    value = strtol(str4, &endptr, 10);
    if (errno != 0 || *endptr != '\0') {
        printf("Conversion failed for '%s': '%s' is not a valid number\n", str4, str4);
    } else {
        printf("The decimal value of '%s' is %ld\n", str4, value);
    }

    errno = 0;
    value = strtol(str5, &endptr, 10);
    if (errno != 0 || *endptr != '\0') {
        printf("Conversion failed for '%s': '%s' is not a valid number\n", str5, str5);
        printf("the conversion result is %ld\n", value);
    } else {
        printf("The decimal value of '%s' is %ld\n", str5, value);
    }

    return 0;
}
