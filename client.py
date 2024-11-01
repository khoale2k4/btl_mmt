from collections import defaultdict
import json
import os
import threading
from time import sleep
from helper import main as helper
import socket

self_ip_address = "127.0.0.1"
self_port = 65435
PIECE_SIZE = 1
file_lock = threading.Lock()

# download 754ce21c061ee4c8ca8a0625f7e2ceb683f614c3

# mô phỏng khi muốn download file và gửi yêu cầu tải file lên tracker, tracker trả về những peers chứa file đó
res = {
    "peers": [
        {"IPaddress": "127.0.0.1", "port" : 65432},
        {"IPaddress": "127.0.0.1", "port" : 65434},
        {"IPaddress": "127.0.0.1", "port" : 65435},
    ]
}

# mô phỏng tracker trả về points của các peers
pointsRes = {
    ("127.0.0.1", 65432) : 5,
    ("127.0.0.1", 65434) : 3,
    ("127.0.0.1", 65435) : 1,
}

def download(magnet_link):
    information = helper.decode_magnet_link(magnet_link)
    info_hash = information["info_hash"]
    fileName = information["filename"]
    fileSize =  information["file_size"]

    response = {
        "peers" : (helper.get_file_info_from_server(info_hash))['data'][0]['peers']
    }

    print(response)
    
    ips = [peer["IPaddress"] for peer in response["peers"]]
    ports = [peer["port"] for peer in response["peers"]]
    pieces = [[] for _ in response["peers"]]
    point = [0 for _ in range(len(response["peers"]))]

    for i in range(len(ips)):
        ips[i], ports[i], pieces[i], point[i] = get_file_status_in_peer(ips[i], ports[i], info_hash)

    points = {}

    for i in range(len(ips)):
        points[(ips[i], ports[i])] = point[i]

    peers = [(ips[i], ports[i]) for i in range(len(ips))]

    selected_chunks = {peer: [] for peer in peers}

    num_chunks = len(pieces[0])

    currentStatus = []
    if not os.path.exists(f'files/{info_hash}'):
        os.makedirs(f'files/{info_hash}')

    if not os.path.exists(f'files/{info_hash}/status.json'):
        with open(f'files/{info_hash}/status.json', 'w') as f:
            json.dump({"fileName": fileName, "piece_status": [
                0 for _ in range(fileSize // PIECE_SIZE)
            ]}, f)
    if not os.path.exists(f'storage/{fileName}'):
        with open(f'storage/{fileName}', 'w') as f:
            pass

    with open(f'files/{info_hash}/status.json', 'r') as f:
        data = json.load(f)

    if data != None:
        currentStatus = data["piece_status"]

    for chunk_index in range(num_chunks):
        if data != None and currentStatus[chunk_index] == 1:
            continue
        best_peer = None
        best_priority = -1

        for peer_index, peer_chunks in enumerate(pieces):
            if peer_chunks[chunk_index] == 1:
                peer = peers[peer_index]
                priority = points[peer]

                if priority > best_priority:
                    best_priority = priority
                    best_peer = peer

        if best_peer is not None:
            selected_chunks[best_peer].append(chunk_index)

    threads = []
    for (ip, port), chunks in selected_chunks.items():
        peer_thread = threading.Thread(target=download_file_chunk_from_peer, args=(ip, port, info_hash, chunks, f"storage/{fileName}"),daemon=True)
        peer_thread.start()
        threads.append(peer_thread)
    
    for thread in threads:
        thread.join()

    dataInJsonFile = {}

    with open(f"files/{info_hash}/status.json", "r") as file:
        data = json.load(file)
        dataInJsonFile = data
        if all(status == 0 for status in data["piece_status"]):
            return
    
    f = open("userId.txt", "r")
    userId = f.read()
    userPoint = helper.search_by_id(userId)["data"]["point"]
    newPoint = userPoint + sum(dataInJsonFile["piece_status"])
    print(newPoint)
    helper.update_user(newPoint, userId)
    helper.upload_file(info_hash, fileName, fileSize, self_ip_address, self_port, userId)

def login(username, password) -> bool:
    url = 'http://localhost:3000/v1/user/login'
    data = {
        "username": username,
        "password": password
    }
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    if response.status_code == 201:
        f = open("userId.txt", "a")
        f.write(response.json()['data']['id'])
        return True
    else:
        print("Wrong username or password!")
        return False
    
def logout():
    with open("userId.txt", "w") as f:
        pass

def checkLogin():
    f = open("userId.txt", "r")
    userId = f.read()
    if userId == "":
        option = input("Login?(y/n)")
        if option == 'y':
            print("Login")
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
            print("Signup")
            username = input("Username: ")
            password = input("Password: ")
            fullName = input("Full name: ")
            valid = sigup(username, password, fullName)
            if valid['success']:
                return checkLogin()
            else:
                con = input(f"Failed, message: {valid["message"]}, continue? (y/n): ")
                if con == "n":
                    return False
                else: 
                    checkLogin()

    else:
        return True

def download_file_chunk_from_peer(peer_ip, peer_port, info_hash, chunk_list, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_ip, peer_port))
        # print(f"Connected to {peer_ip}:{peer_port}")
        
        request = {
            'type': 'GET_FILE_CHUNK',
            'info_hash': info_hash,
            'chunk_list': chunk_list
        }

        s.sendall(json.dumps(request).encode('utf-8'))
        
        response_data = s.recv(4096)
        response = json.loads(response_data.decode('utf-8'))
        # print(f"and get chunks: {response['chunk_data']}")
        if response['type'] == 'RETURN_FILE_CHUNK' and response['info_hash'] == info_hash:
            chunk_data = response['chunk_data']

            with file_lock:
                with open(f"files/{info_hash}/status.json", "r") as file:
                    data = json.load(file)
                    currentStatus = data["piece_status"]
                    fileName = data["fileName"]


                with open(file_path, "r+b") as f:  
                    for i, chunk in enumerate(chunk_data):
                        f.seek(chunk_list[i] * PIECE_SIZE)
                        f.write(chunk.encode('latin1'))
                        currentStatus[chunk_list[i]] = 1

                with open(f"files/{info_hash}/status.json", "w") as file:
                    json.dump(
                        {
                            "fileName": fileName,
                            "piece_status": currentStatus
                        }, 
                        file
                    )
        else:
            print("Has been received invalid response from peer")

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
            print(f"and get: {response}")
            if response['type'] == 'RETURN_FILE_STATUS' and response['info_hash'] == info_hash:
                pieces_status = response['pieces_status']
                point = response['point']
                return peer_ip, peer_port, pieces_status, point
            else:
                return None, None, None, 0
    except (socket.error, ConnectionRefusedError, TimeoutError) as e:
        print(f"Connection error: {e}")
        return None, None, None, 0

def start_peer_server(peer_ip=self_ip_address, peer_port=self_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((peer_ip, peer_port))
        server_socket.listen(5)
        print(f"Peer is listening at {peer_ip}:{peer_port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Message from {client_address}")
            handle_client(client_socket)

def get_filename_in_folder(folder_path):
    try:
        with open(f'{folder_path}/status.json', 'r') as f:
            data = json.load(f)
            return data["fileName"]
        
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
                'pieces_status': [],
                'point': 0
            }

            with open(f'files/{info_hash}/status.json', 'r') as f:
                data = json.load(f)

            if not data:
                client_socket.sendall(json.dumps(response).encode('utf-8'))
                return
            
            file_name = get_filename_in_folder(f"files/{info_hash}")

            
            f = open("userId.txt", "r")
            userId = f.read()

            point = helper.search_by_id(userId)["data"]["point"]
            
            response = {
                'type': 'RETURN_FILE_STATUS',
                'info_hash': info_hash,
                'fName': file_name,
                'pieces_status': data['piece_status'],
                'point': point
            }

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
                with open(f"storage/{file_name}", "rb") as f:
                    for chunk_index in chunk_list:
                        f.seek(chunk_index * PIECE_SIZE)
                        data = f.read(PIECE_SIZE)
                        chunk_data.append(data.decode('latin1'))

                f = open("userId.txt", "r")
                userId = f.read()
                userPoint = helper.search_by_id(userId)["data"]["point"]
                newPoint = userPoint - (len(chunk_list))
                helper.update_user(newPoint, userId)
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

def sigup(username, passwork, fullname):
    response = helper.sigup(username, passwork, fullname)
    print(response)
    return response

def upload_full_file(filename, filesize):
    infohash = helper.generate_hash_info(f"storage/{filename}")

    os.makedirs(f"files/{infohash}", exist_ok=True)
    with open(f'files/{infohash}/status.json', 'w') as file:
        json.dump(
            {
                "fileName": filename,
                "piece_status": [1 for _ in range(filesize / PIECE_SIZE) ]
            }, 
            file
        )
        

    f = open("userId.txt", "r")
    userId = f.read()
    helper.upload_file(infohash, filename, filesize, self_ip_address, self_port, userId)

    return helper.generate_magnet_link(infohash, filename, filesize, "http://localhost:3000/v1", None)

def main():
    userInput = ""
    while 1:
        userInput = input(">> ")
        if userInput == "EXIT":
            return

        userRequest = userInput.split(" ")

        if userRequest[0] == "download":
            magnet_link =  userRequest[1]
            download(magnet_link)
        elif userRequest[0] == "upload":
            file_name = userRequest[1]
            file_size = userRequest[2]
            upload_full_file(file_name, file_size)
        elif userRequest[0] == "logout":
            logout()
            return
        else:
            print("User input something")

if checkLogin():
    server_thread = threading.Thread(target=start_peer_server, daemon=True)
    server_thread.start()
    print("Login!")
    sleep(0.2)
    main()

print("End working")
