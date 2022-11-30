def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for symbol in plaintext:
        if symbol.isalpha():
            new_symbol = (ord(symbol.lower()) + shift) % ord("z")
            if new_symbol < ord("a"):
                new_symbol += ord("a") - 1
            if symbol.isupper():
                ciphertext += chr(new_symbol).upper()
            else:
                ciphertext += chr(new_symbol)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for symbol in ciphertext:
        if symbol.isalpha():
            new_symbol = ord(symbol.lower()) - shift
            if new_symbol < ord("a"):
                new_symbol += ord("z") - ord("a") + 1
            if symbol.isupper():
                plaintext += chr(new_symbol).upper()
            else:
                plaintext += chr(new_symbol)
        else:
            plaintext += symbol
    return plaintext
