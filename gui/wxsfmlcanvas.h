// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __WXSFMLCANVAS_HH__
#define __WXSFMLCANVAS_HH__

#include <SFML/Graphics.hpp>
#include <wx/wx.h>

class wxSFMLCanvas : public wxControl, public sf::RenderWindow {
public:
  wxSFMLCanvas(wxWindow* Parent = NULL, wxWindowID Id = -1,
               const wxPoint& Position = wxDefaultPosition,
               const wxSize& Size = wxDefaultSize, long Style = 0);
  virtual ~wxSFMLCanvas();
private:

  DECLARE_EVENT_TABLE()

  virtual void OnUpdate();
  virtual void OnKeyDown(wxKeyEvent&);
  virtual void OnKeyUp(wxKeyEvent&);
  void OnIdle(wxIdleEvent&);
  void OnPaint(wxPaintEvent&);
  void OnEraseBackground(wxEraseEvent&);
};

#endif //__WXSFMLCANVAS_HH__
