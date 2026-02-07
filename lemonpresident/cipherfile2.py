import hashlib
import hmac
import secrets
import sys

NONCE_BYTES = 12
CHUNK_SIZE = 4096
KEY_BYTES = 32

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

def encrypt_file(input_path, output_path, passphrase):
    nonce = secrets.token_bytes(NONCE_BYTES)

    key_material = hkdf(passphrase, nonce, info=b"file-encryption", length=64)
    enc_key = key_material[:32]
    mac_key = key_material[32:]

    stream = keystream_generator(enc_key, nonce)
    mac = hmac.new(mac_key, nonce, hashlib.sha256)

    with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        f_out.write(nonce)

        while chunk := f_in.read(CHUNK_SIZE):
            encrypted = bytes(b ^ next(stream) for b in chunk)
            mac.update(encrypted)
            f_out.write(encrypted)

        f_out.write(mac.digest())

    print("File encrypted successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python cipherfile.py <input> <output> <passphrase>")
        sys.exit(1)

    encrypt_file(sys.argv[1], sys.argv[2], sys.argv[3])
