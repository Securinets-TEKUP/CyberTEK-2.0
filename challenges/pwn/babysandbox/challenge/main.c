#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <sys/sendfile.h>

void setup() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
}

void challenge() {
    puts("----------------Welcome to BABYSANDBOX----------------");
    puts("I invite you to upload a custom shellcode to do whatever you want");
    puts("Well whatever we agree on");

    char jail_path[] = "/tmp/jail-XXXXXX";
    mkdtemp(jail_path);
    chroot(jail_path);
    chdir("/");

    printf(">");
    void *shellcode = mmap((void *)0x1337000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);
    read(0, shellcode, 0x1000);

    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendfile), 0); 
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mkdir), 0); 
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(chdir), 0); 
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(chroot), 0); 
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(stat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    

    puts("Executing shellcode!\n");
    seccomp_load(ctx);
    ((void(*)())shellcode)();
    seccomp_release(ctx);
}

int main() {
    setup();
    challenge();
    return 0;
}
