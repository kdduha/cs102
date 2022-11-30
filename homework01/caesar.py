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
    up_case = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    low_case = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    for letter in plaintext:
        if letter.isupper():
            ciphertext += up_case[(up_case.index(letter) + shift) % 26]
        elif letter.islower():
            ciphertext += low_case[(low_case.index(letter) + shift) % 26]
        else:
            ciphertext += letter
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
    up_case = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    low_case = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    for letter in ciphertext:
        if letter.isupper():
            plaintext += up_case[(up_case.index(letter) - shift) % 26]
        elif letter.islower():
            plaintext += low_case[(low_case.index(letter) - shift) % 26]
        else:
            plaintext += letter
    return plaintext
