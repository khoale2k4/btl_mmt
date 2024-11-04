import requests
import hashlib

def upload_file(hash_info, file_name, filesize, address, port, user_id):
    response = requests.post('http://localhost:3000/files/upload', data = { 'hashInfo': hash_info, 'name': file_name, 'peerAddress': address, 'peerPort': port, 'size': filesize, 'userId': user_id })
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

def get_file_by_info_hash(info_hash):
    response = requests.get(f'http://localhost:3000/files?hash_info={info_hash}')
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

def update_user(new_user_point, user_id):
    response = requests.post(f'http://localhost:3000/user/{user_id}', data = { 'point': new_user_point })
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
