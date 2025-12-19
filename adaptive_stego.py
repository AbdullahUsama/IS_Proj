# adaptive_stego.py
"""
Adaptive LSB-MSB Steganography with Edge-Adaptive Enhancement

Implements the algorithm from:
"An Adaptive Image Steganography Technique Using LSB and MSB"
by A. Lakkshmaan, P. U. Dharia, F. Gandhi (2013)

Enhanced with:
- Edge-adaptive embedding using Sobel edge detection
- Integration with AES-CTR encryption
"""

import numpy as np
import cv2
from typing import Tuple, List
import base64


class AdaptiveSteganography:
    """
    Adaptive LSB-MSB Steganography with Edge-Adaptive Enhancement
    """
    
    def __init__(self, block_size=8, edge_threshold=30):
        """
        Args:
            block_size: Size of image blocks (default 8x8)
            edge_threshold: Threshold for edge detection (higher = only strong edges)
        """
        self.BLOCK_SIZE = block_size
        self.EDGE_THRESHOLD = edge_threshold
        
    def _compute_edge_map(self, image: np.ndarray) -> np.ndarray:
        """
        Compute edge magnitude using Sobel operator
        Higher values indicate edge regions where embedding is less detectable
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        # Compute Sobel gradients
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Edge magnitude
        edge_magnitude = np.sqrt(sobelx**2 + sobely**2)
        return edge_magnitude
    
    def _partition_into_blocks(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Partition image into 8x8 blocks
        Returns list of blocks
        """
        h, w = image.shape[:2]
        blocks = []
        
        for i in range(0, h - self.BLOCK_SIZE + 1, self.BLOCK_SIZE):
            for j in range(0, w - self.BLOCK_SIZE + 1, self.BLOCK_SIZE):
                block = image[i:i+self.BLOCK_SIZE, j:j+self.BLOCK_SIZE]
                blocks.append((block, i, j))
                
        return blocks
    
    def _compute_mean_of_medians(self, block: np.ndarray) -> float:
        """
        Compute mean-of-medians (Me) for a block
        1. Find median of each column
        2. Compute mean of these medians
        """
        if len(block.shape) == 3:
            block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
            
        medians = []
        for col_idx in range(block.shape[1]):
            column = block[:, col_idx]
            medians.append(np.median(column))
            
        mean_of_medians = np.mean(medians)
        return mean_of_medians
    
    def _get_embedding_case(self, p1: int, p2: int) -> int:
        """
        Determine embedding case based on MSB patterns
        
        Case 0: MSB(p1)==MSB(p2)==0 -> embed in bit 1 of both pixels
        Case 1: MSB(p1)==1, MSB(p2)==0 -> embed in bits 2,3 of p1 and bit 1 of p2
        Case 2: MSB(p1)==0, MSB(p2)==1 -> embed in bit 1 of p1 and bits 2,3 of p2
        Case 3: MSB(p1)==MSB(p2)==1 -> embed in bits 2,3 of both pixels
        """
        msb_p1 = (p1 >> 7) & 1
        msb_p2 = (p2 >> 7) & 1
        
        if msb_p1 == 0 and msb_p2 == 0:
            return 0
        elif msb_p1 == 1 and msb_p2 == 0:
            return 1
        elif msb_p1 == 0 and msb_p2 == 1:
            return 2
        else:  # both MSBs are 1
            return 3
    
    def _embed_bits_in_pixel_pair(self, p1: int, p2: int, bits: List[int]) -> Tuple[int, int]:
        """
        Embed bits into pixel pair based on MSB case
        Returns modified (p1, p2)
        """
        case = self._get_embedding_case(p1, p2)
        
        if case == 0:
            # Embed in bit position 1 (LSB+1) of both pixels
            if len(bits) >= 2:
                p1 = (p1 & 0b11111101) | (bits[0] << 1)
                p2 = (p2 & 0b11111101) | (bits[1] << 1)
        
        elif case == 1:
            # Embed in bits 2,3 of p1 and bit 1 of p2
            if len(bits) >= 3:
                p1 = (p1 & 0b11110011) | (bits[0] << 2) | (bits[1] << 3)
                p2 = (p2 & 0b11111101) | (bits[2] << 1)
        
        elif case == 2:
            # Embed in bit 1 of p1 and bits 2,3 of p2
            if len(bits) >= 3:
                p1 = (p1 & 0b11111101) | (bits[0] << 1)
                p2 = (p2 & 0b11110011) | (bits[1] << 2) | (bits[2] << 3)
        
        elif case == 3:
            # Embed in bits 2,3 of both pixels
            if len(bits) >= 4:
                p1 = (p1 & 0b11110011) | (bits[0] << 2) | (bits[1] << 3)
                p2 = (p2 & 0b11110011) | (bits[2] << 2) | (bits[3] << 3)
        
        return p1, p2
    
    def _extract_bits_from_pixel_pair(self, p1: int, p2: int) -> List[int]:
        """
        Extract embedded bits from pixel pair based on MSB case
        """
        case = self._get_embedding_case(p1, p2)
        bits = []
        
        if case == 0:
            bits.append((p1 >> 1) & 1)
            bits.append((p2 >> 1) & 1)
        
        elif case == 1:
            bits.append((p1 >> 2) & 1)
            bits.append((p1 >> 3) & 1)
            bits.append((p2 >> 1) & 1)
        
        elif case == 2:
            bits.append((p1 >> 1) & 1)
            bits.append((p2 >> 2) & 1)
            bits.append((p2 >> 3) & 1)
        
        elif case == 3:
            bits.append((p1 >> 2) & 1)
            bits.append((p1 >> 3) & 1)
            bits.append((p2 >> 2) & 1)
            bits.append((p2 >> 3) & 1)
        
        return bits
    
    def encode(self, cover_image_path: str, output_path: str, 
               payload_bytes: bytes) -> dict:
        """
        Embed payload into image using adaptive LSB-MSB with edge enhancement
        
        Args:
            cover_image_path: Path to cover image
            output_path: Path to save stego image
            payload_bytes: Encrypted payload to embed
            
        Returns:
            dict with metadata (UB, LB, capacity, etc.)
        """
        # Load image
        image = cv2.imread(cover_image_path)
        if image is None:
            raise ValueError(f"Cannot load image: {cover_image_path}")
        
        # Compute edge map for edge-adaptive embedding
        edge_map = self._compute_edge_map(image)
        
        # Convert payload to bit string
        payload_bits = ''.join(format(byte, '08b') for byte in payload_bytes)
        payload_len = len(payload_bits)
        
        print(f"[*] Payload size: {len(payload_bytes)} bytes ({payload_len} bits)")
        
        # Convert to grayscale for embedding
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image.copy()
        
        stego_image = gray_image.copy()
        h, w = stego_image.shape
        
        # Calculate UB and LB (Upper and Lower Bounds)
        UB = int(np.max(gray_image))
        LB = int(np.min(gray_image))
        
        print(f"[*] Image bounds: UB={UB}, LB={LB}")
        
        # Embed UB and LB in first 16 pixels (2 bytes each in LSB)
        # UB in first 8 pixels, LB in next 8 pixels
        ub_bits = format(UB, '08b')
        lb_bits = format(LB, '08b')
        
        for i in range(8):
            stego_image[0, i] = (stego_image[0, i] & 0xFE) | int(ub_bits[i])
            stego_image[0, i+8] = (stego_image[0, i+8] & 0xFE) | int(lb_bits[i])
        
        # Embed payload length in next 32 pixels (4 bytes)
        len_bits = format(payload_len, '032b')
        for i in range(32):
            stego_image[0, i+16] = (stego_image[0, i+16] & 0xFE) | int(len_bits[i])
        
        # Partition into blocks
        blocks = self._partition_into_blocks(stego_image)
        
        # Track embedding statistics
        bit_idx = 0
        embedded_bits = 0
        blocks_used = 0
        
        # Sort blocks by edge intensity (prioritize edge regions)
        block_edge_scores = []
        for block, bi, bj in blocks[1:]:  # Skip first block (contains UB/LB)
            edge_score = np.mean(edge_map[bi:bi+self.BLOCK_SIZE, bj:bj+self.BLOCK_SIZE])
            block_edge_scores.append((edge_score, block, bi, bj))
        
        # Sort by edge score (descending) for edge-adaptive embedding
        block_edge_scores.sort(reverse=True, key=lambda x: x[0])
        
        print(f"[*] Processing {len(block_edge_scores)} blocks (edge-adaptive order)")
        
        # Embed in blocks
        for edge_score, block, bi, bj in block_edge_scores:
            if bit_idx >= payload_len:
                break
            
            # Only embed in blocks with sufficient edge strength
            if edge_score < self.EDGE_THRESHOLD:
                continue
                
            # Compute mean-of-medians for adaptive threshold
            Me = self._compute_mean_of_medians(block)
            
            # Process pixel pairs in the block
            for i in range(0, self.BLOCK_SIZE - 1, 2):
                for j in range(0, self.BLOCK_SIZE):
                    if bit_idx >= payload_len:
                        break
                    
                    p1 = int(stego_image[bi+i, bj+j])
                    p2 = int(stego_image[bi+i+1, bj+j])
                    
                    # Pixel difference threshold (adaptive)
                    Di = abs(p1 - p2)
                    
                    if Di <= Me:
                        # Determine how many bits we can embed
                        case = self._get_embedding_case(p1, p2)
                        bits_per_pair = [2, 3, 3, 4][case]
                        
                        # Extract bits from payload
                        bits_to_embed = []
                        for _ in range(bits_per_pair):
                            if bit_idx < payload_len:
                                bits_to_embed.append(int(payload_bits[bit_idx]))
                                bit_idx += 1
                        
                        if bits_to_embed:
                            # Embed bits
                            p1_new, p2_new = self._embed_bits_in_pixel_pair(p1, p2, bits_to_embed)
                            stego_image[bi+i, bj+j] = p1_new
                            stego_image[bi+i+1, bj+j] = p2_new
                            embedded_bits += len(bits_to_embed)
            
            blocks_used += 1
        
        if bit_idx < payload_len:
            print(f"[!] Warning: Only embedded {bit_idx}/{payload_len} bits")
        else:
            print(f"[*] Successfully embedded all {payload_len} bits")
        
        # Save stego image
        cv2.imwrite(output_path, stego_image)
        print(f"[*] Stego image saved to: {output_path}")
        
        # Return metadata
        capacity_bpp = embedded_bits / (h * w)
        return {
            'UB': UB,
            'LB': LB,
            'payload_bits': payload_len,
            'embedded_bits': embedded_bits,
            'blocks_used': blocks_used,
            'capacity_bpp': capacity_bpp,
            'image_size': (h, w)
        }
    
    def decode(self, stego_image_path: str) -> bytes:
        """
        Extract payload from stego image
        
        Args:
            stego_image_path: Path to stego image
            
        Returns:
            Extracted payload bytes
        """
        # Load stego image
        image = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Cannot load image: {stego_image_path}")
        
        h, w = image.shape
        
        # Extract UB and LB from first 16 pixels
        ub_bits = ''.join(str(image[0, i] & 1) for i in range(8))
        lb_bits = ''.join(str(image[0, i+8] & 1) for i in range(8))
        UB = int(ub_bits, 2)
        LB = int(lb_bits, 2)
        
        print(f"[*] Extracted bounds: UB={UB}, LB={LB}")
        
        # Extract payload length from next 32 pixels
        len_bits = ''.join(str(image[0, i+16] & 1) for i in range(32))
        payload_len = int(len_bits, 2)
        
        print(f"[*] Payload length: {payload_len} bits ({payload_len//8} bytes)")
        
        # Compute edge map (same as encoding)
        edge_map = self._compute_edge_map(image)
        
        # Partition into blocks
        blocks = self._partition_into_blocks(image)
        
        # Sort blocks by edge score (same order as encoding)
        block_edge_scores = []
        for block, bi, bj in blocks[1:]:
            edge_score = np.mean(edge_map[bi:bi+self.BLOCK_SIZE, bj:bj+self.BLOCK_SIZE])
            block_edge_scores.append((edge_score, block, bi, bj))
        
        block_edge_scores.sort(reverse=True, key=lambda x: x[0])
        
        # Extract bits
        extracted_bits = []
        
        for edge_score, block, bi, bj in block_edge_scores:
            if len(extracted_bits) >= payload_len:
                break
            
            if edge_score < self.EDGE_THRESHOLD:
                continue
            
            Me = self._compute_mean_of_medians(block)
            
            for i in range(0, self.BLOCK_SIZE - 1, 2):
                for j in range(0, self.BLOCK_SIZE):
                    if len(extracted_bits) >= payload_len:
                        break
                    
                    p1 = int(image[bi+i, bj+j])
                    p2 = int(image[bi+i+1, bj+j])
                    
                    Di = abs(p1 - p2)
                    
                    if Di <= Me:
                        bits = self._extract_bits_from_pixel_pair(p1, p2)
                        for bit in bits:
                            if len(extracted_bits) < payload_len:
                                extracted_bits.append(bit)
        
        print(f"[*] Extracted {len(extracted_bits)}/{payload_len} bits")
        
        # Convert bits to bytes
        payload_bytes = bytearray()
        for i in range(0, len(extracted_bits), 8):
            if i + 8 <= len(extracted_bits):
                byte_bits = extracted_bits[i:i+8]
                byte_val = int(''.join(map(str, byte_bits)), 2)
                payload_bytes.append(byte_val)
        
        return bytes(payload_bytes)
