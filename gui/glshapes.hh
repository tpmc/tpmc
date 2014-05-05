// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef GLSHAPES_HH
#define GLSHAPES_HH

#include <GL/gl.h>
#include <dune/common/exceptions.hh>

class UnknownShapeException : public Dune::Exception {};

template <typename ValueType, int dim, int codim, bool border>
struct GLShape;

// 2D codim 0
template <typename ValueType>
struct GLShape<ValueType, 2, 0, false> {
  template <class E>
  static void draw(const E& e) {
    switch (e.size()) {
    case 3 : triangle(e); break;
    case 4 : quad(e); break;
    default : DUNE_THROW(UnknownShapeException, "shape unkown");
    }
  }

  template <class E>
  static void triangle(const E& e) {
    glBegin(GL_TRIANGLES);
    for (unsigned short i = 0; i<3; ++i) {
      const typename E::VectorType& p = e[i].vertex();
      glVertex2d(p[0], p[1]);
    }
    glEnd();
  }

  template <class E>
  static void quad(const E& e) {
    const typename E::VectorType& p0 = e[0].vertex(),
    p1 = e[1].vertex(), p2 = e[2].vertex(),
    p3 = e[3].vertex();
    glBegin(GL_QUADS);
    glVertex2d(p0[0], p0[1]);
    glVertex2d(p1[0], p1[1]);
    glVertex2d(p3[0], p3[1]);
    glVertex2d(p2[0], p2[1]);
    glEnd();
  }
};

// 2D codim 1
template <typename ValueType>
struct GLShape<ValueType, 2, 1, false> {
  template <class E>
  static void draw(const E& e) {
    switch (e.size()) {
    case 2 : line(e); break;
    default : DUNE_THROW(UnknownShapeException, "shape unknown");
    }
  }

  template <class E>
  static void line(const E& e) {
    const typename E::VectorType& p0 = e[0].vertex(),
    p1 = e[1].vertex();
    glBegin(GL_LINES);
    glVertex2d(p0[0], p0[1]);
    glVertex2d(p1[0], p1[1]);
    glEnd();
  }
};

// 3D codim 0
template <typename ValueType>
struct GLShape<ValueType, 3, 0, false> {
  template <class E>
  static void draw(const E& e) {
    switch (e.size()) {
    case 4 : simplex(e); break;
    case 5 : pyramid(e); break;
    case 6 : prism(e); break;
    case 8 : cube(e); break;
    default : DUNE_THROW(UnknownShapeException, "shape unknown");
    }
  }

  template <class E>
  static void simplex(const E& e) {
    unsigned short faces[4][3] = {{0,1,2},{0,1,3},{0,2,3},{1,2,3}};
    glBegin(GL_TRIANGLES);
    for (unsigned short i = 0; i<4; ++i) {
      for (unsigned short j = 0; j<3; ++j) {
        const typename E::VectorType& p = e[faces[i][j]].vertex();
        const typename E::VectorType& n = e[faces[i][j]].normal();
        glNormal3f(n[0], n[2], -n[1]);
        glVertex3d(p[0], p[2], 1.f-p[1]);
      }
    }
    glEnd();
  }

  template <class E>
  static void pyramid(const E& e) {
    unsigned short triangle_faces[4][3] = {{0,1,4},{0,2,4},{1,3,4},{2,3,4}};
    unsigned short quad_face[4] = {0,1,3,2};
    glBegin(GL_TRIANGLES);
    for (unsigned short i = 0; i<4; ++i) {
      for (unsigned short j = 0; j<3; ++j) {
        const typename E::VectorType& p = e[triangle_faces[i][j]].vertex();
        const typename E::VectorType& n = e[triangle_faces[i][j]].normal();
        glNormal3f(n[0], n[2], -n[1]);
        glVertex3d(p[0], p[2], 1.f-p[1]);
      }
    }
    glEnd();
    glBegin(GL_QUADS);
    for (unsigned short j = 0; j<4; ++j) {
      const typename E::VectorType& p = e[quad_face[j]].vertex();
      const typename E::VectorType& n = e[quad_face[j]].normal();
      glNormal3f(n[0], n[2], -n[1]);
      glVertex3d(p[0], p[2], 1.f-p[1]);
    }
    glEnd();
  }

  template <class E>
  static void prism(const E& e) {
    unsigned short triangle_faces[2][3] = {{0,1,2},{3,4,5}};
    unsigned short quad_faces[3][4] = {{0,1,4,3},{1,2,5,4},{0,2,5,3}};
    glBegin(GL_TRIANGLES);
    for (unsigned short i = 0; i<2; ++i) {
      for (unsigned short j = 0; j<3; ++j) {
        const typename E::VectorType& p = e[triangle_faces[i][j]].vertex();
        const typename E::VectorType& n = e[triangle_faces[i][j]].normal();
        glNormal3f(n[0], n[2], -n[1]);
        glVertex3d(p[0], p[2], 1.f-p[1]);
      }
    }
    glEnd();
    glBegin(GL_QUADS);
    for (unsigned short i = 0; i<3; ++i) {
      for (unsigned short j = 0; j<4; ++j) {
        const typename E::VectorType& p = e[quad_faces[i][j]].vertex();
        const typename E::VectorType& n = e[quad_faces[i][j]].normal();
        glNormal3f(n[0], n[2], -n[1]);
        glVertex3d(p[0], p[2], 1.f-p[1]);
      }
    }
    glEnd();
  }

  template <class E>
  static void cube(const E& e) {
    unsigned short faces[6][4] = {{0,2,6,4},{1,3,7,5},{0,1,5,4},
                                  {2,3,7,6},{0,1,3,2},{4,5,7,6}};
    glBegin(GL_QUADS);
    for (unsigned short i = 0; i<6; ++i) {
      for (unsigned short j = 0; j<4; ++j) {
        const typename E::VectorType& p = e[faces[i][j]].vertex();
        const typename E::VectorType& n = e[faces[i][j]].normal();
        glNormal3f(n[0], n[2], -n[1]);
        glVertex3d(p[0], p[2], 1.f-p[1]);
      }
    }
    glEnd();
  }
};

// 3D codim 0 border
template <typename ValueType>
struct GLShape<ValueType, 3, 0, true> {
  template <class E>
  static void draw(const E& e) {
    switch (e.size()) {
    case 4 : simplex(e); break;
    case 5 : pyramid(e); break;
    case 6 : prism(e); break;
    case 8 : cube(e); break;
    default : DUNE_THROW(UnknownShapeException, "shape unknown");
    }
  }

  template <class E>
  static void simplex(const E& e) {
    unsigned short lines[6][2] = {{0,1},{1,2},{0,2},{0,3},{1,3},{2,3}};
    glBegin(GL_LINES);
    for (unsigned short i = 0; i<6; ++i) {
      const typename E::VectorType& p1 = e[lines[i][0]].vertex(),
      p2 = e[lines[i][1]].vertex();
      const typename E::VectorType& n1 = e[lines[i][0]].normal(),
      n2 = e[lines[i][1]].normal();
      glNormal3f(n1[0], n1[2], -n1[1]);
      glVertex3f(p1[0], p1[2], 1.f-p1[1]);
      glNormal3f(n2[0], n2[2], -n2[1]);
      glVertex3f(p2[0], p2[2], 1.f-p2[1]);
    }
    glEnd();
  }

  template <class E>
  static void pyramid(const E& e) {
    unsigned short lines[8][2] = {{0,1},{1,3},{2,3},{0,2},
                                  {0,4},{1,4},{2,4},{3,4}};
    glBegin(GL_LINES);
    for (unsigned short i = 0; i<8; ++i) {
      const typename E::VectorType& p1 = e[lines[i][0]].vertex(),
      p2 = e[lines[i][1]].vertex();
      const typename E::VectorType& n1 = e[lines[i][0]].normal(),
      n2 = e[lines[i][1]].normal();
      glNormal3f(n1[0], n1[2], -n1[1]);
      glVertex3f(p1[0], p1[2], 1.f-p1[1]);
      glNormal3f(n2[0], n2[2], -n2[1]);
      glVertex3f(p2[0], p2[2], 1.f-p2[1]);
    }
    glEnd();
  }

  template <class E>
  static void prism(const E& e) {
    unsigned short lines[9][2] = {{0,1},{1,2},{0,2},{3,4},{4,5},{3,5},
                                  {0,3},{1,4},{2,5}};
    glBegin(GL_LINES);
    for (unsigned short i = 0; i<9; ++i) {
      const typename E::VectorType& p1 = e[lines[i][0]].vertex(),
      p2 = e[lines[i][1]].vertex();
      const typename E::VectorType& n1 = e[lines[i][0]].normal(),
      n2 = e[lines[i][1]].normal();
      glNormal3f(n1[0], n1[2], -n1[1]);
      glVertex3f(p1[0], p1[2], 1.f-p1[1]);
      glNormal3f(n2[0], n2[2], -n2[1]);
      glVertex3f(p2[0], p2[2], 1.f-p2[1]);
    }
    glEnd();
  }

  template <class E>
  static void cube(const E& e) {
    unsigned short lines[12][2] = {{0,1},{1,3},{2,3},{0,2},
                                   {4,5},{5,7},{6,7},{4,6},
                                   {0,4},{1,5},{2,6},{3,7}};
    glBegin(GL_LINES);
    for (unsigned short i = 0; i<12; ++i) {
      const typename E::VectorType& p1 = e[lines[i][0]].vertex(),
      p2 = e[lines[i][1]].vertex();
      const typename E::VectorType& n1 = e[lines[i][0]].normal(),
      n2 = e[lines[i][1]].normal();
      glNormal3f(n1[0], n1[2], -n1[1]);
      glVertex3f(p1[0], p1[2], 1.f-p1[1]);
      glNormal3f(n2[0], n2[2], -n2[1]);
      glVertex3f(p2[0], p2[2], 1.f-p2[1]);
    }
    glEnd();
  }
};

// 3d codim 1
template <typename ValueType>
struct GLShape<ValueType, 3, 1, false> {
  template <class E>
  static void draw(const E& e) {
    switch (e.size()) {
    case 3 : triangle(e); break;
    case 4 : quad(e); break;
    default : DUNE_THROW(UnknownShapeException, "shape unknown");
    }
  }

  template <class E>
  static void triangle(const E& e) {
    glBegin(GL_TRIANGLES);
    for (unsigned short i = 0; i<3; ++i) {
      const typename E::VectorType& p = e[i].vertex();
      const typename E::VectorType& n = e[i].normal();
      glNormal3f(n[0], n[2], -n[1]);
      glVertex3d(p[0], p[2], 1.f-p[1]);
    }
    glEnd();
  }

  template <class E>
  static void quad(const E& e) {
    const typename E::VectorType& p0 = e[0].vertex(), p1 = e[1].vertex(),
    p2 = e[2].vertex(), p3 = e[3].vertex();
    const typename E::VectorType& n0 = e[0].normal(), n1 = e[1].normal(),
    n2 = e[2].normal(), n3 = e[3].normal();
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
};

// 3d codim 1 border
template <typename ValueType>
struct GLShape<ValueType, 3, 1, true> {
  template <class E>
  static void draw(const E& e) {
    switch (e.size()) {
    case 3 : triangle(e); break;
    case 4 : quad(e); break;
    default : DUNE_THROW(UnknownShapeException, "shape unknown");
    }
  }

  template <class E>
  static void triangle(const E& e) {
    glBegin(GL_LINES);
    for (unsigned short i = 0; i<3; ++i) {
      const typename E::VectorType& p1 = e[i].vertex(),
      p2 = e[(i+1)%3].vertex();
      const typename E::VectorType& n1 = e[i].normal(),
      n2 = e[(i+1)%3].normal();
      glNormal3f(n1[0], n1[2], -n1[1]);
      glVertex3f(p1[0], p1[2], 1.f-p1[1]);
      glNormal3f(n2[0], n2[2], -n2[1]);
      glVertex3f(p2[0], p2[2], 1.f-p2[1]);
    }
    glEnd();
  }

  template <class E>
  static void quad(const E& e) {
    const typename E::VectorType& p0 = e[0].vertex(), p1 = e[1].vertex(),
    p2 = e[2].vertex(), p3 = e[3].vertex();
    const typename E::VectorType& n0 = e[0].normal(), n1 = e[1].normal(),
    n2 = e[2].normal(), n3 = e[3].normal();
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
};

#endif //GLSHAPES_HH
