// mutex_server.c - Remote CTF challenge involving semaphore vulnerabilities
// Compile with: gcc -o mutex_server mutex_server.c -pthread

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <pthread.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <malloc.h>

#define SHM_SIZE 256
#define FLAG_SIZE 64
#define MAX_USERS 100
#define MAX_CLIENTS 50
#define PORT 6002
#define BUFFER_SIZE 1024

// Union for semctl
union semun {
    int val;
    struct semid_ds *buf;
    unsigned short *array;
};

// Global variables
int sem_id;
int shm_id;
char *shared_memory;
char flag[FLAG_SIZE] ;
int user_count = 0;
pthread_t admin_thread;
pthread_mutex_t users_mutex = PTHREAD_MUTEX_INITIALIZER;
int server_socket;

// User structure
typedef struct {
    int id;
    char name[32];
    int privilege;
    int logged_in;
} User;

User users[MAX_USERS];

// Client structure
typedef struct {
    int socket;
    struct sockaddr_in address;
    pthread_t thread;
    int user_id;
    int is_active;
} Client;

Client clients[MAX_CLIENTS];

// Function prototypes
void cleanup();
void *admin_routine(void *arg);
void initialize_semaphore();
void initialize_shared_memory();
void initialize_server();
void *handle_client(void *arg);
void send_to_client(int socket, const char *message);
void register_user(int client_socket, char *username);
void login_user(int client_socket, char *username, int client_id);
void access_resource(int client_socket);
void send_message(int client_socket, char *message);
void view_message(int client_socket);

// Signal handler
void sigint_handler(int sig) {
    printf("\nShutting down server...\n");
    fflush(stdout);
    
    // Close all client connections
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (clients[i].is_active) {
            close(clients[i].socket);
        }
    }
    
    // Close server socket
    close(server_socket);
    
    cleanup();
    exit(0);
}

// Initialize semaphore
void initialize_semaphore() {
    key_t key = ftok("mutex_server.c", 'S');
    sem_id = semget(key, 3, IPC_CREAT | 0666);
    
    if (sem_id == -1) {
        perror("semget");
        exit(1);
    }
    
    // Initialize semaphores
    union semun argument;
    unsigned short values[3] = {1, 0, 1}; // mutex, signal, resource access
    argument.array = values;
    
    if (semctl(sem_id, 0, SETALL, argument) == -1) {
        perror("semctl");
        exit(1);
    }
    
    printf("[+] Semaphores initialized\n");
}

// Initialize shared memory
void initialize_shared_memory() {
    key_t key = ftok("mutex_server.c", 'M');
    shm_id = shmget(key, SHM_SIZE, IPC_CREAT | 0666);
    
    if (shm_id == -1) {
        perror("shmget");
        exit(1);
    }
    
    shared_memory = shmat(shm_id, NULL, 0);
    
    if (shared_memory == (char *)-1) {
        perror("shmat");
        exit(1);
    }
    
    memset(shared_memory, 0, SHM_SIZE);
    printf("[+] Shared memory initialized\n");
    fflush(stdout);

}

// Initialize network server
void initialize_server() {
    struct sockaddr_in server_addr;
    
    // Create socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("socket");
        exit(1);
    }
    
    // Enable address reuse
    int opt = 1;
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt");
        exit(1);
    }
    
    // Prepare server address structure
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);
    
    // Bind socket to address
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        exit(1);
    }
    
    // Listen for connections
    if (listen(server_socket, 5) < 0) {
        perror("listen");
        exit(1);
    }
    
    printf("[+] Server initialized on port %d\n", PORT);
    fflush(stdout);

    
    // Initialize client array
    for (int i = 0; i < MAX_CLIENTS; i++) {
        clients[i].is_active = 0;
        clients[i].user_id = -1;
    }
}

// Cleanup resources
void cleanup() {
    // Detach shared memory
    if (shmdt(shared_memory) == -1) {
        perror("shmdt");
    }
    
    // Remove shared memory
    if (shmctl(shm_id, IPC_RMID, NULL) == -1) {
        perror("shmctl");
    }
    
    // Remove semaphore
    if (semctl(sem_id, 0, IPC_RMID, 0) == -1) {
        perror("semctl");
    }
    
    printf("[+] Resources cleaned up\n");
    fflush(stdout);

}

// Semaphore operations
void sem_operation(int sem_num, int op) {
    struct sembuf sb;
    sb.sem_num = sem_num;
    sb.sem_op = op;
    sb.sem_flg = 0;
    
    if (semop(sem_id, &sb, 1) == -1) {
        perror("semop");
        exit(1);
    }
}

// Admin thread routine
void *admin_routine(void *arg) {
    while (1) {
        sleep(10);
        
        // Lock mutex
        sem_operation(0, -1);
        
        // Simulate admin actions
        printf("[Admin] Checking system...\n");
        fflush(stdout);

        
        // VULNERABLE: Race condition if a user is accessing the resource
        // Admin copies the flag to shared memory but doesn't properly secure it
        if (strlen(shared_memory) > 0) {
            // Admin responds to any message in shared memory
            printf("[Admin] Processing message: %s\n", shared_memory);
            fflush(stdout);

            memset(shared_memory, 0, SHM_SIZE);
            
            // VULNERABILITY: The admin occasionally copies the flag to memory
            // without proper access control checks
            if (rand() % 12 == 0) {
                strncpy(shared_memory, flag, FLAG_SIZE);
                printf("[Admin] Flag copied to memory for verification\n");
                fflush(stdout);

                // Admin forgot to clear the flag after verification!
                sleep(3);
                memset(shared_memory, 0, SHM_SIZE);
            }
        }
        
        // Release mutex
        sem_operation(0, 1);
    }
    
    return NULL;
}

// Send message to client
void send_to_client(int socket, const char *message) {
    send(socket, message, strlen(message), 0);
}

// Print menu to client
void print_menu(int client_socket) {
    char menu[BUFFER_SIZE];
    snprintf(menu, sizeof(menu), 
             "\n===== Secure Message System =====\n"
             "1. Register\n"
             "2. Login\n"
             "3. Access Resource\n"
             "4. Send Message\n"
             "5. View Message\n"
             "6. Exit\n"
             "Choice: ");
             fflush(stdout);
    
    send_to_client(client_socket, menu);
}

// Register a new user
void register_user(int client_socket, char *username) {
    pthread_mutex_lock(&users_mutex);
    
    if (user_count >= MAX_USERS) {
        send_to_client(client_socket, "Maximum number of users reached\n");
        pthread_mutex_unlock(&users_mutex);
        return;
    }
    
    // Check if username already exists
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].name, username) == 0) {
            send_to_client(client_socket, "Username already exists\n");
            pthread_mutex_unlock(&users_mutex);
            return;
        }
    }
    
    User new_user;
    new_user.id = user_count + 1;
    new_user.privilege = 0; // Regular user
    new_user.logged_in = 0;
    strncpy(new_user.name, username, sizeof(new_user.name) - 1);
    new_user.name[sizeof(new_user.name) - 1] = '\0';
    
    // VULNERABILITY: No proper validation on username
    users[user_count++] = new_user;
    
    send_to_client(client_socket, "User registered successfully!\n");
    pthread_mutex_unlock(&users_mutex);
}

// Login user
void login_user(int client_socket, char *username, int client_id) {
    pthread_mutex_lock(&users_mutex);
    int found = 0;
    
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].name, username) == 0) {
            char msg[100];
            snprintf(msg, sizeof(msg), "Login successful! Welcome, %s\n", username);
            fflush(stdout);

            send_to_client(client_socket, msg);
            
            users[i].logged_in = 1;
            clients[client_id].user_id = users[i].id;
            
            found = 1;
            break;
        }
    }
    
    if (!found) {
        send_to_client(client_socket, "User not found\n");
    }
    
    pthread_mutex_unlock(&users_mutex);
}

// Access resource
void access_resource(int client_socket) {
    send_to_client(client_socket, "Attempting to access resource...\n");
    
    // VULNERABILITY: Race condition possible here
    // Try to get resource access semaphore
    sem_operation(2, -1);
    
    send_to_client(client_socket, "Resource access granted\n");
    
    // Read from shared memory
    char msg[BUFFER_SIZE];
    snprintf(msg, sizeof(msg), "Resource content: %s\n", shared_memory);
    fflush(stdout);

    send_to_client(client_socket, msg);
    
    // Sleep to simulate work and increase chance of race condition
    sleep(1);
    
    // Release resource
    sem_operation(2, 1);
}

// Send message
void send_message(int client_socket, char *message) {
    // Acquire mutex
    sem_operation(0, -1);
    
    // Write to shared memory
    strncpy(shared_memory, message, SHM_SIZE - 1);
    shared_memory[SHM_SIZE - 1] = '\0';
    
    // Signal that a message is available
    sem_operation(1, 1);
    
    // Release mutex
    sem_operation(0, 1);
    
    send_to_client(client_socket, "Message sent\n");
}

// View message
void view_message(int client_socket) {
    send_to_client(client_socket, "Waiting for a message...\n");
    
    // Wait for message signal
    sem_operation(1, -1);
    
    // Acquire mutex
    sem_operation(0, -1);
    
    // Read from shared memory
    char msg[BUFFER_SIZE];
    snprintf(msg, sizeof(msg), "Message: %s\n", shared_memory);
    fflush(stdout);

    send_to_client(client_socket, msg);
    
    // VULNERABILITY: Message is not cleared, leading to potential info leak
    
    // Release mutex
    sem_operation(0, 1);
}

// Handle client connection
void *handle_client(void *arg) {
    int client_id = *((int *)arg);
    int client_socket = clients[client_id].socket;
    free(arg);
    
    char buffer[BUFFER_SIZE];
    int choice;
    
    send_to_client(client_socket, "=== Secure Message System ===\n");
    send_to_client(client_socket, "Try to capture the flag if you can!\n");
    
    while (1) {
        print_menu(client_socket);
        
        int bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
        if (bytes_received <= 0) {
            break;
        }
        buffer[bytes_received] = '\0';
        
        choice = atoi(buffer);
        
        switch (choice) {
            case 1: // Register
                send_to_client(client_socket, "Enter username: ");
                bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
                if (bytes_received <= 0) break;
                buffer[bytes_received] = '\0';
                register_user(client_socket, buffer);
                break;
                
            case 2: // Login
                send_to_client(client_socket, "Enter username: ");
                bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
                if (bytes_received <= 0) break;
                buffer[bytes_received] = '\0';
                login_user(client_socket, buffer, client_id);
                break;
                
            case 3: // Access Resource
                access_resource(client_socket);
                break;
                
            case 4: // Send Message
                send_to_client(client_socket, "Enter message: ");
                bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
                if (bytes_received <= 0) break;
                buffer[bytes_received] = '\0';
                send_message(client_socket, buffer);
                break;
                
            case 5: // View Message
                view_message(client_socket);
                break;
                
            case 6: // Exit
                send_to_client(client_socket, "Goodbye!\n");
                close(client_socket);
                clients[client_id].is_active = 0;
                return NULL;
                
            default:
                send_to_client(client_socket, "Invalid choice\n");
        }
    }
    
    // Client disconnected
    close(client_socket);
    clients[client_id].is_active = 0;
    return NULL;
}


int openflag() {
    FILE *flag_file = fopen("flag.txt", "r");
    if (flag_file == NULL) {
        perror("Error opening flag file");
        return -1;
    }
    
    if (fgets(flag, FLAG_SIZE, flag_file) == NULL) {
        perror("Error reading flag");
        fclose(flag_file);
        return -1;
    }
    size_t len = strlen(flag);
    if (len > 0 && flag[len-1] == '\n') {
        flag[len-1] = '\0';
    }
    
    fclose(flag_file);
    return 0;
}

// Main function
int main() {
    // Set up signal handler
    signal(SIGINT, sigint_handler);
    
    // Seed random number generator
    srand(time(NULL));
    openflag();
    
    // Initialize resources
    initialize_semaphore();
    initialize_shared_memory();
    initialize_server();
    
    // Create admin thread
    if (pthread_create(&admin_thread, NULL, admin_routine, NULL) != 0) {
        perror("pthread_create");
        cleanup();
        exit(1);
    }
    
    printf("=== Secure Message System Server Started ===\n");
    fflush(stdout);

    
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    
    while (1) {
        // Accept new connection
        int client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
        if (client_socket < 0) {
            perror("accept");
            continue;
        }
        
        printf("[+] New connection from %s:%d\n", 
               inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
        
        // Find available client slot
        int client_id = -1;
        for (int i = 0; i < MAX_CLIENTS; i++) {
            if (!clients[i].is_active) {
                client_id = i;
                break;
            }
        }
        
        if (client_id == -1) {
            // No slots available
            send_to_client(client_socket, "Server is full. Try again later.\n");
            close(client_socket);
        } else {
            // Set up client
            clients[client_id].socket = client_socket;
            clients[client_id].address = client_addr;
            clients[client_id].is_active = 1;
            clients[client_id].user_id = -1;
            
            // Create thread for client
            int *arg = malloc(sizeof(int));
            *arg = client_id;
            if (pthread_create(&clients[client_id].thread, NULL, handle_client, arg) != 0) {
                perror("pthread_create");
                free(arg);
                close(client_socket);
                clients[client_id].is_active = 0;
            }
        }
    }
    
    return 0;
}
