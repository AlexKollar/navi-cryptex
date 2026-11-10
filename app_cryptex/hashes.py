"""One-way hashes via hashlib. A hash cannot be decoded; the core
parser answers -d on these with an honest note instead of a function.
"""

import hashlib


def _make(name):
    def run(text, keys=None):
        return hashlib.new(name, text.encode("utf-8")).hexdigest()
    run.__name__ = name + "_encode"
    return run


md5_encode = _make("md5")
sha224_encode = _make("sha224")
sha256_encode = _make("sha256")
sha384_encode = _make("sha384")
