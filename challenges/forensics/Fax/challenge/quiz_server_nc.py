#!/usr/bin/env python3

import sys

FLAG = "Securinets{Y0u_4r3_7oo_0ld_aNd_5m4rt}"

questions = [
    {"question": "whats the attackers ip @", "answer": "10.1.31.101"},
    {"question": "whats the attacker mac @", "answer": "00:08:02:1c:47:ae"},
    {"question": "the username found", "answer": "director@igakuin.com"},
    {"question": "the password found", "answer": "Global786@"},
    {"question": "whats the protocol used for data exfil", "answer": "smtp"},
    {"question": "whats the mail transfer agent used", "answer": "postfix"},
    {"question": "whats the data being stealed", "answer": "coockies"},
    {"question": "in what format their being encoded", "answer": "base64"},
    {"question": "give me the  sha256 for the coockies", "answer": "8f2523b1647d856ca732072c036582b253bcc1e1f5dfaac5658bbbdeeed1316b"},
    {"question": "whats the expiry value for the host .reddit.com", "answer": "13382914235858980"}
]

def main():
    print("Welcome to FAX!")
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
