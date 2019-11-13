"""
Encurtador usando base62
~~~~~~
Originated from http://blog.suminb.com/archives/558
"""

__title__ = "base62"
__author__ = "Sumin Byeon"
__email__ = "suminb@gmail.com"
__version__ = "0.4.3"

""" ajustado para Python 3.7 por Gerson Rodrigues"""

BASE = 62
CHARSET_DEFAULT = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# ordem do charset reajustada por Gerson Rodrigues
CHARSET_INVERTED = "0123789abcdefLMNOPQghijklmnopqrstuvwxyzABCDEFGHIJKRSTUVWXYZ456"

try:
    bytes_types = (
        bytes,
        bytearray,
    )
except NameError:
    bytes_types = (bytes,)


def bytes_to_int(barray, byteorder="big", signed=False):
    """ Converte um arrar de bytes para um numero inteiro"""
    """Converts a byte array to an integer value.
    Python 3 comes with a built-in function to do this, but we would like to
    keep our code Python 2 compatible.
    """

    try:
        return int.from_bytes(barray, byteorder, signed=signed)
    except AttributeError:
        # For Python 2.x
        if byteorder != "big" or signed:
            raise NotImplementedError()

        # NOTE: This won't work if a generator is given
        n = len(barray)
        ds = (x << (8 * (n - 1 - i)) for i, x in enumerate(bytearray(barray)))

        return sum(ds)


def encode(n, minlen=1, charset=CHARSET_DEFAULT):
    """Encodes a given integer ``n``."""

    chs = []
    while n > 0:
        r = n % BASE
        n //= BASE

        chs.append(charset[r])

    if len(chs) > 0:
        chs.reverse()
    else:
        chs.append("0")

    s = "".join(chs)
    s = charset[0] * max(minlen - len(s), 0) + s
    return s


def encodebytes(barray, charset=CHARSET_DEFAULT):
    """Encodes a bytestring into a base62 string.
    :param barray: A byte array
    :type barray: bytes
    :rtype: str
    """

    _check_type(barray, bytes_types)
    return encode(bytes_to_int(barray), charset=charset)


def decode(encoded, charset=CHARSET_DEFAULT):
    """Decodes a base62 encoded value ``encoded``.
    :type encoded: str
    :rtype: int
    """
    _check_type(encoded, str)

    if encoded.startswith("0z"):
        encoded = encoded[2:]

    l, i, v = len(encoded), 0, 0
    for x in encoded:
        v += _value(x, charset=charset) * (BASE ** (l - (i + 1)))
        i += 1

    return v


def decodebytes(encoded, charset=CHARSET_DEFAULT):
    """Decodes a string of base62 data into a bytes object.
    :param encoded: A string to be decoded in base62
    :type encoded: str
    :rtype: bytes
    """

    decoded = decode(encoded, charset=charset)
    buf = bytearray()
    while decoded > 0:
        buf.append(decoded & 0xFF)
        decoded //= 256
    buf.reverse()

    return bytes(buf)


def _value(ch, charset):
    """Decodes an individual digit of a base62 encoded string."""

    try:
        return charset.index(ch)
    except ValueError:
        raise ValueError("base62: Invalid character (%s)" % ch)


def _check_type(value, expected_type):
    """Checks if the input is in an appropriate type."""

    if not isinstance(value, expected_type):
        msg = "Expected {} object, not {}".format(
            expected_type, value.__class__.__name__
        )
        raise TypeError(msg)

if __name__ == '__main__':
    x = encode(1115802, charset=CHARSET_INVERTED)
    print(x)
    y = decode(x, charset=CHARSET_INVERTED)
    print(y)