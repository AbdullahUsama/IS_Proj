# main.py
import sys
import base64
import os

from AESCTR import aes_ctr_encrypt, aes_ctr_decrypt
from steno import SteganographyLSB
from metricscalc import psnr_for_images

def hide_message_in_image(input_image, output_image, secret_message):
    """
    Encrypt secret_message using AES-CTR, then embed in image via LSB stego.
    Returns: AES key used for encryption (must be saved for decryption)
    """
    print("[*] Encrypting secret message with AES-CTR...")
    key, nonce, ciphertext = aes_ctr_encrypt(secret_message.encode())
    
    # Convert nonce + ciphertext to Base64 string for LSB embedding
    data_to_hide = base64.b64encode(nonce + ciphertext).decode('utf-8')
    
    print(f"[*] Embedding encrypted message into image: {input_image}")
    stego = SteganographyLSB()
    stego.encode(input_image, output_image, data_to_hide, password="unused")
    
    print(f"[*] Message embedded in {output_image}")
    return key  # must keep key safe for decryption

def extract_message_from_image(stego_image, key):
    """
    Extract Base64 string from image, decode, then decrypt using AES-CTR.
    """
    print(f"[*] Extracting hidden data from image: {stego_image}")
    stego = SteganographyLSB()
    data_extracted = stego.decode(stego_image, password="unused")
    
    # Decode Base64 to get nonce + ciphertext
    raw_bytes = base64.b64decode(data_extracted)
    nonce = raw_bytes[:8]
    ciphertext = raw_bytes[8:]
    
    # Decrypt AES-CTR
    decrypted_message = aes_ctr_decrypt(ciphertext, key, nonce)
    return decrypted_message.decode('utf-8')

if __name__ == "__main__":
    DEFAULT_IMAGE = "media/tyla.jpg"
    STEGO_IMAGE = "media/stego_image.png"
    
    print("="*50)
    print("AES-CTR + LSB Steganography Demo")
    print("="*50)
    
    # Secret message input
    secret_message = input("Enter the secret message to hide: ").strip()
    if not secret_message:
        print("[!] Error: Secret message cannot be empty!")
        sys.exit(1)
    
    # Step 1: Hide message
    aes_key = hide_message_in_image(DEFAULT_IMAGE, STEGO_IMAGE, secret_message)
    
    # Step 2: Extract and decrypt
    recovered_message = extract_message_from_image(STEGO_IMAGE, aes_key)
    print("\n[*] Recovered Message:")
    print(recovered_message)
    
    # Step 3: Compute PSNR between original and stego images
    print("\n[*] Calculating PSNR between original and stego images...")
    psnr_for_images(DEFAULT_IMAGE, STEGO_IMAGE)
