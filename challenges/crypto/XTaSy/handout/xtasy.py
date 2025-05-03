from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, json

flag = 'Securinets{REDACTED}'

class AES_XTS:
    def __init__(self):
        self.key = os.urandom(64)
        self.tweak = os.urandom(16)

    def encrypt(self, plaintext):
        encryptor = Cipher(algorithms.AES(self.key), modes.XTS(self.tweak)).encryptor()
        return encryptor.update(plaintext.encode('latin-1'))

    def decrypt(self, ciphertext):
        decryptor = Cipher(algorithms.AES(self.key), modes.XTS(self.tweak)).decryptor()
        return decryptor.update(ciphertext).decode('latin-1')

def get_token(username, password):
    json_data = {
        "username": username,
        "admin": 0,
        "password": password
    }
    str_data = json.dumps(json_data, ensure_ascii=False)
    token = cipher.encrypt(str_data)
    return token

def check_admin(token):
    try:
        str_data = cipher.decrypt(token)
        json_data = json.loads(str_data)
        return json_data['admin']
    except:
        print(json.dumps({'error': f'Invalid JSON token'}))
        return None


if __name__ == '__main__':
    print("Welcome to the XTaSy vault! You need to become a VIP (admin) to get a taste.")
    
    cipher = AES_XTS()
    
    while True:
        print("\nOptions:\n - get_token(username, password) : Generate an access token\n - check_admin(token) : Check admin access\n - leave : Leave the vault\n")

        try:
            inp = json.loads(input('> '))
            assert isinstance(inp, dict)

        except:
            print(json.dumps({'error': 'Invalid JSON input'}))
            continue

        if 'option' not in inp:
            print(json.dumps({'error': 'You must send an option'}))

        elif inp['option'] == 'get_token':
            try:
                username = bytes.fromhex(inp['username']).decode('latin-1')
                password = bytes.fromhex(inp['password']).decode('latin-1')  
                token = get_token(username, password)
                print(json.dumps({'token': token.hex()}))
            
            except:
                print(json.dumps({'error': 'Invalid username or/and password'}))

        elif inp['option'] == 'check_admin':
            try:
                token = bytes.fromhex(inp['token'])
                assert len(token) >= 16

            except:
                print(json.dumps({'error': 'Invalid token'}))
                continue

            is_admin = check_admin(token)

            if is_admin is None:
                continue
            elif is_admin:
                print(json.dumps({'result': f'Access granted! Enjoy the taste of the flag {flag}'}))
            else:
                print(json.dumps({'result': 'Access denied! You don\'t seem a VIP'}))

        elif inp['option'] == 'leave':
            print('Adios :)')
            break
