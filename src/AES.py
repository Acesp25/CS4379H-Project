import pbkdf2
import pyaes

passwordSalt = b'\\`\xd6\xdaB\x03\xdd\xd4z\xb6p\xe8O\xf0\xa8\xc0'
iv = 113573230825063269301116483319046608643543151989648198772824118452040014644050


def encrypt(raw, password):
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    # Return the raw ciphertext bytes (no hexlify): half the size to embed.
    return aes.encrypt(raw.encode('utf-8'))


def decrypt(cipherBytes, password):
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    originalByte = aes.decrypt(cipherBytes)
    return originalByte.decode('utf-8')
