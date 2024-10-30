from collections import defaultdict
import json
import os
import requests
import hashlib
import bencodepy

self_ip_address = "123.0.0.0"
socketSource = "122.0.0.0"
socketPort = "80"

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
    f = open("client1/userId.txt", "r")
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
       
def connectSocket(source, port):
    print(f"Connect to {source}, {port}")

# if checkLogin():
#     print("Login!")
#     connectSocket(socketSource, socketPort)
#     main()

def get_info_hash(torrent_file_path):
    with open(torrent_file_path, 'rb') as f:
        # Load and decode the torrent file
        torrent_data = bencodepy.decode(f.read())
        
        # Extract the 'info' dictionary
        info = torrent_data[b'info']
        
        # Encode the 'info' dictionary back to bencoded format
        bencoded_info = bencodepy.encode(info)
        
        # Calculate the SHA-1 hash of the bencoded 'info' dictionary
        info_hash = hashlib.sha1(bencoded_info).hexdigest()
        return info_hash

torrent_file = "client1/files/123/123.txt"
print(f"Info Hash: {get_info_hash(torrent_file)}")

print("End working")
