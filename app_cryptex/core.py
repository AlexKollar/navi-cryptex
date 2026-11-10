"""Navi Cryptex command core: the cipher registry, the argument
parser, brute force, and the --test self-test table.

Grammar (the original's, kept):
    cryptex                      list the ciphers
    cryptex <code>               one cipher's help
    cryptex <code> -e -t "text"  encode
    cryptex <code> -d -t "text"  decode
    cryptex <code> -e -t "text" -k KEY     (-k a,b for two keys)
    cryptex <code> -b -t "text"  brute force, where that means something
    cryptex --test               self-test against known vectors
    cryptex --tui                text menu
"""

try:
    from . import classical, encodings, fun, hashes, media
except ImportError:  # imported outside the package (should not happen)
    from app_cryptex import classical, encodings, fun, hashes, media

VERSION = "2.0.0"
USAGE = ('usage: cryptex <code> [-e|-d] [-t "text"] [-k key] [-b]'
         "  |  cryptex --test  |  cryptex --tui")


def _entry(name, encode, decode, key="none", is_hash=False, help_text=""):
    return {
        "name": name,
        "encode": encode,
        "decode": decode,
        "key": key,
        "hash": is_hash,
        "help": help_text,
    }


REGISTRY = {
    "hex": _entry(
        "Hexadecimal", encodings.hex_encode, encodings.hex_decode,
        help_text="The text's UTF-8 bytes as hex. "
                  'cryptex hex -e -t "Hello world!" -> 48656c6c6f20776f726c6421'),
    "b64": _entry(
        "Base64", encodings.b64_encode, encodings.b64_decode,
        help_text="Standard base64. Decode tolerates missing padding."),
    "bin": _entry(
        "Binary", encodings.bin_encode, encodings.bin_decode,
        help_text="Each byte as 8 binary digits, space-separated."),
    "oct": _entry(
        "Octal", encodings.oct_encode, encodings.oct_decode,
        help_text="Each byte as 3 octal digits, space-separated."),
    "mor": _entry(
        "Morse code", encodings.mor_encode, encodings.mor_decode,
        help_text="ITU Morse. Letters are space-separated, words take ' / '."),
    "r13": _entry(
        "ROT13", classical.r13_encode, classical.r13_decode,
        help_text="Rotate letters by 13. Encode and decode are the same act."),
    "r47": _entry(
        "ROT47", classical.r47_encode, classical.r47_decode,
        help_text="Rotate printable ASCII (33-126) by 47. Self-inverse."),
    "cae": _entry(
        "Caesar", classical.cae_encode, classical.cae_decode, key="optional",
        help_text="Shift letters by -k (default 3). -b tries all 25 shifts."),
    "vig": _entry(
        "Vigenere", classical.vig_encode, classical.vig_decode, key="required",
        help_text="Polyalphabetic cipher; -k is the alphabetic key word."),
    "affn": _entry(
        "Affine", classical.affn_encode, classical.affn_decode, key="pair",
        help_text="E(x) = (a*x + b) mod 26. Two keys: -k a,b, "
                  "a coprime with 26. -b tries every valid a and b."),
    "xor": _entry(
        "XOR", classical.xor_encode, classical.xor_decode, key="required",
        help_text="Repeat-key XOR. Encode outputs hex; decode takes hex."),
    "atb": _entry(
        "Atbash", classical.atb_encode, classical.atb_decode,
        help_text="Mirror the alphabet: A<->Z, B<->Y, ... Self-inverse."),
    "md5": _entry(
        "MD5", hashes.md5_encode, None, is_hash=True,
        help_text="One-way MD5 digest (hex)."),
    "sha224": _entry(
        "SHA-224", hashes.sha224_encode, None, is_hash=True,
        help_text="One-way SHA-224 digest (hex)."),
    "sha256": _entry(
        "SHA-256", hashes.sha256_encode, None, is_hash=True,
        help_text="One-way SHA-256 digest (hex)."),
    "sha384": _entry(
        "SHA-384", hashes.sha384_encode, None, is_hash=True,
        help_text="One-way SHA-384 digest (hex)."),
    "l33t": _entry(
        "Leetspeak", fun.l33t_encode, fun.l33t_decode,
        help_text="a=4 b=8 e=3 g=6 i/l=1 o=0 s=5 t=7 z=2. "
                  "Decode is best-effort: leetspeak is ambiguous backwards."),
    "pswd": _entry(
        "Password generator", fun.pswd_encode, None,
        help_text="A fresh random password (secrets module). "
                  "-t is the length, default 16."),
    "str2int": _entry(
        "A1Z26", fun.str2int_encode, fun.str2int_decode,
        help_text="Letters as alphabet positions (A=1 ... Z=26, 0 = space)."),
    "qr": _entry(
        "QR code", media.qr_encode, media.qr_decode,
        help_text="Render the text as a QR code in the terminal. "
                  "Optional extra: needs the qrcode package."),
    "midify": _entry(
        "MIDI cipher", media.midify_encode, media.midify_decode,
        help_text="Text as MIDI notes, written to cryptex.mid. "
                  "Optional extra: needs the mido package."),
    "translate": _entry(
        "Translate", media.translate_encode, media.translate_decode,
        help_text="Unavailable in this build — the original used a web "
                  "service and a chip runs offline. See README."),
}

_KEY_NOTES = {
    "none": "",
    "optional": " [key optional]",
    "required": " [needs -k key]",
    "pair": " [needs -k a,b]",
}


def print_list():
    print("Navi Cryptex %s — a cryptography toolkit in a chip." % VERSION)
    print(USAGE)
    print("")
    for code, entry in REGISTRY.items():
        print("  %-8s %-20s%s" % (code, entry["name"], _KEY_NOTES[entry["key"]]))
    print("")
    print("cryptex <code> shows one cipher's help. "
          "Hashes (md5, sha224, sha256, sha384) only encode.")


def print_help(code, entry):
    print("%s — %s" % (code, entry["name"]))
    if entry["help"]:
        print(entry["help"])
    print('use: cryptex %s -e -t "text"%s' % (
        code, " -k KEY" if entry["key"] in ("required", "optional") else
        " -k a,b" if entry["key"] == "pair" else ""))
    if entry["decode"]:
        print('     cryptex %s -d -t "text"' % code)


def print_menu():
    # --tui in the original opened an interactive menu. A chip runs
    # non-interactively with captured output, so the menu is printed
    # as text instead (a flagged divergence — see README).
    print("Navi Cryptex — menu")
    print("")
    print_list()
    print("")
    print("Pick a code and run it, e.g.:  cryptex hex -e -t \"Hello world!\"")


def _do_brute(code, entry, text, keys):
    if code == "cae":
        for shift in range(1, 26):
            print("shift %2d: %s" % (shift, classical._rot_alpha(text, -shift)))
        return 0
    if code == "r13":
        print(classical.r13_encode(text))
        return 0
    if code == "r47":
        print(classical.r47_encode(text))
        return 0
    if code == "affn":
        for a in classical.VALID_AFFINE_A:
            for b in range(26):
                print("a=%2d b=%2d: %s" % (
                    a, b, classical.affn_decode(text, [str(a), str(b)])))
        return 0
    if code == "xor":
        print("xor brute force needs a known-plaintext crib to test keys "
              "against — without one there is nothing honest to try.")
        return 0
    if code == "vig":
        print("vigenere brute force needs a key length and a crib — "
              "not attempted.")
        return 0
    print("brute force does not apply to %s." % code)
    return 0


def _run(argv):
    if not argv:
        print_list()
        return 0
    head = argv[0]
    if head == "--test":
        return self_test()
    if head == "--tui":
        print_menu()
        return 0
    if head in ("--help", "-h", "help"):
        print_list()
        return 0
    code = head.lower()
    entry = REGISTRY.get(code)
    if entry is None:
        print("unknown cipher %r — run cryptex with no arguments "
              "for the list." % head)
        return 2
    rest = argv[1:]
    if not rest:
        print_help(code, entry)
        return 0

    mode = "e"
    text = None
    keys = []
    brute = False
    loose = []
    i = 0
    while i < len(rest):
        tok = rest[i]
        if tok in ("-e", "--encode"):
            mode = "e"
        elif tok in ("-d", "--decode"):
            mode = "d"
        elif tok == "-b":
            brute = True
        elif tok == "-t":
            i += 1
            if i >= len(rest):
                raise ValueError("-t needs the text after it")
            text = rest[i]
        elif tok == "-k":
            i += 1
            if i >= len(rest):
                raise ValueError("-k needs the key after it")
            keys.extend(p.strip() for p in rest[i].split(",") if p.strip())
        elif tok.startswith("-") and tok != "-":
            raise ValueError("unknown flag %r" % tok)
        else:
            loose.append(tok)
        i += 1
    if text is None and loose:
        text = " ".join(loose)
    if text is None:
        print_help(code, entry)
        print("no text given — pass it with -t \"text\".")
        return 2
    if entry["key"] == "required" and not keys:
        raise ValueError("%s needs a key: -k KEY" % code)
    if brute:
        return _do_brute(code, entry, text, keys)
    if mode == "d":
        if entry["hash"]:
            print("%s is a one-way hash — hashes don't decode. "
                  "Run it with -e to hash text." % code)
            return 0
        if entry["decode"] is None:
            print("%s is one-way — there is nothing to decode." % code)
            return 0
        result = entry["decode"](text, keys)
    else:
        result = entry["encode"](text, keys)
    if result is not None:
        print(result)
    return 0


def run_command(argv):
    """Entry for root.py. Prints everything; never tracebacks on
    bad input — a chip answers honestly or not at all."""
    try:
        return _run(list(argv))
    except ValueError as exc:
        print("error: " + str(exc))
        return 1
    except Exception as exc:  # a chip in a sandbox stays polite
        print("error: " + str(exc))
        return 1


def self_test():
    e = encodings
    c = classical
    h = hashes
    f = fun
    checks = [
        ("hex encode", lambda: e.hex_encode("Hello world!") == "48656c6c6f20776f726c6421"),
        ("hex decode", lambda: e.hex_decode("48656c6c6f20776f726c6421") == "Hello world!"),
        ("b64 encode", lambda: e.b64_encode("Hello world!") == "SGVsbG8gd29ybGQh"),
        ("b64 decode", lambda: e.b64_decode("SGVsbG8gd29ybGQh") == "Hello world!"),
        ("bin roundtrip", lambda: e.bin_decode(e.bin_encode("Hi")) == "Hi"),
        ("bin vector", lambda: e.bin_encode("A") == "01000001"),
        ("oct roundtrip", lambda: e.oct_decode(e.oct_encode("Hi")) == "Hi"),
        ("oct vector", lambda: e.oct_encode("A") == "101"),
        ("morse encode", lambda: e.mor_encode("SOS") == "... --- ..."),
        ("morse roundtrip", lambda: e.mor_decode(e.mor_encode("HELLO WORLD")) == "HELLO WORLD"),
        ("r13 vector", lambda: c.r13_encode("Hello") == "Uryyb"),
        ("r13 decode", lambda: c.r13_decode("Uryyb") == "Hello"),
        ("r47 roundtrip", lambda: c.r47_decode(c.r47_encode("Hello, World! 123")) == "Hello, World! 123"),
        ("cae vector", lambda: c.cae_encode("Hello", ["3"]) == "Khoor"),
        ("cae decode", lambda: c.cae_decode("Khoor", ["3"]) == "Hello"),
        ("vig vector", lambda: c.vig_encode("ATTACKATDAWN", ["LEMON"]) == "LXFOPVEFRNHR"),
        ("vig decode", lambda: c.vig_decode("LXFOPVEFRNHR", ["LEMON"]) == "ATTACKATDAWN"),
        ("affn vector", lambda: c.affn_encode("AFFINECIPHER", ["5", "8"]) == "IHHWVCSWFRCP"),
        ("affn decode", lambda: c.affn_decode("IHHWVCSWFRCP", ["5", "8"]) == "AFFINECIPHER"),
        ("affn bad a refused", lambda: _affine_refuses_bad_a()),
        ("xor vector", lambda: c.xor_encode("AAA", ["K"]) == "0a0a0a"),
        ("xor roundtrip", lambda: c.xor_decode(c.xor_encode("Hello world", ["key"]), ["key"]) == "Hello world"),
        ("atb vector", lambda: c.atb_encode("abcXYZ") == "zyxCBA"),
        ("md5 vector", lambda: h.md5_encode("abc") == "900150983cd24fb0d6963f7d28e17f72"),
        ("sha224 vector", lambda: h.sha224_encode("abc") == "23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7"),
        ("sha256 vector", lambda: h.sha256_encode("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        ("sha384 vector", lambda: h.sha384_encode("abc") == "cb00753f45a35e8bb5a03d699ac65007272c32ab0eded1631a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7"),
        ("l33t vector", lambda: f.l33t_encode("leet") == "1337"),
        ("str2int encode", lambda: f.str2int_encode("ABC Z") == "1 2 3 0 26"),
        ("str2int decode", lambda: f.str2int_decode("1 2 3 0 26") == "ABC Z"),
        ("pswd length", lambda: len(f.generate_password(20)) == 20),
        ("pswd default length", lambda: len(f.generate_password()) == 16),
    ]
    passed = 0
    for label, fn in checks:
        try:
            ok = bool(fn())
            detail = ""
        except Exception as exc:
            ok = False
            detail = ": " + str(exc)
        print("%s %s%s" % ("PASS" if ok else "FAIL", label, detail))
        if ok:
            passed += 1
    print("self-test: %d/%d passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def _affine_refuses_bad_a():
    try:
        classical.affn_encode("ABC", ["4", "1"])
    except ValueError:
        return True
    return False
