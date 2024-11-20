Protocol Specification:

------ Server Commands: ------

Execution of the server is done using the following command:
./numbers_server.py users_file [port]
"port" is the port number on which the server listens for connections. If not provided, the program will default to 1337.

1. User Login: Command: User: username Password: password (including enter between the lines)
   Response: If success: Hi username, good to see you. If failure: Failed to login.

2. Calculation:
   Command: calculate: X operator Z (e.g., calculate: 5 + 3),
   when, X and Z are integers and operator is one of the following: +, -, \*, /, ^.
   If the input received from the client is in the correct format:
   Server calculates the result (result = X op Z) and responds with the message: response : result. Else, the server closes the connection with the client.

3. Maximum:
   Command: max: (X1 X2 ... Xn) (e.g., max: (123 45 678 -987 654 32 -1) )
   Response: the maximum is {maximum_number}
   If the data received from the client does not adhere to the expected format (e.g., one of the inputs isn't a valid integer), the server terminates the connection with the client.

4. Prime factorization:
   Command: factors: number (e.g., factors: 49)
   Response: the prime factors of X are: p1, p2, ..., pn (e.g., the prime factors of 6 are: 2, 3)
   If the data received from the client does not adhere to the expected format (e.g., the input is not valid integer or negative), the server terminates the connection with the client.

5. Quit Command:
   Command: quit. Response: Close the connection with the client. Remove the client from the list of active sockets. If the client was authenticated, remove it from the list of authenticated sockets.

------ Client Commands: ------

Execution of the client is done using the following command: ./numbers_client.py [hostname [port]]
hostname and port number are optional parameters.

- "hostname" refers to the server's hostname or IP address. If not provided, the program will default to localhost.
- "port" is the port number on which the server listens for connections. If not provided, the program will default to 1337.

1. User Authentication:
   When a client connects to the server, the server sends him a message: Welcome!, Please log in.
   Client sends the username and password. If successful, the server responds with the message: Hi {username}, good to see you. Otherwise, responds with the message: Failed to login.
   If the login attempt fails, the client has the option to retry by entering a valid username and password.

2. Calculation Request:
   Client sends a command in the format: calculate: X operator Z (e.g., calculate: 5 + 3),
   when X and Z are integers and operator is one of the following: +, -, \*, /, ^.
   If the input received from the client is in the correct format:
   Server calculates the result (result = X op Z) and responds with the message: response : result.
   Else, the server closes the connection with the client.

3. Maximum Check Request:
   Client sends a command in the format: max: number (e.g., max: (123 45 678 -987 654 32 -1) ).
   If the input received from the client is in the correct format: Server responds with the following message: the maximum is {maximum_number}
   Else, the server closes the connection with the client.

4. Prime factorization Request:
   Client sends a command in the format: factors: number (e.g., factors: 6).
   If the input received from the client is in the correct format: Server responds with the message: the prime factors of X are: p1, p2, ..., pn
   Else, the server closes the connection with the client.

5. Quit:
   Client can send : "quit" message to disconnect from the server (if the client has already authenticated). Then, the client will close the connection.
