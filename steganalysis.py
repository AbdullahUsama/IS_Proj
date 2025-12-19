# steganalysis.py
"""
Steganalysis Attack Implementations

Includes:
1. RS Analysis (Regular-Singular Analysis)
2. Histogram-based Detection
3. Chi-Square Attack

These attacks help evaluate the robustness of steganographic methods.
"""

import numpy as np
import cv2
from typing import Tuple, Dict
import matplotlib.pyplot as plt


class RSAnalysis:
    """
    RS Steganalysis Attack
    
    RS analysis detects LSB steganography by analyzing the correlation
    between adjacent pixels. It measures how many pixel groups become
    'Regular' or 'Singular' after applying a mask function.
    """
    
    def __init__(self, mask_size=2):
        """
        Args:
            mask_size: Size of pixel groups (typically 2 or 4)
        """
        self.mask_size = mask_size
        
    def _flip_lsb(self, pixels):
        """Flip LSB of pixels"""
        return pixels ^ 1
    
    def _apply_mask_positive(self, group):
        """Apply positive mask: flip LSB of all pixels"""
        return self._flip_lsb(group)
    
    def _apply_mask_negative(self, group):
        """Apply negative mask: flip LSB of even-indexed pixels only"""
        result = group.copy()
        result[::2] = self._flip_lsb(result[::2])
        return result
    
    def _calculate_smoothness(self, group):
        """
        Calculate smoothness (variation) of a pixel group
        Lower variation = smoother = Regular
        Higher variation = rougher = Singular
        """
        if len(group) < 2:
            return 0
        variation = np.sum(np.abs(np.diff(group.astype(np.int32))))
        return variation
    
    def _classify_group(self, group, masked_group):
        """
        Classify group as Regular or Singular
        Regular: smoothness decreases after masking
        Singular: smoothness increases after masking
        """
        f_original = self._calculate_smoothness(group)
        f_masked = self._calculate_smoothness(masked_group)
        
        if f_masked > f_original:
            return 'S'  # Singular
        elif f_masked < f_original:
            return 'R'  # Regular
        else:
            return 'U'  # Unusable
    
    def analyze(self, image_path: str) -> Dict:
        """
        Perform RS analysis on an image
        
        Returns:
            Dict with RM, SM, RN, SN values and estimated embedding rate
        """
        # Load image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        h, w = image.shape
        pixels = image.flatten()
        
        # Counters
        RM = 0  # Regular groups with positive mask
        SM = 0  # Singular groups with positive mask
        RN = 0  # Regular groups with negative mask
        SN = 0  # Singular groups with negative mask
        total_groups = 0
        
        # Process pixel groups
        for i in range(0, len(pixels) - self.mask_size + 1, self.mask_size):
            group = pixels[i:i+self.mask_size]
            
            # Apply positive mask
            masked_pos = self._apply_mask_positive(group)
            classification_pos = self._classify_group(group, masked_pos)
            
            if classification_pos == 'R':
                RM += 1
            elif classification_pos == 'S':
                SM += 1
            
            # Apply negative mask
            masked_neg = self._apply_mask_negative(group)
            classification_neg = self._classify_group(group, masked_neg)
            
            if classification_neg == 'R':
                RN += 1
            elif classification_neg == 'S':
                SN += 1
            
            total_groups += 1
        
        # Normalize
        RM_norm = RM / total_groups if total_groups > 0 else 0
        SM_norm = SM / total_groups if total_groups > 0 else 0
        RN_norm = RN / total_groups if total_groups > 0 else 0
        SN_norm = SN / total_groups if total_groups > 0 else 0
        
        # Estimate embedding rate using RS formula
        # For ideal cover image: RM ≈ RN and SM ≈ SN
        # For stego image: |RM - RN| and |SM - SN| increase
        
        d_R = RM_norm - RN_norm
        d_S = SM_norm - SN_norm
        
        # Embedding rate estimation (simplified)
        # p ≈ |d_R| / (|d_R| + |d_S|) if data is embedded
        denominator = abs(d_R) + abs(d_S)
        embedding_rate = abs(d_R) / denominator if denominator > 0.001 else 0
        
        # Detection criterion: if embedding_rate > threshold, likely contains hidden data
        is_stego_detected = embedding_rate > 0.1
        
        return {
            'RM': RM_norm,
            'SM': SM_norm,
            'RN': RN_norm,
            'SN': SN_norm,
            'd_R': d_R,
            'd_S': d_S,
            'embedding_rate_estimate': embedding_rate,
            'stego_detected': is_stego_detected,
            'total_groups': total_groups
        }


class HistogramAnalysis:
    """
    Histogram-based Steganalysis
    
    Detects steganography by analyzing histogram patterns.
    LSB embedding creates characteristic histogram patterns.
    """
    
    def analyze(self, cover_path: str, stego_path: str) -> Dict:
        """
        Compare histograms of cover and stego images
        """
        cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        
        if cover is None or stego is None:
            raise ValueError("Cannot load images")
        
        # Calculate histograms
        hist_cover, _ = np.histogram(cover.flatten(), bins=256, range=(0, 256))
        hist_stego, _ = np.histogram(stego.flatten(), bins=256, range=(0, 256))
        
        # Normalize
        hist_cover = hist_cover.astype(np.float64) / hist_cover.sum()
        hist_stego = hist_stego.astype(np.float64) / hist_stego.sum()
        
        # Chi-square distance
        chi_square = np.sum((hist_cover - hist_stego) ** 2 / (hist_cover + hist_stego + 1e-10))
        
        # Kolmogorov-Smirnov statistic
        ks_statistic = np.max(np.abs(np.cumsum(hist_cover) - np.cumsum(hist_stego)))
        
        # Bhattacharyya distance
        bhattacharyya = -np.log(np.sum(np.sqrt(hist_cover * hist_stego)) + 1e-10)
        
        # Detection threshold (empirical)
        is_detectable = chi_square > 0.01 or ks_statistic > 0.05
        
        return {
            'chi_square': chi_square,
            'ks_statistic': ks_statistic,
            'bhattacharyya': bhattacharyya,
            'detectable': is_detectable
        }
    
    def visualize(self, cover_path: str, stego_path: str, output_path: str = None):
        """
        Visualize histogram comparison
        """
        cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Cover image
        axes[0, 0].imshow(cover, cmap='gray')
        axes[0, 0].set_title('Cover Image')
        axes[0, 0].axis('off')
        
        # Stego image
        axes[0, 1].imshow(stego, cmap='gray')
        axes[0, 1].set_title('Stego Image')
        axes[0, 1].axis('off')
        
        # Cover histogram
        axes[1, 0].hist(cover.flatten(), bins=256, range=(0, 256), color='blue', alpha=0.7)
        axes[1, 0].set_title('Cover Histogram')
        axes[1, 0].set_xlabel('Pixel Value')
        axes[1, 0].set_ylabel('Frequency')
        
        # Stego histogram
        axes[1, 1].hist(stego.flatten(), bins=256, range=(0, 256), color='red', alpha=0.7)
        axes[1, 1].set_title('Stego Histogram')
        axes[1, 1].set_xlabel('Pixel Value')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path)
            print(f"[*] Histogram visualization saved to: {output_path}")
        else:
            plt.show()


class ChiSquareAttack:
    """
    Chi-Square Attack for LSB Steganography Detection
    
    Exploits the statistical imbalance created by LSB embedding
    in pairs of values (PoVs).
    """
    
    def analyze(self, image_path: str, sample_size: int = None) -> Dict:
        """
        Perform Chi-Square attack
        
        Args:
            image_path: Path to test image
            sample_size: Number of pixels to analyze (None = all)
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        pixels = image.flatten()
        
        if sample_size:
            pixels = pixels[:sample_size]
        
        # Count frequency of each pixel value
        freq = np.bincount(pixels, minlength=256)
        
        # Chi-square test on pairs of values (PoVs)
        # PoVs are pairs (2i, 2i+1) which should have similar frequencies
        # if no data is embedded
        
        chi_square = 0
        pairs_tested = 0
        
        for i in range(0, 128):  # 128 pairs: (0,1), (2,3), ..., (254,255)
            n_2i = freq[2*i]
            n_2i_plus_1 = freq[2*i + 1]
            
            # Expected frequency if data embedded
            expected = (n_2i + n_2i_plus_1) / 2.0
            
            if expected > 0:
                chi_square += ((n_2i - expected) ** 2) / expected
                chi_square += ((n_2i_plus_1 - expected) ** 2) / expected
                pairs_tested += 1
        
        # Critical value for chi-square distribution (95% confidence, df=127)
        # If chi_square > critical value, reject null hypothesis (no embedding)
        critical_value_95 = 154.3  # Approximate for df=127
        
        is_detected = chi_square > critical_value_95
        
        # Calculate p-value approximation
        confidence = min(99.9, (chi_square / critical_value_95) * 95)
        
        return {
            'chi_square_statistic': chi_square,
            'critical_value_95': critical_value_95,
            'pairs_tested': pairs_tested,
            'stego_detected': is_detected,
            'confidence_percent': confidence
        }


def comprehensive_steganalysis(cover_path: str, stego_path: str) -> Dict:
    """
    Perform comprehensive steganalysis using multiple attacks
    """
    print("\n" + "="*60)
    print("STEGANALYSIS - ROBUSTNESS EVALUATION")
    print("="*60)
    
    results = {}
    
    # 1. RS Analysis
    print("\n[*] Running RS Analysis...")
    rs = RSAnalysis()
    try:
        rs_cover = rs.analyze(cover_path)
        rs_stego = rs.analyze(stego_path)
        results['RS_Analysis'] = {
            'cover': rs_cover,
            'stego': rs_stego
        }
        print(f"    Cover - Embedding Rate Estimate: {rs_cover['embedding_rate_estimate']:.4f}")
        print(f"    Stego - Embedding Rate Estimate: {rs_stego['embedding_rate_estimate']:.4f}")
        print(f"    Stego Detected: {rs_stego['stego_detected']}")
    except Exception as e:
        print(f"    [!] RS Analysis failed: {e}")
    
    # 2. Histogram Analysis
    print("\n[*] Running Histogram Analysis...")
    hist = HistogramAnalysis()
    try:
        hist_results = hist.analyze(cover_path, stego_path)
        results['Histogram_Analysis'] = hist_results
        print(f"    Chi-Square Distance: {hist_results['chi_square']:.6f}")
        print(f"    KS Statistic: {hist_results['ks_statistic']:.6f}")
        print(f"    Detectable: {hist_results['detectable']}")
    except Exception as e:
        print(f"    [!] Histogram Analysis failed: {e}")
    
    # 3. Chi-Square Attack
    print("\n[*] Running Chi-Square Attack...")
    chi_attack = ChiSquareAttack()
    try:
        chi_cover = chi_attack.analyze(cover_path)
        chi_stego = chi_attack.analyze(stego_path)
        results['ChiSquare_Attack'] = {
            'cover': chi_cover,
            'stego': chi_stego
        }
        print(f"    Cover - Chi-Square: {chi_cover['chi_square_statistic']:.2f}")
        print(f"    Stego - Chi-Square: {chi_stego['chi_square_statistic']:.2f}")
        print(f"    Stego Detected: {chi_stego['stego_detected']}")
    except Exception as e:
        print(f"    [!] Chi-Square Attack failed: {e}")
    
    print("\n" + "="*60)
    print("STEGANALYSIS SUMMARY")
    print("="*60)
    
    # Overall assessment
    detection_count = 0
    total_tests = 0
    
    if 'RS_Analysis' in results:
        total_tests += 1
        if results['RS_Analysis']['stego']['stego_detected']:
            detection_count += 1
            print("⚠ RS Analysis: DETECTED")
        else:
            print("✓ RS Analysis: NOT DETECTED (good)")
    
    if 'Histogram_Analysis' in results:
        total_tests += 1
        if results['Histogram_Analysis']['detectable']:
            detection_count += 1
            print("⚠ Histogram Analysis: DETECTABLE")
        else:
            print("✓ Histogram Analysis: LOW DETECTABILITY (good)")
    
    if 'ChiSquare_Attack' in results:
        total_tests += 1
        if results['ChiSquare_Attack']['stego']['stego_detected']:
            detection_count += 1
            print("⚠ Chi-Square Attack: DETECTED")
        else:
            print("✓ Chi-Square Attack: NOT DETECTED (good)")
    
    print("\n" + "-"*60)
    print(f"Overall Detection Rate: {detection_count}/{total_tests} tests detected embedding")
    
    if detection_count == 0:
        print("✓ EXCELLENT: No attacks detected the steganography")
    elif detection_count <= total_tests // 2:
        print("✓ GOOD: Majority of attacks failed to detect")
    else:
        print("⚠ MODERATE: Multiple attacks detected the embedding")
    
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    # Example usage
    cover = "media/tyla.jpg"
    stego = "media/adaptive_stego_image.png"
    
    if __name__ == "__main__":
        import os
        if os.path.exists(cover) and os.path.exists(stego):
            results = comprehensive_steganalysis(cover, stego)
        else:
            print("Please run main.py first to generate stego images")
