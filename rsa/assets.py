"""Speichert Funktionen, die nicht spezifisch sind zu einem Teil des algorithmus."""
import math
import sys


def is_prime(num: int) -> bool:
    """gibt an, ob eine gegebene Zahl prim ist oder nicht."""
    if num <= 1:
        return False
    elif not num % 2 or not num % 3:
        # python kann Integer als bools gebrauchen -> bool(0) = False, bool(n!=0) = True.
        # wir wollen aber nur True haben, wenn num%2 == 0 oder num%3 == 0, aber bool(0) = False.
        # also drehen wir es um (not num%2)
        return False
    # 6k-1 optimization
    i = 5
    while i <= (num**0.5):
        if (not num % i) or (not num % (i+2)):
            return False
        i += 6
    return True


def llt(num: int) -> bool:
    """tests the primality of a Mersenne prime based on https://en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test.
    :param num: given a Mersenne prime Mp = (p**2)-1, enter the Number p for testing."""
    s = 4
    mp = 2**num-1
    for i in range(num-2):
        s = (s**2-2) % mp

    return s % mp == 0


def convert(val: int, key: tuple[int, int], progress_bar: bool = False) -> int:
    """de/encoded einen einzigen Wert."""
    e = key[1]
    n = key[0]
    return mod_expo(base=val, power=e, modulus=n, progress_bar=progress_bar)


def mod_expo(base: int, power: int, modulus: int, progress_bar: bool = False) -> int:
    """berechnet a^b mod c via https://en.wikipedia.org/wiki/Modular_exponentiation#Left-to-right_binary_method"""
    bar_len = 64  # für progress bar

    acc = 1  # accumulator
    index = 0
    power = bin(power).removeprefix("0b")  # Binäre Zahl ist in der Form '0b[num]'.
    for i in power:
        acc **= 2
        if i == "1":
            acc *= base
        acc %= modulus
        index += 1

        if progress_bar:
            # progress bar
            done_ness = index / len(power)
            if index % math.ceil(len(power)/64) == 0 or done_ness == 1:
                left = math.ceil(bar_len - done_ness * bar_len)
                prog_bar = "\33[102m" + " " * int(done_ness * bar_len) + "\33[107m" + " " * left
                sys.stdout.write("\r" + prog_bar + "\33[0m\33[36m  " + str(round(done_ness * 100, 2)) + "%")

    if progress_bar:
        sys.stdout.write("\33[0m\n")

    return acc


def num_to_bytes(num: int, base: int = 256) -> bytes:
    """übersetzt eine Nummer in ein String zurück/reversed bit_to_num"""

    # Berechnet die Stellen, die die Zahl hat mit Basis [base].
    # log(num, base) berechnet c für base^c = num, anders gesagt: c ist die minimale Menge an Stellen, die die zahl [num] hat.
    # da diese Zahl aber ein Integer sein muss, rundet man c auf.
    # edge case, wo base^c = num mit type(c) = int. Beispiel: num = 100, base = 10,  stellen(num, base) = 3, aber log(base, num) = 2
    # um das zu verhindern, addiert man 1 zu der Nummer. Zahlen, die nicht eine Power von [base] sind, werden über diesen heraustreten.
    # num = 100, base = 10,  stellen(num, base) = 3, log(num+1, base) = log(101, 10) > 2
    # num = 99, base = 10, stellen(num, base) = 2, log(num+1, base) = log(100, 10) = 2
    # für den Edge case num = 0: log(num+1, base) = log(1, base) = 0
    # um das zu verhindern, muss ein unteres Limit gesetzt werden, in dem Fall 1, demnach: max(log(num+1, base), 1))
    lim = max(math.ceil(math.log(num+1, base)), 1)
    out_str = bytes()
    for i in range(lim, 0, -1):
        char = num//base**(i-1)
        out_str += bytes((char,))
        num = num % base**(i-1)

    return out_str


def bytes_to_num(text: bytes, base: int = 256) -> int:
    """converts the characters in a string to a number."""
    acc = 0
    for i in range(len(text)):
        acc += base ** i * text[-i - 1]

    return acc


