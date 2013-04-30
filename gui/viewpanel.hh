// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __VIEWPANEL_HH__
#define __VIEWPANEL_HH__

#include <wx/wx.h>
#include "mainframe.hh"

template <std::size_t N>
class ViewPanel : public wxPanel {
public:
  ViewPanel(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame, wxPanel *parent);
  void OnShowCubeToggle(wxCommandEvent& event);
  void OnShowPlaneToggle(wxCommandEvent& event);
  void OnShowFaceCenterToggle(wxCommandEvent& event);
  void OnInterfaceVisibleToggle(wxCommandEvent& event);
  void OnSetGridSize(wxCommandEvent& event);
  void OnResetView(wxCommandEvent& event);
private:
  MarchingCubesGUI<N> *mGui;
  MainFrame<N> *mParentFrame;
  wxCheckBox *mInterfaceVisibleCheckBox[N];
  wxTextCtrl *mGridSizeText[N];
  wxCheckBox *mShowCubeCheckBox;
  wxCheckBox *mShowPlaneCheckBox;
  wxCheckBox *mShowFaceCenterCheckBox;
  static const int CTL_SHOWCUBECB = 108;
  static const int CTL_RESETVIEW = 111;
  static const int CTL_SHOWPLANECB = 114;
  static const int CTL_SHOWFACECENTERCB = 112;
  static const int CTL_SETGRIDSIZE = 120;
  static const int CTL_INTERFACEVISIBLECB = 200;   // has to be last
};

template <std::size_t N>
ViewPanel<N>::ViewPanel(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame, wxPanel *parent)
  : wxPanel(parent, -1, wxPoint(-1, -1), wxSize(-1, -1)), mGui(gui),
    mParentFrame(parentFrame) {
  wxBoxSizer *hbox = new wxBoxSizer(wxHORIZONTAL);

  mShowPlaneCheckBox = new wxCheckBox(this, CTL_SHOWPLANECB, _("Show plane"), wxPoint(20,20));
  mShowPlaneCheckBox->SetValue(mParentFrame->getShowPlane());
  Connect(CTL_SHOWPLANECB, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(ViewPanel::OnShowPlaneToggle));

  mShowFaceCenterCheckBox = new wxCheckBox(this, CTL_SHOWFACECENTERCB, _("Show face-center"),
                                           wxPoint(20, 20));
  mShowFaceCenterCheckBox->SetValue(mParentFrame->getShowFaceCenter());
  Connect(CTL_SHOWFACECENTERCB, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(ViewPanel::OnShowFaceCenterToggle));

  mShowCubeCheckBox = new wxCheckBox(this, CTL_SHOWCUBECB, _("Show cube"), wxPoint(20,20));
  mShowCubeCheckBox->SetValue(mParentFrame->getShowCube());
  Connect(CTL_SHOWCUBECB, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(ViewPanel::OnShowCubeToggle));

  wxButton *rvButton = new wxButton(this, CTL_RESETVIEW, _("Reset view"), wxPoint(20, 20));
  Connect(CTL_RESETVIEW, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(ViewPanel::OnResetView));

  hbox->Add(mShowFaceCenterCheckBox, 0, wxLEFT, 5);
  hbox->Add(mShowPlaneCheckBox, 0, wxLEFT, 5);
  hbox->Add(mShowCubeCheckBox, 0, wxLEFT, 5);
  hbox->Add(rvButton, 0, wxLEFT, 5);

  for (std::size_t i = 0; i<N; ++i) {
    std::stringstream gsText;
    gsText << "Size grid " << i << ":";
    wxStaticText *gsLabel = new wxStaticText(this, wxID_ANY, wxString(gsText.str().c_str(), wxConvUTF8));
    mGridSizeText[i] = new wxTextCtrl(this, wxID_ANY);
    *mGridSizeText[i] << static_cast<long int>(mGui->getRefinements(i));
    mGridSizeText[i]->SetMinSize(wxSize(40,-1));
    mGridSizeText[i]->SetMaxSize(wxSize(40,-1));
    wxBoxSizer *gsbox = new wxBoxSizer(wxHORIZONTAL);
    gsbox->Add(gsLabel,0, wxLEFT,5);
    gsbox->Add(mGridSizeText[i], 1, wxLEFT, 2);

    mInterfaceVisibleCheckBox[i] = new wxCheckBox(this, CTL_INTERFACEVISIBLECB+i, _(""), wxPoint(20,20));
    mInterfaceVisibleCheckBox[i]->SetValue(mParentFrame->getShowInterface(i));
    Connect(CTL_INTERFACEVISIBLECB+i, wxEVT_COMMAND_CHECKBOX_CLICKED,
            wxCommandEventHandler(ViewPanel::OnInterfaceVisibleToggle));
    gsbox->Add(mInterfaceVisibleCheckBox[i],0,wxLEFT,5);

    hbox->Add(gsbox,0,wxLeft, 2);
  }
  wxButton *sgsButton = new wxButton(this, CTL_SETGRIDSIZE, _("Set refs"), wxPoint(20,20));
  Connect(CTL_SETGRIDSIZE, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(ViewPanel::OnSetGridSize));
  hbox->Add(sgsButton, 0, wxLEFT, 5);

  this->SetSizer(hbox);
}

template <std::size_t N>
void ViewPanel<N>::OnShowPlaneToggle(wxCommandEvent& event) {
  mParentFrame->setShowPlane(mShowPlaneCheckBox->GetValue());
}

template <std::size_t N>
void ViewPanel<N>::OnShowCubeToggle(wxCommandEvent& event) {
  mParentFrame->setShowCube(mShowCubeCheckBox->GetValue());
}

template <std::size_t N>
void ViewPanel<N>::OnShowFaceCenterToggle(wxCommandEvent& event) {
  mParentFrame->setShowFaceCenter(mShowFaceCenterCheckBox->GetValue());
}

template <std::size_t N>
void ViewPanel<N>::OnResetView(wxCommandEvent& event) {
  mParentFrame->resetView();
}

template <std::size_t N>
void ViewPanel<N>::OnInterfaceVisibleToggle(wxCommandEvent& event) {
  for (std::size_t i = 0; i<N; ++i) {
    mParentFrame->setShowInterface(i, mInterfaceVisibleCheckBox[i]->GetValue());
  }
}

template <std::size_t N>
void ViewPanel<N>::OnSetGridSize(wxCommandEvent& event) {
  for (std::size_t i = 0; i<N; ++i) {
    std::stringstream ss;
    ss << mGridSizeText[i]->GetValue().mb_str();
    std::size_t gs;
    ss >> gs;
    mGui->setRefinements(i, gs);
  }
  mGui->computeTriangulations();
}

#endif //__VIEWPANEL_HH__
