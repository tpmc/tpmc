# $Id: $

# the dune-mc library
lib_LTLIBRARIES = libdunemc.la

# this is just a renaming of libmc to prevent name clashes
libdunemc_la_SOURCES =
# This forces automake to use the C++ linker
# (see the automake manual, section "Libtool Convenience Libraries")
nodist_EXTRA_libdunemc_la_SOURCES = dummy.cc
sourcescheck_DUMMY = dummy.cc
libdunemc_la_LIBADD = ../dune/marchingcubes/lut/libmclut.la

include $(top_srcdir)/am/global-rules
