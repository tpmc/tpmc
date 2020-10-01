TPMC
====
.. image:: https://img.shields.io/badge/License-GPL%20v3-yellow.svg
  :target: https://opensource.org/licenses
		   
.. image:: https://img.shields.io/github/v/release/tpmc/tpmc
  :target: https://github.com/tpmc/tpmc

.. image:: https://img.shields.io/travis/com/tpmc/tpmc-test?label=build%20tpmc
  :target: https://travis-ci.com/github/tpmc/tpmc
		   
.. image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InRwbWMiLCJyZXBvMSI6InRwbWMiLCJpbmNsdWRlTGludCI6ZmFsc2UsImF1dGhvcklkIjoxNTg3OSwiaWF0IjoxNjAxNTgwNTU2fQ.YUDLEgIwVyoEN5zB5TDLqhsnsbUBuJEYEhDP_WhFwxg
  :target: https://www.deepcode.ai/app/gh/tpmc/tpmc/_/dashboard?utm_content=gh%2Ftpmc%2Ftpmc
		   
.. image:: https://img.shields.io/travis/com/tpmc/tpmc-test?label=build%20tpmc-test
  :target: https://travis-ci.com/github/tpmc/tpmc-test

The TPMC library implements a *topology preserving marching cubes*
algorithm, see [EN2017]_.

The algorithm alows to compute polyhedral reconstructions of implicitly
given interfaces and subdomains. In particular it is used to
geometrically evaluate integrals over domains described by a fist-order,
conforming level-set function. It preserves various topological
properties of the implicit geometry in its polyhedral reconstruction,
making it suitable for Finite Element computations.

The main part of the algorithm is a code generator written in python.
With the library we ship the code generator and a simple C++
implementation. The code is generated and the C++ library is build
during the installation process.

.. [EN2017] Engwer, C., & Nüßing, A. (2017). Geometric reconstruction of implicitly defined surfaces and domains with topological guarantees. ACM TOMS, 44(2), 1-20, `doi:10.1145`1_, `arxiv preprint`2_.

.. _1: https://doi.org/10.1145
.. _2: https://arxiv.org/abs/1601.03597

License
-------

The TPMC library, headers and test programs are free open-source
software, dual-licensed under version 3 or later of the GNU Lesser
General Public License and version 2 of the GNU General Public License
with a special run-time exception.

See the file LICENSE.txt for full copying permissions.

Installation
------------

The easiest way to install the library is using pip:

::

    > pip install tpmc

This will also install the C++ library

The development version can always be installed directly from github:

::

    > pip install git+https://github.com/tpmc/tpmc.git

Dependencies
~~~~~~~~~~~~

While most python dependencies are handled automatically, you have to
make sure to fulfill two additional requirements, before installation:

- `numpy <http://www.numpy.org/>`__: is needed for setup and thus pip
  can not handle this dependency automatically

- C++ compiler: to build the C++ library. We successfully used recent
  versions of g++ and clang++.

Using the C++ library
~~~~~~~~~~~~~~~~~~~~~

To use the C++ library from your own code, you can either use ``cmake``
and the ``FindTpmc.cmake`` that we ship with the python package, or you
use the ``tpmc-config`` program, which can give you information about
the necessary compiler flags. It behaves similar to ``pkg-config``.
