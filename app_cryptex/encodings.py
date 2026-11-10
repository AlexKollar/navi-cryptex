"""Text encodings: hex, base64, binary, octal and Morse code.

Every function takes (text, keys) and returns the transformed string;
keys are ignored here and exist only for a uniform registry shape.
"""

import base64
import binascii


def hex_encode(text, keys=None):
    return text.encode("utf-8").hex()


def hex_decode(text, keys=None):
    cleaned = "".join(text.split())
    try:
        raw = bytes.fromhex(cleaned)
    except ValueError:
        raise ValueError("not valid hex (odd number of digits or non-hex characters)")
    return raw.decode("utf-8", "replace")


def b64_encode(text, keys=None):
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def b64_decode(text, keys=None):
    cleaned = "".join(text.split())
    cleaned += "=" * (-len(cleaned) % 4)
    try:
        raw = base64.b64decode(cleaned)
    except (binascii.Error, ValueError):
        raise ValueError("not valid base64")
    return raw.decode("utf-8", "replace")


def bin_encode(text, keys=None):
    return " ".join(format(b, "08b") for b in text.encode("utf-8"))


def bin_decode(text, keys=None):
    tokens = text.split()
    if len(tokens) == 1 and len(tokens[0]) > 8:
        tokens = [tokens[0][i:i + 8] for i in range(0, len(tokens[0]), 8)]
    out = bytearray()
    for tok in tokens:
        if not tok or any(c not in "01" for c in tok) or len(tok) > 8:
            raise ValueError("not valid binary: %r" % tok)
        out.append(int(tok, 2))
    return bytes(out).decode("utf-8", "replace")


def oct_encode(text, keys=None):
    return " ".join(format(b, "03o") for b in text.encode("utf-8"))


def oct_decode(text, keys=None):
    tokens = text.split()
    if len(tokens) == 1 and len(tokens[0]) > 3 and len(tokens[0]) % 3 == 0:
        tokens = [tokens[0][i:i + 3] for i in range(0, len(tokens[0]), 3)]
    out = bytearray()
    for tok in tokens:
        if not tok or any(c not in "01234567" for c in tok):
            raise ValueError("not valid octal: %r" % tok)
        value = int(tok, 8)
        if value > 255:
            raise ValueError("octal group out of byte range: %r" % tok)
        out.append(value)
    return bytes(out).decode("utf-8", "replace")


MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.", "(": "-.--.", ")": "-.--.-",
    "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.", "-": "-....-", "_": "..--.-", '"': ".-..-.",
    "$": "...-..-", "@": ".--.-.",
}
_MORSE_REVERSE = {v: k for k, v in MORSE.items()}


def mor_encode(text, keys=None):
    words = []
    for word in text.upper().split():
        letters = []
        for ch in word:
            code = MORSE.get(ch)
            if code is None:
                raise ValueError("no Morse code for character %r" % ch)
            letters.append(code)
        words.append(" ".join(letters))
    return " / ".join(words)


def mor_decode(text, keys=None):
    words = []
    for word in text.split("/"):
        letters = []
        for token in word.split():
            ch = _MORSE_REVERSE.get(token)
            if ch is None:
                raise ValueError("not a Morse code group: %r" % token)
            letters.append(ch)
        if letters:
            words.append("".join(letters))
    return " ".join(words)
