import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def decryptAES(cipher, password, salt, iv):
    cipher_text_bytes = base64.b64decode(cipher)
    salt_bytes = base64.b64decode(salt)
    iv_bytes = base64.b64decode(iv)

    key = PBKDF2(password, salt_bytes, dkLen=32, count=1000)

    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted = cipher.decrypt(cipher_text_bytes)

    padding = decrypted[-1]
    decrypted = decrypted[:-padding]

    return decrypted.decode('utf-8')


def decryptPassword(passwords, key):
    decrypted = {}

    for item in passwords.items():
        site, encryptedPass = item

        cipher = encryptedPass["cipher"]
        salt = encryptedPass["salt"]
        iv = encryptedPass["iv"]

        password = decryptAES(cipher, key, salt, iv)

        decrypted[site] = password
    
    return decrypted