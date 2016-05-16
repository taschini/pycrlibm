"""
test_docs
===========

Verify the code examples on all reStructuredText files in the project.

"""


def rst_files():
    import os
    root = os.path.join(os.path.dirname(__file__), '..')

    def prune(p, d):
        return d.startswith('.') or (p == root and d != 'docs')

    def filter(p, f):
        return f.endswith('.rst')

    for (dirpath, dirnames, filenames) in os.walk(root):
        dirnames[:] = [d for d in dirnames if not prune(dirpath, d)]
        filenames = [f for f in filenames if filter(dirpath, f)]
        for f in filenames:
            yield os.path.join(dirpath, f)


def load_tests(loader, tests, pattern):
    # The load_tests protocol has been introduced in Python 2.7, so
    # doctests will be skipped on earlier Pythons.  This is an
    # advantage in this case, as changes in float.__repr__ would break
    # doctests anyway.
    import doctest
    import unittest
    s = unittest.TestSuite()
    s.addTest(doctest.DocFileSuite(module_relative=False, *rst_files()))
    return s
