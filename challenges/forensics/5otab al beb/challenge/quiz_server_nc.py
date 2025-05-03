#!/usr/bin/env python3

import sys

FLAG = "Securinets{Wh4t_4_6olD3n_Era!}"

questions = [
    {"question": "whats the victim ip @ :", "answer": "172.16.1.84"},
    {"question": "whats the victim mac @ :", "answer": "00:28:f8:df:77:b4"},
    {"question": "whats the attacker ip @ :", "answer": "91.222.173.186"},
    {"question": "whats the attacker mac @ :", "answer": "00:26:ca:1b:74:3f"},
    {"question": "whats the malicious hostname :", "answer": "flexiblemaria.com"},
    {"question": "provide the md5 of the powershell script :", "answer": "974baa3b6dea92e9d1a8ffe4f69742d5"},
    {"question": "whats the executable name :", "answer": "Autoit3.exe"},
    {"question": "whats the malware name :", "answer": "darkgate"}
]

def main():
    print("Welcome to 5otab al beb!")
    print("Answer all questions correctly to receive the flag.\n")

    for idx, q in enumerate(questions):
        print(f"Question {idx + 1}: {q['question']}")
        print("Your answer: ", end="")
        sys.stdout.flush()
        
        answer = sys.stdin.readline().strip()
        if answer.lower() != q["answer"].lower():
            print("Wrong answer. Try again later!")
            return

    print("Congratulations! You answered all questions correctly.")
    print(f"Here is your flag: {FLAG}")

if __name__ == "__main__":
    main()
