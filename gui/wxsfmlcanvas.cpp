// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include "wxsfmlcanvas.h"

#ifdef __WXGTK__
#include <gdk/gdkx.h>
#include <gtk/gtk.h>
#include <wx/gtk/win_gtk.h>
#endif

#include <SFML/Window.hpp>

BEGIN_EVENT_TABLE(wxSFMLCanvas, wxControl)
EVT_IDLE(wxSFMLCanvas::OnIdle)
EVT_PAINT(wxSFMLCanvas::OnPaint)
EVT_ERASE_BACKGROUND(wxSFMLCanvas::OnEraseBackground)
EVT_KEY_DOWN(wxSFMLCanvas::OnKeyDown)
EVT_KEY_UP(wxSFMLCanvas::OnKeyUp)
END_EVENT_TABLE()

void wxSFMLCanvas::OnIdle(wxIdleEvent&) {
  Refresh();
}

void wxSFMLCanvas::OnPaint(wxPaintEvent&) {
  wxPaintDC Dc(this);
  OnUpdate();
#if SFML_VERSION_MAJOR >= 2
  display();
#else
  Display();
#endif
}

void wxSFMLCanvas::OnKeyDown(wxKeyEvent&) {}

void wxSFMLCanvas::OnKeyUp(wxKeyEvent&) {}

void wxSFMLCanvas::OnUpdate() {}

wxSFMLCanvas::~wxSFMLCanvas() {}

void wxSFMLCanvas::OnEraseBackground(wxEraseEvent&) {}

wxSFMLCanvas::wxSFMLCanvas(wxWindow* Parent, wxWindowID Id, const wxPoint& Position, const wxSize& Size, long Style) :
  wxControl(Parent, Id, Position, Size, Style)
{
    #ifdef __WXGTK__

  // GTK implementation requires to go deeper to find the
  // low-level X11 identifier of the widget
  gtk_widget_realize(m_wxwindow);
  gtk_widget_set_double_buffered(m_wxwindow, false);
  GdkWindow* Win = GTK_PIZZA(m_wxwindow)->bin_window;
  XFlush(GDK_WINDOW_XDISPLAY(Win));
      #if SFML_VERSION_MAJOR >= 2
  sf::RenderWindow::create(GDK_WINDOW_XWINDOW(Win));
      #else
  sf::RenderWindow::Create(GDK_WINDOW_XWINDOW(Win));
      #endif

    #else

  // Tested under Windows XP only (should work with X11
  // and other Windows versions - no idea about MacOS)
      #if SFML_VERSION_MAJOR >= 2
  sf::RenderWindow::Create(GetHandle());
      #else
  sf::RenderWindow::create(GetHandle());
      #endif

    #endif
}
