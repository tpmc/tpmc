// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef MARCHINGCUBESCONTAINER_HH
#define MARCHINGCUBESCONTAINER_HH

#include "triangulation.hh"

template <typename ctype, int dim>
class MarchingCubesContainer {
public:
  typedef typename Triangulation<ctype, dim>::const_iterator const_iterator;

  template <class GridViewType, class FunctorType>
  void computeTriangulation(const GridViewType& gv,
                            const FunctorType& f = FunctorType());
  const_iterator fbegin() const { return mInterface.begin(); }
  const_iterator fend() const { return mInterface.end(); }
  const_iterator ibegin() const { return mInterior.begin(); }
  const_iterator iend() const { return mInterior.end(); }
  const_iterator ebegin() const { return mExterior.begin(); }
  const_iterator eend() const { return mExterior.end(); }
private:
  typedef Dune::MarchingCubes::ThresholdFunctor<ctype> ThresholdFunctor;
  typedef Dune::MarchingCubes33<ctype, dim, ThresholdFunctor> MCType;
  MCType mMc;
  Triangulation<ctype, dim> mInterface, mInterior, mExterior;

  template <class VectorType, class Geometry, class FunctorType>
  void update(const std::vector<std::vector<VectorType> >& localElements,
              const Geometry& geometry,
              const FunctorType& f,
              Triangulation<ctype, dim>& result);
};

template <typename ctype, int dim>
template <class GridViewType, class FunctorType>
void MarchingCubesContainer<ctype, dim>::computeTriangulation(const GridViewType& gv,
                                                              const FunctorType& f) {
  mInterface.clear();
  mInterior.clear();
  mExterior.clear();
  typedef typename GridViewType::template Codim<0>::Iterator Iterator;
  typedef typename GridViewType::template Codim<0>::Entity::Geometry Geometry;
  Iterator endit = gv.template end<0>();
  for (Iterator it = gv.template begin<0>(); it != endit; ++it) {
    const Geometry& geometry = it->geometry();
    std::vector<ctype> vertex_values;
    std::size_t corners = geometry.corners();
    for (std::size_t i = 0; i<corners; ++i) {
      vertex_values.push_back(f(geometry.corner(i)));
    }
    typedef Dune::FieldVector<ctype, dim> FVType;
    typedef std::vector<std::vector<FVType> > ResultType;
    ResultType resInterface, resInterior, resExterior;
    std::size_t key = mMc.getKey(vertex_values, corners, true);
    mMc.getElements(vertex_values, corners, key, true, false, resInterface);
    mMc.getElements(vertex_values, corners, key, false, false, resInterior);
    mMc.getElements(vertex_values, corners, key, false, true, resExterior);
    // update local to global and compute gradient
    update(resInterface, geometry, f, mInterface);
    update(resInterior, geometry, f, mInterior);
    update(resExterior, geometry, f, mExterior);
  }
}

template <typename ctype, int dim>
template <class VectorType, class Geometry, class FunctorType>
void MarchingCubesContainer<ctype, dim>::update(const std::vector<std::vector<VectorType> >& localElements,
                                                const Geometry& geometry,
                                                const FunctorType& f,
                                                Triangulation<ctype, dim>& result) {
  for (std::size_t i = 0; i<localElements.size(); ++i) {
    Element<ctype, dim> e;
    for (std::size_t j = 0; j<localElements[i].size(); ++j) {
      VectorType vertex = geometry.global(localElements[i][j]);
      VectorType gradient = f.gradient(vertex);
      gradient /= gradient.two_norm();
      e.add(Vertex<ctype, dim>(vertex, gradient));
    }
    result.add(e);
  }
}

#endif //MARCHINGCUBESCONTAINER_HH
