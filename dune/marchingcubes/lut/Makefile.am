# $Id: duneproject 5370 2008-11-15 17:43:24Z christi $

lib_LTLIBRARIES = libmclut.la

libmclut_la_SOURCES = marchinglut.cc

marchinglut.cc: generate_lut.py
	./generate_lut.py

include $(top_srcdir)/am/global-rules

