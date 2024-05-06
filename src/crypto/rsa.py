from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii


def generate_keys():
    key = RSA.generate(2048)  # Generate a public and a private key pair
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_message(message, public_key):
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return binascii.hexlify(encrypted_message).decode()


def decrypt_message(encrypted_message, private_key):
    private_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(binascii.unhexlify(encrypted_message))
    return decrypted_message.decode()


# Example usage
if __name__ == "__main__":
    priv_key, pub_key = generate_keys()
    print("Private Key:", priv_key)
    print("Public Key:", pub_key)

    message = "Hello, this is a test message!"
    encrypted_msg = encrypt_message(message, pub_key)
    print("Encrypted:", encrypted_msg)

    decrypted_msg = decrypt_message(encrypted_msg, priv_key)
    print("Decrypted:", decrypted_msg)
