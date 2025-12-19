# main.py
"""
Enhanced Adaptive Steganography System

Combines:
1. AES-CTR Encryption (confidentiality)
2. Adaptive LSB-MSB Steganography (from research paper)
3. Edge-Adaptive Embedding (robustness enhancement)

Improvements over basic LSB:
- Multi-bit adaptive embedding based on pixel MSB patterns
- Edge-aware embedding for better imperceptibility
- Block-based processing with mean-of-medians threshold
- Cryptographic protection of payload
"""

import sys
import base64
import os

from AESCTR import aes_ctr_encrypt, aes_ctr_decrypt
from adaptive_stego import AdaptiveSteganography
from metricscalc import comprehensive_evaluation, print_evaluation_results


def hide_message_adaptive(input_image, output_image, secret_message, edge_threshold=30):
    """
    Encrypt message with AES-CTR, then embed using adaptive LSB-MSB with edge enhancement
    
    Args:
        input_image: Path to cover image
        output_image: Path to save stego image
        secret_message: Secret message to hide
        edge_threshold: Threshold for edge detection (higher = only strong edges)
        
    Returns: 
        tuple (AES key, embedding metadata)
    """
    print("\n" + "="*60)
    print("ENCRYPTION PHASE")
    print("="*60)
    print("[*] Encrypting secret message with AES-CTR...")
    key, nonce, ciphertext = aes_ctr_encrypt(secret_message.encode())
    
    # Combine nonce + ciphertext for embedding
    payload_bytes = nonce + ciphertext
    print(f"[*] Payload size: {len(payload_bytes)} bytes")
    
    print("\n" + "="*60)
    print("EMBEDDING PHASE - Adaptive LSB-MSB + Edge Enhancement")
    print("="*60)
    
    # Use adaptive steganography with edge enhancement
    stego = AdaptiveSteganography(block_size=8, edge_threshold=edge_threshold)
    metadata = stego.encode(input_image, output_image, payload_bytes)
    
    print("\n[✓] Embedding complete!")
    print(f"[*] Capacity: {metadata['capacity_bpp']:.4f} bits per pixel")
    print(f"[*] Blocks used: {metadata['blocks_used']}")
    
    return key, metadata


def extract_message_adaptive(stego_image, key, edge_threshold=30):
    """
    Extract encrypted payload from stego image and decrypt with AES-CTR
    
    Args:
        stego_image: Path to stego image
        key: AES key for decryption
        edge_threshold: Same threshold used during embedding
        
    Returns:
        Decrypted message string
    """
    print("\n" + "="*60)
    print("EXTRACTION PHASE")
    print("="*60)
    
    # Extract payload using adaptive steganography
    stego = AdaptiveSteganography(block_size=8, edge_threshold=edge_threshold)
    payload_bytes = stego.decode(stego_image)
    
    print(f"[*] Extracted payload size: {len(payload_bytes)} bytes")
    
    # Split nonce and ciphertext
    if len(payload_bytes) < 8:
        raise ValueError("Extracted payload too small - extraction may have failed")
    
    nonce = payload_bytes[:8]
    ciphertext = payload_bytes[8:]
    
    print(f"[*] Nonce: {nonce.hex()[:16]}...")
    print(f"[*] Ciphertext size: {len(ciphertext)} bytes")
    
    print("\n" + "="*60)
    print("DECRYPTION PHASE")
    print("="*60)
    print("[*] Decrypting with AES-CTR...")
    
    # Decrypt
    decrypted_message = aes_ctr_decrypt(ciphertext, key, nonce)
    
    print("[✓] Decryption complete!")
    print(f"[*] Decrypted data size: {len(decrypted_message)} bytes")
    
    # Try to decode with multiple encodings
    for encoding in ['utf-8', 'latin-1', 'ascii', 'utf-16']:
        try:
            decoded = decrypted_message.decode(encoding)
            # Check if it's printable
            if decoded.isprintable() or encoding == 'utf-8':
                if encoding != 'utf-8':
                    print(f"[!] Note: Decoded using {encoding} encoding")
                return decoded
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # If all encodings fail, show hex dump for debugging
    print("\n[!] Warning: Could not decode as text. Showing hex dump:")
    print(f"First 64 bytes: {decrypted_message[:64].hex()}")
    print(f"\nTrying to show as raw bytes (errors='replace'):")
    return decrypted_message.decode('utf-8', errors='replace')


def compare_with_basic_lsb(cover_image, secret_message):
    """
    Compare adaptive method with basic LSB steganography
    """
    print("\n" + "="*60)
    print("COMPARISON WITH BASIC LSB")
    print("="*60)
    
    from steno import SteganographyLSB
    
    # Basic LSB
    basic_output = "media/basic_lsb_stego.png"
    stego_basic = SteganographyLSB()
    try:
        stego_basic.encode(cover_image, basic_output, secret_message, password="test123")
        print("[*] Basic LSB embedding completed")
        
        # Evaluate basic LSB
        results_basic = comprehensive_evaluation(cover_image, basic_output)
        print_evaluation_results(results_basic, "Basic LSB Steganography")
    except Exception as e:
        print(f"[!] Basic LSB comparison failed: {e}")


if __name__ == "__main__":
    DEFAULT_IMAGE = "media/landscape.jpg"
    STEGO_IMAGE = "media/adaptive_stego_image.png"
    
    print("\n" + "="*70)
    print(" ENHANCED ADAPTIVE STEGANOGRAPHY SYSTEM ".center(70, "="))
    print("="*70)
    print("Features:")
    print("  • AES-CTR Encryption")
    print("  • Adaptive LSB-MSB Embedding (Research Paper Implementation)")
    print("  • Edge-Adaptive Enhancement (Sobel-based)")
    print("  • Comprehensive Quality Evaluation")
    print("="*70)
    
    # Check if cover image exists
    if not os.path.exists(DEFAULT_IMAGE):
        print(f"\n[!] Error: Cover image not found: {DEFAULT_IMAGE}")
        print("[*] Please place an image at the specified path")
        sys.exit(1)
    
    # Get secret message
    print("\n[?] Enter the secret message to hide:")
    secret_message = input(">>> ").strip()
    
    if not secret_message:
        print("[!] Error: Secret message cannot be empty!")
        sys.exit(1)
    
    # Edge threshold setting
    print("\n[?] Edge threshold (10-50, default 30, higher = stronger edges only):")
    edge_input = input(">>> ").strip()
    edge_threshold = int(edge_input) if edge_input.isdigit() else 30
    
    try:
        # Step 1: Hide message using adaptive method
        aes_key, metadata = hide_message_adaptive(
            DEFAULT_IMAGE, 
            STEGO_IMAGE, 
            secret_message,
            edge_threshold=edge_threshold
        )
        
        # Step 2: Evaluate embedding quality
        print("\n" + "="*60)
        print("QUALITY EVALUATION")
        print("="*60)
        
        results = comprehensive_evaluation(
            DEFAULT_IMAGE, 
            STEGO_IMAGE,
            payload_bits=metadata['payload_bits']
        )
        print_evaluation_results(results, "Adaptive LSB-MSB + Edge Enhancement")
        
        # Step 3: Extract and verify (use same edge threshold!)
        print("\n" + "="*60)
        print("EXTRACTION AND VERIFICATION")
        print("="*60)
        
        recovered_message = extract_message_adaptive(STEGO_IMAGE, aes_key, edge_threshold)
        
        print(f"\n[✓] Original:  {secret_message}")
        print(f"[✓] Recovered: {recovered_message}")
        
        if secret_message == recovered_message:
            print("\n[✓] SUCCESS: Message recovered correctly!")
        else:
            print("\n[✗] ERROR: Message recovery failed!")
        
        print("="*60)
        
        # Optional: Compare with basic LSB
        print("\n[?] Compare with basic LSB method? (y/n):")
        compare = input(">>> ").strip().lower()
        if compare == 'y':
            compare_with_basic_lsb(DEFAULT_IMAGE, secret_message)
        
        print("\n[*] Process complete!")
        print(f"[*] Stego image saved at: {STEGO_IMAGE}")
        
    except Exception as e:
        print(f"\n[!] Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
