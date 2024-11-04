from collections import defaultdict
import json
import os
import threading
import requests
import hashlib
import socket
import urllib.parse
from helper import main as helper

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

def sigup(username, passwork, fullname):
    response = helper.sigup(username, passwork, fullname)
    print(response.text)

def login(username, password) -> bool:
    response = helper.login(username, password)
    if response.success == True:
        f = open("client1/userId.txt", "a")
        f.write(response.data.id)
        return True
    else:
        print("Wrong username or password!")
        return False
    
def logout():
    with open("client1/userId.txt", "w") as f:
        pass

def checkLogin() -> bool:
    f = open("./userId.txt", "r")
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

        userRequest = userInput.split(" ")

        if userRequest[0] == "download":
            download(userInput.split(" ")[1])
        elif userRequest[0] == "sigup":
            sigup(userRequest[1], userRequest[2], userRequest[3])
        elif userRequest[0] == "login":
            helper.login(userRequest[1], userRequest[2])
        elif userRequest[0] == "upload":
            upload(userInput.split(" ")[1])
        elif userRequest[0] == "logout":
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



# if checkLogin():
#     print("Login!")
#     server_thread = threading.Thread(target=start_peer_server, daemon=True)
#     server_thread.start()
#     main()



def generate_magnet_link(info_hash, display_name=None, trackers=None, web_seeds=None, file_size=None):
    # Base magnet link with info hash
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}"
    
    # Add display name if provided
    if display_name:
        magnet_link += f"&dn={urllib.parse.quote(display_name)}"
    
    # Add trackers if provided
    if trackers:
        for tracker in trackers:
            magnet_link += f"&tr={urllib.parse.quote(tracker)}"
    
    # Add web seeds if provided
    if web_seeds:
        for web_seed in web_seeds:
            magnet_link += f"&ws={urllib.parse.quote(web_seed)}"
    
    # Add file size if provided
    if file_size:
        magnet_link += f"&xl={file_size}"
    
    return magnet_link

def decode_magnet_link(magnet_link):
    # Parse the magnet link
    parsed = urllib.parse.urlparse(magnet_link)
    params = urllib.parse.parse_qs(parsed.query)
    
    # Extract components
    info_hash = params.get("xt", [None])[0]
    if info_hash and info_hash.startswith("urn:btih:"):
        info_hash = info_hash[9:]  # Remove 'urn:btih:' prefix

    display_name = params.get("dn", [None])[0]
    trackers = params.get("tr", [])
    web_seeds = params.get("ws", [])
    file_size = params.get("xl", [None])[0]
    if file_size:
        file_size = int(file_size)
    
    # Return extracted info as a dictionary
    return {
        "info_hash": info_hash,
        "display_name": display_name,
        "trackers": trackers,
        "web_seeds": web_seeds,
        "file_size": file_size
    }

# Example usage
magnet_link = "magnet:?xt=urn:btih:1d5d36563d7e4fbd1d5d36563d7e4fbd&dn=Example+File+Name&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&ws=http%3A%2F%2Fexample.com%2Ffile&xl=123456789"

decoded_info = decode_magnet_link(magnet_link)
print(decoded_info)



print("End working")
