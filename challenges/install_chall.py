import os,glob

categories = ["web","forensics","misc","osint","crypto","pwn","rev","hardware"]

for category in categories:
    if os.path.exists(f"./{category}"):
        challenges = glob.glob(f"{category}/*")
        print(challenges)
        challenges.sort()
        for challenge in challenges:
                print(f"[+] Installing challenge: {challenge}")
                os.system(f"python3 -m ctfcli challenge add \"{challenge}\" && python3 -m ctfcli challenge install \"{challenge}\"")
    else:
        print(f"[-] Cant find : {category}")
        exit(1)

exit(0)
