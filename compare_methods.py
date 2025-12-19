# compare_methods.py
"""
Comparison Script: Basic LSB vs Adaptive LSB-MSB vs Edge-Enhanced

This script compares three steganographic methods:
1. Basic LSB (sequential embedding)
2. Adaptive LSB-MSB (research paper)
3. Edge-Enhanced Adaptive (our improvement)
"""

import sys
import os
from AESCTR import aes_ctr_encrypt, aes_ctr_decrypt
from steno import SteganographyLSB
from adaptive_stego import AdaptiveSteganography
from metricscalc import comprehensive_evaluation, print_evaluation_results
from steganalysis import comprehensive_steganalysis


def compare_methods(cover_image: str, secret_message: str):
    """
    Compare three steganographic methods on the same message
    """
    print("\n" + "="*70)
    print(" STEGANOGRAPHY METHODS COMPARISON ".center(70, "="))
    print("="*70)
    print(f"\nCover Image: {cover_image}")
    print(f"Message Length: {len(secret_message)} characters")
    print("="*70)
    
    # Encrypt message once (same for all methods)
    print("\n[*] Encrypting message with AES-CTR...")
    key, nonce, ciphertext = aes_ctr_encrypt(secret_message.encode())
    payload_bytes = nonce + ciphertext
    
    results = {}
    
    # ========== METHOD 1: Basic LSB ==========
    print("\n" + "="*70)
    print(" METHOD 1: BASIC LSB STEGANOGRAPHY ".center(70, "="))
    print("="*70)
    
    try:
        output_basic = "media/comparison_basic_lsb.png"
        stego_basic = SteganographyLSB()
        
        # Encode with base64 for basic LSB
        import base64
        data_to_hide = base64.b64encode(payload_bytes).decode('utf-8')
        
        stego_basic.encode(cover_image, output_basic, data_to_hide, password="test")
        print("[✓] Basic LSB embedding complete")
        
        # Evaluate
        eval_basic = comprehensive_evaluation(cover_image, output_basic, 
                                               payload_bits=len(payload_bytes)*8)
        print_evaluation_results(eval_basic, "Basic LSB Steganography")
        
        results['basic_lsb'] = {
            'output': output_basic,
            'metrics': eval_basic,
            'method': 'Sequential LSB'
        }
        
    except Exception as e:
        print(f"[!] Basic LSB failed: {e}")
        results['basic_lsb'] = {'error': str(e)}
    
    # ========== METHOD 2: Adaptive LSB-MSB (No Edge) ==========
    print("\n" + "="*70)
    print(" METHOD 2: ADAPTIVE LSB-MSB (Research Paper) ".center(70, "="))
    print("="*70)
    
    try:
        output_adaptive = "media/comparison_adaptive.png"
        stego_adaptive = AdaptiveSteganography(block_size=8, edge_threshold=10)  # Low threshold = more blocks
        
        metadata_adaptive = stego_adaptive.encode(cover_image, output_adaptive, payload_bytes)
        print("[✓] Adaptive LSB-MSB embedding complete")
        print(f"[*] Capacity: {metadata_adaptive['capacity_bpp']:.4f} bpp")
        
        # Evaluate
        eval_adaptive = comprehensive_evaluation(cover_image, output_adaptive,
                                                  payload_bits=len(payload_bytes)*8)
        print_evaluation_results(eval_adaptive, "Adaptive LSB-MSB")
        
        results['adaptive'] = {
            'output': output_adaptive,
            'metrics': eval_adaptive,
            'metadata': metadata_adaptive,
            'method': 'Adaptive MSB-based'
        }
        
    except Exception as e:
        print(f"[!] Adaptive LSB-MSB failed: {e}")
        results['adaptive'] = {'error': str(e)}
    
    # ========== METHOD 3: Edge-Enhanced Adaptive ==========
    print("\n" + "="*70)
    print(" METHOD 3: EDGE-ENHANCED ADAPTIVE (Our Improvement) ".center(70, "="))
    print("="*70)
    
    try:
        output_edge = "media/comparison_edge_enhanced.png"
        stego_edge = AdaptiveSteganography(block_size=8, edge_threshold=30)  # Higher threshold = only edges
        
        metadata_edge = stego_edge.encode(cover_image, output_edge, payload_bytes)
        print("[✓] Edge-enhanced embedding complete")
        print(f"[*] Capacity: {metadata_edge['capacity_bpp']:.4f} bpp")
        
        # Evaluate
        eval_edge = comprehensive_evaluation(cover_image, output_edge,
                                             payload_bits=len(payload_bytes)*8)
        print_evaluation_results(eval_edge, "Edge-Enhanced Adaptive")
        
        results['edge_enhanced'] = {
            'output': output_edge,
            'metrics': eval_edge,
            'metadata': metadata_edge,
            'method': 'Edge-adaptive MSB-based'
        }
        
    except Exception as e:
        print(f"[!] Edge-enhanced failed: {e}")
        results['edge_enhanced'] = {'error': str(e)}
    
    # ========== COMPARISON TABLE ==========
    print("\n" + "="*70)
    print(" COMPARISON SUMMARY ".center(70, "="))
    print("="*70)
    
    print("\n{:<25} {:<15} {:<15} {:<15}".format(
        "Metric", "Basic LSB", "Adaptive", "Edge-Enhanced"
    ))
    print("-"*70)
    
    metrics_to_compare = ['PSNR', 'MSE', 'Entropy_Difference', 'Histogram_Deviation']
    
    for metric in metrics_to_compare:
        row = f"{metric:<25}"
        
        for method in ['basic_lsb', 'adaptive', 'edge_enhanced']:
            if method in results and 'metrics' in results[method]:
                val = results[method]['metrics'].get(metric, 'N/A')
                if isinstance(val, (int, float)):
                    if metric == 'PSNR':
                        row += f"{val:>14.2f} "
                    else:
                        row += f"{val:>14.4f} "
                else:
                    row += f"{str(val):>15}"
            else:
                row += f"{'ERROR':>15}"
        
        print(row)
    
    # Capacity comparison
    print("-"*70)
    row = f"{'Capacity (bpp)':<25}"
    for method in ['basic_lsb', 'adaptive', 'edge_enhanced']:
        if method in results and 'metrics' in results[method]:
            val = results[method]['metrics'].get('Capacity_bpp', 'N/A')
            if isinstance(val, (int, float)):
                row += f"{val:>14.4f} "
            else:
                row += f"{str(val):>15}"
        else:
            row += f"{'N/A':>15}"
    print(row)
    
    print("="*70)
    
    # ========== STEGANALYSIS COMPARISON ==========
    print("\n" + "="*70)
    print(" STEGANALYSIS RESISTANCE COMPARISON ".center(70, "="))
    print("="*70)
    
    for method_name, method_key in [
        ("Basic LSB", "basic_lsb"),
        ("Adaptive LSB-MSB", "adaptive"),
        ("Edge-Enhanced", "edge_enhanced")
    ]:
        if method_key in results and 'output' in results[method_key]:
            print(f"\n[*] Testing {method_name}...")
            try:
                steg_results = comprehensive_steganalysis(
                    cover_image, 
                    results[method_key]['output']
                )
                results[method_key]['steganalysis'] = steg_results
            except Exception as e:
                print(f"[!] Steganalysis failed: {e}")
    
    # ========== RECOMMENDATIONS ==========
    print("\n" + "="*70)
    print(" RECOMMENDATIONS ".center(70, "="))
    print("="*70)
    
    print("\n📊 Quality Analysis:")
    
    # Best PSNR
    psnr_values = {}
    for method in ['basic_lsb', 'adaptive', 'edge_enhanced']:
        if method in results and 'metrics' in results[method]:
            psnr_values[method] = results[method]['metrics'].get('PSNR', 0)
    
    if psnr_values:
        best_psnr = max(psnr_values, key=psnr_values.get)
        method_names = {
            'basic_lsb': 'Basic LSB',
            'adaptive': 'Adaptive LSB-MSB',
            'edge_enhanced': 'Edge-Enhanced'
        }
        print(f"✓ Best Quality (PSNR): {method_names[best_psnr]} ({psnr_values[best_psnr]:.2f} dB)")
    
    # Histogram deviation
    hist_values = {}
    for method in ['basic_lsb', 'adaptive', 'edge_enhanced']:
        if method in results and 'metrics' in results[method]:
            hist_values[method] = results[method]['metrics'].get('Histogram_Deviation', 999)
    
    if hist_values:
        best_hist = min(hist_values, key=hist_values.get)
        print(f"✓ Best Stealth (Histogram): {method_names[best_hist]} ({hist_values[best_hist]:.6f})")
    
    print("\n🎯 Use Case Recommendations:")
    print("• Basic LSB: Simple messages, high capacity needed")
    print("• Adaptive LSB-MSB: Better quality than basic LSB")
    print("• Edge-Enhanced: Maximum security and imperceptibility")
    
    print("\n⚠️ Trade-offs:")
    print("• Basic LSB: High capacity, moderate detectability")
    print("• Adaptive: Balanced capacity and quality")
    print("• Edge-Enhanced: Lower capacity, best stealth")
    
    print("\n" + "="*70)
    print(" COMPARISON COMPLETE ".center(70, "="))
    print("="*70)
    
    return results


if __name__ == "__main__":
    # Configuration
    DEFAULT_IMAGE = "media/landscape.jpg"
    DEFAULT_MESSAGE = "This is a test message for comparison analysis!"
    
    # Check if cover image exists
    if not os.path.exists(DEFAULT_IMAGE):
        print(f"[!] Error: Cover image not found: {DEFAULT_IMAGE}")
        print("[*] Please place an image at the specified path")
        sys.exit(1)
    
    # Get message
    print("\n[?] Enter secret message (or press Enter for default):")
    message = input(">>> ").strip()
    
    if not message:
        message = DEFAULT_MESSAGE
        print(f"[*] Using default message: {message}")
    
    # Run comparison
    try:
        results = compare_methods(DEFAULT_IMAGE, message)
        
        print("\n[✓] Comparison complete!")
        print(f"[*] Output images saved in media/ directory:")
        print(f"    - media/comparison_basic_lsb.png")
        print(f"    - media/comparison_adaptive.png")
        print(f"    - media/comparison_edge_enhanced.png")
        
    except Exception as e:
        print(f"\n[!] Error during comparison: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
