"""Optional, dependency-guarded extras: qr, midify, translate.

Navi Cryptex's core is standard-library only, so anything that needs a
third-party package or the network checks first and answers honestly
instead of tracebacking. No MIDI writer is hand-rolled here: if mido
is absent, midify says so.
"""

import io

QR_NOTE = (
    "qr needs the optional 'qrcode' package (pip install qrcode) — "
    "Navi Cryptex's core is stdlib-only, so QR rendering is an optional "
    "extra and nothing was generated."
)
MIDI_NOTE = (
    "midify needs the optional 'mido' package (pip install mido) — "
    "Navi Cryptex's core is stdlib-only, so MIDI writing is an optional "
    "extra and nothing was written."
)
TRANSLATE_NOTE = (
    "translate is unavailable in this build: the original reached the "
    "googletrans web service, and a chip runs offline inside its "
    "sandbox. The honest equivalent is a refusal — no network call "
    "was made."
)


def qr_encode(text, keys=None):
    try:
        import qrcode
    except ImportError:
        return QR_NOTE
    qr = qrcode.QRCode(border=1)
    qr.add_data(text)
    qr.make()
    buf = io.StringIO()
    qr.print_ascii(out=buf, invert=True)
    return buf.getvalue().rstrip()


def qr_decode(text, keys=None):
    return "a QR code is one-way output — there is nothing to decode from text."


def midify_encode(text, keys=None):
    try:
        import mido
    except ImportError:
        return MIDI_NOTE
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    for ch in text:
        note = 21 + (ord(ch) % 88)
        track.append(mido.Message("note_on", note=note, velocity=80, time=0))
        track.append(mido.Message("note_off", note=note, velocity=0, time=240))
    mid.save("cryptex.mid")
    return "wrote cryptex.mid — one note per character (%d notes)" % len(text)


def midify_decode(text, keys=None):
    return "midify is one-way: text becomes a MIDI file, not the other way round."


def translate_encode(text, keys=None):
    return TRANSLATE_NOTE


translate_decode = translate_encode
