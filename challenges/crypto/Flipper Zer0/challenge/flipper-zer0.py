from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from Crypto.Cipher import AES
from fastecdsa.curve import P256 as curve
from fastecdsa.point import Point
import os, random, hashlib, json

flag = 'Securinets{e802a90c48c74a977247f03bc9abc2ea}'.lstrip("Securinets{").rstrip("}")

key = os.urandom(16)
iv = os.urandom(16)

G = Point(curve.gx, curve.gy, curve=curve)
order = curve.q
p = curve.p
a = curve.a
b = curve.b

def get_flag(privkey):
    x = bytes_to_long(flag.encode())
    assert x < order
    y2 = (x**3 + a*x + b) % p
    y = pow(y2, (p+3)//4, p)
    Q = Point(x, y, curve=curve)
    T = privkey*Q
    return long_to_bytes(T.x)

def generate_keys():
    privkey = random.randrange(1, order - 1)
    pubkey = (privkey * G)
    return (pubkey, privkey)

def ecdsa_sign(message, privkey):
    z = int(hashlib.sha256(message).hexdigest(), 16)
    k = random.randrange(1, order - 1)
    r = (k*G).x % order
    s = (inverse(k, order) * (z + r*privkey)) % order
    return (r, s)

def ecdsa_verify(message, r, s, pubkey):
    r %= order
    s %= order
    if s == 0 or r == 0:
        return False
    z = int(hashlib.sha256(message).hexdigest(), 16)
    s_inv = inverse(s, order)
    u1 = (z*s_inv) % order
    u2 = (r*s_inv) % order
    W = u1*G + u2*pubkey
    return W.x == r

def aes_gcm_encrypt(plaintext):
    aes = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = aes.encrypt_and_digest(plaintext)
    return tag + ciphertext

def aes_gcm_decrypt(ciphertext, tag):
    aes = AES.new(key, AES.MODE_GCM, nonce=iv)
    plaintext = aes.decrypt_and_verify(ciphertext, tag)
    return plaintext


if __name__ == '__main__':
    print("Welcome to Flipper Zer0!")

    pubkey, privkey = generate_keys()
    signkey = aes_gcm_encrypt(long_to_bytes(privkey))

    print("Here are your public key and signing key :")
    print(json.dumps({"pubkey": {"x": hex(pubkey.x), "y": hex(pubkey.y)}, "signkey": signkey.hex()}))

    while True:
        print("\nOptions:\n - sign(msg, signkey) : Sign a message\n - verify(msg, signature, pubkey) : Verify a message\n - change_keys : Change your keys\n - get_flag : Get the flag\n - leave : Leave the server\n")

        try:
            inp = json.loads(input('> '))

            if 'option' not in inp:
                print(json.dumps({'error': 'You must send an option'}))

            elif inp['option'] == 'sign':
                msg = bytes.fromhex(inp['msg'])
                signkey = bytes.fromhex(inp['signkey'])
                signkey_ciphertext, signkey_tag = signkey[16:], signkey[:16]
                sk = bytes_to_long(aes_gcm_decrypt(signkey_ciphertext, signkey_tag))

                r, s = ecdsa_sign(msg, sk)
                print(json.dumps({'r': hex(r), 's': hex(s)}))

            elif inp['option'] == 'verify':
                msg = bytes.fromhex(inp['msg'])
                r = int(inp['r'], 16)
                s = int(inp['s'], 16)
                px = int(inp['px'], 16)
                py = int(inp['py'], 16)
                pub = Point(px, py, curve=curve)

                verified = ecdsa_verify(msg, r, s, pub)

                if verified:
                    print(json.dumps({'result': 'Success'}))
                else:
                    print(json.dumps({'result': 'Invalid signature'}))

            elif inp['option'] == 'change_keys':
                pubkey, privkey = generate_keys()
                signkey = aes_gcm_encrypt(long_to_bytes(privkey))
                print("Here are your *NEW* public key and signing key :")
                print(json.dumps({"pubkey": {"x": hex(pubkey.x), "y": hex(pubkey.y)}, "signkey": signkey.hex()}))

            elif inp['option'] == 'get_flag':
                encrypted_flag = get_flag(privkey)
                print(json.dumps({'flag': encrypted_flag.hex()}))

            elif inp['option'] == 'leave':
                print('Adios :)')
                break
        
        except:
            print(json.dumps({'error': 'Oops! Something went wrong'}))
            break
