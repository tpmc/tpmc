// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __CTLPANEL_HH__
#define __CTLPANEL_HH__

#include <wx/wx.h>
#include <wx/panel.h>
#include "marchingcubesgui.hh"
#include "mainframe.hh"

template <std::size_t N>
class CtlPanel : public wxPanel {
public:
  typedef typename MarchingCubesGUI<N>::VectorType VectorType;
  CtlPanel(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame, wxPanel *parent);
  void OnComputeWhenSlidingToggle(wxCommandEvent& event);
  void OnComputeTriangulation(wxCommandEvent& event);
  void OnSliderScroll(wxScrollEvent& event);
  void OnSetPlane(wxCommandEvent& event);
  void startComputation();
private:
  MarchingCubesGUI<N> *mGui;
  MainFrame<N> *mParentFrame;
  wxCheckBox *mComputeWhenSlidingCheckBox;
  wxTextCtrl* mVertexValuesText[8];
  wxTextCtrl* mPlanePositionText[3];
  wxTextCtrl* mPlaneFirstText[3];
  wxTextCtrl* mPlaneSecondText[3];
  wxSlider* mVertexValuesSlider[8];
  bool mComputeWhenSliding;
  static const int CTL_SLIDER = 100;
  static const int CTL_CWSCB = 109;
  static const int CTL_COMPUTETRIANG = 110;
  static const int CTL_SETPLANE = 113;
};


template <std::size_t N>
CtlPanel<N>::CtlPanel(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame, wxPanel *parent)
  : wxPanel(parent, -1, wxPoint(-1, -1), wxSize(-1, -1)),
    mGui(gui), mParentFrame(parentFrame), mComputeWhenSliding(true) {
  wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
  for (int i = 0; i<8; ++i) {
    wxBoxSizer *box = new wxBoxSizer(wxHORIZONTAL);
    std::stringstream ls;
    ls << "v" << i << ": ";
    wxStaticText *label = new wxStaticText(this, wxID_ANY, wxString(ls.str().c_str(), wxConvUTF8));
    mVertexValuesText[i] = new wxTextCtrl(this, wxID_ANY);
    std::stringstream vs;
    vs << mGui->getVertexValue(i);
    *mVertexValuesText[i] << wxString(vs.str().c_str(), wxConvUTF8);
    box->Add(label, 0, wxRIGHT, 8);
    box->Add(mVertexValuesText[i], 1);
    mVertexValuesSlider[i] = new wxSlider(this, CTL_SLIDER+i,
                                          mGui->getVertexValue(i), -100,
                                          100, wxPoint(10, 30),
                                          wxSize(140, -1));
    Connect(CTL_SLIDER+i, wxEVT_COMMAND_SLIDER_UPDATED,
            wxScrollEventHandler(CtlPanel::OnSliderScroll));
    vbox->Add(box, 0, wxTOP, 2);
    vbox->Add(mVertexValuesSlider[i], 0, wxTOP, 2);
  }
  const int twidth = 40;
  wxBoxSizer *ppbox = new wxBoxSizer(wxHORIZONTAL);
  wxStaticText *pplabel = new wxStaticText(this, wxID_ANY, _("Pos:"));
  ppbox->Add(pplabel, 0, wxALL, 0);
  for (int i = 0; i<3; ++i) {
    mPlanePositionText[i] = new wxTextCtrl(this, wxID_ANY);
    mPlanePositionText[i]->SetMinSize(wxSize(twidth,-1));
    mPlanePositionText[i]->SetMaxSize(wxSize(twidth,-1));
    std::stringstream ss;
    ss << mGui->getPlanePosition()[i];
    mPlanePositionText[i]->SetValue(wxString(ss.str().c_str(), wxConvUTF8));
    ppbox->Add(mPlanePositionText[i], 0, wxLEFT, 2);
  }

  wxBoxSizer *pfbox = new wxBoxSizer(wxHORIZONTAL);
  wxStaticText *pflabel = new wxStaticText(this, wxID_ANY, _("First:"));
  pfbox->Add(pflabel, 0, wxALL, 0);
  for (int i = 0; i<3; ++i) {
    mPlaneFirstText[i] = new wxTextCtrl(this, wxID_ANY);
    mPlaneFirstText[i]->SetMinSize(wxSize(twidth,-1));
    mPlaneFirstText[i]->SetMaxSize(wxSize(twidth,-1));
    std::stringstream ss;
    ss << mGui->getPlaneFirst()[i];
    mPlaneFirstText[i]->SetValue(wxString(ss.str().c_str(), wxConvUTF8));
    pfbox->Add(mPlaneFirstText[i], 0, wxLEFT, 2);
  }

  wxBoxSizer *psbox = new wxBoxSizer(wxHORIZONTAL);
  wxStaticText *pslabel = new wxStaticText(this, wxID_ANY, _("Second:"));
  psbox->Add(pslabel, 0, wxALL, 0);
  for (int i = 0; i<3; ++i) {
    mPlaneSecondText[i] = new wxTextCtrl(this, wxID_ANY);
    mPlaneSecondText[i]->SetMinSize(wxSize(twidth,-1));
    mPlaneSecondText[i]->SetMaxSize(wxSize(twidth,-1));
    std::stringstream ss;
    ss << mGui->getPlaneSecond()[i];
    mPlaneSecondText[i]->SetValue(wxString(ss.str().c_str(), wxConvUTF8));
    psbox->Add(mPlaneSecondText[i], 0, wxLEFT, 2);
  }
  wxButton *spButton = new wxButton(this, CTL_SETPLANE, _("Set plane"), wxPoint(20, 20));
  Connect(CTL_SETPLANE, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(CtlPanel::OnSetPlane));

  mComputeWhenSlidingCheckBox = new wxCheckBox(this, CTL_CWSCB, _("Compute when sliding"), wxPoint(20, 20));
  mComputeWhenSlidingCheckBox->SetValue(mComputeWhenSliding);
  Connect(CTL_CWSCB, wxEVT_COMMAND_CHECKBOX_CLICKED,
          wxCommandEventHandler(CtlPanel::OnComputeWhenSlidingToggle));

  wxButton *ctButton = new wxButton(this, CTL_COMPUTETRIANG, _("Compute triangulation"), wxPoint(20,20));
  Connect(CTL_COMPUTETRIANG, wxEVT_COMMAND_BUTTON_CLICKED,
          wxCommandEventHandler(CtlPanel::OnComputeTriangulation));

  vbox->Add(ppbox, 0, wxTOP, 5);
  vbox->Add(pfbox, 0, wxTOP, 5);
  vbox->Add(psbox, 0, wxTOP, 5);
  vbox->Add(spButton, 0, wxTop, 5);
  vbox->Add(mComputeWhenSlidingCheckBox, 0, wxTOP, 5);
  vbox->Add(ctButton, 0, wxTOP, 5);

  this->SetSizer(vbox);
}

template <std::size_t N>
void CtlPanel<N>::startComputation() {
  for (int i = 0; i<8; ++i) {
    std::stringstream ss;
    ss << mVertexValuesText[i]->GetValue().mb_str();
    float v;
    ss >> v;
    mGui->setVertexValue(i, v);
  }
  mGui->computeTriangulations();
}

template <std::size_t N>
void CtlPanel<N>::OnSetPlane(wxCommandEvent& event) {
  VectorType position, first, second;
  for (int i = 0; i<3; ++i) {
    std::stringstream sp, sf, ss;
    sp << mPlanePositionText[i]->GetValue().mb_str();
    sf << mPlaneFirstText[i]->GetValue().mb_str();
    ss << mPlaneSecondText[i]->GetValue().mb_str();
    sp >> position[i];
    sf >> first[i];
    ss >> second[i];
  }
  mGui->setPlanePosition(position);
  mGui->setPlaneFirst(first);
  mGui->setPlaneSecond(second);
  startComputation();
}

template <std::size_t N>
void CtlPanel<N>::OnComputeWhenSlidingToggle(wxCommandEvent& event) {
  mComputeWhenSliding = mComputeWhenSlidingCheckBox->GetValue();
}

template <std::size_t N>
void CtlPanel<N>::OnComputeTriangulation(wxCommandEvent& event) {
  startComputation();
}

template <std::size_t N>
void CtlPanel<N>::OnSliderScroll(wxScrollEvent& event) {
  int i = event.GetId()-CTL_SLIDER;
  float v = mVertexValuesSlider[i]->GetValue();
  v /= 10;
  std::stringstream ss;
  ss << v;
  mVertexValuesText[i]->SetValue(wxString(ss.str().c_str(), wxConvUTF8));
  if (mComputeWhenSliding)
    startComputation();
}


#endif //__CTLPANEL_HH__
