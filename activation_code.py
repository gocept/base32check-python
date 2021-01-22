#!/usr/bin/env python3
import base32check1
from base64 import b32encode


def format(activation_code):
    return ' '.join([activation_code[i:i + 4] for i in range(0, len(activation_code), 4)])


def compute(*, insurance_corp_code, version=0, specific_code):
    icc = insurance_corp_code & 0x3FF
    v = version & 0x1F
    sc = specific_code & 0xFFF_FFFF_FFFF_FFFF
    assert icc == insurance_corp_code
    assert v == version
    assert sc == specific_code
    base32 = b32encode((icc << 65 | v << 60 | sc).to_bytes(10, 'big')).decode('us-ascii')[1:]
    return base32 + base32check1.compute(base32)


if __name__ == '__main__':
    from sys import _getframe

    line = _getframe().f_lineno + 2
    tests = (
        ('AAAA AAAA AAAA AAAA', 0, 0),
        ('AAAA AAAA AAA3 B7BU', 0xD_87E1, 0),
        ('AIAE TZ3E XO4X 5NNN', 0x24F_3B25_DDCB_F5AD, 0x8),
        ('67AB CDEF GHIJ KLMU', 0x88_6429_8E84_A96C, 0x3DF),
        ('7IAA AAAA AAAA AAAR', 0, 0x3E8),
        ('7JAA AAAA AAAA AAPJ', 0xF, 0x3E9),
        ('7MAA AAAA AAAV BPNN', 0xA_85ED, 0x3EC),
        ('7UAI UJAG CIM4 5TFZ', 0x451_2030_90CE_7665, 0x3F4),
        ('77AA AAAA AAAA 7EBF', 0x7C81, 0x3FF),
        ('77A7 7777 7777 7773', 0xFFF_FFFF_FFFF_FFFF, 0x3FF)
    )
    for i, (activation_code, specific_code, insurance_corp_code) in zip(range(len(tests)), tests):
        formatted = format(compute(insurance_corp_code=insurance_corp_code, specific_code=specific_code))
        assert formatted == activation_code, f'File "{__file__}", line {line + i}: Expected: "{activation_code}", but was: "{formatted}"'