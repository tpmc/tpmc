// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef GEOMETRYPANEL_HH_
#define GEOMETRYPANEL_HH_

#include <wx/wx.h>
#include <wx/panel.h>
#include "marchingcubesgui.hh"
#include "mainframe.hh"
#include "geometrycontainer.hh"
#include "python.hh"

template <std::size_t N>
class GeometryPanel : public wxPanel {
public:
  typedef typename MarchingCubesGUI<N>::VectorType VectorType;
  GeometryPanel(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame, wxPanel *parent);
  void OnAdd(wxCommandEvent& event);
  void updateInterfaceList();
  void updateInteriorList();
  void updateExteriorList();
private:
  MarchingCubesGUI<N> *mGui;
  MainFrame<N> *mParentFrame;
  wxTextCtrl* mPatternText;
  wxListBox* mInterfaceList;
  wxListBox* mInteriorList;
  wxListBox* mExteriorList;
  wxComboBox* mTypeCombo;

  static const int GP_ADD = 300;
  static const int GP_PATTERN = 301;
};


template <std::size_t N>
GeometryPanel<N>::GeometryPanel(MarchingCubesGUI<N> *gui,
                                MainFrame<N> *parentFrame,
                                wxPanel *parent)
  : wxPanel(parent, -1, wxPoint(-1, -1), wxSize(-1, -1)),
    mGui(gui), mParentFrame(parentFrame) {
  wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
  wxStaticText *label = new wxStaticText(this, wxID_ANY, _("Add Element:"));
  int twidth = 200;
  mPatternText = new wxTextCtrl(this, GP_PATTERN, _(""), wxDefaultPosition, wxDefaultSize,
                                wxTE_PROCESS_ENTER);
  Connect(GP_PATTERN, wxEVT_COMMAND_TEXT_ENTER,
          wxCommandEventHandler(GeometryPanel::OnAdd));
  mPatternText->SetMinSize(wxSize(twidth,-1));
  mPatternText->SetMaxSize(wxSize(twidth,-1));
  wxString choices[] = {_("Interior"), _("Exterior"), _("Interface")};
  mTypeCombo = new wxComboBox(this, wxID_ANY, _(""), wxDefaultPosition, wxDefaultSize, 3, choices, wxCB_READONLY);
  mTypeCombo->SetValue(choices[0]);
  wxButton *addButton = new wxButton(this, GP_ADD, _("Add"), wxPoint(20,20));
  Connect(GP_ADD, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnAdd));
  wxStaticText *interfaceLabel = new wxStaticText(this, wxID_ANY, _("Interface:"));
  mInterfaceList = new wxListBox(this, wxID_ANY);
  mInterfaceList->SetMinSize(wxSize(twidth,100));
  mInterfaceList->SetMaxSize(wxSize(twidth,-1));
  updateInterfaceList();
  wxStaticText *interiorLabel = new wxStaticText(this, wxID_ANY, _("Interior:"));
  mInteriorList = new wxListBox(this, wxID_ANY);
  mInteriorList->SetMinSize(wxSize(twidth,100));
  mInteriorList->SetMaxSize(wxSize(twidth,-1));
  updateInteriorList();
  wxStaticText *exteriorLabel = new wxStaticText(this, wxID_ANY, _("Exterior:"));
  mExteriorList = new wxListBox(this, wxID_ANY);
  mExteriorList->SetMinSize(wxSize(twidth,100));
  mExteriorList->SetMaxSize(wxSize(twidth,-1));
  updateExteriorList();
  vbox->Add(label, 0, wxTOP, 5);
  vbox->Add(mPatternText, 0, wxTOP, 5);
  vbox->Add(mTypeCombo, 0, wxTOP, 5);
  vbox->Add(addButton, 0, wxTOP, 5);
  vbox->Add(interfaceLabel, 0, wxTOP, 5);
  vbox->Add(mInterfaceList, 0, wxTOP, 5);
  vbox->Add(interiorLabel, 0, wxTOP, 5);
  vbox->Add(mInteriorList, 0, wxTOP, 5);
  vbox->Add(exteriorLabel, 0, wxTOP, 5);
  vbox->Add(mExteriorList, 0, wxTOP, 5);
  this->SetSizer(vbox);
}

template <std::size_t N>
void GeometryPanel<N>::OnAdd(wxCommandEvent& event) {
  std::stringstream s;
  s << mPatternText->GetValue().mb_str();
  mPatternText->Clear();
  std::cout << "s: " << mTypeCombo->GetSelection() << " string: " << s.str() << "\n";
  try {
    switch (mTypeCombo->GetSelection()) {
    case 0 : mGui->addGeometryElement(s.str(), MarchingCubesGUI<N>::INTERIOR); updateInteriorList(); break;
    case 1 : mGui->addGeometryElement(s.str(), MarchingCubesGUI<N>::EXTERIOR); updateExteriorList(); break;
    case 2 : mGui->addGeometryElement(s.str(), MarchingCubesGUI<N>::INTERFACE); updateInterfaceList(); break;
    default : mGui->addGeometryElement(s.str(), MarchingCubesGUI<N>::INTERIOR); updateInteriorList(); break;
    }
  } catch (Dune::Exception& e) {
    // print some error
  }
}

template <std::size_t N>
void GeometryPanel<N>::updateInterfaceList() {
  mInterfaceList->Clear();
  typedef typename MarchingCubesGUI<N>::geo_iterator Iterator;
  typedef typename MarchingCubesGUI<N>::GeoContainer GC;
  Iterator itend = mGui->geometryContainer().geoend(GC::INTERFACE);
  for (Iterator it = mGui->geometryContainer().geobegin(GC::INTERFACE); it != itend; ++it) {
    std::stringstream s;
    s << PythonAdapter<double, 3>(*it);
    mInterfaceList->Append(wxString(s.str().c_str(), wxConvUTF8));
  }
}

template <std::size_t N>
void GeometryPanel<N>::updateInteriorList() {
  mInteriorList->Clear();
  typedef typename MarchingCubesGUI<N>::geo_iterator Iterator;
  typedef typename MarchingCubesGUI<N>::GeoContainer GC;
  Iterator itend = mGui->geometryContainer().geoend(GC::INTERIOR);
  for (Iterator it = mGui->geometryContainer().geobegin(GC::INTERIOR); it != itend; ++it) {
    std::stringstream s;
    s << PythonAdapter<double, 3>(*it);
    mInteriorList->Append(wxString(s.str().c_str(), wxConvUTF8));
  }
}

template <std::size_t N>
void GeometryPanel<N>::updateExteriorList() {
  mExteriorList->Clear();
  typedef typename MarchingCubesGUI<N>::geo_iterator Iterator;
  typedef typename MarchingCubesGUI<N>::GeoContainer GC;
  Iterator itend = mGui->geometryContainer().geoend(GC::EXTERIOR);
  for (Iterator it = mGui->geometryContainer().geobegin(GC::EXTERIOR); it != itend; ++it) {
    std::stringstream s;
    s << PythonAdapter<double, 3>(*it);
    mExteriorList->Append(wxString(s.str().c_str(), wxConvUTF8));
  }
}


#endif //GEOMETRYPANEL_HH_
