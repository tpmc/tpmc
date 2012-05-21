// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __PLANECANVAS_HH__
#define __PLANECANVAS_HH__

#include "wxsfmlcanvas.h"
#include "marchingcubesgui.hh"

template <std::size_t N>
class PlaneCanvas : public wxSFMLCanvas {
public:
  PlaneCanvas(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame,
              wxWindow* Parent = NULL, wxWindowID Id = -1,
              const wxPoint& Position = wxDefaultPosition,
              const wxSize& Size = wxDefaultSize,
              long Style = 0);
  virtual ~PlaneCanvas() {}
private:
  MarchingCubesGUI<N> *mGui;
  MainFrame<N> *mParentFrame;

  virtual void OnUpdate();
  void drawGrid();
  void drawBorder();
};

template <std::size_t N>
PlaneCanvas<N>::PlaneCanvas(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame,
                            wxWindow* Parent, wxWindowID Id,
                            const wxPoint& Position,
                            const wxSize& Size,
                            long Style)
  : wxSFMLCanvas(Parent, Id, Position, Size, Style),
    mGui(gui), mParentFrame(parentFrame) {

  glClearDepth(1.f);
  glClearColor(0.f, 1.f, 0.f, 0.f);
  glEnable(GL_DEPTH_TEST);
  glDepthMask(GL_TRUE);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(-0.1,1.1,-0.1,1.1);
}

template <std::size_t N>
void PlaneCanvas<N>::OnUpdate() {
  SetActive();
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  drawGrid();
}

template <std::size_t N>
void PlaneCanvas<N>::drawGrid() {
  glColor3f(0.f, 0.f, 0.f);
  drawBorder();
}

template <std::size_t N>
void PlaneCanvas<N>::drawBorder() {
  glBegin(GL_LINE_LOOP);
  glVertex2f(0.f, 0.f);
  glVertex2f(0.f, 1.f);
  glVertex2f(1.f, 1.f);
  glVertex2f(1.f, 0.f);
  glEnd();
}

#endif //__PLANECANVAS_HH__
