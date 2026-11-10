# Navi Cryptex

A cryptography toolkit that rides inside a single Apex chip. Twenty-two
commands — encodings, classical ciphers, hashes and a few extras — in a
proper multi-file package (`root.py` + `app_cryptex/`), forged into one
`.png` cartridge whose picture *is* the install.

This is the 2.0 ground-up rebuild of the original SaintsSec
`navi-cryptex` (release 1.3). The command grammar is the original's;
the divergences are listed honestly at the bottom.

## Using it

In Apex chat, or anywhere the chip runs:

```
cryptex                        list the ciphers
cryptex <code>                 one cipher's help
cryptex <code> -e -t "text"    encode
cryptex <code> -d -t "text"    decode
cryptex <code> -e -t "text" -k KEY     keyed ciphers (-k a,b = two keys)
cryptex <code> -b -t "text"    brute force, where that means something
cryptex --test                 self-test against known vectors
cryptex --tui                  text menu
```

Worked example:

```
$ cryptex hex -e -t "Hello world!"
48656c6c6f20776f726c6421

$ cryptex hex -d -t 48656c6c6f20776f726c6421
Hello world!
```

## The shelf

| Code | Cipher | Key |
| --- | --- | --- |
| `hex` | Hexadecimal | — |
| `b64` | Base64 | — |
| `bin` | Binary (8-bit groups) | — |
| `oct` | Octal (3-digit groups) | — |
| `mor` | Morse code | — |
| `r13` | ROT13 | — |
| `r47` | ROT47 | — |
| `cae` | Caesar | `-k` shift, optional (default 3) |
| `vig` | Vigenère | `-k` key word, required |
| `affn` | Affine | `-k a,b`, a coprime with 26 |
| `xor` | XOR (hex in/out) | `-k` key, required |
| `atb` | Atbash | — |
| `md5` | MD5 | one-way |
| `sha224` | SHA-224 | one-way |
| `sha256` | SHA-256 | one-way |
| `sha384` | SHA-384 | one-way |
| `l33t` | Leetspeak | decode is best-effort |
| `pswd` | Password generator | `-t` is the length (default 16) |
| `str2int` | A1Z26 | 0 = space |
| `qr` | QR code | optional extra (see below) |
| `midify` | MIDI cipher | optional extra (see below) |
| `translate` | — | unavailable offline (see below) |

Hashes answer `-d` with the truth: hashes don't decode.

Brute mode (`-b`) is honest about where it applies: Caesar tries all
25 shifts, affine tries every valid (a, b) pair, ROT13/ROT47 have a
single answer, and XOR/Vigenère refuse — they would need a
known-plaintext crib, and the chip says so.

## Standard library at the core

The rebuild runs on the Python standard library alone — nothing to
install, nothing to break. Two commands are *optional extras*, guarded
so they degrade to an honest sentence instead of a traceback:

- `qr` renders a terminal QR code when the `qrcode` package is present.
- `midify` writes `cryptex.mid` (one note per character) when the
  `mido` package is present.

Both are declared in `chip-requirements.txt` as comments/extras; Apex
surfaces declared requirements on the chip's card and never installs
them automatically.

## Install it in Apex

1. Open the **Chips** tab, then **Navi User Repo (NUR)**.
2. **Search NUR** — every public repo tagged `navi-chips` is listed.
3. **Install** — Apex downloads every Python file in the repo at the
   latest release, keeping folder paths, and forges them into a chip:
   `root.py` is the entry, the `app_cryptex/` package rides beside it,
   and the runner's package mode makes its imports resolve exactly as
   authored.

## Divergences from the 1.3 original

Stated plainly, per the porting rule (best modern equivalent, flagged):

- **Standard library only.** The original's `chip-requirements.txt`
  pulled qrcode, googletrans, colorama, pillow, numpy, mido, psutil
  and a hashcat entry. The rebuild needs none of them; `qrcode` and
  `mido` survive as guarded optional extras.
- **`translate` is an honest refusal.** The original called the
  googletrans web service; a chip runs offline in its sandbox, so the
  command explains that and makes no network call.
- **`--tui` prints a text menu.** The original opened an interactive
  menu; chip output is captured non-interactively, so the menu is
  printed instead of navigated.
- **`qr` / `midify` are capability-guarded**, per above.
- **Hex is standard hex.** The original's worked example encoded the
  quotation marks around the text along with it; this build encodes
  exactly the text given.
- **Added:** `cae` (Caesar with a settable shift — ROT13's general
  case, and the cipher brute mode is *for*) and `atb` (Atbash).
- **Dropped:** the original's `template` module — it was a starter
  template for writing new cipher modules, not a cipher.

## Files

- `root.py` — the chip entry (`run(args)`); small on purpose.
- `app_cryptex/core.py` — registry, argument parsing, brute force,
  and the `--test` self-test table.
- `app_cryptex/encodings.py` — hex, b64, bin, oct, mor.
- `app_cryptex/classical.py` — r13, r47, cae, vig, affn, xor, atb.
- `app_cryptex/hashes.py` — md5, sha224, sha256, sha384.
- `app_cryptex/fun.py` — l33t, pswd, str2int.
- `app_cryptex/media.py` — qr, midify, translate (guarded).
- `navi-chip.json` — the `navi-chip/1` manifest.
- `navi-cryptex.png` — the forged cartridge (once forged): the whole
  file set rides inside the picture.

## Publishing an update

Edit the code, bump `version` in `navi-chip.json`, push, and publish a
new release — a newer release tag is what offers everyone who
installed the chip an update. Keep the `navi-chips` topic on the repo;
that is how Apex finds it.

## License

MIT — see `LICENSE`. Copyright (c) SaintsSec.
