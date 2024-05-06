from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii


def generate_key():
    key = get_random_bytes(16)  # AES-128, for AES-256 use 32 bytes
    return binascii.hexlify(key).decode()


def encrypt_message(message, key):
    key = binascii.unhexlify(key)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = binascii.hexlify(cipher.iv).decode()
    message = pad(message)
    encrypted_message = cipher.encrypt(message.encode())
    return iv + binascii.hexlify(encrypted_message).decode()


def decrypt_message(encrypted_message, key):
    key = binascii.unhexlify(key)
    iv = binascii.unhexlify(encrypted_message[:32])
    encrypted_message = binascii.unhexlify(encrypted_message[32:])
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_message)).decode()
    return decrypted_message


def pad(text):
    # Pads text to be a multiple of 16 bytes
    return text + (16 - len(text) % 16) * chr(16 - len(text) % 16)


def unpad(text):
    # Remove the padding from the text
    return text[:-ord(text[-1])]


# Example usage
if __name__ == "__main__":
    key = generate_key()
    print("AES Key:", key)

    message = "Hello, this is a test message!"
    encrypted_msg = encrypt_message(message, key)
    print("Encrypted:", encrypted_msg)

    decrypted_msg = decrypt_message(encrypted_msg, key)
    print("Decrypted:", decrypted_msg)
