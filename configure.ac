# -*- Autoconf -*-
# $Id$
# Process this file with autoconf to produce a configure script.

DUNE_AC_INIT # gets module version from dune.module file
AM_INIT_AUTOMAKE
AC_CONFIG_SRCDIR([dune/marchingcubes/marchingcubes.hh])
AM_CONFIG_HEADER([config.h])

# we need no more than the standard DE-stuff
# this module depends on dune-common
# this implies checking for [dune-common]
DUNE_CHECK_ALL

# stuff for gui program
# install libwxgtk2.X-dev
AM_OPTIONS_WXCONFIG
reqwx=2.4.0
AM_PATH_WXCONFIG($reqwx, wxWin=1)
# install libgtk2.0-dev
PKG_CHECK_MODULES(GTK, [gdk-x11-2.0], [
  have_gtk=1
], [
  have_gtk=0
])
AC_LANG_PUSH([C++])
# install libsfml-dev
AC_CHECK_HEADER([SFML/Graphics.hpp],[
  have_sfml=1
],[
  have_sfml=0
])
AC_LANG_POP

AM_CONDITIONAL(GUI, [true])
if test "$wxWin" != 1 -o "$have_gtk" != 1 -o "$have_sfml" != 1; then
  AC_MSG_WARN(not building the gui)
  AM_CONDITIONAL(GUI, [false])
fi


# implicitly set the Dune-flags everywhere
AC_SUBST(AM_CPPFLAGS, '$(DUNE_CPPFLAGS) -I$(top_srcdir)')
AC_SUBST(AM_LDFLAGS, $DUNE_LDFLAGS)
AC_SUBST([LDADD], '$(top_builddir)/lib/libdunemc.la')
LIBS="$DUNE_LIBS"

AC_CONFIG_FILES([
  Makefile
  m4/Makefile
  doc/Makefile
  doc/doxygen/Makefile
  dune/Makefile
  dune/marchingcubes/Makefile
  dune/marchingcubes/test/Makefile
  dune/marchingcubes/lut/Makefile
  dune/marchingcubes/gui/Makefile
  lib/Makefile
  doc/doxygen/Doxyfile
  dune-mc.pc
])
AC_OUTPUT
# finally print the summary information
DUNE_SUMMARY_ALL
