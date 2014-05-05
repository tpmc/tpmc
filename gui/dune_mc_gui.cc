// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifdef HAVE_CONFIG_H
# include "config.h"
#endif

#include <iostream>

#include <dune/common/parallel/mpihelper.hh> // An initializer of MPI
#include <dune/common/exceptions.hh> // We use exceptions

#include <iostream>
#include <wx/wx.h>
#include "mainframe.hh"

class MainApp : public wxApp {
public:
  virtual bool OnInit();
};

IMPLEMENT_APP(MainApp);

bool MainApp::OnInit() {
  int argc = 0;
  char **argv = {};
  Dune::MPIHelper::instance(argc, argv);
  std::cout << "starting dune mc gui\n";
  // parse command line parameters
  std::vector<double> vertex_values;
  for (int i = 1; i<wxApp::argc; ++i) {
    wxCharBuffer buffer = wxString(wxApp::argv[i]).ToUTF8();
    std::stringstream ss(buffer.data());
    double value;
    ss >> value;
    vertex_values.push_back(value);
  }
  const std::size_t N = 2;
  MainFrame<N> *frame;
  frame = new MainFrame<N>(_("Marching Cubes GUI"), vertex_values.begin(), vertex_values.end());
  frame->Show(true);
  return true;
}
