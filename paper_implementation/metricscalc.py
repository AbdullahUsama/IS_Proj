import cv2
import numpy as np
import math

def calculate_mse(original, stego):
    original = original.astype(np.float64)
    stego = stego.astype(np.float64)
    mse = np.mean((original - stego) ** 2)
    return mse

def calculate_psnr(original, stego):
    mse = calculate_mse(original, stego)
    if mse == 0:
        return float('inf')
    MAX = 255.0
    psnr = 10 * math.log10((MAX * MAX) / mse)
    return psnr

def psnr_for_images(original_path, stego_path):
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
    
    if original is None:
        print(f"Error: Could not load original image {original_path}")
        return
    if stego is None:
        print(f"Error: Could not load stego image {stego_path}")
        return
    if original.shape != stego.shape:
        print("Error: Images are not the same size!")
        return
    
    psnr_value = calculate_psnr(original, stego)
    print(f"PSNR between {original_path} and {stego_path}: {psnr_value:.4f} dB")

psnr_for_images("media/tyla.jpg", "media/stego_image.png")
psnr_for_images("media/burger.jpg", "media/stego_image_2.png")
