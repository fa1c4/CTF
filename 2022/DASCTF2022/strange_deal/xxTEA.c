#include <stdio.h>
#include <stdint.h>

#define KEYLEN 4
#define DELTA 0x9E3779B9

#define MX ( ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z)) )

void BTEA(uint32_t *v, int n, uint32_t const key[KEYLEN]) {
    uint32_t y, z, sum;
    unsigned p, rounds, e;

    if (n > 1) {
        rounds = 6 + 52 / n;
        sum = 0;
        z = v[n - 1];
        while (rounds--) {
            sum += DELTA;
            e = (sum >> 2) & 3;
            for (p = 0; p < n - 1; ++p) {
                y = v[p+1];
                v[p] += MX;
                z = v[p];
            }
            y = v[0];
            v[n-1] += MX;
            z = v[n-1];
        }
    } else if (n < -1) {
        n = -n;
        rounds = 6 + 52 / n;
        sum = rounds * DELTA;
        y = v[0];
        while (rounds--) {
            e = (sum >> 2) & 3;
            for (p = n - 1; p > 0; --p) {
                z = v[p-1];
                v[p] -= MX;
                y = v[p];
            }
            z = v[n-1];
            v[0] -= MX;
            y = v[0];
            sum -= DELTA;
        }
    }
}


int main(void) {
    uint32_t values[] = {0xD28ED952, 1472742623, 0xD91BA938, 0xF9F3BD2D, 0x8EF8E43D, 
                        617653972, 1474514999, 1471783658, 1012864704, 0xD7821910, 
                        993855884, 438456717, 0xC83555B7, 0xE8DFF468, 198959101, 
                        0xC5B84FEB, 0xD9F837C6, 613157871, 0x8EFA4EDD, 97286225, 
                        0x8B4B608C, 1471645170, 0xC0B62792, 583597118, 0xAAB1C22D, 
                        0xBDB9C266, 1384330715, 0xAE9F9816, 0xD1F40B3C, 0x8206DDC3, 
                        0xC4E0BADC, 0xE407BD26, 145643141, 0x8016C6A5, 0xAF4AB9D3, 
                        506798154, 994590281, 0x85082A0B, 0xCA0BC95A, 0xA7BE567C, 
                        1105937096, 1789727804, 0xDFEFB591, 0x93346B38, 1162286478, 
                        680814033, 0xAEE1A7A2, 0x80E574AE, 0xF154F55F, 2121620700, 
                        0xFCBDA653, 0x8E902444, 0xCA742E12, 0xB8424071, 0xB4B15EC2, 
                        0x943BFA09, 0xBC97CD93, 1285603712, 798920280, 0x8B58328F, 
                        0xF9822360, 0xD1FD15EE, 1077514121, 1436444106, 0xA2D6C17E, 
                        1507202797, 500756149, 198754565, 0x8E014807, 880454148, 
                        1970517398, 0xBFC6EE25, 1161840191, 560498076, 1782600856, 
                        0x9D93FEBE, 1285196205, 788797746, 1195724574, 0xF2174A07, 
                        103427523, 0x952BFE83, 0xF730AC4C, 617564657, 978211984, 
                        1781482121, 0x8379D23A, 0xEAD737EE, 0xE41555FB, 659557668, 
                        0x99F3B244, 1561884856, 0x842C31A4, 1189296962, 169145316, 
                        0xA5CE044C, 1323893433, 824667876, 408202876, 0xE0178482, 
                        0xF412BBBC, 1508996065, 162419237, 0xDE740B00, 0xB7CB64FD, 
                        0xEBCADB1F, 0x8EAE2326, 0x933C216C, 0xD7D1F649, 481927014, 
                        0xA448AC16, 0xBC082807, 1261069441, 2063238535, 0x8474A61D, 
                        101459755, 0xBC5654D1, 1721190841, 1078395785, 176506553, 
                        0xD3C5280F, 1566142515, 1938949000, 1499289517, 0xC59872F8, 
                        829714860, 0xE51502A2, 952932374, 1283577465, 2045007203, 
                        0xEBE6A798, 0xE09575CD, 0xADDF4157, 0xC4770191, 482297421, 
                        1734231412, 0xDAC71054, 0x99807E43, 0xA88D74B1, 0xCB77E028, 
                        1533519803, 0xEEEBC3B6, 0xE7E680E5, 272960248, 317508587, 
                        0xC4B10CDC, 0x91776399, 27470488, 1666674386, 1737927609, 
                        750987808, 0x8E364D8F, 0xA0985A77, 562925334, 0x837D6DC3};
    uint32_t key[KEYLEN] = {54, 54, 54, 54};
    int i, idx;
    int vCnt = sizeof(values) / sizeof(uint32_t);

    BTEA(values, -vCnt, key);
    unsigned char* p = (unsigned char*)values;
    for (i = 0, idx = 0; idx < vCnt; i += 4, idx++) {
        printf("%c%c%c%c", p[i + 3], p[i + 2], p[i + 1], p[i]);
    }

    return 0;
}
