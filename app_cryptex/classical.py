"""Classical ciphers: ROT13, ROT47, Caesar, Vigenere, affine, XOR, Atbash.

Every function takes (text, keys) where keys is the list of -k values
(already split on commas by the core parser).
"""

import math

VALID_AFFINE_A = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)


def _rot_alpha(text, shift):
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)


def r13_encode(text, keys=None):
    return _rot_alpha(text, 13)


r13_decode = r13_encode


def r47_encode(text, keys=None):
    out = []
    for ch in text:
        o = ord(ch)
        if 33 <= o <= 126:
            out.append(chr(33 + (o - 33 + 47) % 94))
        else:
            out.append(ch)
    return "".join(out)


r47_decode = r47_encode


def _caesar_shift(keys):
    if keys:
        try:
            return int(keys[0]) % 26
        except (TypeError, ValueError):
            raise ValueError("caesar key must be a number (the shift), e.g. -k 3")
    return 3


def cae_encode(text, keys=None):
    return _rot_alpha(text, _caesar_shift(keys))


def cae_decode(text, keys=None):
    return _rot_alpha(text, -_caesar_shift(keys))


def _vig(text, key, decrypt):
    if not key or not key.isalpha():
        raise ValueError("vigenere needs an alphabetic key: -k LEMON")
    key = key.upper()
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = 65 if ch.isupper() else 97
            shift = ord(key[ki % len(key)]) - 65
            if decrypt:
                shift = -shift
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def vig_encode(text, keys=None):
    return _vig(text, keys[0] if keys else None, False)


def vig_decode(text, keys=None):
    return _vig(text, keys[0] if keys else None, True)


def _affine_params(keys):
    if not keys or len(keys) < 2:
        raise ValueError(
            "affine needs two keys: -k a,b with a coprime with 26 "
            "(valid a: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)")
    try:
        a = int(keys[0]) % 26
        b = int(keys[1]) % 26
    except (TypeError, ValueError):
        raise ValueError("affine keys must be numbers: -k a,b")
    if math.gcd(a, 26) != 1:
        raise ValueError(
            "affine key a=%d is not coprime with 26; valid a values: %s"
            % (a, ", ".join(str(v) for v in VALID_AFFINE_A)))
    return a, b


def _affine(text, keys, decrypt):
    a, b = _affine_params(keys)
    ainv = pow(a, -1, 26)
    out = []
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = 65 if ch.isupper() else 97
            x = ord(ch) - base
            y = (ainv * (x - b)) % 26 if decrypt else (a * x + b) % 26
            out.append(chr(y + base))
        else:
            out.append(ch)
    return "".join(out)


def affn_encode(text, keys=None):
    return _affine(text, keys, False)


def affn_decode(text, keys=None):
    return _affine(text, keys, True)


def _xor_bytes(data, key):
    kb = key.encode("utf-8")
    return bytes(b ^ kb[i % len(kb)] for i, b in enumerate(data))


def xor_encode(text, keys=None):
    if not keys or not keys[0]:
        raise ValueError("xor needs a key: -k KEY")
    return _xor_bytes(text.encode("utf-8"), keys[0]).hex()


def xor_decode(text, keys=None):
    if not keys or not keys[0]:
        raise ValueError("xor needs a key: -k KEY")
    cleaned = "".join(text.split())
    try:
        raw = bytes.fromhex(cleaned)
    except ValueError:
        raise ValueError("xor decode takes the hex that xor encode produced")
    return _xor_bytes(raw, keys[0]).decode("utf-8", "replace")


def atb_encode(text, keys=None):
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr(219 - ord(ch)))
        elif "A" <= ch <= "Z":
            out.append(chr(155 - ord(ch)))
        else:
            out.append(ch)
    return "".join(out)


atb_decode = atb_encode
