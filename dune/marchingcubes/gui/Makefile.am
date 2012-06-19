
SUBDIRS =

if GUI

noinst_PROGRAMS = dune_mc_gui

dune_mc_gui_SOURCES = dune_mc_gui.cc ctlpanel.hh geometries.hh \
	geometrycontainer.hh geometrypanel.hh geometryparser.hh \
	glshapes.hh mainframe.hh \
	marchingcubescontainer.hh marchingcubesgui.hh \
	mccanvas.hh origincenteredcamera.hh planefunctor.hh python.hh \
	triangulation.hh trilinearfunctor.hh viewpanel.hh wxsfmlcanvas.cpp

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
	$(GL_LIBS) -lGLU
dune_mc_gui_LDFLAGS = $(AM_LDFLAGS) \
	$(DUNEMPILDFLAGS) \
	-L$(top_srcdir)/dune/marchingcubes/lut -lmclut \
	$(DUNE_LDFLAGS)
dune_mc_gui_DEPENDENCIES = $(top_srcdir)/dune/marchingcubes/lut/libmclut.la

endif # GUI

include $(top_srcdir)/am/global-rules

