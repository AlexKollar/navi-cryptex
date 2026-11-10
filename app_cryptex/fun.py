"""The lighter shelf: leetspeak, a password generator, and A1Z26."""

import secrets
import string

_L33T_ENC = {
    "a": "4", "b": "8", "e": "3", "g": "6", "i": "1",
    "l": "1", "o": "0", "s": "5", "t": "7", "z": "2",
}
# Best effort only: leetspeak is ambiguous going back (1 can be i or l),
# so decode picks the common reading and says nothing it cannot back up.
_L33T_DEC = {
    "4": "a", "8": "b", "3": "e", "6": "g", "1": "i",
    "0": "o", "5": "s", "7": "t", "2": "z",
}


def l33t_encode(text, keys=None):
    out = []
    for ch in text:
        out.append(_L33T_ENC.get(ch.lower(), ch) if ch.isalpha() else ch)
    return "".join(out)


def l33t_decode(text, keys=None):
    return "".join(_L33T_DEC.get(ch, ch) for ch in text)


_PWD_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"


def generate_password(length=16):
    try:
        length = int(length)
    except (TypeError, ValueError):
        length = 16
    length = max(4, min(length, 256))
    return "".join(secrets.choice(_PWD_ALPHABET) for _ in range(length))


def pswd_encode(text, keys=None):
    # For pswd the "text" is the wanted length: cryptex pswd -t 24
    candidate = (text or "").strip()
    return generate_password(candidate if candidate else 16)


def str2int_encode(text, keys=None):
    out = []
    for ch in text.upper():
        if "A" <= ch <= "Z":
            out.append(str(ord(ch) - 64))
        elif ch == " ":
            out.append("0")
    return " ".join(out)


def str2int_decode(text, keys=None):
    out = []
    for tok in text.replace(",", " ").split():
        try:
            n = int(tok)
        except ValueError:
            raise ValueError("str2int decode takes A1Z26 numbers, e.g. 8 5 12 12 15")
        if n == 0:
            out.append(" ")
        elif 1 <= n <= 26:
            out.append(chr(n + 64))
        else:
            raise ValueError("A1Z26 codes run 1-26 (0 is a space); got %d" % n)
    return "".join(out)
