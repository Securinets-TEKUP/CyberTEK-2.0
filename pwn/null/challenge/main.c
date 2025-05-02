#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <err.h>

#define MAX_BOOKS 50

typedef struct book {
  char *title;
  int title_len;
  char isbn[128];
} book_t;

void setup() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
}

book_t *library[MAX_BOOKS];
int num_books = 0;

void generate_isbn(book_t *b) {
  const char charset[] = "0123456789X";
  int i;

  for(i = 0; i < sizeof(b->isbn)-1; i++) {
    b->isbn[i] = charset[rand()%(sizeof(charset)-1)];
  }
  b->isbn[sizeof(b->isbn) - 1] = 0;
}

void remove_book(int id) {
  if(id < 0 || id >= num_books)
    return;

  free(library[id]->title);
  free(library[id]);
  library[id] = library[num_books-1];
  num_books--;
}

void add_book(char *buffer, int len) {
  if(num_books >= MAX_BOOKS)
    return;

  library[num_books] = malloc(sizeof(book_t));
  library[num_books]->title = malloc(len+1);
  
  strcpy(library[num_books]->title, "_");
  memcpy(library[num_books]->title+1, buffer, len);
  library[num_books]->title[len+1] = 0;
  
  library[num_books]->title_len = len+1;
  generate_isbn(library[num_books]);
  num_books++;
}

void list_books(void) {
  int i;

  for(i = 0; i < num_books; i++) {
    printf("\n\n");
    printf("%d\n", i);
    printf("ISBN = %s\n", library[i]->isbn);
    printf("TITLE = %s\n", library[i]->title);
  }
}

void update_book(char *buffer, int id, int len) {
  if(id < 0 || id >= num_books)
    return;

  if(library[id]->title_len < len+1) {
    library[id]->title = realloc(library[id]->title, len+1);
    library[id]->title_len = len+1;
  }
  memcpy(library[id]->title, buffer, len);

  library[id]->title[len] = 0;
}

int get_book_id(const char *isbn) {
  int i;

  for(i = 0; i < num_books; i++) {
    if(!strcmp(isbn, library[i]->isbn))
      return i;
  }

  printf("Invalid ISBN: <%s>\n", isbn);
  return -1;
}

void process_command(char *buffer, int len) {
  char *p;

  if(!strncmp(buffer, "remove ", 7)) {
    remove_book(get_book_id(buffer+7));
  } else if(!strncmp(buffer, "add ", 4)) {
    add_book(buffer+4, len-4);
  } else if(!strncmp(buffer, "list", 4)) {
    list_books();
  } else if(!strncmp(buffer, "update ", 7)) {
    if((p = strchr(buffer+7, ' '))) {
      *(p++) = 0;
      update_book(p, get_book_id(buffer+7), len-(p-buffer+1));
    }
  } else {
    printf("Invalid command: <%s>\n", buffer);
  }
}

void prompt(void) {
  printf("Library> ");
  fflush(stdout);
}

void menu(void) {
  printf("Library Management System Commands\n");
  printf("  * add <title>\n");
  printf("  * remove <isbn>\n");
  printf("  * update <isbn> <new_title>\n");
  printf("  * list\n");
}

int challenge(void) {
  char buffer[4096];
  int len;
  srand(time(NULL));
  menu();
  prompt();

  while((len = read(0, buffer, sizeof(buffer) - 1)) > 0) {
    buffer[len] = 0;

    if(buffer[len - 1] == '\n')
      buffer[len - 1] = 0;

    process_command(buffer, len);
    prompt();
  }

  return 0;
}

int main() {
    setup();
    challenge();
    return 0;
}
