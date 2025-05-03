import math, random, base64, json, yaml

random.seed(999999999)  
NUM_QUBITS = 100000
alice_bits = [random.randrange(2) for _ in range(NUM_QUBITS)]
alice_bases = [random.choice(['+','x']) for _ in range(NUM_QUBITS)]
qubits = []
for bit, base in zip(alice_bits, alice_bases):
    if base == '+':
        if bit == 0:
            qubit = {'real': 0.0, 'imag': 1.0}
        else:
            qubit = {'real': 1.0, 'imag': 0.0}
    else:
        amp = 1/math.sqrt(2)
        if bit == 0:
            qubit = {'real': amp, 'imag': amp}
        else:
            qubit = {'real': amp, 'imag': -amp}
    qubits.append(qubit)
bob_bases = [random.choice(['+','x']) for _ in range(NUM_QUBITS)]
bob_bits = []
for i in range(NUM_QUBITS):
    if bob_bases[i] == alice_bases[i]:
        bob_bits.append(alice_bits[i])
    else:
        bob_bits.append(random.randrange(2))
shared_key_bits = [alice_bits[i] for i in range(NUM_QUBITS)
                   if bob_bases[i] == alice_bases[i]]

flag = b"Securinets{QKD_zzzzzzzzzzzzzzzzzzMrx0rd}"  

flag_bits = []
for byte in flag:
    for j in range(8):
        flag_bits.append((byte >> (7-j)) & 1)
if len(shared_key_bits) < len(flag_bits):
    shared_key_bits = (shared_key_bits * (len(flag_bits) // len(shared_key_bits) + 1))[:len(flag_bits)]
cipher_bits = [flag_bits[i] ^ shared_key_bits[i] for i in range(len(flag_bits))]
cipher_bytes = []
for i in range(0, len(cipher_bits), 8):
    byte = 0
    for b in cipher_bits[i:i+8]:
        byte = (byte << 1) | b
    cipher_bytes.append(byte)
ciphertext_b64 = base64.b64encode(bytes(cipher_bytes)).decode()

public_data = {
    'qubits': qubits,
    'bob_bases': ''.join(bob_bases),
    'ciphertext': ciphertext_b64
}

with open("challenge.yml", "w") as f:
    yaml.dump(public_data, f, default_flow_style=False)

print("Challenge data written to challenge.yml")
