def _bits(num_pixels: int) -> int:
    # Bits needed for the largest index (num_pixels - 1)
    # Minimun is 8 so the final byte's padding (<8 bits) can't be read as an extra index
    return max(8, (num_pixels - 1).bit_length())

def encode_pls(indices, num_pixels: int) -> bytes:
    bits = _bits(num_pixels)

    # Place index k at bit offset k * bits in one big int (acc)
    acc = 0
    for k, i in enumerate(indices):
        acc |= int(i) << (k * bits)

    # Round up to whole bytes using little-endian ordering
    return acc.to_bytes((len(indices) * bits + 7) // 8, "little")

def decode_pls(data: bytes, num_pixels: int) -> list[int]:
    bits = _bits(num_pixels)
    acc = int.from_bytes(data, "little")
    mask = (1 << bits) - 1  # lowest "bits" bits set

    # Shift each slot down and mask it; floor division drops the padding
    indices = [(acc >> (k * bits)) & mask for k in range(len(data) * 8 // bits)]

    # Wrong password -> random bytes -> almost always out-of-range indices
    if any(i >= num_pixels for i in indices):
        raise ValueError("PLS contains out-of-range indices (wrong password??)")

    return indices
