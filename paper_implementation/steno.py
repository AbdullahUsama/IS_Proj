import sys
import os
from PIL import Image
from AESCTR import aes_gcm_encrypt_with_password, aes_gcm_decrypt_with_password

class SteganographyLSB:
    def __init__(self):
        self.PIXELS_PER_CHAR = 3

    def encrypt_message(self, plain_text, password):
        """
        Encrypts message using AES-256-GCM with password-based key derivation
        Includes authentication tag for tamper detection
        """
        return aes_gcm_encrypt_with_password(plain_text, password)

    def decrypt_message(self, cipher_text, password):
        """
        Decrypts AES-256-GCM encrypted message
        Verifies authentication tag - detects corruption/tampering
        """
        try:
            return aes_gcm_decrypt_with_password(cipher_text, password)
        except Exception as e:
            return "[!] Error: Incorrect Key or Corrupted Data"

    def _int_to_bin(self, rgb):
        r, g, b = rgb
        return (f'{r:08b}', f'{g:08b}', f'{b:08b}')

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return (int(r, 2), int(g, 2), int(b, 2))

    def _merge_rgb(self, rgb1, rgb2, rgb3):
        return list(rgb1) + list(rgb2) + list(rgb3)

    def encode(self, image_path, output_path, secret_text, password):
        print(f"[*] Loading image: {image_path}")
        image = Image.open(image_path)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        width, height = image.size
        pixels = image.load()

        print("[*] Encrypting text...")
        cipher_text = self.encrypt_message(secret_text, password)
        print(f"[*] Ciphertext length: {len(cipher_text)} chars")

        total_pixels = width * height
        required_pixels = len(cipher_text) * self.PIXELS_PER_CHAR
        
        if required_pixels > total_pixels:
            raise ValueError(f"[-] Image too small. Need {required_pixels} pixels, have {total_pixels}.")

        idx = 0
        total_chars = len(cipher_text)
        
        for i in range(0, total_chars):
            char = cipher_text[i]
            binary_char = f'{ord(char):08b}'
            
            coord_sets = []
            for _ in range(3):
                x = idx % width
                y = idx // width
                coord_sets.append((x, y))
                idx += 1
                
            p1 = pixels[coord_sets[0]]
            p2 = pixels[coord_sets[1]]
            p3 = pixels[coord_sets[2]]
            
            nine_vals = list(p1) + list(p2) + list(p3)
            
            for bit_index in range(8):
                current_val = nine_vals[bit_index]
                bin_val = list(f'{current_val:08b}')
                bin_val[-1] = binary_char[bit_index]
                nine_vals[bit_index] = int("".join(bin_val), 2)
            
            has_more = 1 if i < (total_chars - 1) else 0
            
            last_val = nine_vals[8]
            bin_last = list(f'{last_val:08b}')
            bin_last[-1] = str(has_more)
            nine_vals[8] = int("".join(bin_last), 2)
            
            pixels[coord_sets[0]] = tuple(nine_vals[0:3])
            pixels[coord_sets[1]] = tuple(nine_vals[3:6])
            pixels[coord_sets[2]] = tuple(nine_vals[6:9])

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"[*] Created directory: {output_dir}")
        
        print(f"[*] Encoding successful. Saving to {output_path}")
        image.save(output_path)

    def decode(self, image_path, password):
        print(f"[*] Scanning image: {image_path}")
        image = Image.open(image_path)
        pixels = image.load()
        width, height = image.size
        
        extracted_bits = ""
        cipher_text = ""
        idx = 0
        total_pixels = width * height
        
        while idx < total_pixels:
            if idx + 3 > total_pixels:
                break
                
            coord_sets = []
            for _ in range(3):
                x = idx % width
                y = idx // width
                coord_sets.append((x, y))
                idx += 1
                
            p1 = pixels[coord_sets[0]]
            p2 = pixels[coord_sets[1]]
            p3 = pixels[coord_sets[2]]
            
            nine_vals = list(p1) + list(p2) + list(p3)
            
            char_bits = ""
            for i in range(8):
                val = nine_vals[i]
                char_bits += f'{val:08b}'[-1]
            
            char_code = int(char_bits, 2)
            cipher_text += chr(char_code)
            
            flag_val = nine_vals[8]
            flag_bit = f'{flag_val:08b}'[-1]
            
            if flag_bit == '0':
                break
        
        print(f"[*] Extraction complete. Ciphertext length: {len(cipher_text)}")
        
        print("[*] Decrypting...")
        plain_text = self.decrypt_message(cipher_text, password)
        return plain_text


if __name__ == "__main__":
    stego = SteganographyLSB()
    
    DEFAULT_INPUT_IMAGE = "media/tyla.jpg"
    DEFAULT_OUTPUT_IMAGE = "media/stego_image.png"
    
    print("\n" + "="*50)
    print("   Image Steganography - LSB Technique")
    print("="*50)
    print("\nChoose an option:")
    print("1. Encrypt - Hide a secret message in an image")
    print("2. Decrypt - Extract a hidden message from an image")
    print("="*50)
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n" + "-"*50)
        print("   ENCRYPTION MODE")
        print("-"*50)
        
        secret_message = input("\nEnter the secret message to hide: ").strip()
        
        if not secret_message:
            print("[!] Error: Secret message cannot be empty!")
            sys.exit(1)
        
        password = input("Enter a password for encryption: ").strip()
        
        if not password:
            print("[!] Error: Password cannot be empty!")
            sys.exit(1)
        
        output_image = input(f"Enter output image name (default: {DEFAULT_OUTPUT_IMAGE}): ").strip()
        if not output_image:
            output_image = DEFAULT_OUTPUT_IMAGE
        else:
            if not os.path.dirname(output_image):
                output_image = os.path.join("media", output_image)
        
        try:
            print(f"\n[*] Using input image: {DEFAULT_INPUT_IMAGE}")
            stego.encode(DEFAULT_INPUT_IMAGE, output_image, secret_message, password)
            print(f"\n✓ Success! Secret message hidden in '{output_image}'")
            print(f"✓ Keep your password safe to decrypt the message later!")
            
        except FileNotFoundError:
            print(f"\n[!] Error: Input image '{DEFAULT_INPUT_IMAGE}' not found!")
            print(f"[!] Please make sure '{DEFAULT_INPUT_IMAGE}' exists in the current directory.")
        except ValueError as e:
            print(f"\n[!] Error: {e}")
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}")
    
    elif choice == "2":
        print("\n" + "-"*50)
        print("   DECRYPTION MODE")
        print("-"*50)
        
        image_path = input("\nEnter the path to the steganography image: ").strip()
        
        if not image_path:
            print("[!] Error: Image path cannot be empty!")
            sys.exit(1)
        
        if not os.path.dirname(image_path):
            image_path = os.path.join("media", image_path)
        
        password = input("Enter the password used for encryption: ").strip()
        
        if not password:
            print("[!] Error: Password cannot be empty!")
            sys.exit(1)
        
        try:
            recovered_msg = stego.decode(image_path, password)
            print("\n" + "="*50)
            print("   RECOVERED MESSAGE")
            print("="*50)
            print(f"\n{recovered_msg}\n")
            print("="*50)
            
        except FileNotFoundError:
            print(f"\n[!] Error: Image '{image_path}' not found!")
        except Exception as e:
            print(f"\n[!] Error during decryption: {e}")
    
    else:
        print("\n[!] Invalid choice! Please enter 1 or 2.")
        sys.exit(1)