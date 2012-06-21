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
  typedef typename MarchingCubesGUI<N>::GeoContainer GeoContainer;
  typedef typename GeoContainer::TriangulationType TriangulationType;
  GeometryPanel(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame, wxPanel *parent);
  void OnAdd(wxCommandEvent& event);
  void OnShowInterior(wxCommandEvent& event);
  void OnShowExterior(wxCommandEvent& event);
  void OnShowInterface(wxCommandEvent& event);
  void OnRemoveInterior(wxCommandEvent& event);
  void OnRemoveExterior(wxCommandEvent& event);
  void OnRemoveInterface(wxCommandEvent& event);
  void updateInterface();
  void updateInterior();
  void updateExterior();
  int selectedInterface() const;
  int selectedExterior() const;
  int selectedInterior() const;
private:
  MarchingCubesGUI<N> *mGui;
  MainFrame<N> *mParentFrame;
  wxTextCtrl* mPatternText;
  wxTextCtrl *mInterfaceText, *mInteriorText, *mExteriorText;
  wxListBox *mInterfaceList, *mInteriorList, *mExteriorList;
  wxCheckBox *mShowInterface, *mShowInterior, *mShowExterior;
  wxComboBox* mTypeCombo;

  void updateImpl(TriangulationType t, wxListBox* list, wxTextCtrl* text);

  static const int GP_ADD = 300;
  static const int GP_PATTERN = 301;
  static const int GP_SHOWINTERFACE = 302, GP_SHOWINTERIOR = 303,
                   GP_SHOWEXTERIOR = 304;
  static const int GP_REMOVEINTERFACE = 305, GP_REMOVEINTERIOR = 306,
                   GP_REMOVEEXTERIOR = 307;
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
  // ###### INTERFACE ######
  wxBoxSizer *interfaceBoxTop = new wxBoxSizer(wxHORIZONTAL);
  wxStaticText *interfaceLabel = new wxStaticText(this, wxID_ANY, _("Interface:"));
  mShowInterface = new wxCheckBox(this, GP_SHOWINTERFACE, _("visible"),
                                  wxPoint(20,20));
  mShowInterface->SetValue(mParentFrame->getShowGeo(GeoContainer::INTERFACE));
  Connect(GP_SHOWINTERFACE, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnShowInterface));
  interfaceBoxTop->Add(interfaceLabel, 0, wxALL, 0);
  interfaceBoxTop->Add(mShowInterface, 0, wxLEFT, 5);
  mInterfaceList = new wxListBox(this, wxID_ANY);
  mInterfaceList->SetMinSize(wxSize(twidth,100));
  mInterfaceList->SetMaxSize(wxSize(twidth,-1));
  wxBoxSizer *interfaceBoxBottom = new wxBoxSizer(wxHORIZONTAL);
  mInterfaceText = new wxTextCtrl(this, wxID_ANY, _(""), wxDefaultPosition, wxDefaultSize, wxTE_READONLY);
  wxButton *interfaceRemove = new wxButton(this, GP_REMOVEINTERFACE, _("remove"), wxPoint(20,20));
  Connect(GP_REMOVEINTERFACE, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnRemoveInterface));
  interfaceBoxBottom->Add(mInterfaceText, 0, wxALL, 0);
  interfaceBoxBottom->Add(interfaceRemove, 0, wxLEFT, 5);
  updateInterface();
  // ###### INTERIOR ######
  wxBoxSizer *interiorBoxTop = new wxBoxSizer(wxHORIZONTAL);
  wxStaticText *interiorLabel = new wxStaticText(this, wxID_ANY, _("Interior:"));
  mShowInterior = new wxCheckBox(this, GP_SHOWINTERIOR, _("visible"),
                                 wxPoint(20,20));
  mShowInterior->SetValue(mParentFrame->getShowGeo(GeoContainer::INTERIOR));
  Connect(GP_SHOWINTERIOR, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnShowInterior));
  interiorBoxTop->Add(interiorLabel, 0, wxALL, 0);
  interiorBoxTop->Add(mShowInterior, 0, wxLEFT, 5);
  mInteriorList = new wxListBox(this, wxID_ANY);
  mInteriorList->SetMinSize(wxSize(twidth,100));
  mInteriorList->SetMaxSize(wxSize(twidth,-1));
  wxBoxSizer *interiorBoxBottom = new wxBoxSizer(wxHORIZONTAL);
  mInteriorText = new wxTextCtrl(this, wxID_ANY, _(""), wxDefaultPosition, wxDefaultSize, wxTE_READONLY);
  wxButton *interiorRemove = new wxButton(this, GP_REMOVEINTERIOR, _("remove"), wxPoint(20,20));
  Connect(GP_REMOVEINTERIOR, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnRemoveInterior));
  interiorBoxBottom->Add(mInteriorText, 0, wxALL, 0);
  interiorBoxBottom->Add(interiorRemove, 0, wxLEFT, 5);
  updateInterior();
  // ###### EXTERIOR ######
  wxBoxSizer *exteriorBoxTop = new wxBoxSizer(wxHORIZONTAL);
  wxStaticText *exteriorLabel = new wxStaticText(this, wxID_ANY, _("Exterior:"));
  mShowExterior = new wxCheckBox(this, GP_SHOWEXTERIOR, _("visible"),
                                 wxPoint(20,20));
  mShowExterior->SetValue(mParentFrame->getShowGeo(GeoContainer::EXTERIOR));
  Connect(GP_SHOWEXTERIOR, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnShowExterior));
  exteriorBoxTop->Add(exteriorLabel, 0, wxALL, 0);
  exteriorBoxTop->Add(mShowExterior, 0, wxLEFT, 5);
  mExteriorList = new wxListBox(this, wxID_ANY);
  mExteriorList->SetMinSize(wxSize(twidth,100));
  mExteriorList->SetMaxSize(wxSize(twidth,-1));
  wxBoxSizer *exteriorBoxBottom = new wxBoxSizer(wxHORIZONTAL);
  mExteriorText = new wxTextCtrl(this, wxID_ANY, _(""), wxDefaultPosition, wxDefaultSize, wxTE_READONLY);
  wxButton *exteriorRemove = new wxButton(this, GP_REMOVEEXTERIOR, _("remove"), wxPoint(20,20));
  Connect(GP_REMOVEEXTERIOR, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(GeometryPanel::OnRemoveExterior));
  exteriorBoxBottom->Add(mExteriorText, 0, wxALL, 0);
  exteriorBoxBottom->Add(exteriorRemove, 0, wxLEFT, 5);
  updateExterior();
  vbox->Add(label, 0, wxTOP, 5);
  vbox->Add(mPatternText, 0, wxTOP, 5);
  vbox->Add(mTypeCombo, 0, wxTOP, 5);
  vbox->Add(addButton, 0, wxTOP, 5);
  vbox->Add(interfaceBoxTop, 0, wxTOP, 5);
  vbox->Add(mInterfaceList, 0, wxTOP, 5);
  vbox->Add(interfaceBoxBottom, 0, wxTOP, 5);
  vbox->Add(interiorBoxTop, 0, wxTOP, 5);
  vbox->Add(mInteriorList, 0, wxTOP, 5);
  vbox->Add(interiorBoxBottom, 0, wxTOP, 5);
  vbox->Add(exteriorBoxTop, 0, wxTOP, 5);
  vbox->Add(mExteriorList, 0, wxTOP, 5);
  vbox->Add(exteriorBoxBottom, 0, wxTOP, 5);
  this->SetSizer(vbox);
}

template <std::size_t N>
void GeometryPanel<N>::OnAdd(wxCommandEvent& event) {
  std::stringstream s;
  s << mPatternText->GetValue().mb_str();
  mPatternText->Clear();
  try {
    switch (mTypeCombo->GetSelection()) {
    case 0 : mGui->addGeometryElement(s.str(), GeoContainer::INTERIOR); updateInterior(); break;
    case 1 : mGui->addGeometryElement(s.str(), GeoContainer::EXTERIOR); updateExterior(); break;
    case 2 : mGui->addGeometryElement(s.str(), GeoContainer::INTERFACE); updateInterface(); break;
    default : mGui->addGeometryElement(s.str(), GeoContainer::INTERIOR); updateInterior(); break;
    }
  } catch (Dune::Exception& e) {
    // print some error
  }
}

template <std::size_t N>
void GeometryPanel<N>::updateImpl(TriangulationType t, wxListBox* list, wxTextCtrl* text) {
  list->Clear();
  text->SetValue(_(""));
  if (!mGui->geometryContainer().empty(t)) {
    typedef typename GeoContainer::geo_iterator Iterator;
    Iterator itend = mGui->geometryContainer().geoend(t);
    for (Iterator it = mGui->geometryContainer().geobegin(t); it != itend; ++it) {
      std::stringstream s;
      s << PythonAdapter<double, 3>(*it);
      list->Append(wxString(s.str().c_str(), wxConvUTF8));
    }
    std::stringstream sa;
    sa << PythonAdapter<double, 3>(mGui->geometryContainer(), t);
    text->SetValue(wxString(sa.str().c_str(), wxConvUTF8));
  }
  list->Select(list->GetCount()-1);
}

template <std::size_t N>
void GeometryPanel<N>::updateInterface() {
  updateImpl(GeoContainer::INTERFACE, mInterfaceList, mInterfaceText);
}

template <std::size_t N>
void GeometryPanel<N>::updateInterior() {
  updateImpl(GeoContainer::INTERIOR, mInteriorList, mInteriorText);
}

template <std::size_t N>
void GeometryPanel<N>::updateExterior() {
  updateImpl(GeoContainer::EXTERIOR, mExteriorList, mExteriorText);
}

template <std::size_t N>
void GeometryPanel<N>::OnShowInterface(wxCommandEvent& event) {
  mParentFrame->setShowGeo(GeoContainer::INTERFACE, mShowInterface->GetValue());
}

template <std::size_t N>
void GeometryPanel<N>::OnShowExterior(wxCommandEvent& event) {
  mParentFrame->setShowGeo(GeoContainer::EXTERIOR, mShowExterior->GetValue());
}

template <std::size_t N>
void GeometryPanel<N>::OnShowInterior(wxCommandEvent& event) {
  mParentFrame->setShowGeo(GeoContainer::INTERIOR, mShowInterior->GetValue());
}

template <std::size_t N>
int GeometryPanel<N>::selectedInterface() const {
  return mInterfaceList->GetSelection();
}

template <std::size_t N>
int GeometryPanel<N>::selectedExterior() const {
  return mExteriorList->GetSelection();
}

template <std::size_t N>
int GeometryPanel<N>::selectedInterior() const {
  return mInteriorList->GetSelection();
}

template <std::size_t N>
void GeometryPanel<N>::OnRemoveInterface(wxCommandEvent& event) {
  if (mInterfaceList->GetSelection()>=0) {
    mGui->removeGeometryElement(mInterfaceList->GetSelection(),
                                GeoContainer::INTERFACE);
    updateInterface();
  }
}

template <std::size_t N>
void GeometryPanel<N>::OnRemoveExterior(wxCommandEvent& event) {
  if (mExteriorList->GetSelection()>=0) {
    mGui->removeGeometryElement(mExteriorList->GetSelection(),
                                GeoContainer::EXTERIOR);
    updateExterior();
  }
}

template <std::size_t N>
void GeometryPanel<N>::OnRemoveInterior(wxCommandEvent& event) {
  if (mInteriorList->GetSelection()>=0) {
    mGui->removeGeometryElement(mInteriorList->GetSelection(),
                                GeoContainer::INTERIOR);
    updateInterior();
  }
}


#endif //GEOMETRYPANEL_HH_
