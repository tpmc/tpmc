// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef GEOMETRYCONTAINER_HH
#define GEOMETRYCONTAINER_HH

#include <dune/common/shared_ptr.hh>
#include <dune/geometry/type.hh>
#include <dune/geometry/referenceelements.hh>
#include "geometries.hh"

template <typename ctype, int dim>
class GeometryContainer {
public:
  enum TriangulationType {
    INTERIOR, EXTERIOR, INTERFACE
  };
  typedef std::size_t SizeType;
  typedef std::vector<Geometry::Element<ctype, dim> > ElementVectorType;
  typedef typename ElementVectorType::const_iterator geo_iterator;
  typedef typename Triangulation<ctype, dim>::const_iterator const_iterator;

  template <class FunctorType>
  void computeTriangulation(const FunctorType& f,
                            SizeType vertexCount);

  void add(const Geometry::Element<ctype, dim>& element,
           TriangulationType t) {
    switch (t) {
    case INTERIOR : mGeoInterior.push_back(element); break;
    case EXTERIOR : mGeoExterior.push_back(element); break;
    default : mGeoInterface.push_back(element); break;
    }
  }

  void remove(SizeType index,
              TriangulationType t) {
    switch (t) {
    case INTERIOR : mGeoInterior.erase(mGeoInterior.begin()+index); break;
    case EXTERIOR : mGeoExterior.erase(mGeoExterior.begin()+index); break;
    default : mGeoInterface.erase(mGeoInterface.begin()+index); break;
    }
  }

  bool empty(TriangulationType t) const {
    switch (t) {
    case INTERIOR : return mGeoInterior.empty();
    case EXTERIOR : return mGeoExterior.empty();
    default : return mGeoInterface.empty();
    }
  }

  SizeType size(TriangulationType t) const {
    switch (t) {
    case INTERIOR : return mGeoInterior.size();
    case EXTERIOR : return mGeoExterior.size();
    default : return mGeoInterface.size();
    }
  }

  const_iterator begin(TriangulationType t) const {
    switch (t) {
    case INTERIOR : return mInterior.begin();
    case EXTERIOR : return mExterior.begin();
    default : return mInterface.begin();
    }
  }
  const_iterator end(TriangulationType t) const {
    switch (t) {
    case INTERIOR : return mInterior.end();
    case EXTERIOR : return mExterior.end();
    default : return mInterface.end();
    }
  }

  geo_iterator geobegin(TriangulationType t) const {
    switch (t) {
    case INTERIOR : return mGeoInterior.begin();
    case EXTERIOR : return mGeoExterior.begin();
    default : return mGeoInterface.begin();
    }
  }
  geo_iterator geoend(TriangulationType t) const {
    switch (t) {
    case INTERIOR : return mGeoInterior.end();
    case EXTERIOR : return mGeoExterior.end();
    default : return mGeoInterface.end();
    }
  }
private:
  ElementVectorType mGeoInterior, mGeoExterior, mGeoInterface;
  Triangulation<ctype, dim> mInterior, mExterior, mInterface;

  template <class FunctorType, class VectorType>
  void ctImpl(const FunctorType& f, const VectorType& vertexValues,
              SizeType vertexCount,
              const ElementVectorType& geo,
              Triangulation<ctype,dim>& tri);
};

template <typename ctype, int dim>
template <class FunctorType>
void GeometryContainer<ctype, dim>::computeTriangulation(const FunctorType& f,
                                                         SizeType vertexCount) {
  Dune::GeometryType::BasicType bt = Dune::GeometryType::none;
  if (dim == 2) {
    switch (vertexCount) {
    case 3 : bt = Dune::GeometryType::simplex; break;
    case 4 : bt = Dune::GeometryType::cube; break;
    }
  } else if (dim == 3) {
    switch (vertexCount) {
    case 4 : bt = Dune::GeometryType::simplex; break;
    case 5 : bt = Dune::GeometryType::pyramid; break;
    case 6 : bt = Dune::GeometryType::prism; break;
    case 8 : bt = Dune::GeometryType::cube; break;
    }
  }
  Dune::GeometryType gt(bt, dim);
#if DUNE_VERSION_NEWER(DUNE_COMMON,2,3)
  const Dune::ReferenceElement<ctype, dim>& ref =
    Dune::ReferenceElements<ctype, dim>::general(gt);
#else
  const Dune::GenericReferenceElement<ctype, dim>& ref =
    Dune::GenericReferenceElements<ctype, dim>::general(gt);
#endif
  std::vector<ctype> vertexValues;
  for (int i = 0; i<ref.size(dim); ++i) {
    vertexValues.push_back(f(ref.position(i,dim)));
  }
  ctImpl(f, vertexValues, vertexCount, mGeoInterior, mInterior);
  ctImpl(f, vertexValues, vertexCount, mGeoExterior, mExterior);
  ctImpl(f, vertexValues, vertexCount, mGeoInterface, mInterface);
}

template <typename ctype, int dim>
template <class FunctorType, class VectorType>
void GeometryContainer<ctype, dim>::ctImpl(const FunctorType& f,
                                           const VectorType& vertexValues,
                                           SizeType vertexCount,
                                           const ElementVectorType& geo,
                                           Triangulation<ctype, dim>& tri) {
  typedef typename ElementVectorType::const_iterator element_iterator;
  typedef typename Geometry::Element<ctype, dim>::const_iterator vertex_iterator;
  tri.clear();
  element_iterator eitend = geo.end();
  for (element_iterator eit = geo.begin(); eit != eitend; ++eit) {
    Element<ctype, dim> element;
    vertex_iterator vitend = eit->end();
    for (vertex_iterator vit = eit->begin(); vit != vitend; ++vit) {
      Dune::FieldVector<ctype, dim> vertex;
      (*vit)->evaluate(vertexValues, vertexCount, vertex);
      Dune::FieldVector<ctype, dim> normal = f.gradient(vertex);
      normal /= normal.two_norm();
      element.add(Vertex<ctype, dim>(vertex, normal));
    }
    tri.add(element);
  }
}

#endif //GEOMETRYCONTAINER_HH
