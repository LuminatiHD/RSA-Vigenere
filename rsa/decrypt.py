"""Enthält alle Funktionen relevant zu decoding"""
import math
import assets
import sys
import Keys


def main(msg_path: str, out_path: str, key_path: str, keyword_path: str):
    """Wrapper für das Programm, das für die Pipeline gebaut wurde"""
    key = Keys.file_to_key(key_path)

    with open(keyword_path, "rb") as kw_file:
        kw = kw_file.read()

    with open(msg_path, "rb") as file:
        msg = file.read()
        dec = hybrid_decode(msg, key, kw)

    with open(out_path, "wb") as out_file:
        out_file.write(dec)


def vigenere(msg: bytes, key: bytes, progress_bar: bool = False) -> bytes:
    """Decoded eine Nachricht nach dem Vigenère-prinzip"""
    out = bytes()
    msg_len = len(msg)
    bar_len = 64
    for i in range(msg_len):
        m = msg[i]
        k = key[i % len(key)]
        out += bytes(((m - k) % 256,))

        if progress_bar:
            done_ness = (i + 1) / msg_len
            if i % math.ceil(msg_len/bar_len) == 0 or done_ness == 1:
                left = math.ceil(bar_len - done_ness * bar_len)
                prog_bar = "\33[102m" + " " * int(done_ness * bar_len) + "\33[107m" + " " * left
                sys.stdout.write("\r" + prog_bar + "\33[0m\33[36m  " + str(round(done_ness * 100, 2)) + "%")
    if progress_bar:
        sys.stdout.write("\n")
    return out


def hybrid_decode(message: bytes, key: tuple[int, int], keyword: bytes) -> bytes:
    """See encode.hybrid_encode"""
    sys.stdout.write("\33[0m" + "decode key...\n")
    dec_keyword = assets.num_to_bytes(assets.convert(assets.bytes_to_num(keyword), key, progress_bar=True))
    sys.stdout.write("\33[0m" + "decode message...\n")
    dec_message = vigenere(message, dec_keyword, progress_bar=True)

    sys.stdout.write("\33[0m" + "done\n\n")
    return dec_message
