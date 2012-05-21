// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __MAINFRAME_HH__
#define __MAINFRAME_HH__

#include <wx/wx.h>
#include "marchingcubesgui.hh"
#include "mccanvas.hh"
#include "ctlpanel.hh"
#include "viewpanel.hh"

template <std::size_t N>
class MainFrame : public wxFrame {
public:
  MainFrame(const wxString& title);
  bool getShowInterface(std::size_t i) const { return mShowInterface[i]; }
  void setShowInterface(std::size_t i, bool v) { mShowInterface[i] = v; }
  bool getShowCube() const { return mShowCube; }
  void setShowCube(bool v) { mShowCube = v; }
  bool getShowPlane() const { return mShowPlane; }
  void setShowPlane(bool v) { mShowPlane = v; }
  bool getShowFaceCenter() const { return mShowFaceCenter; }
  void setShowFaceCenter(bool v) { mShowFaceCenter = v; }
  void resetView() { mccanvas->resetView(); }
private:
  static const int ID_CANVAS = 701;
  bool mShowInterface[N];
  bool mShowCube;
  bool mShowFaceCenter;
  bool mShowPlane;
  MarchingCubesGUI<N> mGui;
  MCCanvas<N> *mccanvas;
};

template <std::size_t N>
MainFrame<N>::MainFrame(const wxString& title)
  : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(1000,800)),
    mShowCube(true), mShowFaceCenter(false), mShowPlane(false) {
  std::fill(mShowInterface, mShowInterface+N, true);

  wxPanel *panel = new wxPanel(this, -1);
  //GLPanel *glpanel = new GLPanel(panel);
  mccanvas = new MCCanvas<N>(&mGui, this, panel, ID_CANVAS);
  CtlPanel<N> *ctlpanel = new CtlPanel<N>(&mGui, this, panel);
  ViewPanel<N> *viewpanel = new ViewPanel<N>(&mGui, this, panel);

  wxBoxSizer *hbox = new wxBoxSizer(wxHORIZONTAL);
  wxBoxSizer *vboxl = new wxBoxSizer(wxVERTICAL);
  wxBoxSizer *vboxr = new wxBoxSizer(wxVERTICAL);

  vboxl->Add(viewpanel, 0, wxBOTTOM, 10);
  vboxl->Add(mccanvas, 1, wxEXPAND | wxALL, 0);
  vboxr->Add(ctlpanel, 0, wxBOTTOM, 5);
  hbox->Add(vboxl, 1, wxEXPAND | wxALL, 10);
  hbox->Add(vboxr, 0, wxALL, 10);

  panel->SetSizer(hbox);

  Centre();
}


#endif //__MAINFRAME_HH__
