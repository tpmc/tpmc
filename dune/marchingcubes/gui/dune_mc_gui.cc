// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifdef HAVE_CONFIG_H
# include "config.h"
#endif

#include <iostream>
#include "dune/common/mpihelper.hh" // An initializer of MPI
#include "dune/common/exceptions.hh" // We use exceptions

#include <iostream>
#include <wx/wx.h>
#include "mainframe.hh"

class MainApp : public wxApp {
public:
  virtual bool OnInit();
};

IMPLEMENT_APP(MainApp);

bool MainApp::OnInit() {
  const std::size_t N = 2;
  MainFrame<N> *frame = new MainFrame<N>(_("Marchings Cubes GUI"));
  frame->Show(true);
  return true;
}
