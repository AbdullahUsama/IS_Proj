# Enhanced Adaptive Steganography System

## 📋 Project Overview

Implementation and enhancement of the adaptive LSB-MSB steganography technique from the research paper **"An Adaptive Image Steganography Technique Using LSB and MSB"** by A. Lakkshmaan, P. U. Dharia, F. Gandhi (2013).

### Key Improvements Implemented:

1. **✅ Adaptive LSB-MSB Algorithm** (from research paper)
   - 8×8 block decomposition
   - UB/LB (Upper/Lower Bound) embedding
   - Mean-of-medians (Me) computation
   - Pixel difference thresholding (Di ≤ Me)
   - Case-based multi-bit embedding (Cases 0-3)

2. **✅ AES-CTR Encryption** (Security Enhancement)
   - Cryptographic protection of payload
   - Encrypted bits appear as random noise
   - Protects confidentiality even if detected

3. **✅ Edge-Adaptive Embedding** (Robustness Enhancement)
   - Sobel edge detection to identify high-gradient regions
   - Prioritizes embedding in edge areas (less detectable)
   - Reduces statistical anomalies

4. **✅ Comprehensive Evaluation Metrics**
   - PSNR (Peak Signal-to-Noise Ratio)
   - MSE (Mean Squared Error)
   - Entropy (Shannon Entropy)
   - Capacity (bits per pixel)
   - Histogram Deviation

5. **✅ Steganalysis Testing**
   - RS Analysis (Regular-Singular)
   - Histogram-based Detection
   - Chi-Square Attack

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run the enhanced steganography system
python main.py
```

Follow the prompts to:
1. Enter your secret message
2. Set edge threshold (10-50, default: 30)
3. View comprehensive quality metrics
4. Optionally compare with basic LSB

---

## 📂 Project Structure

```
IS_Proj/
├── main.py                  # Main orchestration (enhanced with adaptive method)
├── adaptive_stego.py        # NEW: Adaptive LSB-MSB + Edge enhancement
├── AESCTR.py               # AES-CTR encryption/decryption
├── steno.py                # Basic LSB steganography (for comparison)
├── metricscalc.py          # ENHANCED: Comprehensive metrics evaluation
├── steganalysis.py         # NEW: Steganalysis attacks (RS, Histogram, Chi-Square)
├── requirements.txt        # Python dependencies
└── media/                  # Cover and stego images
    ├── tyla.jpg           # Example cover image
    └── adaptive_stego_image.png  # Generated stego image
```

---

## 🔬 Technical Implementation

### 1. Adaptive LSB-MSB Algorithm

#### Block-Based Processing
- Image partitioned into **8×8 blocks**
- First block stores UB/LB metadata
- Remaining blocks used for adaptive embedding

#### Mean-of-Medians (Me) Threshold
```
For each 8×8 block:
  1. Compute median of each column
  2. Calculate mean of these medians → Me
  3. Use Me as adaptive threshold for embedding
```

#### Case-Based Embedding Strategy
Based on MSB patterns of pixel pairs (p1, p2):

| Case | MSB(p1) | MSB(p2) | Embedding Positions | Bits/Pair |
|------|---------|---------|---------------------|-----------|
| 0    | 0       | 0       | bit 1 of both       | 2 bits    |
| 1    | 1       | 0       | bits 2,3 of p1, bit 1 of p2 | 3 bits    |
| 2    | 0       | 1       | bit 1 of p1, bits 2,3 of p2 | 3 bits    |
| 3    | 1       | 1       | bits 2,3 of both    | 4 bits    |

**Adaptive Criterion**: Only embed when `|p1 - p2| ≤ Me`

### 2. Edge-Adaptive Enhancement

```python
# Compute Sobel edge magnitude
edge_map = √(sobelx² + sobely²)

# Sort blocks by edge intensity (descending)
# Prioritize embedding in high-gradient regions
blocks_sorted = sort_by_edge_score(blocks)

# Only embed in blocks with edge_score > threshold
```

**Benefits**:
- Modifications less visible in textured/edge regions
- Reduces statistical detectability
- Maintains high PSNR

### 3. Security: AES-CTR Integration

```
Workflow:
1. Encrypt message: plaintext → AES-CTR → ciphertext
2. Combine: payload = nonce (8 bytes) + ciphertext
3. Embed: payload → adaptive steganography → stego_image
4. Extract: stego_image → adaptive extraction → payload
5. Decrypt: payload → AES-CTR → plaintext
```

---

## 📊 Evaluation Metrics

### Quality Metrics

| Metric | Description | Good Range |
|--------|-------------|------------|
| **PSNR** | Peak Signal-to-Noise Ratio | > 40 dB (excellent) |
| **MSE** | Mean Squared Error | < 10 (imperceptible) |
| **Entropy** | Shannon Entropy | ~7.5-7.9 bits (natural) |
| **Capacity** | Bits per pixel | Varies (higher = more data) |
| **Histogram Deviation** | Chi-square distance | < 0.01 (undetectable) |

### Steganalysis Resistance

| Attack | Detection Method | Resistance |
|--------|------------------|------------|
| **RS Analysis** | Regular-Singular groups | Tests correlation patterns |
| **Histogram** | Statistical distribution | Tests pixel value changes |
| **Chi-Square** | Pairs of Values (PoVs) | Tests LSB embedding artifacts |

---

## 🎯 Usage Examples

### Example 1: Basic Embedding

```python
python main.py
```

```
Enter the secret message to hide:
>>> This is a confidential message!

Edge threshold (10-50, default 30, higher = stronger edges only):
>>> 30

[*] Encrypting secret message with AES-CTR...
[*] Payload size: 41 bytes (328 bits)
[*] Processing blocks (edge-adaptive order)
[✓] Successfully embedded all 328 bits
```

### Example 2: Programmatic Usage

```python
from adaptive_stego import AdaptiveSteganography
from AESCTR import aes_ctr_encrypt, aes_ctr_decrypt

# Encrypt message
message = "Secret data"
key, nonce, ciphertext = aes_ctr_encrypt(message.encode())
payload = nonce + ciphertext

# Embed with adaptive method
stego = AdaptiveSteganography(block_size=8, edge_threshold=30)
metadata = stego.encode("cover.jpg", "stego.png", payload)

# Extract
extracted_payload = stego.decode("stego.png")
nonce_ex = extracted_payload[:8]
cipher_ex = extracted_payload[8:]
decrypted = aes_ctr_decrypt(cipher_ex, key, nonce_ex)
print(decrypted.decode())  # "Secret data"
```

### Example 3: Steganalysis Testing

```python
from steganalysis import comprehensive_steganalysis

results = comprehensive_steganalysis("cover.jpg", "stego.png")

# Results include:
# - RS Analysis (embedding rate estimation)
# - Histogram Analysis (statistical deviation)
# - Chi-Square Attack (detection confidence)
```

---

## 📈 Performance Comparison

### Adaptive LSB-MSB vs Basic LSB

| Aspect | Basic LSB | Adaptive LSB-MSB | Edge-Enhanced |
|--------|-----------|------------------|---------------|
| **Embedding Strategy** | Sequential LSB | MSB-adaptive multi-bit | Edge-prioritized |
| **Capacity** | Fixed 1 bpp | Variable 2-4 bits/pair | Adaptive |
| **PSNR** | ~45-50 dB | ~48-55 dB | ~50-58 dB |
| **RS Detection** | Easily detected | Moderate resistance | High resistance |
| **Histogram Impact** | Noticeable pairs | Reduced artifacts | Minimal deviation |

---

## 🔍 Research Paper Implementation

### Original Algorithm Features (✅ Implemented)

- [x] 8×8 block decomposition
- [x] UB/LB value embedding in first block
- [x] Median computation for each column
- [x] Mean-of-medians (Me) calculation
- [x] Pixel difference thresholding (Di ≤ Me)
- [x] MSB-based case determination (Cases 0-3)
- [x] Adaptive bit position embedding
- [x] PSNR evaluation
- [x] MSE calculation
- [x] Entropy measurement
- [x] Capacity analysis

### Proposed Enhancements (✅ Implemented)

- [x] **AES-CTR encryption** for payload confidentiality
- [x] **Sobel edge detection** for edge-adaptive embedding
- [x] **Edge-prioritized block sorting** for imperceptibility
- [x] **Comprehensive steganalysis** (RS, Histogram, Chi-Square)
- [x] **Histogram deviation metric** for detection resistance

---

## 🛡️ Security Considerations

### Cryptographic Protection
- **AES-256-CTR** ensures payload appears random
- Even if extracted, data is unintelligible without key
- Key management: Store securely, never embed in image

### Steganalysis Resistance
- **Edge-adaptive embedding** reduces statistical anomalies
- **Adaptive thresholding** preserves natural pixel correlations
- **Multi-bit embedding** increases complexity for attackers

### Limitations
- **Key distribution**: Requires secure channel for key exchange
- **Capacity trade-off**: Edge-only embedding reduces capacity
- **Cover selection**: Works best with natural images (rich textures)

---

## 📚 References

1. **Original Paper**: Lakkshmaan, A., Dharia, P. U., & Gandhi, F. (2013). "An Adaptive Image Steganography Technique Using LSB and MSB." IARS International Research Journal.

2. **AES-CTR**: NIST SP 800-38A - Recommendation for Block Cipher Modes of Operation

3. **Edge Detection**: Sobel Operator - Digital Image Processing (Gonzalez & Woods)

4. **Steganalysis**: 
   - Fridrich, J. et al. (2001). "Reliable Detection of LSB Steganography in Color and Grayscale Images"
   - Provos, N. & Honeyman, P. (2003). "Hide and Seek: An Introduction to Steganography"

---

## 🔧 Troubleshooting

### Issue: "Image too small for payload"
**Solution**: Use larger cover image or reduce message length

### Issue: "Only embedded X/Y bits"
**Solution**: Lower edge_threshold to allow more blocks for embedding

### Issue: "Import errors for scipy/matplotlib"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Low PSNR (<30 dB)
**Solution**: Increase edge_threshold or use image with more texture

---

## 👥 Contributors

- **Aima Sibtain** (411885)
- **Muhammad Musfir Baig** (409968)
- **Abdullah Usama** (417872)

---

## 📄 License

Academic project for Information Security course.

---

## 🎓 Academic Context

**Course**: Information Security  
**Institution**: [Your Institution]  
**Semester**: [Your Semester]  
**Project Type**: Research Paper Reimplementation + Enhancement

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments in `adaptive_stego.py`
3. Run `python main.py` with verbose output
4. Contact project contributors

---

**Last Updated**: December 2025
