# $Id: duneproject 5370 2008-11-15 17:43:24Z christi $

check: all

check_PROGRAMS=testmc33 testmarchingcubesrefinement

testmc33_SOURCES=testmc33.cc
testmc33_CPPFLAGS=$(AM_CPPFLAGS) -g -Wall -O0
testmc33_LDFLAGS=-L$(top_srcdir)/dune/marchingcubes/lut -lmclut
testmc33_DEPENDENCIES = $(top_srcdir)/dune/marchingcubes/lut/libmclut.la

testmarchingcubesrefinement_SOURCES=testmarchingcubesrefinement.cc
testmarchingcubesrefinement_CPPFLAGS=$(AM_CPPFLAGS) -g -Wall -O0
testmarchingcubesrefinement_LDFLAGS=-L$(top_srcdir)/dune/marchingcubes/lut -lmclut
testmarchingcubesrefinement_DEPENDENCIES = $(top_srcdir)/dune/marchingcubes/lut/libmclut.la

TESTS=$(check_PROGRAMS)

include $(top_srcdir)/am/global-rules

