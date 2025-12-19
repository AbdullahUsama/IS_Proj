# QUICK_START_GUIDE.md

## 🚀 Quick Start Guide

### Prerequisites

```bash
# Python 3.8 or higher required
python --version

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Basic Usage

### 1. Run the Enhanced System

```bash
python main.py
```

**Interactive Prompts**:
```
Enter the secret message to hide:
>>> My secret message

Edge threshold (10-50, default 30):
>>> 30
```

**Output**:
- Encrypted message with AES-CTR
- Embedded using adaptive LSB-MSB + edge enhancement
- Comprehensive quality metrics (PSNR, MSE, Entropy, etc.)
- Extracted and decrypted message verification

---

### 2. Run Steganalysis Tests

```bash
python run_steganalysis.py media/tyla.jpg media/adaptive_stego_image.png
```

**Tests Performed**:
- RS Analysis (Regular-Singular)
- Histogram Analysis (Chi-square, KS statistic)
- Chi-Square Attack (PoV detection)

---

### 3. Compare with Basic LSB

When running `main.py`, answer 'y' when prompted:
```
Compare with basic LSB method? (y/n):
>>> y
```

**Comparison Shows**:
- Basic LSB metrics vs Adaptive method
- Quality differences
- Capacity trade-offs

---

## 🔧 Advanced Usage

### Programmatic Access

#### Example 1: Basic Embedding

```python
from adaptive_stego import AdaptiveSteganography
from AESCTR import aes_ctr_encrypt, aes_ctr_decrypt

# Prepare payload
message = "Confidential information"
key, nonce, ciphertext = aes_ctr_encrypt(message.encode())
payload = nonce + ciphertext

# Embed
stego = AdaptiveSteganography(block_size=8, edge_threshold=30)
metadata = stego.encode("cover.jpg", "stego.png", payload)

print(f"Capacity: {metadata['capacity_bpp']:.4f} bpp")
print(f"Blocks used: {metadata['blocks_used']}")
```

#### Example 2: Extraction

```python
# Extract
extracted = stego.decode("stego.png")
nonce_ex = extracted[:8]
cipher_ex = extracted[8:]

# Decrypt
decrypted = aes_ctr_decrypt(cipher_ex, key, nonce_ex)
print(decrypted.decode())
```

#### Example 3: Custom Evaluation

```python
from metricscalc import comprehensive_evaluation, print_evaluation_results

results = comprehensive_evaluation(
    "cover.jpg", 
    "stego.png",
    payload_bits=1024
)

print_evaluation_results(results, "My Evaluation")
```

#### Example 4: Steganalysis

```python
from steganalysis import RSAnalysis, HistogramAnalysis, ChiSquareAttack

# RS Analysis
rs = RSAnalysis()
rs_results = rs.analyze("stego.png")
print(f"Embedding rate: {rs_results['embedding_rate_estimate']:.4f}")

# Histogram Analysis
hist = HistogramAnalysis()
hist_results = hist.analyze("cover.jpg", "stego.png")
print(f"Chi-square: {hist_results['chi_square']:.6f}")

# Chi-Square Attack
chi = ChiSquareAttack()
chi_results = chi.analyze("stego.png")
print(f"Detected: {chi_results['stego_detected']}")
```

---

## ⚙️ Configuration Options

### Edge Threshold Settings

| Threshold | Effect | Use Case |
|-----------|--------|----------|
| **10-20** | More blocks, higher capacity | Large payloads |
| **25-35** | Balanced (default: 30) | General use |
| **40-50** | Fewer blocks, better quality | Maximum security |

### Block Size (Advanced)

```python
# Default: 8x8 (recommended)
stego = AdaptiveSteganography(block_size=8)

# Larger blocks (experimental)
stego = AdaptiveSteganography(block_size=16)  # Lower capacity
```

---

## 📊 Understanding Metrics

### PSNR (Peak Signal-to-Noise Ratio)

```
>50 dB = Excellent (imperceptible)
40-50 dB = Good (minimal changes)
30-40 dB = Fair (some visible changes)
<30 dB = Poor (obvious changes)
```

### Histogram Deviation

```
<0.01 = Excellent (undetectable)
0.01-0.05 = Good (low detectability)
>0.05 = Moderate (may be detected)
```

### Entropy Difference

```
<0.1 = Excellent (randomness preserved)
0.1-0.3 = Good (acceptable change)
>0.3 = Moderate (noticeable change)
```

---

## 🎯 Use Case Examples

### Use Case 1: Confidential Message

**Scenario**: Hide a short confidential message

```python
# main.py
Enter the secret message to hide:
>>> Meeting at 3pm, Project Alpha

Edge threshold: 35  # High security
```

**Expected Results**:
- PSNR: >52 dB
- Capacity: 0.3-0.4 bpp
- RS Detection: Not detected

---

### Use Case 2: Large Data Payload

**Scenario**: Embed longer text or small file

```python
# Read file
with open("data.txt", "rb") as f:
    data = f.read()

# Encrypt
key, nonce, ciphertext = aes_ctr_encrypt(data)
payload = nonce + ciphertext

# Use lower threshold for capacity
stego = AdaptiveSteganography(edge_threshold=20)
metadata = stego.encode("large_image.jpg", "stego.png", payload)
```

**Requirements**:
- Use high-resolution cover image (>1500x1500)
- Lower edge threshold (20-25)
- Accept PSNR ~45-50 dB

---

### Use Case 3: Multiple Messages

**Scenario**: Embed different messages in different images

```python
messages = [
    "Message 1 for image A",
    "Message 2 for image B",
    "Message 3 for image C"
]

covers = ["img1.jpg", "img2.jpg", "img3.jpg"]
keys = []

for msg, cover in zip(messages, covers):
    key, nonce, cipher = aes_ctr_encrypt(msg.encode())
    payload = nonce + cipher
    
    stego = AdaptiveSteganography(edge_threshold=30)
    output = f"stego_{covers.index(cover)}.png"
    stego.encode(cover, output, payload)
    
    keys.append(key)  # Store for later decryption

# Save keys securely
import pickle
with open("keys.pkl", "wb") as f:
    pickle.dump(keys, f)
```

---

## 🐛 Troubleshooting

### Problem: "Image too small for payload"

**Cause**: Cover image doesn't have enough edge regions

**Solutions**:
1. Use larger cover image
2. Reduce message length
3. Lower edge_threshold (e.g., 20)
4. Choose more textured image

---

### Problem: Low PSNR (<40 dB)

**Cause**: Too much data embedded

**Solutions**:
1. Increase edge_threshold
2. Reduce payload size
3. Use higher resolution image

---

### Problem: "Only embedded X/Y bits"

**Cause**: Insufficient embedding capacity

**Solutions**:
1. Lower edge_threshold (more blocks available)
2. Use larger image
3. Compress message before encrypting

---

### Problem: Steganalysis detects embedding

**Cause**: Large payload or low edge threshold

**Solutions**:
1. Increase edge_threshold (use stronger edges)
2. Reduce payload size
3. Use more textured cover image
4. Verify AES encryption is applied

---

## 📁 File Structure Reference

```
IS_Proj/
├── main.py                      # Main program (start here)
├── adaptive_stego.py            # Adaptive LSB-MSB algorithm
├── AESCTR.py                    # AES-CTR encryption
├── steno.py                     # Basic LSB (for comparison)
├── metricscalc.py              # Quality metrics
├── steganalysis.py             # Attack implementations
├── run_steganalysis.py         # Standalone steganalysis
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── IMPLEMENTATION_ANALYSIS.md  # Technical analysis
└── media/
    ├── tyla.jpg               # Example cover image
    └── adaptive_stego_image.png  # Generated stego
```

---

## 🔑 Key Management

### Storing Keys Securely

```python
import pickle

# Save key after embedding
with open("secret.key", "wb") as f:
    pickle.dump(aes_key, f)

# Load key for extraction
with open("secret.key", "rb") as f:
    aes_key = pickle.load(f)
```

**Security Note**: Never embed key in the stego image!

---

## 📞 Getting Help

1. **Check README.md** for comprehensive documentation
2. **Review IMPLEMENTATION_ANALYSIS.md** for technical details
3. **Run with verbose output** to see detailed logs
4. **Check code comments** in `adaptive_stego.py`

---

## ✅ Verification Checklist

Before using in production:

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Cover image exists and is high-quality
- [ ] Message encrypted with AES-CTR
- [ ] PSNR > 40 dB after embedding
- [ ] Extraction recovers original message
- [ ] Steganalysis tests run successfully
- [ ] Keys stored securely

---

## 🎓 Learning Path

1. **Start**: Run `python main.py` with a simple message
2. **Understand**: Review quality metrics output
3. **Experiment**: Try different edge_threshold values
4. **Evaluate**: Run `run_steganalysis.py` to test robustness
5. **Compare**: Enable basic LSB comparison
6. **Advanced**: Use programmatic API for custom workflows

---

**Happy Steganography!** 🎉

For questions, refer to README.md or contact project contributors.
