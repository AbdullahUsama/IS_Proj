import cv2
import numpy as np
import math
from typing import Tuple, Dict


def calculate_mse(original, stego):
    """Calculate Mean Squared Error between two images"""
    original = original.astype(np.float64)
    stego = stego.astype(np.float64)
    mse = np.mean((original - stego) ** 2)
    return mse


def calculate_psnr(original, stego):
    """Calculate Peak Signal-to-Noise Ratio"""
    mse = calculate_mse(original, stego)
    if mse == 0:
        return float('inf')
    MAX = 255.0
    psnr = 10 * math.log10((MAX * MAX) / mse)
    return psnr


def calculate_entropy(image):
    """
    Calculate Shannon entropy of an image
    Higher entropy indicates more randomness/information
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate histogram
    hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 256))
    
    # Normalize to get probability distribution
    hist = hist / hist.sum()
    
    # Remove zero entries
    hist = hist[hist > 0]
    
    # Calculate entropy
    ent = -np.sum(hist * np.log2(hist))
    return ent


def calculate_capacity(payload_bits: int, image_shape: Tuple[int, int]) -> float:
    """
    Calculate embedding capacity in bits per pixel (bpp)
    """
    total_pixels = image_shape[0] * image_shape[1]
    capacity_bpp = payload_bits / total_pixels
    return capacity_bpp


def calculate_histogram_deviation(original, stego):
    """
    Calculate histogram deviation between original and stego images
    Lower deviation indicates better resistance to histogram-based detection
    """
    if len(original.shape) == 3:
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    if len(stego.shape) == 3:
        stego = cv2.cvtColor(stego, cv2.COLOR_BGR2GRAY)
    
    # Calculate histograms
    hist_orig, _ = np.histogram(original.flatten(), bins=256, range=(0, 256))
    hist_stego, _ = np.histogram(stego.flatten(), bins=256, range=(0, 256))
    
    # Normalize
    hist_orig = hist_orig.astype(np.float64) / hist_orig.sum()
    hist_stego = hist_stego.astype(np.float64) / hist_stego.sum()
    
    # Calculate Chi-square distance
    chi_square = np.sum((hist_orig - hist_stego) ** 2 / (hist_orig + hist_stego + 1e-10))
    
    return chi_square


def comprehensive_evaluation(original_path: str, stego_path: str, 
                            payload_bits: int = None) -> Dict:
    """
    Perform comprehensive evaluation of steganography quality
    
    Returns dict with all metrics: PSNR, MSE, Entropy, Capacity, Histogram Deviation
    """
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
    
    if original is None:
        raise ValueError(f"Could not load original image: {original_path}")
    if stego is None:
        raise ValueError(f"Could not load stego image: {stego_path}")
    if original.shape != stego.shape:
        raise ValueError("Images must have the same dimensions")
    
    # Calculate all metrics
    mse_value = calculate_mse(original, stego)
    psnr_value = calculate_psnr(original, stego)
    entropy_orig = calculate_entropy(original)
    entropy_stego = calculate_entropy(stego)
    hist_deviation = calculate_histogram_deviation(original, stego)
    
    results = {
        'MSE': mse_value,
        'PSNR': psnr_value,
        'Entropy_Original': entropy_orig,
        'Entropy_Stego': entropy_stego,
        'Entropy_Difference': abs(entropy_stego - entropy_orig),
        'Histogram_Deviation': hist_deviation,
    }
    
    if payload_bits is not None:
        capacity = calculate_capacity(payload_bits, original.shape)
        results['Capacity_bpp'] = capacity
    
    return results


def print_evaluation_results(results: Dict, title: str = "Evaluation Results"):
    """Pretty print evaluation results"""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)
    print(f"MSE (Mean Squared Error):      {results['MSE']:.4f}")
    print(f"PSNR (Peak SNR):               {results['PSNR']:.2f} dB")
    print(f"Entropy (Original):            {results['Entropy_Original']:.4f} bits")
    print(f"Entropy (Stego):               {results['Entropy_Stego']:.4f} bits")
    print(f"Entropy Difference:            {results['Entropy_Difference']:.4f} bits")
    print(f"Histogram Deviation:           {results['Histogram_Deviation']:.6f}")
    
    if 'Capacity_bpp' in results:
        print(f"Capacity:                      {results['Capacity_bpp']:.4f} bpp")
    
    print("="*60)
    
    # Interpretation
    print("\nInterpretation:")
    if results['PSNR'] > 40:
        print("✓ PSNR: Excellent quality (>40 dB) - imperceptible changes")
    elif results['PSNR'] > 30:
        print("✓ PSNR: Good quality (30-40 dB) - minimal visible changes")
    else:
        print("⚠ PSNR: Fair quality (<30 dB) - changes may be noticeable")
    
    if results['Histogram_Deviation'] < 0.01:
        print("✓ Histogram: Excellent - very low statistical deviation")
    elif results['Histogram_Deviation'] < 0.05:
        print("✓ Histogram: Good - acceptable statistical similarity")
    else:
        print("⚠ Histogram: Moderate - statistical changes may be detectable")
    
    if results['Entropy_Difference'] < 0.1:
        print("✓ Entropy: Excellent - randomness preserved")
    elif results['Entropy_Difference'] < 0.3:
        print("✓ Entropy: Good - acceptable randomness change")
    else:
        print("⚠ Entropy: Moderate - noticeable change in information content")
    
    print("="*60 + "\n")


def psnr_for_images(original_path, stego_path):
    """Legacy function for backward compatibility"""
    try:
        results = comprehensive_evaluation(original_path, stego_path)
        print(f"PSNR between {original_path} and {stego_path}: {results['PSNR']:.4f} dB")
    except ValueError as e:
        print(f"Error: {e}")
