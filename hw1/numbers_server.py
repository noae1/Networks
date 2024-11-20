#!/usr/bin/python3
import sys
import socket
import select
import math


def close_socket(reason, sock, socket_list, authenticated_sockets):
    sock.send((f"{reason}, closing socket").encode())
    sock.close()
    authenticated_sockets.remove(sock)
    socket_list.remove(sock)

def handle_user_login(msg, sock, authenticated_sockets, socket_list, users_dict):
    if sock in authenticated_sockets:
        sock.send("You are already logged in".encode())
        sock.close()
        socket_list.remove(sock)
        return
    lines = msg.split("\n")
    if len(lines) != 2 or lines[1].split(":")[0] != "Password":
        sock.send("Failed to login.".encode())
        return
    user = lines[0].split(":")[1][1:]
    password = lines[1].split(":")[1][1:]
    if user in users_dict:
        if users_dict[user] == password:
            sock.send((f"Hi {user}, good to see you.").encode())
            authenticated_sockets.append(sock)
        else:
            sock.send("Failed to login.".encode())
    else:
        sock.send("Failed to login.".encode())

def handle_calculation(msg, sock, authenticated_sockets, socket_list):
    if sock not in authenticated_sockets:
        sock.send("Not authenticated".encode())
        sock.close()
        socket_list.remove(sock)
        return
    try:
        x, y, z = msg.split(":")[1][1:].split(" ")
        x = int(x)
        z = int(z)
        if y == "+":
            result = x + z
        elif y == "-":
            result = x - z
        elif y == "*":
            result = x * z
        elif y == "/":
            result = x / z
        elif y == "^":
            result = x ** z
        else:
            raise ValueError("Invalid operation")
        
        if not (-2**31 <= result <= 2**31 - 1):
            sock.send("error: result is too big".encode())
            return
        
        result = int(result) if result.is_integer() else round(result, 2)
        sock.send((f"response: {result}.").encode())
    except:
        close_socket("Invalid calculation", sock, socket_list, authenticated_sockets)

def handle_maximum(msg, sock, authenticated_sockets, socket_list):
    if sock not in authenticated_sockets:
        sock.send("Not authenticated".encode())
        sock.close()
        socket_list.remove(sock)
        return
    try:
        numbers = list(map(int, msg.split(":")[1][2:-1].split()))
        if not numbers:
            raise ValueError("No numbers provided")
        
        maximum = max(numbers)
        sock.send(f"the maximum is {maximum}".encode())
    except Exception:
        close_socket("Invalid input", sock, socket_list, authenticated_sockets)


def handle_factors(msg, sock, authenticated_sockets, socket_list):
    if sock not in authenticated_sockets:
        sock.send("Not authenticated".encode())
        sock.close()
        socket_list.remove(sock)
        return
    try:
        num = int(msg.split(":")[1][1:])
        original_num = num
        if 0 <= num < 2:
            sock.send(f"the prime factors of {original_num} are:".encode())
            return
        if num < 0:
            close_socket("Invalid input", sock, socket_list, authenticated_sockets)
        
        factors = []
        divisor = 2
        while num > 1:
            while num % divisor == 0:
                factors.append(divisor)
                num //= divisor
            divisor += 1
            if divisor * divisor > num:
                if num > 1:
                    factors.append(num)
                break
        
        distinct_sorted_factors = sorted(set(factors))
        factors_str = ", ".join(map(str, distinct_sorted_factors))
        sock.send(f"the prime factors of {original_num} are: {factors_str}".encode())
    except Exception as e:
        #print(str(e))
        close_socket("Invalid input", sock, socket_list, authenticated_sockets)

def create_users_dict(users_file_path):
    users_dict = {}
    try:
        with open(users_file_path, "r") as users_file:
            for line in users_file:
                line = line.strip()
                user, password = line.split()
                users_dict[user] = password
    except FileNotFoundError:
        print("Users file not found.")
        return False
    except ValueError:
        print("Invalid format in users file.")
        return False
    return users_dict

def main():
    port = "1337"
    #parsing args
    if(len(sys.argv) == 3): # port is given
        port = sys.argv[2]
    #anyway, need to parse users file
    users_file_path = sys.argv[1]
    try:
        users_dict = create_users_dict(users_file_path)
    except Exception as e:
        print(f"Error reading users file: {e}")
        sys.exit(1)
       
    # Create socket
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', int(port)))
        server_socket.listen(len(users_dict))
    except OSError as e:
        print(f"Error binding socket: {e}")
        if server_socket:
            server_socket.close()
        sys.exit(1)
    

    socket_list = [server_socket]
    authenticated_sockets = []

    try:
        while True:
            ready_to_read, _ , in_error = select.select(socket_list, [], [], 0)
            for sock in ready_to_read:
                if sock == server_socket:
                    client_sock, _ = server_socket.accept()
                    client_sock.send("Welcome! Please log in.".encode())
                    socket_list.append(client_sock)
                else:
                    try:
                        msg = sock.recv(1024).decode()
                        cmd = msg.split(":")[0]
                        if cmd == "User":
                            handle_user_login(msg, sock, authenticated_sockets, socket_list, users_dict)
                        elif cmd == "calculate":
                            handle_calculation(msg, sock, authenticated_sockets, socket_list)
                        elif cmd == "max":
                            handle_maximum(msg, sock, authenticated_sockets, socket_list)
                        elif cmd == "factors":
                            handle_factors(msg, sock, authenticated_sockets, socket_list)
                        elif cmd == "quit":
                            sock.close()
                            socket_list.remove(sock)
                            if sock in authenticated_sockets:
                                authenticated_sockets.remove(sock)
                        else:
                            sock.send("Invalid command, closing socket".encode())
                            sock.close()
                            socket_list.remove(sock)
                            if sock in authenticated_sockets:
                                authenticated_sockets.remove(sock)
                    except Exception:
                        sock.close()
                        socket_list.remove(sock)
                        if sock in authenticated_sockets:
                            authenticated_sockets.remove(sock)

            for notified_socket in in_error:
                socket_list.remove(notified_socket)
                notified_socket.close()
                if notified_socket in authenticated_sockets:
                    authenticated_sockets.remove(notified_socket)
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
