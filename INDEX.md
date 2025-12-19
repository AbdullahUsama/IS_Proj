# 📚 PROJECT INDEX

## Quick Navigation Guide

### 🚀 Getting Started

1. **First Time Users**: Start here → [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
2. **Complete Documentation**: Read → [README.md](README.md)
3. **Technical Details**: Explore → [IMPLEMENTATION_ANALYSIS.md](IMPLEMENTATION_ANALYSIS.md)
4. **Project Summary**: Review → [SUMMARY.md](SUMMARY.md)

---

## 📁 File Directory

### 🎮 Main Programs (Start Here!)

| File | Purpose | Usage |
|------|---------|-------|
| [main.py](main.py) | Main interactive program | `python main.py` |
| [run_steganalysis.py](run_steganalysis.py) | Standalone steganalysis | `python run_steganalysis.py cover.jpg stego.png` |
| [compare_methods.py](compare_methods.py) | Compare 3 methods | `python compare_methods.py` |

### 🔧 Core Implementation

| File | Description | Key Features |
|------|-------------|--------------|
| [adaptive_stego.py](adaptive_stego.py) | **Adaptive LSB-MSB Algorithm** | • 8×8 blocks<br>• UB/LB embedding<br>• Mean-of-medians<br>• Edge-adaptive |
| [AESCTR.py](AESCTR.py) | **AES-CTR Encryption** | • AES-256<br>• Random keys<br>• CTR mode |
| [metricscalc.py](metricscalc.py) | **Quality Metrics** | • PSNR, MSE<br>• Entropy<br>• Histogram deviation |
| [steganalysis.py](steganalysis.py) | **Attack Implementations** | • RS Analysis<br>• Histogram<br>• Chi-Square |

### 📖 Documentation

| File | Content | Best For |
|------|---------|----------|
| [README.md](README.md) | Complete user guide (70+ sections) | Understanding the system |
| [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) | Quick reference & examples | Getting started quickly |
| [IMPLEMENTATION_ANALYSIS.md](IMPLEMENTATION_ANALYSIS.md) | Technical deep-dive | Understanding the implementation |
| [SUMMARY.md](SUMMARY.md) | Project completion report | Overview of deliverables |
| [INDEX.md](INDEX.md) | This file | Navigation |

### 📦 Configuration

| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies |

### 🗃️ Legacy (For Comparison)

| File | Purpose |
|------|---------|
| [steno.py](steno.py) | Basic LSB steganography (kept for comparison) |

---

## 🎯 Common Tasks

### Task 1: Hide a Message
```bash
python main.py
# Follow prompts to enter message and settings
```

### Task 2: Test Robustness
```bash
python run_steganalysis.py media/tyla.jpg media/adaptive_stego_image.png
```

### Task 3: Compare Methods
```bash
python compare_methods.py
# Compares Basic LSB vs Adaptive vs Edge-Enhanced
```

### Task 4: Understand the Algorithm
Read: [IMPLEMENTATION_ANALYSIS.md](IMPLEMENTATION_ANALYSIS.md) → Section "Adaptive LSB-MSB Algorithm"

### Task 5: Troubleshoot Issues
Read: [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) → Section "🐛 Troubleshooting"

---

## 📊 Documentation Map

### For Different Audiences

#### 👨‍💻 Developers
**Path**: README.md → IMPLEMENTATION_ANALYSIS.md → Code files
- Start with README for overview
- Read IMPLEMENTATION_ANALYSIS for technical details
- Review code with comments

#### 👩‍🎓 Students/Researchers
**Path**: SUMMARY.md → README.md → Research paper comparison
- SUMMARY.md for project overview
- README.md for algorithm explanation
- Compare with original research paper

#### 🚀 Quick Users
**Path**: QUICK_START_GUIDE.md → main.py
- QUICK_START_GUIDE for immediate usage
- Run main.py for interactive experience

#### 🔬 Evaluators
**Path**: SUMMARY.md → Run all programs → IMPLEMENTATION_ANALYSIS.md
- SUMMARY.md for completion status
- Test all programs (main, steganalysis, compare)
- IMPLEMENTATION_ANALYSIS for technical verification

---

## 🗂️ Code Organization

### Module Dependencies

```
main.py
├── AESCTR.py (encryption)
├── adaptive_stego.py (steganography)
└── metricscalc.py (evaluation)

run_steganalysis.py
└── steganalysis.py (attacks)

compare_methods.py
├── AESCTR.py
├── steno.py (basic LSB)
├── adaptive_stego.py
├── metricscalc.py
└── steganalysis.py

adaptive_stego.py
├── numpy (numerical)
└── cv2 (image processing)

steganalysis.py
├── numpy
├── cv2
└── matplotlib (visualization)
```

### Class Hierarchy

```
AdaptiveSteganography (adaptive_stego.py)
├── _compute_edge_map()
├── _partition_into_blocks()
├── _compute_mean_of_medians()
├── _get_embedding_case()
├── _embed_bits_in_pixel_pair()
├── _extract_bits_from_pixel_pair()
├── encode()
└── decode()

RSAnalysis (steganalysis.py)
├── _flip_lsb()
├── _calculate_smoothness()
├── _classify_group()
└── analyze()

HistogramAnalysis (steganalysis.py)
├── analyze()
└── visualize()

ChiSquareAttack (steganalysis.py)
└── analyze()
```

---

## 🎓 Learning Path

### Beginner Path
1. Read [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
2. Run `python main.py`
3. Experiment with different messages
4. Read [README.md](README.md) - "How it Works" section

### Intermediate Path
1. Understand research paper algorithm
2. Read [IMPLEMENTATION_ANALYSIS.md](IMPLEMENTATION_ANALYSIS.md)
3. Run `python compare_methods.py`
4. Analyze output metrics

### Advanced Path
1. Study code implementation in [adaptive_stego.py](adaptive_stego.py)
2. Run steganalysis tests
3. Modify edge_threshold and observe effects
4. Experiment with different images

---

## 📋 Feature Checklist

### Core Features ✅
- [x] 8×8 block decomposition
- [x] UB/LB embedding
- [x] Mean-of-medians computation
- [x] MSB-based cases (0-3)
- [x] Adaptive bit embedding
- [x] AES-CTR encryption
- [x] Edge-adaptive enhancement

### Evaluation Features ✅
- [x] PSNR calculation
- [x] MSE calculation
- [x] Entropy measurement
- [x] Capacity analysis
- [x] Histogram deviation
- [x] RS Analysis
- [x] Histogram-based detection
- [x] Chi-Square attack

### Usability Features ✅
- [x] Interactive CLI
- [x] Error handling
- [x] Progress logging
- [x] Result interpretation
- [x] Comparison tools

### Documentation ✅
- [x] User guide (README.md)
- [x] Quick start (QUICK_START_GUIDE.md)
- [x] Technical analysis (IMPLEMENTATION_ANALYSIS.md)
- [x] Project summary (SUMMARY.md)
- [x] Code comments
- [x] Navigation guide (this file)

---

## 🔍 Finding Specific Information

### "How do I...?"

| Question | Answer Location |
|----------|----------------|
| Install dependencies? | QUICK_START_GUIDE.md → Prerequisites |
| Run the program? | QUICK_START_GUIDE.md → Basic Usage |
| Understand the algorithm? | README.md → Technical Implementation |
| Fix errors? | QUICK_START_GUIDE.md → Troubleshooting |
| Compare methods? | Run compare_methods.py |
| Evaluate robustness? | Run run_steganalysis.py |
| Use programmatically? | QUICK_START_GUIDE.md → Advanced Usage |
| Understand metrics? | README.md → Evaluation Metrics |

### "Where is...?"

| Looking For | File Location |
|-------------|--------------|
| Research paper implementation | adaptive_stego.py |
| Encryption code | AESCTR.py |
| Quality metrics | metricscalc.py |
| Attack implementations | steganalysis.py |
| Main program | main.py |
| Examples | QUICK_START_GUIDE.md |
| Technical details | IMPLEMENTATION_ANALYSIS.md |
| Algorithm explanation | README.md + IMPLEMENTATION_ANALYSIS.md |

---

## 📈 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Files** | 13 (8 code + 5 docs) |
| **Total Lines of Code** | ~3,450 |
| **Documentation Words** | ~10,000+ |
| **Functions/Classes** | 30+ |
| **Features Implemented** | 20+ |
| **Metrics Tracked** | 7 |
| **Attacks Implemented** | 3 |

---

## 🏆 Key Files by Importance

### Must Read
1. [README.md](README.md) - Start here for complete overview
2. [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Quick reference

### Core Implementation
3. [adaptive_stego.py](adaptive_stego.py) - Main algorithm
4. [main.py](main.py) - Program entry point

### Evaluation
5. [metricscalc.py](metricscalc.py) - Quality metrics
6. [steganalysis.py](steganalysis.py) - Security testing

### Technical Deep-Dive
7. [IMPLEMENTATION_ANALYSIS.md](IMPLEMENTATION_ANALYSIS.md) - For researchers

---

## 🎯 Recommended Reading Order

### For First-Time Users:
1. INDEX.md (this file) - 5 min
2. QUICK_START_GUIDE.md - 10 min
3. Run main.py - 5 min
4. README.md - 20 min

### For Technical Review:
1. SUMMARY.md - 10 min
2. IMPLEMENTATION_ANALYSIS.md - 30 min
3. Code files with comments - 60 min

### For Academic Evaluation:
1. SUMMARY.md - Project completion
2. README.md - Algorithm overview
3. IMPLEMENTATION_ANALYSIS.md - Technical verification
4. Run all programs - Practical verification

---

## 📞 Need Help?

1. **Quick answers**: Check QUICK_START_GUIDE.md → Troubleshooting
2. **Understanding concepts**: Read README.md → specific section
3. **Technical details**: See IMPLEMENTATION_ANALYSIS.md
4. **Code questions**: Review code comments in relevant file
5. **Usage examples**: See QUICK_START_GUIDE.md → Advanced Usage

---

## ✅ Project Completion Status

**Status**: ✅ COMPLETE

All components implemented, tested, and documented.

---

**Last Updated**: December 19, 2025  
**Version**: 1.0  
**Authors**: Aima Sibtain, Muhammad Musfir Baig, Abdullah Usama

---

[Back to README](README.md) | [Quick Start](QUICK_START_GUIDE.md) | [Technical Analysis](IMPLEMENTATION_ANALYSIS.md)
