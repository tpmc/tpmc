
SUBDIRS =

noinst_PROGRAMS = dune_mc_gui

dune_mc_gui_SOURCES = dune_mc_gui.cc \
	wxsfmlcanvas.cpp

dune_mc_gui_CPPFLAGS = $(AM_CPPFLAGS) \
	$(DUNEMPICPPFLAGS) \
	$(GTK_CFLAGS) \
	$(WX_CPPFLAGS)
# The libraries have to be given in reverse order (most basic libraries
# last).  Also, due to some misunderstanding, a lot of libraries include the
# -L option in LDFLAGS instead of LIBS -- so we have to include the LDFLAGS
# here as well.
dune_mc_gui_LDADD = \
	$(DUNE_LDFLAGS) $(DUNE_LIBS) \
	$(DUNEMPILIBS)	\
	$(GTK_LIBS) \
	$(WX_LIBS) \
	-lsfml-system -lsfml-window -lsfml-graphics \
	$(GL_LIBS) -lGLU \
	$(LDADD)
dune_mc_gui_LDFLAGS = $(AM_LDFLAGS) \
	$(DUNEMPILDFLAGS) \
	$(DUNE_LDFLAGS)

# don't follow the full GNU-standard
# we need automake 1.5
AUTOMAKE_OPTIONS = foreign 1.5

# pass most important options when "make distcheck" is used
DISTCHECK_CONFIGURE_FLAGS = --with-dune-common=$(DUNE_COMMON_ROOT) --with-dune-grid=$(DUNE_GRID_ROOT) --with-dune-mc=$(DUNE_MC_ROOT)  CXX="$(CXX)" CC="$(CC)"

include $(top_srcdir)/am/global-rules

