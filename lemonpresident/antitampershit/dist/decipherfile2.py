import hashlib
import hmac
import sys

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

def decrypt_file(input_path, output_path, passphrase):
    with open(input_path, "rb") as f:
        nonce = f.read(NONCE_BYTES)
        data = f.read()

    if len(data) < HMAC_BYTES:
        raise ValueError("File too short to be valid")

    ciphertext = data[:-HMAC_BYTES]
    tag = data[-HMAC_BYTES:]

    key_material = hkdf(passphrase, nonce, info=b"file-encryption", length=64)
    enc_key = key_material[:32]
    mac_key = key_material[32:]

    mac = hmac.new(mac_key, nonce, hashlib.sha256)
    mac.update(ciphertext)

    if not hmac.compare_digest(mac.digest(), tag):
        raise ValueError("Authentication failed: wrong key or tampered file")

    stream = keystream_generator(enc_key, nonce)

    with open(output_path, "wb") as f_out:
        for i in range(0, len(ciphertext), CHUNK_SIZE):
            chunk = ciphertext[i:i+CHUNK_SIZE]
            decrypted = bytes(b ^ next(stream) for b in chunk)
            f_out.write(decrypted)

    print("File decrypted successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python decipherfile.py <input> <output> <passphrase>")
        sys.exit(1)

    decrypt_file(sys.argv[1], sys.argv[2], sys.argv[3])
