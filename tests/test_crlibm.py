"""
test_crlibm
===========

Tests for the `crlibm` module.

"""
import unittest


class TestData(object):
    """Class to load test datasets from the CRlibm library."""

    def __init__(self, name):
        import logging
        self.logger = logging.getLogger("testdata parsing")
        self.logger.addHandler(logging.StreamHandler())
        self.name = name

    def open_file(self):
        from os import path
        return open(path.join(
            path.dirname(__file__), '..', 'crlibm',
            'tests', self.name + '.testdata'))

    rounding_modes = {
        'N': '_rn',
        'P': '_ru',
        'M': '_rd',
        'Z': '_rz',
    }

    context_format = """
---
file        : %(f)r
line_number : %(n)r
line        : %(l)r
---"""

    def cases(self):
        """Iterate over the cases in the dataset."""
        import re
        from struct import unpack
        from binascii import unhexlify
        comment_strip = re.compile('#.*')
        strip0x = re.compile('^0x')
        base_function = None

        def fix(s):
            return format(strip0x.sub('', s)).zfill(8)

        with self.open_file() as f:
            for n, line in enumerate(f):
                context = self.context_format % dict(f=f.name, n=n, l=line)
                parsed = comment_strip.sub('', line).strip()
                if not parsed:
                    continue
                if base_function is None:
                    base_function = parsed
                    continue
                try:
                    rm, in_hi, in_lo, out_hi, out_lo = parsed.split()
                    function = base_function + self.rounding_modes[rm]
                    inp, = unpack('>d', unhexlify(fix(in_hi) + fix(in_lo)))
                    out, = unpack('>d', unhexlify(fix(out_hi) + fix(out_lo)))
                    yield function, inp, out, context
                except Exception:
                    self.logger.exception(context)
                    raise


class TestCrlibm(unittest.TestCase):

    expected_functions = (
        'exp expm1 log log1p log2 log10 sinh cosh '
        'sin   cos   tan   asin   acos   atan '
        'sinpi cospi tanpi asinpi acospi atanpi').split()

    def assertCorrect(self, f, x, y, c):
        import crlibm
        z = getattr(crlibm, f)(x)
        if z == y or (z != z and y != y):
            return
        self.fail('{f}({x!r}) == {z!r} != {y!r}{c}'.format(**locals()))

    def test_000_import(self):
        import crlibm
        self.assertNotEqual(crlibm.__doc__, None)

    def test_001_namespace(self):
        import crlibm
        expected_rounding_modes = 'rn ru rd rz'.split()
        expected_symbols = sorted(
            (f + '_' + r)
            for f in self.expected_functions
            for r in expected_rounding_modes)
        exported_symbols = sorted(
            x for x in dir(crlibm) if not x.startswith('_'))
        assert exported_symbols == expected_symbols
        self.assertEqual(exported_symbols, expected_symbols)

    @classmethod
    def add_test_on_dataset(cls, index, name):
        def test(self):
            for f, x, y, c in TestData(name).cases():
                self.assertCorrect(f, x, y, c)
        test.__name__ = 'test_{0:03}_{1}'.format(index, name)
        setattr(cls, test.__name__, test)

    @classmethod
    def add_test_on_all_datasets(cls, base_index):
        for i, f in enumerate(cls.expected_functions):
            cls.add_test_on_dataset(base_index + i, f)

TestCrlibm.add_test_on_all_datasets(2)
