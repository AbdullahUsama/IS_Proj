"""
Edge-Adaptive LSB Steganography

Implements edge-adaptive embedding that avoids high-gradient (edge) pixels
for improved visual quality and detection resistance.

Algorithm:
- P2.1: Compute Sobel gradient (Di) and mean gradient (Me)
- P2.2: Embedding condition: only embed where Di <= Me
- P2.3: Edge-adaptive pixel selection with Sobel filter
- P2.4: Integration with 8+1 bit manipulation scheme
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image
from AESCTR import aes_gcm_encrypt_with_password, aes_gcm_decrypt_with_password


class EdgeAdaptiveLSB:
    """
    Edge-adaptive LSB steganography that embeds data only in smooth regions
    (low gradient pixels) to minimize visual artifacts and detection.
    """

    def __init__(self):
        self.PIXELS_PER_CHAR = 3  # 3 pixels (9 channels) per character

    # -------------------------
    # Encryption Interface
    # -------------------------
    def encrypt_message(self, plain_text, password):
        """Encrypts message using AES-256-GCM with password-based key derivation"""
        return aes_gcm_encrypt_with_password(plain_text, password)

    def decrypt_message(self, cipher_text, password):
        """Decrypts AES-256-GCM encrypted message"""
        try:
            return aes_gcm_decrypt_with_password(cipher_text, password)
        except Exception as e:
            return "[!] Error: Incorrect Key or Corrupted Data"

    # -------------------------
    # P2.1: Statistical Computation
    # -------------------------
    def compute_sobel_gradient(self, image_cv):
        """
        Compute Sobel gradient magnitude for each pixel (Di).

        IMPORTANT: We mask out the LSB before computing gradients to ensure
        encoder and decoder compute identical masks. LSB changes during
        embedding would otherwise affect gradient values and break sync.

        Args:
            image_cv: OpenCV BGR image array

        Returns:
            2D numpy array of gradient magnitudes
        """
        # Mask out LSB from ALL RGB channels BEFORE grayscale conversion
        # This ensures encoder and decoder compute identical masks
        # (grayscale = 0.299*R + 0.587*G + 0.114*B, so RGB LSB changes affect gray)
        image_stable = (image_cv & 0xFE).astype(np.uint8)

        # Convert to grayscale
        gray = cv2.cvtColor(image_stable, cv2.COLOR_BGR2GRAY)

        # Compute Sobel gradients in X and Y directions
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # Compute gradient magnitude: Di = sqrt(Gx^2 + Gy^2)
        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        return gradient_magnitude

    def compute_mean_gradient(self, gradient_map):
        """
        Compute mean gradient (Me) across the entire image.

        Args:
            gradient_map: 2D array of gradient magnitudes

        Returns:
            Mean gradient value (Me)
        """
        return np.mean(gradient_map)

    # -------------------------
    # P2.2: Embedding Condition
    # -------------------------
    def generate_embeddable_mask(self, gradient_map, mean_gradient):
        """
        Generate boolean mask where True indicates embeddable pixels.
        Condition: Di <= Me (embed in smooth regions only)

        Args:
            gradient_map: 2D array of gradient magnitudes (Di)
            mean_gradient: Mean gradient value (Me)

        Returns:
            Boolean mask array
        """
        return gradient_map <= mean_gradient

    def get_embeddable_pixel_coords(self, mask, width, height):
        """
        Extract coordinates of embeddable pixels in deterministic row-major order.
        This order must be identical for encoder and decoder.

        Args:
            mask: Boolean embeddable mask
            width: Image width
            height: Image height

        Returns:
            List of (x, y) tuples for embeddable pixels
        """
        coords = []
        for y in range(height):
            for x in range(width):
                if mask[y, x]:
                    coords.append((x, y))
        return coords

    # -------------------------
    # Utility Methods
    # -------------------------
    def get_capacity(self, image_path):
        """
        Calculate embedding capacity for an image.

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with capacity information
        """
        image_cv = cv2.imread(image_path)
        if image_cv is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        height, width = image_cv.shape[:2]

        # Compute gradient and mask
        gradient_map = self.compute_sobel_gradient(image_cv)
        mean_gradient = self.compute_mean_gradient(gradient_map)
        mask = self.generate_embeddable_mask(gradient_map, mean_gradient)

        embeddable_count = np.sum(mask)
        total_pixels = width * height
        char_capacity = embeddable_count // self.PIXELS_PER_CHAR

        return {
            'total_pixels': total_pixels,
            'embeddable_pixels': int(embeddable_count),
            'embeddable_percent': (embeddable_count / total_pixels) * 100,
            'char_capacity': int(char_capacity),
            'mean_gradient': mean_gradient
        }

    def save_edge_map(self, gradient_map, output_path):
        """
        Save gradient map as visualization image.

        Args:
            gradient_map: 2D array of gradient magnitudes
            output_path: Path to save visualization
        """
        # Normalize to 0-255 for visualization
        normalized = cv2.normalize(gradient_map, None, 0, 255, cv2.NORM_MINMAX)
        cv2.imwrite(output_path, normalized.astype(np.uint8))

    # -------------------------
    # P2.3 + P2.4: Encode
    # -------------------------
    def encode(self, image_path, output_path, secret_text, password):
        """
        Encode secret message into image using edge-adaptive LSB.

        Embeds data only in smooth regions (Di <= Me) for improved
        visual quality and detection resistance.

        Args:
            image_path: Path to cover image
            output_path: Path for stego image output
            secret_text: Message to hide
            password: Encryption password

        Returns:
            Dictionary with encoding statistics
        """
        print(f"[*] Loading image: {image_path}")

        # Load image with both PIL (for pixel manipulation) and OpenCV (for Sobel)
        image_pil = Image.open(image_path)
        if image_pil.mode != 'RGB':
            image_pil = image_pil.convert('RGB')

        image_cv = cv2.imread(image_path)
        if image_cv is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        width, height = image_pil.size
        pixels = image_pil.load()

        # Step 1: Encrypt the secret message
        print("[*] Encrypting text...")
        cipher_text = self.encrypt_message(secret_text, password)
        print(f"[*] Ciphertext length: {len(cipher_text)} chars")

        # Step 2: Compute Sobel gradient map (P2.1)
        print("[*] Computing edge map (Sobel gradient)...")
        gradient_map = self.compute_sobel_gradient(image_cv)
        mean_gradient = self.compute_mean_gradient(gradient_map)
        print(f"[*] Mean gradient (Me): {mean_gradient:.2f}")

        # Step 3: Generate embeddable mask (P2.2)
        mask = self.generate_embeddable_mask(gradient_map, mean_gradient)
        embeddable_coords = self.get_embeddable_pixel_coords(mask, width, height)
        print(f"[*] Embeddable pixels: {len(embeddable_coords)} / {width * height} ({len(embeddable_coords) / (width * height) * 100:.1f}%)")

        # Step 4: Check capacity
        required_pixels = len(cipher_text) * self.PIXELS_PER_CHAR
        if required_pixels > len(embeddable_coords):
            raise ValueError(
                f"[-] Insufficient capacity. Need {required_pixels} pixels, "
                f"have {len(embeddable_coords)} embeddable pixels. "
                f"Max message length: {len(embeddable_coords) // self.PIXELS_PER_CHAR} chars"
            )

        # Step 5: Embed data using edge-adaptive pixel selection (P2.3 + P2.4)
        print("[*] Embedding data in smooth regions...")
        coord_idx = 0
        total_chars = len(cipher_text)

        for i in range(total_chars):
            char = cipher_text[i]
            binary_char = f'{ord(char):08b}'

            # Get 3 consecutive embeddable pixel coordinates
            p1_coord = embeddable_coords[coord_idx]
            p2_coord = embeddable_coords[coord_idx + 1]
            p3_coord = embeddable_coords[coord_idx + 2]
            coord_idx += 3

            # Get pixel values
            p1 = pixels[p1_coord]
            p2 = pixels[p2_coord]
            p3 = pixels[p3_coord]

            # Combine into 9 channel values
            nine_vals = list(p1) + list(p2) + list(p3)

            # Embed 8 bits of character into LSB of first 8 values
            for bit_index in range(8):
                current_val = nine_vals[bit_index]
                bin_val = list(f'{current_val:08b}')
                bin_val[-1] = binary_char[bit_index]
                nine_vals[bit_index] = int("".join(bin_val), 2)

            # Embed continuation flag in 9th LSB (1 = more data, 0 = end)
            has_more = 1 if i < (total_chars - 1) else 0
            last_val = nine_vals[8]
            bin_last = list(f'{last_val:08b}')
            bin_last[-1] = str(has_more)
            nine_vals[8] = int("".join(bin_last), 2)

            # Write back modified pixels
            pixels[p1_coord] = tuple(nine_vals[0:3])
            pixels[p2_coord] = tuple(nine_vals[3:6])
            pixels[p3_coord] = tuple(nine_vals[6:9])

        # Step 6: Save stego image
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"[*] Created directory: {output_dir}")

        print(f"[*] Encoding successful. Saving to {output_path}")
        image_pil.save(output_path, 'PNG')

        return {
            'mean_gradient': mean_gradient,
            'total_pixels': width * height,
            'embeddable_pixels': len(embeddable_coords),
            'used_pixels': required_pixels,
            'capacity_chars': len(embeddable_coords) // self.PIXELS_PER_CHAR,
            'message_chars': total_chars
        }

    # -------------------------
    # Decode
    # -------------------------
    def decode(self, image_path, password):
        """
        Decode secret message from stego image using edge-adaptive LSB.

        Recomputes the same embeddable mask to find embedded data locations.

        Args:
            image_path: Path to stego image
            password: Decryption password

        Returns:
            Decrypted message string
        """
        print(f"[*] Scanning image: {image_path}")

        # Load image with both PIL and OpenCV
        image_pil = Image.open(image_path)
        image_cv = cv2.imread(image_path)

        if image_cv is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        width, height = image_pil.size
        pixels = image_pil.load()

        # Recompute the SAME embeddable mask (critical for decoder sync)
        print("[*] Recomputing edge map for pixel selection...")
        gradient_map = self.compute_sobel_gradient(image_cv)
        mean_gradient = self.compute_mean_gradient(gradient_map)
        mask = self.generate_embeddable_mask(gradient_map, mean_gradient)
        embeddable_coords = self.get_embeddable_pixel_coords(mask, width, height)

        print(f"[*] Found {len(embeddable_coords)} embeddable pixels")

        # Extract hidden data
        cipher_text = ""
        coord_idx = 0

        while coord_idx + 3 <= len(embeddable_coords):
            # Get 3 consecutive embeddable pixel coordinates
            p1_coord = embeddable_coords[coord_idx]
            p2_coord = embeddable_coords[coord_idx + 1]
            p3_coord = embeddable_coords[coord_idx + 2]
            coord_idx += 3

            # Get pixel values
            p1 = pixels[p1_coord]
            p2 = pixels[p2_coord]
            p3 = pixels[p3_coord]

            # Combine into 9 channel values
            nine_vals = list(p1) + list(p2) + list(p3)

            # Extract 8 bits of character from LSBs
            char_bits = ""
            for i in range(8):
                val = nine_vals[i]
                char_bits += f'{val:08b}'[-1]

            char_code = int(char_bits, 2)
            cipher_text += chr(char_code)

            # Check continuation flag
            flag_val = nine_vals[8]
            flag_bit = f'{flag_val:08b}'[-1]

            if flag_bit == '0':
                break

        print(f"[*] Extraction complete. Ciphertext length: {len(cipher_text)}")

        # Decrypt the extracted ciphertext
        print("[*] Decrypting...")
        plain_text = self.decrypt_message(cipher_text, password)
        return plain_text


# -------------------------
# CLI Interface
# -------------------------
if __name__ == "__main__":
    stego = EdgeAdaptiveLSB()

    DEFAULT_INPUT_IMAGE = "media/tyla.jpg"
    DEFAULT_OUTPUT_IMAGE = "media/stego_edge_adaptive.png"

    print("\n" + "="*50)
    print("   Edge-Adaptive LSB Steganography")
    print("="*50)
    print("\nChoose an option:")
    print("1. Encrypt - Hide a secret message in an image")
    print("2. Decrypt - Extract a hidden message from an image")
    print("3. Check Capacity - See how much data an image can hold")
    print("="*50)

    choice = input("\nEnter your choice (1, 2, or 3): ").strip()

    if choice == "1":
        print("\n" + "-"*50)
        print("   ENCRYPTION MODE (Edge-Adaptive)")
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
        elif not os.path.dirname(output_image):
            output_image = os.path.join("media", output_image)

        try:
            print(f"\n[*] Using input image: {DEFAULT_INPUT_IMAGE}")
            stats = stego.encode(DEFAULT_INPUT_IMAGE, output_image, secret_message, password)
            print(f"\n[+] Success! Secret message hidden in '{output_image}'")
            print(f"[+] Used {stats['used_pixels']} of {stats['embeddable_pixels']} embeddable pixels")
            print(f"[+] Keep your password safe to decrypt the message later!")

        except FileNotFoundError as e:
            print(f"\n[!] Error: {e}")
        except ValueError as e:
            print(f"\n[!] Error: {e}")
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}")

    elif choice == "2":
        print("\n" + "-"*50)
        print("   DECRYPTION MODE (Edge-Adaptive)")
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

        except FileNotFoundError as e:
            print(f"\n[!] Error: {e}")
        except Exception as e:
            print(f"\n[!] Error during decryption: {e}")

    elif choice == "3":
        print("\n" + "-"*50)
        print("   CAPACITY CHECK")
        print("-"*50)

        image_path = input(f"\nEnter image path (default: {DEFAULT_INPUT_IMAGE}): ").strip()
        if not image_path:
            image_path = DEFAULT_INPUT_IMAGE
        elif not os.path.dirname(image_path):
            image_path = os.path.join("media", image_path)

        try:
            capacity = stego.get_capacity(image_path)
            print(f"\n[*] Image: {image_path}")
            print(f"[*] Total pixels: {capacity['total_pixels']:,}")
            print(f"[*] Embeddable pixels: {capacity['embeddable_pixels']:,} ({capacity['embeddable_percent']:.1f}%)")
            print(f"[*] Mean gradient (Me): {capacity['mean_gradient']:.2f}")
            print(f"[*] Character capacity: ~{capacity['char_capacity']:,} chars")

        except FileNotFoundError as e:
            print(f"\n[!] Error: {e}")

    else:
        print("\n[!] Invalid choice! Please enter 1, 2, or 3.")
        sys.exit(1)
