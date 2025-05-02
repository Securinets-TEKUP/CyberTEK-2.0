from ecdsa import VerifyingKey, NIST256p
import hashlib

# Load public key
with open("public.pem", "rt") as f:
    pub_key = VerifyingKey.from_pem(f.read())

# Get curve parameters
curve = pub_key.curve
G = curve.generator
n = curve.order

# Message and signature from message.txt
message_hex = "3343435f31735f4272306b336e"
signature = (81656283118670857341884602426840867029778987004268103130686475270399518147476,51070035169163094288170086161579499981349116068533637659570945874191030730099)

r, s = signature
h = hashlib.sha256(bytes.fromhex(message_hex)).digest()
h_int = int.from_bytes(h, 'big')

# Known nonce from the bad implementation
k = 0xdeadbeef

# Recover private key d = (s*k - h) / r mod n
r_inv = pow(r, -1, n)
d = ( (s * k - h_int) * r_inv ) % n

print(f"Recovered private key: {d}")

plaintext = bytes.fromhex(message_hex).decode('utf-8')
print(f"\nRecovered plaintext message: {plaintext}_{d}")
