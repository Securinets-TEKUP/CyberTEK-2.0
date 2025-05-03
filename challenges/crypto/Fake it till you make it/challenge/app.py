from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime, inverse, GCD, bytes_to_long, long_to_bytes
import socket
import random
import argparse
import os
from threading import Thread, Event

HOST = '0.0.0.0'
PORT = 12345
BUFFER_SIZE = 4096
KEY_SIZE = 1024
MAX_RETRIES = 1
TIMEOUT = 5.0

def int_to_bytes(x): return x.to_bytes((x.bit_length()+7)//8, 'big')
def bytes_to_int(b): return int.from_bytes(b, 'big')

def load_or_generate_key():
    PRIMES_FILE = "rsa_primes.txt"
    
    if os.path.exists(PRIMES_FILE):
        with open(PRIMES_FILE, "r") as f:
            try:
                p = int(f.readline().strip())
                q = int(f.readline().strip())
                if p == q:
                    raise ValueError("Invalid primes")
            except:
                os.remove(PRIMES_FILE)
                return load_or_generate_key()
    else:
        while True:
            p, q = getPrime(KEY_SIZE), getPrime(KEY_SIZE)
            if p != q:
                with open(PRIMES_FILE, "w") as f:
                    f.write(f"{p}\n{q}\n")
                break
    
    while True:
        n = p * q
        phi = (p-1)*(q-1)
        e = getPrime(30)
        
        if GCD(e, phi) == 1:
            try:
                d = inverse(e, phi)
                return RSA.construct((n, e, d, p, q))
            except ValueError:
                continue

def raw_encrypt(message, public_key):
    m = bytes_to_long(message)
    if m >= public_key.n:
        raise ValueError("Message too long for key size")
    return long_to_bytes(pow(m, public_key.e, public_key.n))

def raw_decrypt(ciphertext, private_key):
    c = bytes_to_long(ciphertext)
    m = pow(c, private_key.d, private_key.n)
    return long_to_bytes(m)

class UDPChat:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT)
        self.running = Event()
        self.running.set()
        
    def reliable_send(self, data, addr):
        self.sock.sendto(data, addr)
    
    def background_receiver(self, private_key, callback):
        while self.running.is_set():
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                try:
                    decrypted = raw_decrypt(data, private_key).decode()
                    callback(decrypted)
                except:
                    pass
            except socket.timeout:
                continue

def start_server():
    chat = UDPChat()
    chat.sock.bind((HOST, PORT))
    print(f"Server ready on {PORT}. Waiting for client...")
    
    data, addr = chat.sock.recvfrom(260)
    peer_n, peer_e = bytes_to_int(data[:256]), bytes_to_int(data[256:])
    peer_key = RSA.construct((peer_n, peer_e))
    
    my_key = load_or_generate_key()
    chat.sock.sendto(int_to_bytes(my_key.n) + int_to_bytes(my_key.e), addr)
    
    def print_msg(msg): print(f"\nThem: {msg}\nYou: ", end='', flush=True)
    Thread(target=chat.background_receiver, args=(my_key, print_msg), daemon=True).start()
    
    while True:
        msg = input("You: ")
        if msg.lower() == 'exit': break
        encrypted = raw_encrypt(msg.encode(), peer_key)
        chat.reliable_send(encrypted, addr)

def start_client(server_ip):
    chat = UDPChat()
    addr = (server_ip, PORT)
    print(f"Connecting to {server_ip}...")
    
    my_key = load_or_generate_key()
    chat.sock.sendto(int_to_bytes(my_key.n) + int_to_bytes(my_key.e), addr)
    
    data, _ = chat.sock.recvfrom(260)
    peer_n, peer_e = bytes_to_int(data[:256]), bytes_to_int(data[256:])
    peer_key = RSA.construct((peer_n, peer_e))
    
    def print_msg(msg): print(f"\nThem: {msg}\nYou: ", end='', flush=True)
    Thread(target=chat.background_receiver, args=(my_key, print_msg), daemon=True).start()
    
    while True:
        msg = input("You: ")
        if msg.lower() == 'exit': break
        encrypted = raw_encrypt(msg.encode(), peer_key)
        chat.reliable_send(encrypted, addr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action="store_true")
    parser.add_argument("--client", action="store_true")
    parser.add_argument("--ip", default="localhost")
    args = parser.parse_args()
    
    if args.server: start_server()
    elif args.client: start_client(args.ip)
