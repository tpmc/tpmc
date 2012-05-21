// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef MCCANVAS_HH
#define MCCANVAS_HH

#include <wx/wx.h>
#include <dune/common/fvector.hh>
#include "wxsfmlcanvas.h"
#include "marchingcubesgui.hh"
#include "origincenteredcamera.hh"

template <std::size_t N>
class MainFrame;

template <std::size_t N>
class MCCanvas : public wxSFMLCanvas {
public:
  typedef typename MarchingCubesGUI<N>::VectorType VectorType;
  typedef typename MarchingCubesGUI<N>::ValueType ValueType;
  typedef typename MarchingCubesGUI<N>::PlaneVectorType PlaneVectorType;
  MCCanvas(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame,
           wxWindow* Parent = NULL, wxWindowID Id = -1,
           const wxPoint& Position = wxDefaultPosition,
           const wxSize& Size = wxDefaultSize,
           long Style = 0);
  void resetView();
  virtual ~MCCanvas() {}
private:
  virtual void OnUpdate();
  virtual void OnKeyDown(wxKeyEvent&);
  virtual void OnKeyUp(wxKeyEvent&);
  template <typename V>
  void projectOrigin(V& result);
  void drawInterfaces();
  void drawPlaneGrid();
  void drawPlane();
  void drawElement(int codim, const Element<ValueType, 3>& element);
  void drawElement(int codim, const Element<ValueType, 2>& element);
  void drawElementBorder(int codim, const Element<ValueType, 3>& element);
  void drawTriangle(const Element<ValueType, 3>& element);
  void drawTriangle(const Element<ValueType, 2>& element);
  void drawLine(const Element<ValueType, 2>& element);
  void drawTriangleBorder(const Element<ValueType, 3>& element);
  void drawQuad(const Element<ValueType, 3>& element);
  void drawQuad(const Element<ValueType, 2>& element);
  void drawQuadBorder(const Element<ValueType, 3>& element);
  void drawUnitQuadBorder();
  void drawWireframeUnitCube();
  void drawUnitCube();
  void drawAxes();
  MarchingCubesGUI<N> *mGui;
  MainFrame<N> *mParentFrame;
  bool mKeyLeftPressed;
  bool mKeyRightPressed;
  bool mKeyUpPressed;
  bool mKeyDownPressed;
  bool mKeyWPressed;
  bool mKeyAPressed;
  bool mKeySPressed;
  bool mKeyDPressed;
  bool mKeySpacePressed;
  bool mKeyLShiftPressed;
  static const float ROTATIONS_PER_SECOND;
  static const float STEPS_PER_SECOND;
  static const float INDICATOR_CUBE_SIZE;
  static const float TRIANGULATION_COLORS[][3];
  static const std::size_t TRIANGULATION_COLOR_COUNT;
  static const double PLANE_PERCENT;
  //Camera mCamera;
  OriginCenteredCamera mCamera;
  sf::Clock mClock;
  float mAspectRatio;
  float mOrthoBottom, mOrthoTop, mOrthoLeft, mOrthoRight;
};


template <std::size_t N>
const float MCCanvas<N>::ROTATIONS_PER_SECOND = 0.2f;
template <std::size_t N>
const float MCCanvas<N>::STEPS_PER_SECOND = 1.f;
template <std::size_t N>
const float MCCanvas<N>::INDICATOR_CUBE_SIZE = 0.05f;
template <std::size_t N>
const float MCCanvas<N>::TRIANGULATION_COLORS[][3] = {
  {1.f, 0.f, 0.f}, {0.f,1.f,0.f}, {0.f,0.f,1.f}
};
template <std::size_t N>
const std::size_t MCCanvas<N>::TRIANGULATION_COLOR_COUNT = 3;
template <std::size_t N>
const double MCCanvas<N>::PLANE_PERCENT = 0.2;

template <std::size_t N>
MCCanvas<N>::MCCanvas(MarchingCubesGUI<N> *gui, MainFrame<N> *parentFrame,
                      wxWindow* Parent, wxWindowID Id,
                      const wxPoint& Position,
                      const wxSize& Size,
                      long Style)
  : wxSFMLCanvas(Parent, Id, Position, Size, Style),
    mGui(gui), mParentFrame(parentFrame),
    mKeyLeftPressed(false), mKeyRightPressed(false),
    mKeyUpPressed(false), mKeyDownPressed(false),
    mKeyWPressed(false), mKeyAPressed(false),
    mKeySPressed(false), mKeyDPressed(false),
    mKeySpacePressed(false),
    mAspectRatio(1.f), mOrthoBottom(-0.1f), mOrthoTop(1.1f),
    mOrthoLeft(-0.1f), mOrthoRight(1.1f) {
  PreserveOpenGLStates(true);
  glClearDepth(1.f);
  glClearColor(1.f, 1.f, 1.f, 0.f);
  glEnable(GL_DEPTH_TEST);
  glDepthMask(GL_TRUE);

  glEnable(GL_SMOOTH);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

  glShadeModel(GL_SMOOTH);
  glEnable(GL_LIGHTING);
  float lamb[] = {0.f, 0.f, 0.f, 1.f};
  float ldiff[] = {1.f, 1.f, 1.f, 1.f};
  glLightfv(GL_LIGHT0, GL_AMBIENT, lamb);
  glLightfv(GL_LIGHT0, GL_DIFFUSE, ldiff);
  glEnable(GL_LIGHT0);
  glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE ) ;
  glEnable(GL_COLOR_MATERIAL);
}

template <std::size_t N>
void MCCanvas<N>::resetView() {
  mCamera.reset();
}

template <std::size_t N>
template <class V>
void MCCanvas<N>::projectOrigin(V& result) {
  double projection[16];
  double modelview[16];
  int view[4];
  VectorType screen;
  glGetDoublev(GL_PROJECTION_MATRIX, projection);
  glGetDoublev(GL_MODELVIEW_MATRIX, modelview);
  glGetIntegerv(GL_VIEWPORT, view);
  gluProject(0.f, 0.f, 0.f,
             modelview, projection, view,
             &screen[0], &screen[1], &screen[2]);
  result[0] = screen[0];
  result[1] = screen[1];
}

template <std::size_t N>
void MCCanvas<N>::OnUpdate() {
  static const float coords[][3] = {
    {0.f, 0.f, 1.f},
    {1.f, 0.f, 1.f},
    {0.f, 0.f, 0.f},
    {1.f, 0.f, 0.f},
    {0.f, 1.f, 1.f},
    {1.f, 1.f, 1.f},
    {0.f, 1.f, 0.f},
    {1.f, 1.f, 0.f}
  };
  sf::Event Event;
  while (GetEvent(Event)) {
    if (Event.Type == sf::Event::Resized) {
      glViewport(0,0,Event.Size.Width, Event.Size.Height);
      //sf::FloatRect r(0,Event.Size.Height, Event.Size.Width, 0);
      sf::FloatRect r(0,0, Event.Size.Width, Event.Size.Height);
      GetDefaultView().SetFromRect(r);
      // compute new aspect ratio
      mAspectRatio = static_cast<float>(Event.Size.Width)/Event.Size.Height;
      double s = PLANE_PERCENT*std::min(Event.Size.Width, Event.Size.Height);
      mOrthoLeft = 0;
      mOrthoRight = Event.Size.Width/s;
      mOrthoBottom = 1.0-Event.Size.Height/s;
      mOrthoTop = 1.0;
    }
  }
  // update rotation if key is pressed
  float Time = mClock.GetElapsedTime();
  mClock.Reset();
  if (mKeyLeftPressed) {
    mCamera.rotateRight(-Time*ROTATIONS_PER_SECOND*2.f*M_PI);
  }
  if (mKeyRightPressed) {
    mCamera.rotateRight(Time*ROTATIONS_PER_SECOND*2.f*M_PI);
  }
  if (mKeyUpPressed) {
    mCamera.rotateUp(Time*ROTATIONS_PER_SECOND*2.f*M_PI);
  }
  if (mKeyDownPressed) {
    mCamera.rotateUp(-Time*ROTATIONS_PER_SECOND*2.f*M_PI);
  }
  if (mKeyWPressed) {
    mCamera.zoom(Time*STEPS_PER_SECOND);
  }
  if (mKeyAPressed) {
    mCamera.zoom(-Time*STEPS_PER_SECOND);
  }
  if (mKeySPressed) {
    //mCamera.moveRight(-Time*STEPS_PER_SECOND);
  }
  if (mKeyDPressed) {
    //mCamera.moveRight(Time*STEPS_PER_SECOND);
  }
  if (mKeySpacePressed) {
    //mCamera.moveUp(Time*STEPS_PER_SECOND);
  }
  if (mKeyLShiftPressed) {
    //mCamera.moveUp(-Time*STEPS_PER_SECOND);
  }

  std::vector<sf::String> strings;
  SetActive();
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.f, mAspectRatio, 0.1f, 500.f);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glPushMatrix();
  mCamera.apply();
  // translate cubes center to origin
  glTranslatef(-0.5f, -0.5f, -0.5f);
  if (mParentFrame->getShowCube()) {
    glDisable(GL_LIGHTING);
    glColor3f(0.f, 0.f, 0.f);
    drawWireframeUnitCube();
    for (int i = 0; i<8; ++i) {
      glPushMatrix();
      glTranslatef(coords[i][0], coords[i][1], coords[i][2]);
      glScalef(INDICATOR_CUBE_SIZE,INDICATOR_CUBE_SIZE,
               INDICATOR_CUBE_SIZE);
      double pr[2];
      projectOrigin(pr);
      sf::Vector2f vco = ConvertCoords(pr[0], GetHeight()-pr[1], &GetDefaultView());
      std::stringstream id;
      id << i;
      sf::String text(id.str(),sf::Font::GetDefaultFont(), 150.0/(std::abs(mCamera.getDist())+1));
      text.SetColor(sf::Color(0,0,255));
      text.Move(vco.x, vco.y);
      strings.push_back(text);
      if (mGui->getVertexValue(i) >=0) {
        glTranslatef(-0.5f,-0.5f,-0.5f);
        glColor3f(0.f, 0.f, 0.f);
        drawUnitCube();
      }
      glPopMatrix();
    }
    glEnable(GL_LIGHTING);
  }
  if (mParentFrame->getShowFaceCenter()) {
    for (std::size_t i = 0; i<mGui->getFaceCount(); ++i) {
      glPushMatrix();
      glColor3f(0.7f,0.7f,0.7f);
      VectorType fp;
      mGui->getFaceCenter(i, fp);
      glTranslatef(fp[0], fp[2], 1.f-fp[1]);
      glScalef(INDICATOR_CUBE_SIZE,INDICATOR_CUBE_SIZE,
               INDICATOR_CUBE_SIZE);
      glTranslatef(-0.5f,-0.5f,-0.5f);
      drawUnitCube();
      glPopMatrix();
    }
  }
  drawInterfaces();
  if (mParentFrame->getShowPlane()) {
    glColor3f(1.f,1.f,0.f);
    drawPlane();
  }
  glPushMatrix();
  for (std::vector<sf::String>::const_iterator it = strings.begin();
       it != strings.end(); ++it)
    Draw(*it);
  glPopMatrix();
  glMatrixMode(GL_PROJECTION);
  glPushMatrix();
  glLoadIdentity();
  gluOrtho2D(mOrthoLeft, mOrthoRight, mOrthoBottom, mOrthoTop);
  glMatrixMode(GL_MODELVIEW);
  glPushMatrix();
  glLoadIdentity();
  glDisable(GL_LIGHTING);
  glColor4f(0.f,0.f,0.f, 0.5f);
  drawUnitQuadBorder();
  drawPlaneGrid();
  glEnable(GL_LIGHTING);
  glPopMatrix();
  glMatrixMode(GL_PROJECTION);
  glPopMatrix();
  glMatrixMode(GL_MODELVIEW);

  glPopMatrix();

  Display();
}

template <std::size_t N>
void MCCanvas<N>::drawInterfaces() {
  typedef typename MarchingCubesGUI<N>::VolumeTriangulationType::const_iterator const_iterator;
  for (std::size_t i = 0; i<N; ++i) {
    std::size_t c = i % TRIANGULATION_COLOR_COUNT;
    const float *color = TRIANGULATION_COLORS[c];
    if (mParentFrame->getShowInterface(i)) {
      const_iterator itend = mGui->fend(i);
      for (const_iterator it = mGui->fbegin(i); it != itend; ++it) {
        glColor3f(color[0], color[1], color[2]);
        drawElement(1,*it);
        glColor3f(0.f, 0.f, 0.f);
        drawElementBorder(1, *it);
      }
    }
  }
}

template <std::size_t N>
void MCCanvas<N>::drawPlaneGrid() {
  typedef typename MarchingCubesGUI<N>::PlaneTriangulationType::const_iterator const_iterator;
  const_iterator itfend = mGui->pfend();
  for (const_iterator it = mGui->pfbegin(); it != itfend; ++it) {
    glColor4f(0.f,0.f,0.f,0.75f);
    drawElement(1, *it);
  }
  const_iterator itend = mGui->piend();
  for (const_iterator it = mGui->pibegin(); it != itend; ++it) {
    glColor4f(1.f, 1.f, 0.f, 0.75f);
    drawElement(0, *it);
  }
}

template <std::size_t N>
void MCCanvas<N>::drawElement(int codim, const Element<ValueType, 3>& element) {
  if (codim == 1) {
    switch (element.size()) {
    case 3 : drawTriangle(element); break;
    case 4 : drawQuad(element); break;
    default : break;
    }
  }
}

template <std::size_t N>
void MCCanvas<N>::drawElement(int codim, const Element<ValueType, 2>& element) {
  if (codim == 0) {
    switch (element.size()) {
    case 3 : drawTriangle(element); break;
    case 4 : drawQuad(element); break;
    default : break;
    }
  } else if (codim == 1) {
    switch (element.size()) {
    case 2 : drawLine(element); break;
    default : break;
    }
  }
}

template <std::size_t N>
void MCCanvas<N>::drawElementBorder(int codim, const Element<ValueType, 3>& element) {
  if (codim == 1) {
    switch (element.size()) {
    case 3 : drawTriangleBorder(element); break;
    case 4 : drawQuadBorder(element); break;
    default : break;
    }
  }
}

template <std::size_t N>
void MCCanvas<N>::drawTriangle(const Element<ValueType, 3>& element) {
  glBegin(GL_TRIANGLES);
  for (std::size_t i = 0; i<3; ++i) {
    const VectorType& p = element[i].vertex();
    const VectorType& n = element[i].normal();
    glNormal3f(n[0], n[2], -n[1]);
    glVertex3d(p[0], p[2], 1.f-p[1]);
  }
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawTriangle(const Element<ValueType, 2>& element) {
  glBegin(GL_TRIANGLES);
  for (std::size_t i = 0; i<3; ++i) {
    const PlaneVectorType& p = element[i].vertex();
    glVertex2d(p[0], p[1]);
  }
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawTriangleBorder(const Element<ValueType, 3>& element) {
  glBegin(GL_LINES);
  for (std::size_t i = 0; i<3; ++i) {
    const VectorType& p1 = element[i].vertex(),
                      p2 = element[(i+1)%3].vertex();
    const VectorType& n1 = element[i].normal(),
                      n2 = element[(i+1)%3].normal();
    glNormal3f(n1[0], n1[2], -n1[1]);
    glVertex3f(p1[0], p1[2], 1.f-p1[1]);
    glNormal3f(n2[0], n2[2], -n2[1]);
    glVertex3f(p2[0], p2[2], 1.f-p2[1]);
  }
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawPlane() {
  const VectorType& p0 = mGui->getPlanePosition();
  VectorType p1 = mGui->getPlaneFirst();
  VectorType p2 = mGui->getPlaneSecond();
  // compute normal (cross product)
  VectorType n(0);
  n[0] = p1[1]*p2[2]-p1[2]*p2[1];
  n[1] = p1[2]*p2[0]-p1[0]*p2[2];
  n[2] = p1[0]*p2[1]-p1[1]*p1[0];
  VectorType p3 = p0;
  p3 += mGui->getPlaneFirst();
  p3 += mGui->getPlaneSecond();
  p1 += p0;
  p2 += p0;
  glBegin(GL_QUADS);
  glNormal3d(n[0], n[2], -n[1]);
  glVertex3d(p0[0], p0[2], 1.f-p0[1]);
  glNormal3d(n[0], n[2], -n[1]);
  glVertex3d(p1[0], p1[2], 1.f-p1[1]);
  glNormal3d(n[0], n[2], -n[1]);
  glVertex3d(p3[0], p3[2], 1.f-p3[1]);
  glNormal3d(n[0], n[2], -n[1]);
  glVertex3d(p2[0], p2[2], 1.f-p2[1]);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawQuad(const Element<ValueType, 3>& element) {
  const VectorType& p0 = element[0].vertex(),
                    p1 = element[1].vertex(), p2 = element[2].vertex(),
                    p3 = element[3].vertex();
  const VectorType& n0 = element[0].normal(), n1 = element[1].normal(),
                    n2 = element[2].normal(), n3 = element[3].normal();
  glBegin(GL_QUADS);
  glNormal3f(n0[0], n0[2], -n0[1]);
  glVertex3d(p0[0], p0[2], 1.f-p0[1]);
  glNormal3f(n1[0], n1[2], -n1[1]);
  glVertex3d(p1[0], p1[2], 1.f-p1[1]);
  glNormal3f(n3[0], n3[2], -n3[1]);
  glVertex3d(p3[0], p3[2], 1.f-p3[1]);
  glNormal3f(n2[0], n2[2], -n2[1]);
  glVertex3d(p2[0], p2[2], 1.f-p2[1]);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawLine(const Element<ValueType, 2>& element) {
  const PlaneVectorType& p0 = element[0].vertex(),
                         p1 = element[1].vertex();
  glBegin(GL_LINES);
  glVertex2d(p0[0], p0[1]);
  glVertex2d(p1[0], p1[1]);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawQuad(const Element<ValueType, 2>& element) {
  const PlaneVectorType& p0 = element[0].vertex(),
                         p1 = element[1].vertex(), p2 = element[2].vertex(),
                         p3 = element[3].vertex();
  glBegin(GL_QUADS);
  glVertex2d(p0[0], p0[1]);
  glVertex2d(p1[0], p1[1]);
  glVertex2d(p3[0], p3[1]);
  glVertex2d(p2[0], p2[1]);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawQuadBorder(const Element<ValueType, 3>& element) {
  const VectorType& p0 = element[0].vertex(),
                    p1 = element[1].vertex(), p2 = element[2].vertex(),
                    p3 = element[3].vertex();
  const VectorType& n0 = element[0].normal(), n1 = element[1].normal(),
                    n2 = element[2].normal(), n3 = element[3].normal();
  glBegin(GL_LINE_LOOP);
  glNormal3f(n0[0], n0[2], -n0[1]);
  glVertex3d(p0[0], p0[2], 1.f-p0[1]);
  glNormal3f(n1[0], n1[2], -n1[1]);
  glVertex3d(p1[0], p1[2], 1.f-p1[1]);
  glNormal3f(n3[0], n3[2], -n3[1]);
  glVertex3d(p3[0], p3[2], 1.f-p3[1]);
  glNormal3f(n2[0], n2[2], -n2[1]);
  glVertex3d(p2[0], p2[2], 1.f-p2[1]);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawUnitQuadBorder() {
  glBegin(GL_LINE_LOOP);
  glVertex2d(0.f, 0.f);
  glVertex2d(1.f, 0.f);
  glVertex2d(1.f, 1.f);
  glVertex2d(0.f, 1.f);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawWireframeUnitCube() {
  // gl uses RH coordinate system
  glBegin(GL_LINES);
  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(0.f, 1.f, 1.f);

  glVertex3f(1.f, 0.f, 1.f);
  glVertex3f(1.f, 1.f, 1.f);

  glVertex3f(0.f, 0.f, 0.f);
  glVertex3f(0.f, 1.f, 0.f);

  glVertex3f(1.f, 0.f, 0.f);
  glVertex3f(1.f, 1.f, 0.f);

  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(0.f, 0.f, 0.f);

  glVertex3f(1.f, 0.f, 1.f);
  glVertex3f(1.f, 0.f, 0.f);

  glVertex3f(0.f, 1.f, 1.f);
  glVertex3f(0.f, 1.f, 0.f);

  glVertex3f(1.f, 1.f, 1.f);
  glVertex3f(1.f, 1.f, 0.f);

  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(1.f, 0.f, 1.f);

  glVertex3f(0.f, 1.f, 0.f);
  glVertex3f(1.f, 1.f, 0.f);

  glVertex3f(0.f, 0.f, 0.f);
  glVertex3f(1.f, 0.f, 0.f);

  glVertex3f(0.f, 1.f, 1.f);
  glVertex3f(1.f, 1.f, 1.f);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawUnitCube() {
  glBegin(GL_QUADS);
  glVertex3f(0.f, 0.f, 0.f);
  glVertex3f(1.f, 0.f, 0.f);
  glVertex3f(1.f, 1.f, 0.f);
  glVertex3f(0.f, 1.f, 0.f);

  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(1.f, 0.f, 1.f);
  glVertex3f(1.f, 1.f, 1.f);
  glVertex3f(0.f, 1.f, 1.f);

  glVertex3f(0.f, 0.f, 0.f);
  glVertex3f(1.f, 0.f, 0.f);
  glVertex3f(1.f, 0.f, 1.f);
  glVertex3f(0.f, 0.f, 1.f);

  glVertex3f(0.f, 1.f, 0.f);
  glVertex3f(1.f, 1.f, 0.f);
  glVertex3f(1.f, 1.f, 1.f);
  glVertex3f(0.f, 1.f, 1.f);

  glVertex3f(0.f, 0.f, 0.f);
  glVertex3f(0.f, 1.f, 0.f);
  glVertex3f(0.f, 1.f, 1.f);
  glVertex3f(0.f, 0.f, 1.f);

  glVertex3f(1.f, 0.f, 0.f);
  glVertex3f(1.f, 1.f, 0.f);
  glVertex3f(1.f, 1.f, 1.f);
  glVertex3f(1.f, 0.f, 1.f);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::drawAxes() {
  glBegin(GL_LINES);
  glColor3f(1.f, 0.f, 0.f);
  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(1.f, 0.f, 1.f);

  glColor3f(0.f, 1.f, 0.f);
  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(0.f, 0.f, 0.f);

  glColor3f(0.f, 0.f, 1.f);
  glVertex3f(0.f, 0.f, 1.f);
  glVertex3f(0.f, 1.f, 1.f);
  glEnd();
}

template <std::size_t N>
void MCCanvas<N>::OnKeyDown(wxKeyEvent& event) {
  if (event.GetKeyCode() == WXK_LEFT)
    mKeyLeftPressed = true;
  else if (event.GetKeyCode() == WXK_RIGHT)
    mKeyRightPressed = true;
  else if (event.GetKeyCode() == WXK_UP)
    mKeyUpPressed = true;
  else if (event.GetKeyCode() == WXK_DOWN)
    mKeyDownPressed = true;
  else if (event.GetKeyCode() == 87)
    mKeyWPressed = true;
  else if (event.GetKeyCode() == 83)
    mKeyAPressed = true;
  else if (event.GetKeyCode() == 65)
    mKeySPressed = true;
  else if (event.GetKeyCode() == 68)
    mKeyDPressed = true;
  else if (event.GetKeyCode() == WXK_SPACE)
    mKeySpacePressed = true;
  else if (event.GetKeyCode() == WXK_SHIFT)
    mKeyLShiftPressed = true;
}

template <std::size_t N>
void MCCanvas<N>::OnKeyUp(wxKeyEvent& event) {
  if (event.GetKeyCode() == WXK_LEFT)
    mKeyLeftPressed = false;
  else if (event.GetKeyCode() == WXK_RIGHT)
    mKeyRightPressed = false;
  else if (event.GetKeyCode() == WXK_UP)
    mKeyUpPressed = false;
  else if (event.GetKeyCode() == WXK_DOWN)
    mKeyDownPressed = false;
  else if (event.GetKeyCode() == 87)
    mKeyWPressed = false;
  else if (event.GetKeyCode() == 83)
    mKeyAPressed = false;
  else if (event.GetKeyCode() == 65)
    mKeySPressed = false;
  else if (event.GetKeyCode() == 68)
    mKeyDPressed = false;
  else if (event.GetKeyCode() == WXK_SPACE)
    mKeySpacePressed = false;
  else if (event.GetKeyCode() == WXK_SHIFT)
    mKeyLShiftPressed = false;
}


#endif //_MCCANVAS_HH
