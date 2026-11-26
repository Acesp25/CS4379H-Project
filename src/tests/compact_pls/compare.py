import builtins, os, random
from PIL import Image, ImageChops
from definitions import get_project_root
from original_refactored import LSB as orig_lsb, AES as Cipher
from variants.compact_pls import LSB as comp_lsb

# Setup file paths and outputs
ROOT = get_project_root()
IN_IMG = os.path.join(ROOT, "data/images/input/in3.png")
OUT_DIR = os.path.join(ROOT, "src/tests/compact_pls/output")
os.makedirs(OUT_DIR, exist_ok=True)
out_orig = os.path.join(OUT_DIR, "orig_out3.png")
out_comp = os.path.join(OUT_DIR, "compact_out3.png")

# Funny message to place in our output image
msg = Cipher.encrypt("Your shoe is untied, haha made you look", "msgpassword")

# Same seed, same result
random.seed(1111); orig_lsb.lsb_encoding(msg, IN_IMG, out_orig)
random.seed(1111); comp_lsb.lsb_encoding(msg, IN_IMG, out_comp)

# Ensure both outputs are exactly the same
same = ImageChops.difference(Image.open(out_orig).convert("RGB"),
        Image.open(out_comp).convert("RGB")).getbbox() is None

print("Stego images identical:", same)

orig_size = os.path.getsize(orig_lsb.PLS_TXT_ENC_PATH)
comp_size = os.path.getsize(comp_lsb.PLS_BIN_ENC_PATH)

# Output size comparison
print(f"Original PLS: {orig_size} B | Compact PLS: {comp_size} B | {orig_size / comp_size:.2f}x smaller")
print("Round-trip:", Cipher.decrypt(comp_lsb.lsb_decoding(IN_IMG, out_comp), "msgpassword"))
