from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256, HMAC
import os
import base64

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
# Password-based Key Derivation
# -----------------------------
def derive_key_from_password(password, salt=b'steganography_salt_2025', key_length=32):
    """
    Derives a cryptographic key from a password using PBKDF2
    password: string password
    salt: bytes salt (should be unique per application)
    key_length: 16 (AES-128), 24 (AES-192), 32 (AES-256)
    Returns: derived key
    """
    key = PBKDF2(password.encode(), salt, key_length, count=100000, hmac_hash_module=SHA256)
    return key

# -----------------------------
# AES-GCM with Password (Authenticated Encryption)
# -----------------------------
def aes_gcm_encrypt_with_password(plaintext, password):
    """
    Encrypts plaintext using AES-256-GCM with password-based key derivation
    Includes authentication tag to detect tampering/corruption
    Returns: base64 encoded string containing nonce + tag + ciphertext
    """
    key = derive_key_from_password(password)
    cipher = AES.new(key, AES.MODE_GCM)
    
    # Encrypt and generate authentication tag
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    
    # Combine nonce (16 bytes) + tag (16 bytes) + ciphertext
    encrypted_data = cipher.nonce + tag + ciphertext
    
    # Return as base64 for easy storage
    return base64.b64encode(encrypted_data).decode('utf-8')

def aes_gcm_decrypt_with_password(encrypted_data, password):
    """
    Decrypts AES-256-GCM ciphertext with password-based key derivation
    Verifies authentication tag - raises exception if corrupted/tampered
    Returns: decrypted plaintext string
    """
    try:
        key = derive_key_from_password(password)
        
        # Decode from base64
        data = base64.b64decode(encrypted_data)
        
        # Extract components
        nonce = data[:16]       # GCM nonce is 16 bytes
        tag = data[16:32]       # Authentication tag is 16 bytes
        ciphertext = data[32:]  # Rest is ciphertext
        
        # Decrypt and verify
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        return plaintext.decode('utf-8')
    except (ValueError, KeyError) as e:
        raise Exception("Decryption failed: Invalid password or corrupted data")
