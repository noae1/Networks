#!/usr/bin/python3
import socket
import sys
import ipaddress


def connect_to_server(hostname='localhost', port=1337):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((hostname, port))
        return client_socket
    except ConnectionRefusedError:
        print(f"Connection to {hostname}:{port} refused.")
        sys.exit(1)
    except socket.error as e:
        print(f"Socket error occurred: {e}")
        sys.exit(1)

def authenticate_user(client_socket):
    data = client_socket.recv(1024).decode('utf-8')  # data = Welcome! Please log in
    print(data)  
    while True:    

        if "Please log in" in data or "Failed to login" in data:
            user_input = input()
            password_input = input()
            login_message = f"{user_input}\n{password_input}"
            
            # Check if the login message is in the correct format
            if "User:" not in login_message or "Password:" not in login_message:
                print("Invalid login format. Closing connection.")
                return False

            client_socket.send(login_message.encode('utf-8'))

            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(data)
           
            if ", good to see you" in data:
                return True  # connected

def handle_user_commands(client_socket):

    while True:
        command = input()
        Invalid = False

        if command == "quit":
            client_socket.send(command.encode('utf-8'))
            break

        if command.startswith("calculate:"):
            cmd = command.split(":")[1][1:].split(" ")
            if len(cmd) > 3:
                Invalid = True
            x, operator, z = cmd[0], cmd[1], cmd[2]

            if operator not in "+-/*^" or not x.isdigit() or not z.isdigit() or Invalid:
                print("Invalid command, disconnect")
                client_socket.send("quit".encode('utf-8'))
                return
            
            client_socket.send(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            if "closing socket" in response:
                print(f"{response}, disconnect")
                return 
            else:
                print(response)

        elif command.startswith("max:"):          
            numbers_stream = command.split(":")[1][1:]
            if numbers_stream[0] != "(" or numbers_stream[-1] != ")":
                print("Invalid command, disconnect")
                client_socket.send("quit".encode('utf-8'))
                return
            
            # Check if the numbers are valid (supporting negative numbers)
            for number in numbers_stream[1:-1].split(" "):
                if not number.lstrip('-').isdigit():  # Allow leading '-' for negative numbers
                    print("Invalid number, disconnect")
                    client_socket.send("quit".encode('utf-8'))
                    return
                
            client_socket.send(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            
            if "closing socket" in response:
                print(f"{response}, disconnect")
                return 
            else:
                print(response)

        elif command.startswith("factors:"):
            number = command.split(":")[1][1:]
            
            if not number.isdigit():
                print("Invalid command, disconnect")
                client_socket.send("quit".encode('utf-8'))
                return
            client_socket.send(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            
            if "closing socket" in response:
                print(f"{response}, disconnect")
                return 
            else:
                print(response)
        else:
            print("Invalid command, disconnect")
            client_socket.send("quit".encode('utf-8'))
            return

def is_valid_ip_or_hostname(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        try:
            socket.gethostbyname(address)
            return True
        except socket.error:
            # If both attempts fail, the address is not valid
            return False


def run_client(hostname='localhost', port=1337):
    if len(sys.argv) > 1:  # hostname is given
        hostname = sys.argv[1]
    if len(sys.argv) > 2:  # port name is given
        port = int(sys.argv[2])

    if not is_valid_ip_or_hostname(hostname):
        print(f"{hostname} is not a valid IP address.")
        hostname = 'localhost'
        port = 1337

    client_socket = connect_to_server(hostname, port)

    try:
        login = authenticate_user(client_socket)
        if login:
            handle_user_commands(client_socket)
        # else - client close the connection (in finally)
            
    finally:
        # disconnect
        client_socket.close()


if __name__ == "__main__":
    run_client()
