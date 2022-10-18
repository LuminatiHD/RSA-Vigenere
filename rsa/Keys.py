"""enthält alle Funktionen relevant zum generieren von Keys"""

import numpy as np
import random as rand
from math import lcm
import assets

rand.seed(3)


def extended_euclidian(a: int, b: int) -> int:
    """see https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm"""
    a, b = max(a, b), min(a, b)
    r0 = a
    r1 = b
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1
    while r1 != 0:
        q = r0//r1
        r0, r1 = r1, r0 - q*r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return t0 % a


def choose_primes(min_len: int | None) -> tuple[int, int]:
    """
    generates two mersenne prime numbers with both having a bit-length above :param min_len.
    """
    # all possible numbers p, that in the form of 2^p-1 are prime.
    # via https://oeis.org/A000043
    possible_candidates = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213,
                           19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
                           6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657, 37156667, 42643801, 43112609, 57885161]

    # get the biggest number not over the threshold
    for i in range(len(possible_candidates)):
        if min_len <= possible_candidates[i]:
            p, q = possible_candidates[i:i+2]
            return 2**p-1, 2**q-1


def choose_public_key(p: int, q: int) -> int:
    """Generiert einen Wert zwischen 1 und λ(n) = λ(p*q) = lcm(p-1, q-1) = (p-1)(q-1)/gcd(p, q). Dies wird der public Key"""
    totient = np.lcm(p-1, q-1)  # λ(p*q)
    # e und totient müssen teilerfremd sein → sie teilen keinen Teiler ausser 1.
    # darum wird e so lange randomisiert, bis gcd(e, totient) = 1.
    e = rand.randint(1, totient)
    while np.gcd(e, totient) != 1:
        e = rand.randint(2, totient)

    return e


def generate_private_key(e: int, p: int, q: int) -> int:
    """generiert für einen public key (p·q, e) den Wert d für den private key (p*q, d)"""
    totient = lcm(p-1, q-1)
    return extended_euclidian(e, totient)


def get_keys(min_len: int) -> dict[str:tuple[int, int], str:tuple[int, int]]:
    """Gibt ein Dictionary mit 2 Einträgen aus. das Dictionary nimmt die Form:
    {"public":(p*q, e), "private":(p*q, d)}"""
    p, q = choose_primes(min_len)
    e = choose_public_key(p, q)
    d = generate_private_key(e, p, q)
    n = p*q
    return {"public": (n, e), "private": (n, d)}


def key_to_file(key: tuple[int, int], filename: str) -> None:
    """Stores the key [key] in the file [filename]. returns None"""
    # wird ein Filename ohne Dateityp ".vhc" angegeben, wird angenommen, dass dieser vergessen wurde.
    if filename[-4:] != ".vhc":
        filename += ".vhc"

    n, e = key
    # ein Key besteht aus 2 Werten, N und e. Um den key lossless in einem File speichern zu können, muss man beim Entschlüsseln des keys diese unterscheiden können.
    # Den Weg, wie ich das gemacht habe, ist, dass ein Byte, nämlich nr. 255 die beiden Zahlen abgrenzt.
    # N und e werden also in Bytes encoded, jedoch mit Basis 255, heisst, dass beide byte-streams nie den byte 255 enthalten.
    with open(r".\{}".format(filename), "wb") as file:
        file.write(assets.num_to_bytes(n, 255) + b"\xff" + assets.num_to_bytes(e, 255))


def file_to_key(filename: str) -> tuple[int, int]:
    """converts the key in a .vhc back to a key (N, e)"""
    # wird ein Filename ohne Dateityp ".vhc" angegeben, wird angenommen, dass dieser vergessen wurde.
    if filename[-4:] != ".vhc":
        filename += ".vhc"

    with open(r".\{}".format(filename), "rb") as file:
        n = b""
        e = None

        # das Programm looped durch das File, bis es auf ein Byte mit Wert 255 stösst.
        for i in file.read():
            # type(i) ist int
            if not i == 255 and e is None:
                n += bytes([i])
            elif e is not None:
                e += bytes([i])
            else:
                e = b""

    return assets.bytes_to_num(n, 255), assets.bytes_to_num(e, 255)


def main(public: str, private: str, min_len: int) -> None:
    """Wrapper für das Programm. Generiert zwei korrespondierende Keys mit einer Mindestbitlänge min_len
    und speichert diese in den Dateien [public] und [private] respektive"""
    keys = get_keys(min_len)
    if public[-4:] != ".vhc":
        public += ".vhc"

    if private[-4:] != ".vhc":
        private += ".vhc"

    key_to_file(keys["public"], public)
    key_to_file(keys["private"], private)
