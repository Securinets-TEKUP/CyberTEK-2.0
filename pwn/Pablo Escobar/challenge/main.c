#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

__attribute__((naked))void _deal() {
  asm("push %rsp; ret");
}

void prompt() {
    puts("Be careful! The cartel doesn't just take your words... they execute people(mostly).");
    puts("The first part of the deal is done.");
    puts("Speak your final words to seal it:");
}

void vuln() {
    char buffer[0x28];
    *(uint64_t *)(buffer+0x8) =  (uint64_t)&_deal;
    read(0, buffer+0x10, 0x100);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    setup();
    prompt();
    vuln();
    return 0;
}