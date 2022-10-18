"""Enthält alle Funktionen relevant zum Encoding"""
import math
import random
import sys
import assets
import Keys


def vigenere(msg: bytes, key: bytes, progress_bar: bool = False) -> bytes:
    """Encoded eine Nachricht nach dem Vigenère-prinzip"""
    out = b""
    msg_len = len(msg)
    bar_len = 64
    for i in range(msg_len):
        m = msg[i]
        k = key[i % len(key)]
        out += bytes(((m+k) % 256,))

        if progress_bar:
            done_ness = (i + 1) / msg_len
            if i % math.ceil(msg_len/bar_len) == 0 or done_ness == 1:
                left = math.ceil(bar_len - done_ness * bar_len)
                prog_bar = "\33[102m" + " " * int(done_ness * bar_len) + "\33[107m" + " " * left
                sys.stdout.write("\r" + prog_bar + "\33[0m\33[36m  " + str(round(done_ness * 100, 2)) + "%")
    if progress_bar:
        sys.stdout.write("\n")
    return out


def hybrid_encode(message: bytes, key: tuple[int, int]) -> tuple[bytes, bytes]:
    """Encodes a message using an RSA-Vigenère-hybrid encoding scheme.
    The function generates a random keyword and encodes the Message using Vigenère-cryptography using said key.
    The keyword is then encoded using RSA with the key provided.
    The function returns a tuple containing the encrypted message, as well as the encrypted keyword.
    in order to decode the Message, one has to first decode the keyword using the RSA-key corresponding to the one given for encryption.
    the Message can then be decoded using this keyword.
    """
    n = key[0]
    keyword = random.randint(n//2, n-1)

    sys.stdout.write("\33[0m" + "encode message...\n")
    enc_message = vigenere(message, assets.num_to_bytes(keyword), progress_bar=True)

    sys.stdout.write("\33[0m" + "encode keyword...\n")
    enc_keyword = assets.num_to_bytes(assets.convert(keyword, key, progress_bar=True))

    sys.stdout.write("\33[0m" + "done\n\n")
    return enc_message, enc_keyword


def main(msg_path: str, out_path: str, key_path: str, keyword_path: str) -> None:
    """Wrapper für das Programm, das für die Pipeline gebaut wurde"""
    key = Keys.file_to_key(key_path)
    with open(msg_path, "rb") as file:
        msg = file.read()
        enc = hybrid_encode(msg, key)

    enc_msg, enc_kw = enc
    with open(out_path, "wb") as out_file:
        out_file.write(enc_msg)

    with open(keyword_path, "wb") as keyword_file:
        keyword_file.write(enc_kw)
