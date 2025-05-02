from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Math._IntegerGMP import IntegerGMP

def generate_key():
    return ECC.generate(curve='P-256')

def flawed_sign(private_key, message):
    # Convert all values to IntegerGMP for consistent arithmetic
    h = SHA256.new(message).digest()
    h_int = IntegerGMP(int.from_bytes(h, 'big'))
    n = private_key._curve.order
    
    # Using predictable nonce (as IntegerGMP)
    k = IntegerGMP(0xdeadbeef)
    
    # ECDSA signing
    curve = private_key._curve
    K = int(k) * curve.G  # Point multiplication requires int
    r = IntegerGMP(int(K.x)) % n
    
    # All operations with IntegerGMP
    k_inv = k.inverse(n)
    dr = private_key.d * r
    h_plus_dr = h_int + dr
    s = (k_inv * h_plus_dr) % n
    
    return (int(r), int(s))  # Convert back to Python ints for output

if __name__ == "__main__":
    key = generate_key()
    
    # Save public key
    with open("public.pem", "wt") as f:
        f.write(key.public_key().export_key(format='PEM'))
    
    message = b"XXXXXXXXXXXXXXXXXX"
    signature = flawed_sign(key, message)
    
    with open("message.txt", "wt") as f:
        f.write(f"Message: {message.hex()}\n")
        f.write(f"Signature (r,s): {signature[0]},{signature[1]}")
