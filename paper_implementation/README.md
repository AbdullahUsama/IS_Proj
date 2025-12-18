# Edge-Adaptive LSB Steganography

This project implements an enhanced LSB (Least Significant Bit) steganography system that uses edge detection to improve embedding quality and detection resistance.

## Overview

Traditional LSB steganography embeds data sequentially across all pixels, which can cause noticeable artifacts in edge regions where humans are more sensitive to changes. This implementation uses **edge-adaptive embedding** that avoids high-gradient (edge) pixels and only embeds data in smooth regions.

## Files

| File | Description |
|------|-------------|
| `steno_enhanced.py` | Edge-adaptive LSB steganography (main implementation) |
| `steno.py` | Basic sequential LSB steganography (for comparison) |
| `AESCTR.py` | AES-256-GCM encryption module |
| `metricscalc.py` | PSNR/MSE image quality metrics |
| `main.py` | Demo/integration script |

## Algorithm Implementation

### Task P2.1: Statistical Computation (Me and Di)

**Location**: `steno_enhanced.py` - `compute_sobel_gradient()` and `compute_mean_gradient()`

Computes edge information using Sobel filter:

- **Di (Pixel Difference)**: Sobel gradient magnitude at each pixel
  ```
  Di = sqrt(Gx² + Gy²)
  ```
  Where Gx and Gy are Sobel gradients in X and Y directions.

- **Me (Mean Gradient)**: Average of all gradient magnitudes across the image
  ```
  Me = mean(Di for all pixels)
  ```

**Key Implementation Detail**: LSBs of all RGB channels are masked (`& 0xFE`) before grayscale conversion to ensure encoder and decoder compute identical gradient maps regardless of LSB modifications.

```python
image_stable = (image_cv & 0xFE).astype(np.uint8)
gray = cv2.cvtColor(image_stable, cv2.COLOR_BGR2GRAY)
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
```

### Task P2.2: Embedding Condition (Di <= Me)

**Location**: `steno_enhanced.py` - `generate_embeddable_mask()` and `get_embeddable_pixel_coords()`

Creates a boolean mask identifying embeddable pixels:

```python
embeddable_mask = gradient_map <= mean_gradient
```

- **True** = Smooth region (low gradient) - safe to embed
- **False** = Edge region (high gradient) - skip embedding

Pixels are extracted in deterministic row-major order for encoder/decoder synchronization:

```python
for y in range(height):
    for x in range(width):
        if mask[y, x]:
            coords.append((x, y))
```

### Task P2.3: Edge-Adaptive Embedding Logic

**Location**: `steno_enhanced.py` - `encode()` method

The encoding process:

1. Load image with PIL (pixel manipulation) and OpenCV (Sobel computation)
2. Encrypt message using AES-256-GCM
3. Compute Sobel gradient map (Di for all pixels)
4. Compute mean gradient (Me)
5. Generate embeddable mask: `Di <= Me`
6. Extract embeddable pixel coordinates in row-major order
7. Check capacity (need `len(ciphertext) * 3` embeddable pixels)
8. Embed data only in embeddable pixels
9. Save as PNG (lossless format)

### Task P2.4: Integration with Bit Manipulation

**Location**: `steno_enhanced.py` - `encode()` and `decode()` methods

Uses the same 8+1 bit scheme from `steno.py`:

- **3 pixels per character** (9 channel values: R1,G1,B1, R2,G2,B2, R3,G3,B3)
- **8 bits for character data** embedded in LSB of first 8 channel values
- **1 continuation flag** in LSB of 9th channel value (1=more data, 0=end)

```
Character 'A' (ASCII 65 = 01000001):
Pixel 1: [R1_LSB=0, G1_LSB=1, B1_LSB=0]
Pixel 2: [R2_LSB=0, G2_LSB=0, B2_LSB=0]
Pixel 3: [R3_LSB=0, G3_LSB=1, B3_LSB=flag]
```

## Usage

### Encrypt (Hide Message)

```bash
cd paper_implementation
python steno_enhanced.py
# Choose option 1
# Enter your secret message
# Enter a password
# Specify output image (or use default)
```

### Decrypt (Extract Message)

```bash
python steno_enhanced.py
# Choose option 2
# Enter path to stego image
# Enter the password used during encryption
```

### Check Capacity

```bash
python steno_enhanced.py
# Choose option 3
# Enter image path
```

### Programmatic Usage

```python
from steno_enhanced import EdgeAdaptiveLSB

stego = EdgeAdaptiveLSB()

# Encode
stats = stego.encode(
    'media/cover.jpg',           # Input image
    'media/stego_output.png',    # Output (must be PNG)
    'Secret message here',       # Message to hide
    'mypassword123'              # Encryption password
)
print(f"Used {stats['used_pixels']} of {stats['embeddable_pixels']} pixels")

# Decode
message = stego.decode('media/stego_output.png', 'mypassword123')
print(f"Recovered: {message}")

# Check capacity
capacity = stego.get_capacity('media/cover.jpg')
print(f"Can store ~{capacity['char_capacity']} characters")
```

## Key Features

| Feature | Description |
|---------|-------------|
| Edge-Adaptive Embedding | Only embeds in smooth regions (~75% of pixels typically) |
| AES-256-GCM Encryption | Authenticated encryption with tamper detection |
| Password-Based Key | Uses PBKDF2 for key derivation from password |
| Lossless Output | Saves as PNG to preserve LSB values |
| Decoder Sync | RGB LSB masking ensures identical masks for encode/decode |

## Technical Notes

### Why Mask LSBs Before Gradient Computation?

When we embed data by modifying LSBs, pixel values change by +/-1. This affects the Sobel gradient calculation, potentially causing different pixels to cross the `Di <= Me` threshold. By masking LSBs (`& 0xFE`) before computing gradients, both encoder and decoder see identical gradient values regardless of LSB modifications.

### Capacity

Approximately 50-75% of pixels are embeddable (below mean gradient). For a 1000x1000 image:
- Total pixels: 1,000,000
- Embeddable (~60%): ~600,000 pixels
- Character capacity: ~200,000 characters

### Image Format

**Output must be PNG** (or another lossless format). JPEG compression destroys LSB values and will corrupt the hidden data.

## Comparison with Basic LSB

| Metric | Basic LSB (`steno.py`) | Edge-Adaptive (`steno_enhanced.py`) |
|--------|------------------------|-------------------------------------|
| Embedding Location | Sequential (all pixels) | Smooth regions only |
| Capacity | 100% of pixels | ~50-75% of pixels |
| Visual Quality | May have edge artifacts | Better (avoids edges) |
| Detection Resistance | Lower | Higher |
| PSNR | ~51-53 dB | ~52-55 dB (expected improvement) |

## Dependencies

```
Pillow>=10.4.0
opencv-python>=4.10.0.84
pycryptodome>=3.20.0
```

## Class Reference: EdgeAdaptiveLSB

### Methods

| Method | Description |
|--------|-------------|
| `encode(image_path, output_path, secret_text, password)` | Hide message in image |
| `decode(image_path, password)` | Extract hidden message |
| `get_capacity(image_path)` | Get embedding capacity info |
| `compute_sobel_gradient(image_cv)` | Compute Di (gradient map) |
| `compute_mean_gradient(gradient_map)` | Compute Me (mean gradient) |
| `generate_embeddable_mask(gradient_map, mean_gradient)` | Create boolean mask |
| `get_embeddable_pixel_coords(mask, width, height)` | Get embeddable pixel list |
| `encrypt_message(plain_text, password)` | AES-GCM encryption |
| `decrypt_message(cipher_text, password)` | AES-GCM decryption |
