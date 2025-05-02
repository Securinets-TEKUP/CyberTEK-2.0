#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


void vuln() {
    char buffer[0x70];
    printf("Enter something: ");
    fgets(buffer, sizeof(buffer), stdin);
    printf(buffer);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    setup();
    vuln();
    exit(0);
}

void win() {
    system("/bin/sh");
}