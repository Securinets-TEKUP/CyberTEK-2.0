#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_PETS 20

char* shelter[MAX_PETS];
int size[MAX_PETS];

void __debug_routine(){
    char *buf;
    asprintf(&buf, "session:init okk | stable | uid=xxxx | %p", &__debug_routine);
    free(buf);
}

void setup() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
}

void welcome() {
    puts("\n\n🐾 Happy Paws Shelter 🐾");
    puts("1. Adopt a pet");
    puts("2. Return a pet");
    puts("3. Rename pet");
    puts("4. View pets");
    puts("5. Exit");
    printf("> ");
}

int get_id() {
    int id;
    printf("Pet ID (0-19): ");
    scanf("%d", &id);
    if(id < 0 || id >= MAX_PETS) {
        puts("Invalid ID!");
        exit(-1);
    }
    return id;
}

void adopt_pet(){
    int id = get_id();
    if (size[id]){
        printf("Pet with ID %d is already adopted");
        return;
    }
    
    printf("Pet name size: ");
    scanf("%u", &size[id]);
    shelter[id] = malloc(size[id]);
    memset(shelter[id], 0, size[id]);
    printf("Pet name: ");
    if (!read(0 ,shelter[id], size[id])){
        puts("I don't believe there is a pet with no name");
        free(shelter[id]);
        size[id] = 0;
    }
}
                
void return_pet(){
    int id = get_id();
    memset(shelter[id], 0, size[id]);
    free(shelter[id]);
    size[id] = 0;
    puts("Pet returned to shelter");
}

void rename_pet(){
    int id = get_id();
    if (!size[id]){
        printf("Pet with ID %d is not adopted yet");
        return;
    }
    printf("Old name: ");
    printf(shelter[id]);
    printf("\nNew name: ");
    read(0, shelter[id], size[id]);
}

void view_pets(){
    for(int i=0; i<MAX_PETS; i++) {
        if(size[i])
            printf("[%d] %s\n", i, shelter[i]);
    }
}

void challenge() {
    int choice;
    __debug_routine();
    memset(shelter, 0, sizeof(shelter));
    while(1) {
        welcome();
        scanf("%d", &choice); 
        switch(choice) {
            case 1:
                adopt_pet();
                break;
                
            case 2:
                return_pet();
                break;
                
            case 3:
                rename_pet();
                break;
                
            case 4:
                view_pets();
                break;
                
            case 5:
                puts("Goodbye!");
                exit(0);
                
            default:
                puts("Invalid choice!");
        }
    }
}

int main() {
    setup();
    challenge();
    return 0;
}
