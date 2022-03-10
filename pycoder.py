"""
This module implements a RLE compressor and decompressor.

It's also a script and GUI application. Please see function '_main'
for instructions on how to use 'pycoder.py' as script or GUI app.
"""

from typing import BinaryIO, Callable

__all__ = [
    'encode_rle',
    'decode_rle',
]

METHOD_A = b'\x21'  # 33 or b'!'
METHOD_B = b'\x8a'  # 138

def encode_rle(
        in_file_path: str, 
        out_file_path: str,
        method: bytes,
        overwrite: bool=False,
):
    assert method in [METHOD_A, METHOD_B]
    encode_fn = {
        METHOD_A: _encode_mA,
        METHOD_B: _encode_mB,
    }[method]

    with open(in_file_path, 'rb') as in_:
        with open(out_file_path, 'wb' if overwrite else 'xb') as out:
            out.write(method)
            encode_fn(in_, out)
        #:
    #:
#:

def _encode_mA(in_: BinaryIO, out: BinaryIO):
    """
    Para cada byte em in_:
      1. Se próx byte for igual ao byte actual:
          1.1 incrementar contador
      2. Senão (ie, se próx byte terminar série de bytes consecutivos):
          2.1 gravar na stream out o contador e o byte actual
          2.2 colocar contador a 1
          2.3 byte actual = próx byte
    """
    def write_fn(curr_byte: bytes, count: int):
        out.write(_int_to_byte(count))
        out.write(curr_byte)
    #:
    _do_encode(in_, write_fn)
#:

def _encode_mB(in_: BinaryIO, out: BinaryIO):
    def write_fn(curr_byte: bytes, count: int):
        out.write(curr_byte)
        if count > 1:
            out.write(curr_byte)
            out.write(_int_to_byte(count))
        #:
    #:
    _do_encode(in_, write_fn)
#:

def _do_encode(in_: BinaryIO, write_fn):
    curr_byte = in_.read(1)
    count = 1
    for next_byte in iter(lambda: in_.read(1), b''):
        if next_byte == curr_byte:
            count += 1
            if count == 255:
                write_fn(curr_byte, count)
                count = 0
            #:
        #:
        else:
            if count != 0:
                write_fn(curr_byte, count)
            count = 1
            curr_byte = next_byte
        #:
    #:
    if curr_byte:
        write_fn(curr_byte, count)
    #:
#:


def decode_rle(
        in_file_path: str, 
        out_file_path: str,
        overwrite: bool=False,
):
    with open(in_file_path, 'rb') as in_:
        in_.read(1)  # método de compressão/descompressão ... para já ignoramos...
        with open(out_file_path, 'wb' if overwrite else 'xb') as out:
            _decode_mA(in_, out)
        #:
    #:
#:

def _decode_mA(in_: BinaryIO, out: BinaryIO):
    for pair in iter(lambda: in_.read(2), b''):
        count = pair[0]
        next_byte = pair[1:]
        out.write(count * next_byte)
    #:
#:

def _int_to_byte(i: int) -> bytes:
    return bytes((i,)) 
#:

def _main():
    encode_rle('dadosX.bin', 'dadosX.bin.rle', METHOD_A, overwrite=True)
    decode_rle('dadosX.bin.rle', 'dadosX.copia.bin', overwrite=True)
#:

if __name__ == '__main__':
    _main()
