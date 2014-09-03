// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef GEOMETRIES_HH
#define GEOMETRIES_HH

#include <cassert>
#include <sstream>
#include <dune/common/shared_ptr.hh>
#include <dune/marchingcubes/newtonfunctor.hh>
#include <dune/marchingcubes/aberthfunctor.hh>

namespace Geometry {
  namespace {
    template <class ctype>
    double interpolateCoord(const std::vector<double>& v, const Dune::FieldVector<ctype, 3>& c) {
      assert(v.size() == 8);
      return c[2]*(c[1]*(c[0]*v[7]+(1-c[0])*v[6])+(1-c[1])*(c[0]*v[5]+(1-c[0])*v[4]))
             + (1-c[2])*(c[1]*(c[0]*v[3]+(1-c[0])*v[2])+(1-c[1])*(c[0]*v[1]+(1-c[0])*v[0]));
    }
  }

  template <typename ctype, int dim>
  class GeometryVisitor;

  template <typename ctype, int dim>
  class Vertex {
  public:
    typedef std::size_t SizeType;
    typedef std::vector<double> VectorType;

    virtual void evaluate(const VectorType& vertexValues, SizeType vertexCount,
                          Dune::FieldVector<ctype, dim>& result) const = 0;
    virtual void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const = 0;
    virtual ~Vertex() {}
  };

  template <typename ctype, int dim>
  class ReferenceVertex : public Vertex<ctype, dim> {
  public:
    typedef typename Vertex<ctype, dim>::SizeType SizeType;
    typedef typename Vertex<ctype, dim>::VectorType VectorType;

    ReferenceVertex(SizeType id) : mId(id) {}

    void evaluate(const VectorType& vertexValues, SizeType vertexCount,
                  Dune::FieldVector<ctype, dim>& result) const;
    SizeType id() const { return mId; }

    void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const {
      visitor.visitReferenceVertex(*this);
    }
  private:
    SizeType mId;
  };

  template <typename ctype, int dim>
  class CenterVertex : public Vertex<ctype, dim> {
  public:
    typedef typename Vertex<ctype, dim>::SizeType SizeType;
    typedef typename Vertex<ctype, dim>::VectorType VectorType;

    CenterVertex(SizeType id) : mId(id) {}

    void evaluate(const VectorType& vertexValues, SizeType vertexCount,
                  Dune::FieldVector<ctype, dim>& result) const;
    SizeType id() const { return mId; }

    void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const {
      visitor.visitCenterVertex(*this);
    }
  private:
    SizeType mId;
  };

  template <typename ctype, int dim>
  class FaceVertex : public Vertex<ctype, dim> {
  public:
    typedef typename Vertex<ctype, dim>::SizeType SizeType;
    typedef typename Vertex<ctype, dim>::VectorType VectorType;

    FaceVertex(SizeType id) : mId(id) {}

    void evaluate(const VectorType& vertexValues, SizeType vertexCount,
                  Dune::FieldVector<ctype, dim>& result) const;
    SizeType id() const { return mId; }

    void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const {
      visitor.visitFaceVertex(*this);
    }
  private:
    SizeType mId;
  };

  template <typename ctype, int dim>
  class RootVertex : public Vertex<ctype, dim> {
  public:
    typedef typename Vertex<ctype, dim>::SizeType SizeType;
    typedef typename Vertex<ctype, dim>::VectorType VectorType;

    RootVertex(SizeType id) : mId(id) {}

    void evaluate(const VectorType& vertexValues, SizeType vertexCount,
                  Dune::FieldVector<ctype, dim>& result) const;
    SizeType id() const { return mId; }

    void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const {
      visitor.visitRootVertex(*this);
    }
  private:
    SizeType mId;
  };

  template <typename ctype, int dim>
  class IntersectionVertex : public Vertex<ctype, dim> {
  public:
    typedef typename Vertex<ctype, dim>::SizeType SizeType;
    typedef typename Vertex<ctype, dim>::VectorType VectorType;

    IntersectionVertex(Dune::shared_ptr<Vertex<ctype, dim> > first,
                       Dune::shared_ptr<Vertex<ctype, dim> > second)
      : mFirst(first), mSecond(second) {}

    void evaluate(const VectorType& vertexValues, SizeType vertexCount,
                  Dune::FieldVector<ctype, dim>& result) const;

    Dune::shared_ptr<Vertex<ctype, dim> > first() const { return mFirst; }
    Dune::shared_ptr<Vertex<ctype, dim> > second() const { return mSecond; }

    void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const {
      visitor.visitIntersectionVertex(*this);
    }
  private:
    Dune::shared_ptr<Vertex<ctype, dim> > mFirst, mSecond;
  };

  template <typename ctype, int dim>
  class Element {
  public:
    typedef std::size_t SizeType;
    typedef std::vector<Dune::shared_ptr<Vertex<ctype, dim> > > ContainerType;
    typedef typename ContainerType::const_iterator const_iterator;

    void add(Dune::shared_ptr<Vertex<ctype, dim> > v) {
      vertices.push_back(v);
    }

    bool valid() const {
      switch (dim) {
      case 0 :
        return vertices.size() == 1;
      case 1 :
        return vertices.size() == 2;
      case 2 :
        return vertices.size() == 3 || vertices.size() == 4;
      case 3 :
        return vertices.size() == 4 || vertices.size() == 5 || vertices.size() == 6 || vertices.size() == 8;
      default :
        return false;
      }
    }

    const_iterator begin() const { return vertices.begin(); }
    const_iterator end() const { return vertices.end(); }

    void takeVisitor(GeometryVisitor<ctype, dim>& visitor) const {
      visitor.visitElement(*this);
    }
  private:
    ContainerType vertices;
  };

  template <typename ctype, int dim>
  class GeometryVisitor {
  public:
    virtual void visitElement(const Element<ctype, dim>& e) = 0;
    virtual void visitReferenceVertex(const ReferenceVertex<ctype, dim>& v) = 0;
    virtual void visitFaceVertex(const FaceVertex<ctype, dim>& v) = 0;
    virtual void visitRootVertex(const RootVertex<ctype, dim>& v) = 0;
    virtual void visitCenterVertex(const CenterVertex<ctype, dim>& v) = 0;
    virtual void visitIntersectionVertex(const IntersectionVertex<ctype, dim>& v) = 0;
  };

  // Implementations:

  template <typename ctype, int dim>
  void ReferenceVertex<ctype, dim>::evaluate(const VectorType& vertexValues, SizeType vertexCount,
                                             Dune::FieldVector<ctype, dim>& result) const {
    SizeType id = mId;
    // renumber simplex or prism
    if (dim == 3) {
      if (vertexCount == 4) {
        static SizeType r[] = {0,1,2,4};
        id = r[mId];
      } else if (vertexCount == 6) {
        static SizeType r[] = {0,1,2,4,5,6};
        id = r[mId];
      }
    }
    for (int i = 0; i<dim; ++i) {
      result[i] = 1 & (id >> i);
    }
  }

  template <typename ctype, int dim>
  void RootVertex<ctype, dim>::evaluate(const VectorType& vertexValues, SizeType vertexCount,
                                        Dune::FieldVector<ctype, dim>& result) const {
    assert(dim == 3 && vertexCount == 8);
    static unsigned short permutations[][8] = {{0,2,4,6,1,3,5,7}, {0,1,4,5,2,3,6,7}, {0,1,2,3,4,5,6,7}};
    // x dir, y dir, z dir
    static unsigned short coordPerm[][3] = {{1,2,0}, {0,2,1}, {0,1,2}};
    unsigned short * currentPermutation = permutations[mId/2];
    unsigned short * currentCoordPerm = coordPerm[mId/2];
    double v[vertexCount];
    for (int i = 0; i<vertexCount; ++i) {
      v[i] = vertexValues[currentPermutation[i]];
    }
    const double C = v[0]*v[7]-v[1]*v[6]-v[2]*v[5]+v[3]*v[4];
    const double A = C-2*(v[4]*v[7]-v[5]*v[6]);
    const double B = C-2*(v[0]*v[3]-v[1]*v[2]);
    const double D = std::sqrt(-A*B+C*(A+B));
    double root = (B+D)/(A+B);
    double factor0 = A-D;
    double factor1 = B+D;
    if (Dune::FloatCmp::lt(root,0.0) || Dune::FloatCmp::gt(root,1.0)) {
      factor0 = A+D;
      factor1 = B-D;
      root = (B-D)/(A+B);
    }
    const double denom = factor0*(v[0]-v[1]-v[2]+v[3]) + factor1*(v[4]-v[5]-v[6]+v[7]);
    result[currentCoordPerm[0]] = (factor0*(v[0]-v[2])+factor1*(v[4]-v[6]))/denom;
    result[currentCoordPerm[1]] = (factor0*(v[0]-v[1])+factor1*(v[4]-v[5]))/denom;
    result[currentCoordPerm[2]] = root;
  }

  template <typename ctype, int dim>
  void FaceVertex<ctype, dim>::evaluate(const VectorType& vertexValues, SizeType vertexCount,
                                        Dune::FieldVector<ctype, dim>& result) const {
    assert(dim == 3 && vertexCount == 8);
    static unsigned short ids[][4] = {{0,2,4,6},{1,3,5,7},{0,1,4,5},{2,3,6,7},
                                      {0,1,2,3},{4,5,6,7}};
    static unsigned short use[][3] = {{0,1,2},{1,0,2},{2,0,1}};
    double a = vertexValues[ids[mId][0]],
           b = vertexValues[ids[mId][1]],
           c = vertexValues[ids[mId][2]],
           d = vertexValues[ids[mId][3]];
    // if its a 0110 type face, compute center of hyperbola
    if (a*d > 0 && b*c > 0 && a*b < 0) {
      double factor = 1.0/(a-b-c+d);
      result[use[mId/2][0]] = (mId % 2 == 1);
      result[use[mId/2][1]] = factor*(a-c);
      result[use[mId/2][2]] = factor*(a-b);
    } else if (a*b > 0 && c*d > 0 && a*c < 0) {
      result[use[mId/2][0]] = (mId % 2 == 1);
      result[use[mId/2][1]] = 0.5;
      result[use[mId/2][2]] = (a+b)/(a+b-c-d);
    } else if (a*c > 0 && b*d > 0 && a*b < 0) {
      result[use[mId/2][0]] = (mId % 2 == 1);
      result[use[mId/2][1]] = (a+c)/(a-b+c-d);
      result[use[mId/2][2]] = 0.5;
    } else {     // use center of mass
      // translate min to 1
      double m = std::min(std::min(a,b), std::min(c,d));
      a -= m-1;
      b -= m-1;
      c -= m-1;
      d -= m-1;
      double sum = a+b+c+d;
      result[use[mId/2][0]] = (mId % 2 == 1);
      result[use[mId/2][1]] = (b+d)/sum;
      result[use[mId/2][2]] = (c+d)/sum;
    }
  }

  template <typename ctype, int dim>
  void CenterVertex<ctype, dim>::evaluate(const VectorType& vertexValues, SizeType vertexCount,
                                          Dune::FieldVector<ctype, dim>& result) const {
    assert(dim == 3 && vertexCount == 8);
    static unsigned short permutations[][8] = {{0,2,4,6,1,3,5,7}, {0,1,4,5,2,3,6,7}, {0,1,2,3,4,5,6,7}};
    // x dir, y dir, z dir
    static unsigned short coordPerm[][3] = {{1,2,0}, {0,2,1}, {0,1,2}};
    unsigned short * currentPermutation = permutations[mId/2];
    unsigned short * currentCoordPerm = coordPerm[mId/2];
    double v[vertexCount];
    for (int i = 0; i<vertexCount; ++i) {
      v[i] = vertexValues[currentPermutation[i]];
    }
    const double C = v[0]*v[7]-v[1]*v[6]-v[2]*v[5]+v[3]*v[4];
    const double A = C-2*(v[4]*v[7]-v[5]*v[6]);
    const double B = C-2*(v[0]*v[3]-v[1]*v[2]);
    const double D = A*(v[0]-v[1]-v[2]+v[3])
      + B*(v[4]-v[5]-v[6]+v[7]);
    result[currentCoordPerm[0]] = (A*(v[0]-v[2])+B*(v[4]-v[6]))/D;
    result[currentCoordPerm[1]] = (A*(v[0]-v[1])+B*(v[4]-v[5]))/D;
    result[currentCoordPerm[2]] = B/(A+B);
  }

  template <typename ctype, int dim>
  void IntersectionVertex<ctype, dim>::evaluate(const VectorType& vertexValues, SizeType vertexCount,
                                                Dune::FieldVector<ctype, dim>& result) const {
    Dune::FieldVector<ctype, dim> first, second;
    mFirst->evaluate(vertexValues, vertexCount, first);
    mSecond->evaluate(vertexValues, vertexCount, second);
    double va = interpolateCoord(vertexValues, first);
    double vb = interpolateCoord(vertexValues, second);
    static const double eps = 1e-10;
    static Dune::FloatCmpOps<double, Dune::FloatCmp::absolute> cmp(eps);
    if ((cmp.lt(va,0.0) && cmp.lt(vb,0.0))
        || (cmp.gt(va,0.0) && cmp.gt(vb,0.0))
        || (cmp.eq(va,0.0) && cmp.eq(vb,0.0))) {
      result = first;
      result += second;
      result *= 0.5;
    } else {
      //static Dune::NewtonFunctor<double> nf;
      //nf.findRoot(vertexValues, first, second, result);
      Dune::AberthFunctor<double> af;
      af.findRoot(vertexValues, first, second, result);
    }
  }
}

#endif //GEOMETRIES_HH
