#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

int SET=1;

void setup() {
    // Set the gid and uid to 0
    setresgid(0, 0, 0);
    setresuid(0, 0, 0);
  
    
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    SET = 0;

}

void FUN_080485b6() {
    __asm__("pop %rdi; ret");
}

void main() {

    if (SET != 1) {
        exit(1);
    }
    setup();
    char buffer[32];
    fflush(stdout);
    puts(" Welcome to the recall service! ");
    printf("Enter your name: \n");
    fflush(stdout);
    gets(buffer);
    printf("Hello, %s\n", buffer);
    fflush(stdout);
    
  }