from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# -----------------------------
# Utility Functions
# -----------------------------
def save_ciphertext(file_path, nonce, ciphertext):
    """Save nonce + ciphertext to a file"""
    with open(file_path, 'wb') as f:
        f.write(nonce + ciphertext)

def load_ciphertext(file_path, nonce_length=8):
    """Load nonce + ciphertext from a file"""
    with open(file_path, 'rb') as f:
        data = f.read()
    nonce = data[:nonce_length]
    ciphertext = data[nonce_length:]
    return nonce, ciphertext

# -----------------------------
# AES-CTR Encryption
# -----------------------------
def aes_ctr_encrypt(data, key_size=32):
    """
    Encrypts data using AES-CTR
    key_size: 16 (AES-128), 24 (AES-192), 32 (AES-256)
    Returns: key, nonce, ciphertext
    """
    key = get_random_bytes(key_size)      # AES key
    nonce = get_random_bytes(8)           # CTR nonce
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(data)
    return key, nonce, ciphertext

# -----------------------------
# AES-CTR Decryption
# -----------------------------
def aes_ctr_decrypt(ciphertext, key, nonce):
    """
    Decrypts AES-CTR ciphertext
    """
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# -----------------------------
# Example: Text Encryption/Decryption
# -----------------------------
text = b"Sensitive information that needs AES-CTR protection."

key, nonce, ciphertext = aes_ctr_encrypt(text)
print("Ciphertext (hex):", ciphertext.hex())

decrypted_text = aes_ctr_decrypt(ciphertext, key, nonce)
print("Decrypted Text:", decrypted_text.decode())

# -----------------------------
# Example: File Encryption/Decryption
# -----------------------------
input_file = "media/burger.jpg"
output_encrypted = "media/burger_encrypted.bin"
output_decrypted = "media/burger_decrypted.jpg"

# Encrypt file
with open(input_file, "rb") as f:
    file_data = f.read()

key, nonce, ciphertext = aes_ctr_encrypt(file_data)
save_ciphertext(output_encrypted, nonce, ciphertext)
print(f"File encrypted: {output_encrypted}")

# Decrypt file
nonce_loaded, ciphertext_loaded = load_ciphertext(output_encrypted)
decrypted_file_data = aes_ctr_decrypt(ciphertext_loaded, key, nonce_loaded)

with open(output_decrypted, "wb") as f:
    f.write(decrypted_file_data)
print(f"File decrypted: {output_decrypted}")
