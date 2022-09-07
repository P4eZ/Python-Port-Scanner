# Date: 9/7/2022
# Author: P4eZ

# This program is a simple python port scanner created for the command line interface. The scanner uses normal TCP
# connections to scan for open ports. Once the port connects, the program tells the user the port is open, then
# closes the connection. The Python Port Scanner features the argparse, socket, termcolor, and time modules.

import argparse  # Adds arguments to the application
import socket  # Module for network communication
import termcolor  # Colors the text in the terminal
import time  # Times the process of the program

# Ascii art for the intro of the program later in the file
ascii_art = '''  _____  _____ ____________    _____________________   __   _____________
 |_____]|     |_____/  |       |_____|      |_____| \  | \  |_____|_____/
 |      |_____|    \_  |       ______|_____ |     |  \_|  \_|_____|    \_
                                                                         '''

# Initializing arguments/options in the application. Adds descriptions to the program UI
parser = argparse.ArgumentParser(description="A simple Python port scanner.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog='''
This simple python port scanner connects to ports using TCP. This is a full scan completing the TCP three-way handshake

Example:
     main.py -i 127.0.0.1 -p 22-100  # Scans ports 22-100
     main.py --ip 192.168.1.159 --port 53  # Scans ports 1-53
     main.py -i 10.0.0.32  # Scans the IP address '10.0.0.32'

Key:
     Condition unknown  # The port is being blocked by restrictive permissions (possibly by a firewall)
     Port is open  # The port is open and accepting connections
     Port is closed  # The port is closed and is refusing connections
''')

parser.add_argument('-p', '--port', type=str, help="indicates the port range you want to scan")
parser.add_argument('-i', '--ip', type=str, required=True, help="sets the desired IP address")
args = parser.parse_args()

# The main part of the program
if __name__ == '__main__':
    try:  # Checks keyboard interrupt exception for the entire program
        try:  # Checks input validation for port option
            ports = args.port
            ip = args.ip
            if ports is None:
                ports = "1-65535"
            if "-" not in ports:
                minimum_port = 1
                maximum_port = int(ports)
            else:
                index = ports.index("-")
                minimum_port = int(ports[0:index])
                maximum_port = int(ports[index + 1:])
        except ValueError:
            print(termcolor.colored("[*] An incorrect value has been entered. Use '-h' for help.", "red"))
            exit()

        # Intro to application
        print(ascii_art)
        print("Welcome to the Python Port Scanner!")
        print("Disclaimer: This tool is only for educational use only. If you do not wish to continue with the scan,"
              " please cancel using Control + C.")
        time.sleep(3)

        # Countdown after disclaimer
        print(termcolor.colored("[*] Executing scan in...", "blue"))
        x = 5
        while x != 0:
            print(termcolor.colored(str(x), "blue"), end=" ", flush=True)
            x = x - 1
            time.sleep(1)

        # Begin scanning
        sock = socket.socket()
        print(termcolor.colored(f"[*] Scanning {ip} on ports {minimum_port}-{maximum_port}...", "green"))
        for port in range(minimum_port, maximum_port + 1):  # Connects/closes each port based on the min/max values
            try:  # Checks any errors to return the correct information
                sock.connect((ip, port))
                print(termcolor.colored(f"[+] {ip}> Port {port} is open.", "green"))
                sock.close()
            except ConnectionRefusedError:
                print(termcolor.colored(f"[-] {ip}> Port {port} is closed.", "red"))
            except OSError:
                print(termcolor.colored(f"[*] {ip}> Port {port}'s condition is unknown.", "blue"))
    except KeyboardInterrupt:
        print(termcolor.colored("[*] Exiting program...", "blue"))
