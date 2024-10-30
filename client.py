from collections import defaultdict
import json
import os
import threading
import requests
import hashlib
import bencodepy
import socket

self_ip_address = "127.0.0.1"
PIECE_SIZE = 1

res = {
    "peers": [
        {"ip": "123.0.0.1", "chunks": [1, 2, 7]},
        {"ip": "123.0.0.2", "chunks": [4, 11, 6]},
        {"ip": "123.0.0.3", "chunks": [3, 8, 9]},
        {"ip": "123.0.0.4", "chunks": [5, 10, 12]},
    ]
}

def download(fileName):
    with open("server.json", 'r') as file:
        data = json.load(file)
    connect_to_server_by_source_port(data["server1"]["source"], data["server1"]["port"])
    send_filestatus_to_server()
    response = request_file_from_server(fileName)
    
    request_file_pieces_from_peer(response, fileName)
    merge_file(fileName)
    print(f"Completed download file {fileName}, ready to share!")
    
def upload(ip_address, fname, pieces):
    print(f"Sending pieces {pieces} of file {fname} to {ip_address}")

def connect_to_server_by_source_port(source, port):
    print(f"User want to connect to {source}, port {port}")

def send_filestatus_to_server():
    for root, dirs, files in os.walk("files"):
        for file in files:
            if file.endswith(".json"):
                print(f"Sent {os.path.join(root, file)} to the server!")

def request_file_from_server(fname):
    return res

def merge_file(fileName):
    peer_status_files = [os.path.join('files_from_peers', p, 'status.json') for p in os.listdir('files_from_peers') if p.startswith('peer')]
    merged_data = defaultdict(list)

    for status_file in peer_status_files:
        with open(status_file, 'r') as f:
            data = json.load(f)
            for piece in data['pieces']:
                merged_data[piece].append(status_file)

    sorted_pieces = sorted(merged_data.keys())

    os.makedirs(f'files/{fileName}', exist_ok=True)
    with open(f'files/{fileName}/status.json', 'w') as f:
        json.dump({'pieces': sorted_pieces}, f, indent=4)

    with open(f'files/{fileName}/{fileName}.txt', 'w') as f:
        for piece in sorted_pieces:
            f.write(str(piece) + '\n')

    print(f"Merged {len(peer_status_files)} peer status files.")

def request_file_pieces_from_peer(file_info, fileName):
    peers = file_info["peers"]

    for i, peer in enumerate(peers, start=1):
        peer_dir = f"peer{i}"
        os.makedirs(os.path.join("files_from_peers", peer_dir), exist_ok=True)

        with open(os.path.join("files_from_peers", peer_dir, f"{fileName}.txt"), "w") as f:
            for chunk in peer["chunks"]:
                f.write(str(chunk) + "\n")

        status_data = {
            "fname": f"{fileName}.txt",
            "pieces": peer["chunks"]
        }
        with open(os.path.join("files_from_peers", peer_dir, "status.json"), "w") as f:
            json.dump(status_data, f, indent=4)

def login(username, password) -> bool:
    url = 'http://localhost:3000/v1/user/login'
    data = {
        "username": username,
        "password": password
    }
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    if response.status_code == 201:
        f = open("client1/userId.txt", "a")
        f.write(response.json()['data']['id'])
        return True
    else:
        print("Wrong username or password!")
        return False
    
def logout():
    with open("client1/userId.txt", "w") as f:
        pass

def checkLogin() -> bool:
    f = open("userId.txt", "r")
    userId = f.read()
    if userId == "":
        username = ""
        password = ""
        while 1:
            username = input("Username: ")
            password = input("Password: ")
            valid = login(username, password)
            if valid:
                return True
            else:
                con = input("Failed, continue? (y/n): ")
                if con == "n":
                    return False

    else:
        return True

def main():
    userInput = ""
    while 1:
        userInput = input(">> ")
        if userInput == "EXIT":
            return

        userRequest = userInput.split(" ")[0]

        if userRequest == "download":
            download(userInput.split(" ")[1])
        elif userRequest == "upload":
            upload(userInput.split(" ")[1])
        elif userRequest == "logout":
            logout()
            return
        else:
            print("User input something")
       
def connectSocket(source, port, response):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
        s.connect((source, port))
        print(f"Connected to {source}:{port}")

        request = {
            "info_hash" : "123",
            "type" : "GET_FILE_STATUS"
        }

        s.sendall(json.dumps(response).encode('utf-8'))

###########################

def get_file_status_in_peer(peer_ip, peer_port, info_hash):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.connect((peer_ip, peer_port))
            print(f"Connected to {peer_ip}:{peer_port}")
            
            request = {
                'type': 'GET_FILE_STATUS',
                'info_hash': info_hash
            }

            s.sendall(json.dumps(request).encode('utf-8'))
            
            response_data = s.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            if response['type'] == 'RETURN_FILE_STATUS' and response['info_hash'] == info_hash:
                pieces_status = response['pieces_status']
                return peer_ip, peer_port, pieces_status
            else:
                return None, None, None
    except (socket.error, ConnectionRefusedError, TimeoutError) as e:
        print(f"Connection error: {e}")
        return None, None, None

def start_peer_server(peer_ip='127.0.0.1', peer_port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((peer_ip, peer_port))
        server_socket.listen(5)
        print(f"Peer is listening at {peer_ip}:{peer_port}")
        print("Please type your command:\n")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Message from {client_address}")
            handle_client(client_socket)

def get_filename_in_folder(folder_path):
    try:
        for file_name in os.listdir(folder_path):
            if not (file_name.endswith('.json')):
                return file_name
        return None  # Nếu không tìm thấy tệp .txt nào
    except FileNotFoundError:
        print("Folder not found")
        return None

def handle_client(client_socket):
    with client_socket:
        data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)

        if request['type'] == 'GET_FILE_STATUS':
            info_hash = request['info_hash']

            response = {
                'type': 'RETURN_FILE_STATUS',
                'info_hash': info_hash,
                'fName': None,
                'pieces_status': []
            }

            with open(f'files/{info_hash}/status.json', 'r') as f:
                data = json.load(f)

            if not data:
                client_socket.sendall(json.dumps(response).encode('utf-8'))
                return
            
            file_name = get_filename_in_folder(f"files/{info_hash}")
            
            response = {
                'type': 'RETURN_FILE_STATUS',
                'info_hash': info_hash,
                'fName': file_name,
                'pieces_status': data['piece_status']
            }

            # connectSocket("127.0.0.1", 65433, response)

            client_socket.sendall(json.dumps(response).encode('utf-8'))

        elif request['type'] == 'GET_FILE_CHUNK':
            info_hash = request['info_hash']
            chunk_list = request['chunk_list']
            chunk_data = []

            response = {
                'type': 'RETURN_FILE_CHUNK',
                'info_hash': info_hash,
                'chunk_data': []
            }

            with open(f'files/{info_hash}/status.json', 'r') as f:
                data = json.load(f)

            if not data:
                client_socket.sendall(json.dumps(response).encode('utf-8'))
                return

            file_name = get_filename_in_folder(f"files/{info_hash}")
            
            try:
                with open(f"files/{info_hash}/{file_name}", "rb") as f:
                    for chunk_index in chunk_list:
                        f.seek(chunk_index * PIECE_SIZE)
                        data = f.read(PIECE_SIZE)
                        chunk_data.append(data.decode('latin1'))
            except FileNotFoundError:
                print(f"File {file_name} does not exit.")
                client_socket.sendall(json.dumps(response).encode('utf-8'))
                return
            
            response['chunk_data'] = chunk_data

            client_socket.sendall(json.dumps(response).encode('utf-8'))
        elif request['type'] == 'PING':
            response = {
                'type': 'PONG'
            }
            client_socket.sendall(json.dumps(response).encode('utf-8'))

if checkLogin():
    print("Login!")
    server_thread = threading.Thread(target=start_peer_server, daemon=True)
    server_thread.start()
    main()

print("End working")
