#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NUM_BYTES 256
int main() {
    unsigned char* buffer = malloc(NUM_BYTES);
    FILE* f = fopen("testfile1", "w");
    if (f == NULL) {
        return 1;
    }
    for (unsigned int i = 0; i != 256; ++i) {
        memset(buffer, i, NUM_BYTES);
        fwrite(buffer, sizeof(unsigned char), NUM_BYTES, f);
    }
    fclose(f);
    return 0;
}