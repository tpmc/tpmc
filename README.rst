TPMC
====

The TPMC library implements a *topology preserving marching cubes*
algorithm.

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

License
-------

The TPMC library, headers and test programs are free open-source
software, dual-licensed under version 3 or later of the GNU Lesser
General Public License and version 2 of the GNU General Public License
with a special run-time exception.

See the file COPYING for full copying permissions.

Installation
------------

The easiest way to install the library is using pip:

::

    > pip install tpmc

This will also install the C++ library

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