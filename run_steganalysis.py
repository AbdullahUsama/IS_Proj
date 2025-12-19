# run_steganalysis.py
"""
Standalone Steganalysis Runner

Run comprehensive steganalysis tests on cover and stego images
to evaluate the robustness of the steganographic method.
"""

import sys
import os
from steganalysis import comprehensive_steganalysis, HistogramAnalysis

def main():
    print("\n" + "="*70)
    print(" STEGANALYSIS EVALUATION TOOL ".center(70, "="))
    print("="*70)
    print("\nThis tool evaluates steganographic robustness using:")
    print("  • RS Analysis (Regular-Singular)")
    print("  • Histogram-based Detection")
    print("  • Chi-Square Attack")
    print("="*70)
    
    # Get file paths
    if len(sys.argv) >= 3:
        cover_path = sys.argv[1]
        stego_path = sys.argv[2]
    else:
        print("\nUsage: python run_steganalysis.py <cover_image> <stego_image>")
        print("\nOr enter paths manually:")
        cover_path = input("Cover image path: ").strip()
        stego_path = input("Stego image path: ").strip()
    
    # Validate files
    if not os.path.exists(cover_path):
        print(f"\n[!] Error: Cover image not found: {cover_path}")
        sys.exit(1)
    
    if not os.path.exists(stego_path):
        print(f"\n[!] Error: Stego image not found: {stego_path}")
        sys.exit(1)
    
    print(f"\n[*] Cover Image: {cover_path}")
    print(f"[*] Stego Image: {stego_path}")
    
    # Run comprehensive steganalysis
    try:
        results = comprehensive_steganalysis(cover_path, stego_path)
        
        # Optional: Generate histogram visualization
        print("\n[?] Generate histogram visualization? (y/n):")
        viz = input(">>> ").strip().lower()
        
        if viz == 'y':
            output_viz = "media/histogram_comparison.png"
            hist_analyzer = HistogramAnalysis()
            hist_analyzer.visualize(cover_path, stego_path, output_viz)
            print(f"[*] Visualization saved to: {output_viz}")
        
        print("\n[✓] Steganalysis complete!")
        
        # Summary
        print("\n" + "="*70)
        print(" RECOMMENDATIONS ".center(70, "="))
        print("="*70)
        
        if 'RS_Analysis' in results:
            rs_rate = results['RS_Analysis']['stego']['embedding_rate_estimate']
            if rs_rate < 0.1:
                print("✓ Low RS detection rate - Good resistance to RS analysis")
            else:
                print(f"⚠ RS detection rate: {rs_rate:.3f} - Consider edge-adaptive embedding")
        
        if 'Histogram_Analysis' in results:
            chi_sq = results['Histogram_Analysis']['chi_square']
            if chi_sq < 0.01:
                print("✓ Low histogram deviation - Excellent statistical similarity")
            elif chi_sq < 0.05:
                print("✓ Moderate histogram deviation - Acceptable for most cases")
            else:
                print(f"⚠ High histogram deviation: {chi_sq:.4f} - May be detectable")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n[!] Error during steganalysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
