# $Id: duneproject 5370 2008-11-15 17:43:24Z christi $

SUBDIRS = lut

check: all

check_PROGRAMS=testmc33
testmc33_SOURCES=testmc33.cc marchingcubes.hh thresholdfunctor.cc
testmc33_CPPFLAGS=$(AM_CPPFLAGS) -g -Wall -O0
testmc33_LDFLAGS=-Llut -lmclut
testmc33_DEPENDENCIES = lut/libmclut.la

TESTS=$(check_PROGRAMS)

include $(top_srcdir)/am/global-rules

