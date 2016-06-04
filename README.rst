PyCRlibm - Python bindings for CRlibm
=====================================

.. container:: badges

   .. image:: https://img.shields.io/travis/taschini/pycrlibm/master.svg?label=Linux%20build
      :target: https://travis-ci.org/taschini/pycrlibm
      :alt: Travis CI build status (Linux)

   .. image:: https://img.shields.io/appveyor/ci/taschini/pycrlibm/master.svg?label=Windows%20build
      :target: https://ci.appveyor.com/project/taschini/pycrlibm
      :alt: AppVeyor CI build status (Windows)

   .. image:: https://img.shields.io/pypi/v/crlibm.svg
      :target: https://pypi.python.org/pypi/crlibm/
      :alt: Latest PyPI version

   .. image:: https://readthedocs.org/projects/pycrlibm/badge/?version=latest
      :target: http://pycrlibm.readthedocs.org/?badge=latest
      :alt: Documentation Status

Python bindings for `CRlibm
<http://lipforge.ens-lyon.fr/www/crlibm>`_, an efficient and proven
correctly-rounded mathematical library.

CRlibm is a free mathematical library (libm) which provides:

* implementations of the double-precision C99 standard elementary
  functions,

* correctly rounded in the four IEEE-754 rounding modes,

* with a comprehensive proof of both the algorithms used and their
  implementation,

* sufficiently efficient in average time, worst-case time, and
  memory consumption to replace existing libms transparently.

Installation
------------

At the command line::

    $ pip install crlibm

On Microsoft Windows ``pip`` will try first to download a binary
archive in *wheel* format, and if no such a *wheel* can be found for
your Python version, ``pip`` will try to compile the library.  In
order to do so, it is strongly recommended to have `MinGW-w64
<http://mingw-w64.org>`_ installed under `MSYS2
<https://msys2.github.io>`_, for instance by following the
instructions in `<http://stackoverflow.com/a/30071634>`_.


Usage
-----

In Python::

    >>> import crlibm
    >>> crlibm.exp_ru(1)
    2.7182818284590455

    >>> crlibm.exp_rd(1)
    2.718281828459045

Features
--------

* This project provides the bindings for the functions in the following table:

+----------------+------------------+------------------+--------------------+------------+
| f(x)           | Round to nearest | Round up (to +∞) | Round down (to -∞) | Round to 0 |
+----------------+------------------+------------------+--------------------+------------+
|              **Exponentials and logarithms**                                           |
+----------------+------------------+------------------+--------------------+------------+
| exp(x)         | exp_rn           | exp_ru           | exp_rd             | exp_rz     |
+----------------+------------------+------------------+--------------------+------------+
| exp(x)-1       | expm1_rn         | expm1_ru         | expm1_rd           | expm1_rz   |
+----------------+------------------+------------------+--------------------+------------+
| log(x)         | log_rn           | log_ru           | log_rd             | log_rz     |
+----------------+------------------+------------------+--------------------+------------+
| log(1+x)       | log1p_rn         | log1p_ru         | log1p_rd           | log1p_rz   |
+----------------+------------------+------------------+--------------------+------------+
| log(x)/log(2)  | log2_rn          | log2_ru          | log2_rd            | log2_rz    |
+----------------+------------------+------------------+--------------------+------------+
| log(x)/log(10) | log10_rn         | log10_ru         | log10_rd           | log10_rz   |
+----------------+------------------+------------------+--------------------+------------+
| sinh(x)        | sinh_rn          | sinh_ru          | sinh_rd            | sinh_rz    |
+----------------+------------------+------------------+--------------------+------------+
| cosh(x)        | cosh_rn          | cosh_ru          | cosh_rd            | cosh_rz    |
+----------------+------------------+------------------+--------------------+------------+
|              **Trigonometry**                                                          |
+----------------+------------------+------------------+--------------------+------------+
| sin(x)         | sin_rn           | sin_ru           | sin_rd             | sin_rz     |
+----------------+------------------+------------------+--------------------+------------+
| cos(x)         | cos_rn           | cos_ru           | cos_rd             | cos_rz     |
+----------------+------------------+------------------+--------------------+------------+
| tan(x)         | tan_rn           | tan_ru           | tan_rd             | tan_rz     |
+----------------+------------------+------------------+--------------------+------------+
| asin(x)        | asin_rn          | asin_ru          | asin_rd            | asin_rz    |
+----------------+------------------+------------------+--------------------+------------+
| acos(x)        | acos_rn          | acos_ru          | acos_rd            | acos_rz    |
+----------------+------------------+------------------+--------------------+------------+
| atan(x)        | atan_rn          | atan_ru          | atan_rd            | atan_rz    |
+----------------+------------------+------------------+--------------------+------------+
|              **Trigonometry in multiples of π**                                        |
+----------------+------------------+------------------+--------------------+------------+
| sin(π * x)     | sinpi_rn         | sinpi_ru         | sinpi_rd           | sinpi_rz   |
+----------------+------------------+------------------+--------------------+------------+
| cos(π * x)     | cospi_rn         | cospi_ru         | cospi_rd           | cospi_rz   |
+----------------+------------------+------------------+--------------------+------------+
| tan(π * x)     | tanpi_rn         | tanpi_ru         | tanpi_rd           | tanpi_rz   |
+----------------+------------------+------------------+--------------------+------------+
| asin(x)/π      | asinpi_rn        | asinpi_ru        | asinpi_rd          | asinpi_rz  |
+----------------+------------------+------------------+--------------------+------------+
| acos(x)/π      | acospi_rn        | acospi_ru        | acospi_rd          | acospi_rz  |
+----------------+------------------+------------------+--------------------+------------+
| atan(x)/π      | atanpi_rn        | atanpi_ru        | atanpi_rd          | atanpi_rz  |
+----------------+------------------+------------------+--------------------+------------+


* The function ``pow`` in CRlibm is not exported.


License
-------

Both the CRlibm library and the Python bindings are distributed under
the GNU Lesser General Public License as published by the Free
Software Foundation; either version `2.1
<http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>`_ of the
License, or (at your option) any later version.

Authors
-------

David Defour, Catherine Daramy, Florent de Dinechin,
Matthieu Gallet, Nicolas Gast, Christoph Lauter, Jean-Michel Muller.

Python bindings by Stefano Taschini.

Links
-----

* Project home page: https://github.com/taschini/pycrlibm.
* Documentation: https://pycrlibm.readthedocs.io.
* Entry in the Python Package Index: https://pypi.python.org/pypi/crlibm.
* CRlibm home page: http://lipforge.ens-lyon.fr/www/crlibm.
* LGPL v2.1: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
