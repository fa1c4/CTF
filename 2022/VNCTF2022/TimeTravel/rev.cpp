#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


// Rotate Left (ROL) implementation
unsigned int __ROL4__(unsigned int value, int count) {
    return (value << count) | (value >> (32 - count));
}

// Rotate Right (ROR) implementation
unsigned int __ROR4__(unsigned int value, int count) {
    return (value >> count) | (value << (32 - count));
}

int processing_date(int a1) {
    return a1 ^ (unsigned int)(__ROL4__(a1, 13) ^ __ROR4__(a1, 9));
} 

unsigned int byteswap_ulong(unsigned int value) {
    return ((value >> 24) & 0xFF) |      // move byte 3 to byte 0
           ((value << 8) & 0xFF0000) |   // move byte 1 to byte 2
           ((value >> 8) & 0xFF00) |     // move byte 2 to byte 1
           ((value << 24) & 0xFF000000); // move byte 0 to byte 3
}

void print_int_as_ascii(unsigned int value) {
    char ascii_string[5]; // 4 bytes + 1 for null terminator
    ascii_string[4] = '\0'; // null-terminate the string

    // Extract each byte and convert it to its ASCII character
    for (int i = 0; i < 4; ++i) {
        ascii_string[3 - i] = (char)((value >> (i * 8)) & 0xFF); // extract each byte
    }

    printf("ASCII String: %s\n", ascii_string);
}

void rev_date() {
    unsigned int v5[36] = {0};
    unsigned int input_date[4] = {0}; 
    unsigned int date_checkval[4] = {0xFD07C452, 0xEC90A488, 0x68D33CD1, 0x96F64587};
    int constants_val[32] = {462357, 472066609, 943670861, 1415275113, 1886879365,
                    -1936483679, -1464879427, -993275175, -521670923, -66909679,
                    404694573, 876298825, 1347903077, 1819507329, -2003855715,
                    -1532251463, -1060647211, -589042959, -117504499, 337322537,
                    808926789, 1280531041, 1752135293, -2071227751, -1599623499,
                    -1128019247, -656414995, -184876535, 269950501, 741554753,
                    1213159005, 1684763257};

    // get the final 4 dwords
    for (int i = 0; i < 4; ++i) {
        v5[i+32] = date_checkval[i];
    }

    // reverse the processing 
    for (int i = 31; i >= 0; --i) {
        v5[i] = processing_date(v5[i + 3] ^ v5[i + 2] ^ (unsigned int)v5[i + 1] ^ constants_val[i]) ^ v5[i+4];
    }

    // xor with constants
    // input_date[0] = byteswap_ulong(v5[0] ^ 0xA3B1BAC6);
    // input_date[1] = byteswap_ulong(v5[1] ^ 0x56AA3350);
    // input_date[2] = byteswap_ulong(v5[2] ^ 0x677D9197);
    // input_date[3] = byteswap_ulong(v5[3] ^ 0xB27022DC);
    input_date[0] = v5[0] ^ 0xA3B1BAC6;
    input_date[1] = v5[1] ^ 0x56AA3350;
    input_date[2] = v5[2] ^ 0x677D9197;
    input_date[3] = v5[3] ^ 0xB27022DC;

    for (int i = 0; i < 4; ++i) {
        print_int_as_ascii(input_date[i]);
    }
}


int main() {
    // reverse the date
    rev_date();

    // reverse to do...
}
