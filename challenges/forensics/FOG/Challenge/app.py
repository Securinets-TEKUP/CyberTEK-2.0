#!/usr/bin/env python3
correct_answers = {

"identify the hacker IP and the HTTP RCE": "192.168.1.100_cat /etc/passwd",
"identify the leaked username and password flag format : tool_user_hash":"sekurlsa_Administrator_31d6cfe0d16ae931b73c59d7e0c089c0",
"identify the malicious domain":"malicious-c2.xyz",
"Find the Hidden Message":"This_is_Low_Level"
}

user_answers = {}

print("== FOB ==\n== by cybereagle2001 ==\nAnswer The questions save the network:\n")

for question in correct_answers:
    user_answers[question] = input(f"{question}\n> ")

if user_answers == correct_answers:
    print("Good job! \nFlag: Securinets{No1sy_Netw0rk}")
else:
    print("Sorry, incorrect answers.")
