# $Id: duneproject 5370 2008-11-15 17:43:24Z christi $

SUBDIRS = lut

check_PROGRAMS=testmc33
testmc33_SOURCES=testmc33.cc marchingcubes.hh thresholdfunctor.cc
testmc33_LDFLAGS=-Llut -lmclut

TESTS=$(check_PROGRAMS)

include $(top_srcdir)/am/global-rules

