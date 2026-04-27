import os
import sys
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
NONCE_SIZE = 12
def derive_key(passphrase: str, salt: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"file-encryption",
    )
    return hkdf.derive(passphrase.encode())
def encrypt_file(input_path: str, output_path: str, passphrase: str):
    with open(input_path, "rb") as f:
        plaintext = f.read()
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(passphrase, nonce)
    cipher = ChaCha20Poly1305(key)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    with open(output_path, "wb") as f:
        f.write(nonce + ciphertext)
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encrypt.py <input_file> <output_file> <passphrase>")
        raise SystemExit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    passphrase = sys.argv[3]
    encrypt_file(input_file, output_file, passphrase)
    print("File encrypted successfully.")
