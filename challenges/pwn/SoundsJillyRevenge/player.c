#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT_SIZE 4096
#define TEST_FILE "test"

void setup() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main() {
    setup();

    char input[MAX_INPUT_SIZE];
    char test_content[MAX_INPUT_SIZE];

    printf("Enter your CHIP-8 payload (hex or text): ");
    fflush(stdout);

    if (fgets(input, sizeof(input), stdin) == NULL) {
        perror("Error reading input");
        return 1;
    }

    // Remove newline from input
    input[strcspn(input, "\n")] = 0;

    FILE *test_file = fopen(TEST_FILE, "r");
    FILE *payloadfile = fopen("payload", "w");
    if (!payloadfile) {
        perror("Error opening payload file");
        return 1;
    }
    
    fputs(input, payloadfile);
    fclose(payloadfile);
    
    payloadfile = fopen("payload", "r");

    if (!test_file) {
        perror("Error opening test file");
        return 1;
    }

    if (fgets(test_content, sizeof(test_content), test_file) == NULL) {
        perror("Error reading test file");
        fclose(test_file);
        return 1;
    }
    fclose(test_file);

    // Remove newline from test content
    test_content[strcspn(test_content, "\n")] = 0;

    if (strcmp(input, test_content) == 0) {
       
        system("/bin/sh");
    } else {
        execl("./chip8", "./chip8", payloadfile, NULL);
    }

    return 0;
}
