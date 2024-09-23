#include <stdio.h>
#include <string.h>


int main() {
    int i = 0, j = 0, k = 0;
    int flagenc[] = {139, 221, 230, 131, 179, 221, 147, 137, 184, 250, 158, 224, 231, 154, 22, 84, 239, 40, 225, 177, 33, 91, 83};
    int length = sizeof(flagenc) / sizeof(flagenc[0]);
    
    char out[length + 1];

    // S and table arrays
    int S[256];
    char table[256];
    const char *key = "E7E64BF658BAB14A25C9D67A054CEBE5";

    // Initialize S and table arrays
    for (i = 0; i < 256; i++) {
        S[i] = i;
        table[i] = (char)key[i % 32];  // Simulating key.charAt(i % 32)
        // printf("%d: %d\n", i, table[i]);
    }

    // Key scheduling algorithm
    
    for (i = 0; i < 256; i++) {
        j = (S[i] + j + table[i]) % 256;
        int temp = S[i];
        S[i] = S[j];
        S[j] = temp;
    }

    // for (int n = 0; n < 256; ++n) {
    //     if (n % 16 == 0) printf("\n");
    //     printf("%d ", S[n]);
    // }

    // Decryption loop
    for (int i = 0, j = 0, k = 0; i < length; i++) {
        k = (k + 1) % 256;
        j = (S[k] + j) % 256;
        int temp = S[k];
        S[k] = S[j];
        S[j] = temp;
        out[i] = (char)((flagenc[i] ^ S[(S[k] + S[k] % 256) % 256]) + k);
        // out[i] = (char)(((char)flagenc[i] ^ S[(S[k] + S[j] % 256) % 256]) + k); // Corrected this line
        // printf("%d ", flagenc[i]);
    }

    // Print the output
    out[length] = '\0';
    printf("%s\n", out);

    return 0;
}
// change the '6' to 'S' in final flag (= =
