def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    digit_key = []
    for key in keyword:
        if key.isupper():
            digit_key.append(ord(key) % ord("A"))
        else:
            digit_key.append(ord(key) % ord("a"))
    key_len = len(keyword)

    for ind, symbol in enumerate(plaintext):
        if symbol.isalpha():
            new_symbol = (ord(symbol.lower()) + digit_key[ind % key_len]) % ord("z")
            if new_symbol < ord("a"):
                new_symbol += ord("a") - 1
            if symbol.isupper():
                ciphertext += chr(new_symbol).upper()
            else:
                ciphertext += chr(new_symbol)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    digit_key = []
    for key in keyword:
        if key.isupper():
            digit_key.append(ord(key) % ord("A"))
        else:
            digit_key.append(ord(key) % ord("a"))
    key_len = len(keyword)

    for ind, symbol in enumerate(ciphertext):
        if symbol.isalpha():
            new_symbol = ord(symbol.lower()) - digit_key[ind % key_len]
            if new_symbol < ord("a"):
                new_symbol += (ord("z") - ord("a") + 1)
            if symbol.isupper():
                plaintext += chr(new_symbol).upper()
            else:
                plaintext += chr(new_symbol)
        else:
            plaintext += symbol
    return plaintext

