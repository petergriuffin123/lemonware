import hashlib

FILE = "lemonbean.py"
MARKERS = [b"# wsgbro\n", b"# wsgbro\r\n"]

with open(FILE, "rb") as f:
    content = f.read()

marker = None
for m in MARKERS:
    if m in content:
        marker = m
        break

if not marker:
    raise ValueError("Marker not found.")

parts = content.split(marker)
code = parts[0]

hash_value = hashlib.sha256(code).hexdigest()

with open(FILE, "wb") as f:
    f.write(code + marker + b'"' + hash_value.encode() + b'"\n')

print("Hash injected successfully!")