#!/bin/bash

# Define colors using ANSI escape codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[0;35m'
WHITE='\033[0;37m'
BOLD='\033[1m'
RESET='\033[0m'

# Define a list of questions, expected answers, and responses
questions=(
    "We'll start with a little sanity check, what's the sha256 hash of the file ?"
    "What is the full path to the malicious elf file ?"
    "The malware checks for virtual environments through a system file, what is it ? (full path)"
    "The malware installed a fake service as a persistence mechanism, what was the service name ?"
    "The malware connects to two C2 IPs, what are they ? (ip1 - ip2)"
    "The malware copies itself and imitates a library, where is it stored ?"
    "What command does the malware use to make the new copied file immutable ?"
    "What three debugging techniques does the malware specifically check for in its anti-debug routine ? (1-2-3)"
    "Looks like the malware is injecting an ssh key, what type is this key ?"
    "Where is that key being injected ? (full path)"
    "What command is the malware using to clear all traces of executed commands ?"
    "How often is the log cleaning function being executed ? (in seconds)"
)

answers=(
    "9f9d089ad84173dc40e910ad1ba1d584bb5c9b2e82ae2164d6bd22d3b37a7588"
    "/root/malware-f"
    "/proc/cpuinfo"
    ".dbus.service"
    "185.143.223.107 - 45.133.216.219"
    "/lib/.X11-unix/.X1"
    "chattr +i"
    "LD_PRELOAD-strace-ltrace"
    "ssh-ed25519"
    "/root/.ssh/authorized_keys"
    "history -c"
    "3600"
)

# Function to ask a question and verify the answer
ask_question() {
    local question="$1"
    local correct_answer="$2"
    local user_answer

    while true; do
        echo -e "${MAGENTA}${question}${WHITE}${RESET}"
        echo -e "${WHITE}> \c"
        read user_answer

        if [ "$user_answer" == "$correct_answer" ]; then
            echo -e "${GREEN}[+] Correct!${RESET}\n"
            break
        else
            echo -e "${RED}[-] Wrong Answer.${RESET}\n"
        fi
    done
}

# Main function
main() {
    echo -e "\n${YELLOW}Answer all the questions and you'll get the flag. Good Luck !! :3\n${RESET}"

    # Loop through each question and answer it
    for i in "${!questions[@]}"; do
        ask_question "${questions[$i]}" "${answers[$i]}"
    done

    # Once all questions are answered correctly, display the flag
    echo -e "${BLUE}${BOLD}[+] Here is the flag: Securinets{abe0f1332c5ae9c89e32a2fd5f6f1a18}${RESET}"
}

# Call the main function
main
