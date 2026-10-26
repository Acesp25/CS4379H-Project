from math import log10, sqrt
import cv2
import numpy as np
from pathlib import Path

INPUT_DIR = Path("../data/images/input/")
OUTPUT_DIR = Path("../data/images/output/")

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    err = np.sum((original.astype("float") - compressed.astype("float")) ** 2)
    err /= float(original.shape[0] * original.shape[1])
    if (mse == 0):
        return 100
    max_pixel = 255.0
    print("MSE ", mse)
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def main():
    for i in range(1, 6):
        input_path = INPUT_DIR / f"in{i}.png"
        output_path = OUTPUT_DIR / f"out{i}.png"
        
        input = cv2.imread(str(input_path))
        output = cv2.imread(str(output_path))
        
        if input is not None and output is not None:
            value = PSNR(input, output)
            print(f"#{i}: PSNR value is {value:.2f} dB")
        else:
            print(f"Could not find file for index {i}")

if __name__ == "__main__":
    main()
