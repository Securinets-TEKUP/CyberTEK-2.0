section .text
    global _start

_start:
    ; Push exit function to stack (address of exit_syscall)
    mov rax, exit_syscall
    push rax

    ; Print first message
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [msg1]
    mov rdx, msg1_len
    syscall

    ; Print prompt
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [msg2]
    mov rdx, msg2_len
    syscall

    ; Allocate stack space and read input
    sub rsp, 64         ; Make space for buffer
    mov rax, 0          ; sys_read
    mov rdi, 0          ; stdin
    mov rsi, rsp        ; buffer = stack pointer
    mov rdx, 512        ; Overflow possible (reads >64 bytes)
    syscall

    ; Execution will continue to exit_syscall if not hijacked
    xor rsi, rsi
    add rsp, 64
    ret

exit_syscall:
    ; Clean exit function
    mov rax, 60         ; sys_exit
    xor rdi, rdi        ; exit code 0
    syscall

    ; Inline gadgets (raw in instruction stream)
    pop rax
    ret

section .rodata
    msg1 db "No frills, just like my bald head—this binary is as raw as it gets.", 0x0a
    msg1_len equ $ - msg1

    msg2 db "Tell me a secret: "
    msg2_len equ $ - msg2
