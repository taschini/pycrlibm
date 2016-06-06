#!/usr/bin/env python

# Copyright (c) 2015 - 2016, Stefano Taschini <taschini@ieee.org>
# All rights reserved.
# See LICENSE for details.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.core import Extension
from distutils.command.sdist import sdist
from distutils.command.build_ext import build_ext
from distutils.command.upload import upload
from distutils import cygwinccompiler


class Msys2CCompiler(cygwinccompiler.CygwinCCompiler):
    "MSYS2/MinGW-w64 port of GNU C Compiler for MS Windows"

    # Mostly inspired from
    # https://github.com/aleaxit/gmpy/blob/ff2a8cca8e6f6901aa8ebb7e56a5fb19b236aaf0/msys2_build.txt

    compiler_type = 'msys2'

    def __init__(self, verbose=0, dry_run=0, force=0):
        cygwinccompiler.CygwinCCompiler.__init__(self, verbose, dry_run, force)
        shared_option = "-shared" if self.ld_version >= "2.13" else "-mdll -static"
        entry_point = '--entry _DllMain@12' if self.gcc_version <= "2.91.57" else ''
        common_flags = ' -O2 -Wall -fno-strict-aliasing -fwrapv'
        import sys
        if sys.maxsize > 2**32:
            common_flags += ' -DMS_WIN64'
        self.set_executables(compiler     = 'gcc'       + common_flags,
                             compiler_so  = 'gcc -mdll' + common_flags,
                             compiler_cxx = 'g++'       + common_flags,
                             linker_exe='gcc',
                             linker_so='%s %s %s' % (self.linker_dll, shared_option, entry_point))
        self.dll_libraries = []

    def locate_pydll(self):
        import ctypes.util
        import os
        import sys
        dllname = 'python' + ''.join(str(x) for x in sys.version_info[:2])
        dll = ctypes.util.find_library(dllname)
        if dll is None:
            return ''
        dll = dll.lower()
        syswow64 = os.path.join(os.getenv('windir', ''), 'syswow64').lower()
        if dll is not None and sys.maxsize <= 2**32 and os.path.isdir(syswow64):
            dll = dll.replace(os.path.join(os.getenv('windir'), 'system32').lower(), syswow64)
        return dll

    def make_args(self):
        return ['msys2', 'PYTHON_DLL=' + self.locate_pydll()]


def register_msys2ccompiler():
    from distutils import ccompiler
    cygwinccompiler.Msys2CCompiler = Msys2CCompiler
    ccompiler.compiler_class['msys2'] = ('cygwinccompiler', 'Msys2CCompiler', Msys2CCompiler.__doc__.splitlines()[0])
    ccompiler._default_compilers = tuple((plat, cc if cc != 'msvc' else 'msys2') for plat, cc in ccompiler._default_compilers)
register_msys2ccompiler()


class custom_build_ext(build_ext):
    """Build C/C++ extensions with dependencies."""

    def build_extension(self, ext):
        from distutils import log
        log.info("using %s compiler", self.compiler.compiler_type)
        try:
            return build_ext.build_extension(self, ext)
        except Exception:
            import subprocess as sub
            cli = ['make'] + getattr(self.compiler, 'make_args', lambda: ['crlibm-notest'])()
            log.info("invoking: %r", cli)
            sub.call(cli)
            return build_ext.build_extension(self, ext)


class custom_upload(upload):
    """Upload binary package to PyPI with credentials obtained from environment overriding pypirc.

    This is used by Appveyor to upload binary wheels to PyPI.
    """

    def finalize_options(self):
        import os
        upload.finalize_options(self)
        overrides = ((k[5:].lower(), v) for k, v in os.environ.iteritems() if k.startswith('PYPI_'))
        for k, v in overrides:
            setattr(self, k, v)


def read_long_description():
    import io
    parts = []
    for filename in 'README.rst', 'CHANGES.rst':
        with io.open(filename, encoding='utf-8') as f:
            parts.append(f.read())
    return '\n'.join(parts)


metadata = dict(
    author           = "Stefano Taschini",
    author_email     = 'taschini@gmail.com',
    cmdclass         = {'sdist': sdist, 'build_ext': custom_build_ext, 'upload': custom_upload},
    description      = "Python bindings for CRlibm, an efficient and proven correctly-rounded mathematical library",
    install_requires = [],
    keywords         = 'crlibm',
    license          = "LGPLv2+",
    long_description = read_long_description(),
    name             = 'crlibm',
    platforms        = '',
    test_suite       = 'tests',
    tests_require    = [],
    url              = 'https://github.com/taschini/pycrlibm',
    version          = '1.0.2',
    zip_safe         = False,
    ext_modules=[
        Extension(
            'crlibm',
            sources      = ['ext/crlibmmodule.c'],
            include_dirs = ['build/crlibm/include'],
            library_dirs = ['build/crlibm/lib'],
            libraries    = ['crlibm'])
    ],
    extras_require={
        'develop': [
            'Sphinx',
            'flake8',
            'tox',
            'zest.releaser[recommended]',
        ]
    },
    classifiers=[
        # A subset of http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)

if __name__ == '__main__':
    setup(**metadata)
