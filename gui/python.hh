// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef PYTHON_HH
#define PYTHON_HH

#include <iostream>
#include "geometries.hh"

template <typename ctype, int dim>
class PythonAdapter : public Geometry::GeometryVisitor<ctype, dim> {
public:
  PythonAdapter(const Geometry::Vertex<ctype, dim>& v) { v.takeVisitor(*this); }
  PythonAdapter(const Geometry::Element<ctype, dim>& e) { e.takeVisitor(*this); }
  PythonAdapter(const GeometryContainer<ctype, dim>& c,
                typename GeometryContainer<ctype, dim>::TriangulationType t);

  void visitElement(const Geometry::Element<ctype, dim>& e);
  void visitReferenceVertex(const Geometry::ReferenceVertex<ctype, dim>& v);
  void visitFaceVertex(const Geometry::FaceVertex<ctype, dim>& v);
  void visitCenterVertex(const Geometry::CenterVertex<ctype, dim>& v);
  void visitRootVertex(const Geometry::RootVertex<ctype, dim>& v);
  void visitIntersectionVertex(const Geometry::IntersectionVertex<ctype, dim>& v);

  template <typename ct, int d>
  friend std::ostream& operator<<(std::ostream& s,
                                  const PythonAdapter<ct, d>& p);
private:
  std::stringstream s_;
};

template <typename ctype, int dim>
PythonAdapter<ctype, dim>::PythonAdapter(const GeometryContainer<ctype, dim>& c,
                                         typename GeometryContainer<ctype, dim>::TriangulationType t) {
  typedef typename GeometryContainer<ctype, dim>::geo_iterator Iterator;
  Iterator itend = c.geoend(t), itbegin = c.geobegin(t);
  s_ << "[";
  for (Iterator it = itbegin; it != itend; ++it) {
    s_ << (it != itbegin ? ", " : "") << PythonAdapter(*it);
  }
  s_ << "]";
}

template <typename ctype, int dim>
void PythonAdapter<ctype, dim>::visitElement(const Geometry::Element<ctype, dim>& e) {
  typedef typename Geometry::Element<ctype, dim>::const_iterator Iterator;
  Iterator itbegin = e.begin(), itend = e.end();
  s_ << "[";
  for (Iterator it = itbegin; it != itend; ++it)
    s_ << (it != itbegin ? ", " : "") << PythonAdapter(**it);
  s_ << "]";
}

template <typename ctype, int dim>
void PythonAdapter<ctype, dim>::visitReferenceVertex(const Geometry::ReferenceVertex<ctype, dim>& v) {
  s_ << v.id();
}

template <typename ctype, int dim>
void PythonAdapter<ctype, dim>::visitFaceVertex(const Geometry::FaceVertex<ctype, dim>& v) {
  s_ << "Face" << v.id();
}

template <typename ctype, int dim>
void PythonAdapter<ctype, dim>::visitRootVertex(const Geometry::RootVertex<ctype, dim>& v) {
  s_ << "Root" << v.id();
}

template <typename ctype, int dim>
void PythonAdapter<ctype, dim>::visitCenterVertex(const Geometry::CenterVertex<ctype, dim>& v) {
  s_ << "Center" << v.id();
}

template <typename ctype, int dim>
void PythonAdapter<ctype, dim>::visitIntersectionVertex(const Geometry::IntersectionVertex<ctype, dim>& v) {
  s_ << "(" << PythonAdapter(*(v.first())) << ", " << PythonAdapter(*(v.second())) << ")";
}

template <typename ctype, int dim>
std::ostream& operator<<(std::ostream& s,
                         const PythonAdapter<ctype, dim>& v) {
  return s << v.s_.str();
}

#endif //PYTHON_HH
