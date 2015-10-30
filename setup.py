#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.core import Extension
from distutils.command.sdist import sdist
from distutils.command.build_ext import build_ext
from distutils import cygwinccompiler

class Msys2CCompiler (cygwinccompiler.CygwinCCompiler):
    # From https://github.com/aleaxit/gmpy/blob/ff2a8cca8e6f6901aa8ebb7e56a5fb19b236aaf0/msys2_build.txt

    compiler_type = 'msys2'

    def __init__ (self, verbose=0, dry_run=0, force=0):
        cygwinccompiler.CygwinCCompiler.__init__ (self, verbose, dry_run, force)
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
        self.dll_libraries=[]

@apply
def register_msys2ccompiler():
    from distutils.ccompiler import compiler_class
    cygwinccompiler.Msys2CCompiler = Msys2CCompiler
    compiler_class['msys2'] = ('cygwinccompiler', 'Msys2CCompiler', "MSYS2/MinGW-w64 port of GNU C Compiler for MS Windows")
    return 'Done'


class custom_build_ext(build_ext):
    """Build C/C++ extensions with dependencies."""

    def build_extension(self, ext):
        try:
            return build_ext.build_extension(self, ext)
        except Exception as ex:
            import subprocess as sub
            sub.call('make crlibm-notest'.split())
            return build_ext.build_extension(self, ext)

@apply
def readme():
    with open('README.rst') as readme_file:
        return readme_file.read().decode('utf8')

# A subset of http://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Scientific/Engineering :: Mathematics'
]

metadata = dict(
    author           = "Stefano Taschini",
    author_email     = 'taschini@gmail.com',
    classifiers      = classifiers,
    description      = "Python bindings for CRlibm, an efficient and proven correctly-rounded mathematical library",
    keywords         = 'crlibm',
    license          = "LGPLv2+",
    long_description = readme,
    platforms        = '',
    url              = 'https://github.com/taschini/crlibm',
)


data = dict(
    name             = 'crlibm',
    version          = '1.0.0',
    install_requires = [],
    test_suite       = 'tests',
    tests_require    = [],
    cmdclass         = {'sdist': sdist, 'build_ext': custom_build_ext},
    ext_modules      = [
        Extension(
            'crlibm',
            sources      = ['ext/crlibmmodule.c'],
            include_dirs = ['build/crlibm/include'],
            library_dirs = ['build/crlibm/lib'],
            libraries    = ['crlibm'])
        ],
    **metadata
)

if __name__ == '__main__':
    setup(**data)
