from collections import defaultdict
import json
import os
import socket

socketSource = "122.0.0.0"
socketPort = "80"

res = {
    "files" : [
        {
            "fName" : "123456",
            "peers": [
                {"ip": "123.0.0.1", "chunks": [1, 2, 7]},
                {"ip": "123.0.0.2", "chunks": [4, 11, 6]},
                {"ip": "123.0.0.3", "chunks": [3, 8, 9]},
                {"ip": "123.0.0.4", "chunks": [5, 10, 12]},
            ]
        }
    ]
}

def ping(host, port):
    print(f"Pinging {host}, port: {port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        request = {
            "type" : "PING"
        }

        s.sendall(json.dumps(request).encode('utf-8'))

        response_data = s.recv(4096)
        response = json.loads(response_data.decode('utf-8'))

        if response["type"] == "PONG":
            print(f"Host: {host}, port: {port} is running")
        else :
            print(f"Host: {host}, port: {port} is not running")

def discover(host, port, info_hash):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.connect((host, port))
            # print(f"Connected to {host}:{port}")
            
            request = {
                'type': 'GET_FILE_STATUS',
                'info_hash': info_hash
            }

            s.sendall(json.dumps(request).encode('utf-8'))
            
            response_data = s.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            if response['type'] == 'RETURN_FILE_STATUS' and response['info_hash'] == info_hash:
                pieces_status = response['pieces_status']
                print(f"Get pieces: {pieces_status}")
    except (socket.error, ConnectionRefusedError, TimeoutError) as e:
        print(f"Connection error: {e}")

def main():
    userInput = ""
    while 1:
        userInput = input(">> ")
        if userInput == "EXIT":
            return

        userRequest = userInput.split(" ")[0]
        if userRequest == "ping":
            host = userInput.split(" ")[1]
            port = int(userInput.split(" ")[2])
            ping(host, port)
        elif userRequest == "discover":
            host = userInput.split(" ")[1]
            port = int(userInput.split(" ")[2])
            info_hash = userInput.split(" ")[3]
            discover(host, port, info_hash)
        else:
            print("User input something")
       
main()

print("End working")
