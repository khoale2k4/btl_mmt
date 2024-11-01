import requests
import urllib.parse
import hashlib

def upload_file(hash_info, file_name, filesize, address, port, user_id):
    response = requests.post('http://localhost:3000/v1/file/upload', data = { 'infoHash': hash_info, 'filename': file_name, 'peerIPAddress': address, 'peerPort': port, 'size': filesize, 'userId': user_id })
    try:
        # Try to parse the response as JSON regardless of the content type header
        json_response = response.json()
        
        # Extract values with defaults in case fields are missing
        success = json_response.get('success', False)
        data = json_response.get('data', {})
        message = json_response.get('message', "No message provided")

        print("Success:", success)
        print("Data:", data)
        print("Message:", message)

        return {'success': success, 'data': data, 'message': message}

    except ValueError:
        # If JSON decoding fails, handle it as a non-JSON response
        print("Received non-JSON response:", response.text)
        return {'success': False, 'data': {}, 'message': "Non-JSON response"}

def generate_hash_info(file_path, hash_algorithm = 'sha1'):
    if hash_algorithm == 'sha1':
        hash_func = hashlib.sha1()
    elif hash_algorithm == 'sha256':
        hash_func = hashlib.sha256()
    else:
        raise ValueError("Unsupported hash algorithm. Use 'sha1' or 'sha256'.")

    # Đọc file theo từng khối (chunk) để tiết kiệm bộ nhớ
    with open(file_path, 'rb') as file:
        # Đọc file theo từng khối 4096 byte
        while chunk := file.read(4096):
            hash_func.update(chunk)

    # Trả về giá trị hash dưới dạng chuỗi hexa
    return hash_func.hexdigest()

def get_file_info_from_server(info_hash):
    response = requests.get(f'http://localhost:3000/v1/file/fetch?hash_info={info_hash}')
    try:
        # Try to parse the response as JSON regardless of the content type header
        json_response = response.json()
        
        # Extract values with defaults in case fields are missing
        success = json_response.get('success', False)
        data = json_response.get('data', {})
        message = json_response.get('message', "No message provided")

        # print("Success:", success)
        # print("Data:", data)
        # print("Message:", message)

        return {'success': success, 'data': data, 'message': message}

    except ValueError:
        # If JSON decoding fails, handle it as a non-JSON response
        print("Received non-JSON response:", response.text)
        return {'success': False, 'data': {}, 'message': "Non-JSON response"}

def sigup(username, password, fullname):
    response = requests.post('http://localhost:3000/v1/user/signup', data = { 'username': username, 'password': password, 'fullname': fullname })
    try:
        # Try to parse the response as JSON regardless of the content type header
        json_response = response.json()
        
        # Extract values with defaults in case fields are missing
        success = json_response.get('success', False)
        data = json_response.get('data', {})
        message = json_response.get('message', "No message provided")

        print("Success:", success)
        print("Data:", data)
        print("Message:", message)

        return {'success': success, 'data': data, 'message': message}

    except ValueError:
        # If JSON decoding fails, handle it as a non-JSON response
        print("Received non-JSON response:", response.text)
        return {'success': False, 'data': {}, 'message': "Non-JSON response"}

def login(username, password):
    response = requests.post('http://localhost:3000/v1/user/login', data = { 'username': username, 'password': password })
    
    try:
        # Try to parse the response as JSON regardless of the content type header
        json_response = response.json()
        
        # Extract values with defaults in case fields are missing
        success = json_response.get('success', False)
        data = json_response.get('data', {})
        message = json_response.get('message', "No message provided")

        print("Success:", success)
        print("Data:", data)
        print("Message:", message)

        return {'success': success, 'data': data, 'message': message}

    except ValueError:
        # If JSON decoding fails, handle it as a non-JSON response
        print("Received non-JSON response:", response.text)
        return {'success': False, 'data': {}, 'message': "Non-JSON response"}

def search_by_id(user_id):
    response = requests.get(f'http://localhost:3000/v1/user/{user_id}')
    
    try:
        # Try to parse the response as JSON regardless of the content type header
        json_response = response.json()
        
        # Extract values with defaults in case fields are missing
        success = json_response.get('success', False)
        data = json_response.get('data', {})
        message = json_response.get('message', "No message provided")

        print("Success:", success)
        print("Data:", data)
        print("Message:", message)

        return {'success': success, 'data': data, 'message': message}

    except ValueError:
        # If JSON decoding fails, handle it as a non-JSON response
        print("Received non-JSON response:", response.text)
        return {'success': False, 'data': {}, 'message': "Non-JSON response"}

def generate_magnet_link(info_hash, filename=None, file_size=None, trackers=None, web_seeds=None):
    # Base magnet link with info hash
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}"
    
    # Add display name if provided
    if filename:
        magnet_link += f"&dn={urllib.parse.quote(filename)}"
    
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

    filename = params.get("dn", [None])[0]
    trackers = params.get("tr", [])
    web_seeds = params.get("ws", [])
    file_size = params.get("xl", [None])[0]
    if file_size:
        file_size = int(file_size)
    
    # Return extracted info as a dictionary
    return {
        "info_hash": info_hash,
        "filename": filename,
        "trackers": trackers,
        "web_seeds": web_seeds,
        "file_size": file_size
    }

def update_user(new_user_point, user_id):
    response = requests.post(f'http://localhost:3000/v1/user/{user_id}', data = { 'point': new_user_point })
    try:
        # Try to parse the response as JSON regardless of the content type header
        json_response = response.json()
        
        # Extract values with defaults in case fields are missing
        success = json_response.get('success', False)
        data = json_response.get('data', {})
        message = json_response.get('message', "No message provided")

        print("Success:", success)
        print("Data:", data)
        print("Message:", message)

        return {'success': success, 'data': data, 'message': message}

    except ValueError:
        # If JSON decoding fails, handle it as a non-JSON response
        print("Received non-JSON response:", response.text)
        return {'success': False, 'data': {}, 'message': "Non-JSON response"}
    

