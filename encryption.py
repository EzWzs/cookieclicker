from cryptography.fernet import Fernet


#encryption key generation in a binary file
def generate_file_key() -> bool:
    key = Fernet.generate_key()
    with open("enc.key", "wb") as file:
        file.write(key)
    return True

def load_key():
    #read in binary (rb")
    return open("enc.key", "rb").read()

def encrypt_msg(msg: str, key):
    #turns message into bytes so FERNET can encode it
    encoded_message = msg.encode()
    #create f object using Fernet class using key from before
    f = Fernet(key)
    #encrypt the original message in bytes
    encrypted = f.encrypt(encoded_message)
    return encrypted

def decrypt_msg(msg, key):
    #msg is the encryped message parameter
    f = Fernet(key)
    decrypt = f.decrypt(msg)
    #decode() turn from bytes into readable
    return decrypt.decode()
