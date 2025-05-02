#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int sleep_time;
int buffer_size;

void vuln() {
  char buffer[buffer_size];
  read(0, buffer, buffer_size*4);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
  setup();
  srand(time(NULL));
  sleep_time = (rand() % 3) + 1;
  buffer_size = ((rand() % 8) + 1) * 4;
  sleep(sleep_time);
  putchar('>');
  while(true) {
    vuln();
  }
}