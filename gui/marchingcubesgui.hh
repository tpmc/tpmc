// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __MARCHINGCUBESGUI_H__
#define __MARCHINGCUBESGUI_H__

#include <vector>
#include <memory>
#include <dune/marchingcubes/marchingcubes.hh>
#include <dune/marchingcubes/thresholdfunctor.hh>
#include <dune/common/float_cmp.hh>
#include <dune/grid/common/mcmgmapper.hh>
#include "referencegrid.hh"
#include "boundinggrid.hh"
#include "marchingcubescontainer.hh"
#include "trilinearfunctor.hh"
#include "planefunctor.hh"
#include "geometrycontainer.hh"
#include "geometryparser.hh"
#include "geometries.hh"
#include "python.hh"

template <std::size_t N>
class MarchingCubesGUI {
public:
  typedef double ValueType;
  typedef double CoordType;
  typedef MCGui::ReferenceGrid<Dune::GeometryType::cube,CoordType,3> VolumeGridType;
  typedef MCGui::ReferenceGrid<Dune::GeometryType::cube,CoordType,2> PlaneGridType;
  typedef MCGui::BoundingGrid<Dune::GeometryType::cube,CoordType,3> BoundingGridType;
  typedef Element<ValueType, 3>::VectorType VectorType;
  typedef Element<ValueType, 2>::VectorType PlaneVectorType;
  typedef std::vector<Element<ValueType, 3> > VolumeTriangulationType;
  typedef std::vector<Element<ValueType, 2> > PlaneTriangulationType;
  typedef GeometryContainer<CoordType, 3> GeoContainer;
  typedef typename GeoContainer::TriangulationType TriangulationType;
  typedef GeoContainer::geo_iterator geo_iterator;
  static const int TRIANGULATION_COUNT = N;

  template <class I>
  MarchingCubesGUI(I begin, I end);
  void computeTriangulations();
  void getFaceCenter(std::size_t i, VectorType& result) const;
  std::size_t getFaceCount() const { return 6; }
  ValueType getVertexValue(std::size_t i) const { return mValues[i]; }
  void setVertexValue(std::size_t i, ValueType v) { mValues[i] = v; }
  std::size_t getVertexCount() const { return mValues.size(); }
  std::size_t getRefinements(std::size_t i) const { return mRefinements[i]; }
  void setRefinements(std::size_t i, std::size_t v) { mRefinements[i] = v; mGridValid[i] = false; }
  const VectorType& getPlanePosition() const { return mPlanePosition; }
  void setPlanePosition(const VectorType& v) { mPlanePosition = v; }
  const VectorType& getPlaneFirst() const { return mPlaneFirst; }
  void setPlaneFirst(const VectorType& v) { mPlaneFirst = v; }
  const VectorType& getPlaneSecond() const { return mPlaneSecond; }
  void setPlaneSecond(const VectorType& v) { mPlaneSecond = v; }
  const BoundingGridType& getBoundingGrid() const { return mBoundingGrid; }
  void addGeometryElement(const std::string& pattern, TriangulationType t);
  void removeGeometryElement(std::size_t i, TriangulationType t);

  const MarchingCubesContainer<CoordType, 3>& gridContainer(std::size_t i) const { return mGridContainers[i]; }
  const MarchingCubesContainer<CoordType, 2>& planeGridContainer() const { return mPlaneGridContainer; }
  const GeoContainer& geometryContainer() const { return mGeometryContainer; }
private:
  VectorType mPlanePosition;
  VectorType mPlaneFirst;
  VectorType mPlaneSecond;
  VolumeGridType mGrids[N];
  BoundingGridType mBoundingGrid;
  std::vector<ValueType> mValues;
  PlaneGridType mPlaneGrid;
  MarchingCubesContainer<CoordType, 3> mGridContainers[N];
  MarchingCubesContainer<CoordType, 2> mPlaneGridContainer;
  GeoContainer mGeometryContainer;
  std::size_t mRefinements[N];
  bool mGridValid[N];
  std::size_t mPlaneGridRefinements;
  bool mPlaneGridValid;
  void updateGrids();
};

template <std::size_t N>
template <class I>
MarchingCubesGUI<N>::MarchingCubesGUI(I begin, I end)
  : mPlanePosition(0), mPlaneFirst(0), mPlaneSecond(0),
    mPlaneGridRefinements(4), mPlaneGridValid(false) {
  mValues.resize(mBoundingGrid.vertexCount());
  std::size_t index = 0;
  for (; index<mValues.size() && begin != end; ++index, ++begin) {
    mValues[index] = *begin;
  }
  std::fill(mValues.begin()+index, mValues.end(), 1);
  std::fill(mGridValid, mGridValid+N, false);
  std::fill(mRefinements, mRefinements+N, 2);
  mRefinements[0] = 4;
  // start with face 4
  mPlaneFirst[0] = 1;
  mPlaneSecond[1] = 1;
  updateGrids();
}

template <std::size_t N>
void MarchingCubesGUI<N>::updateGrids() {
  for (std::size_t i = 0; i<N; ++i) {
    if (!mGridValid[i]) {
      mGrids[i].reset();
      mGrids[i].refine(mRefinements[i]);
      mGridValid[i] = true;;
    }
  }
  if (!mPlaneGridValid) {
    mPlaneGrid.reset();
    mPlaneGrid.refine(mPlaneGridRefinements);
    mPlaneGridValid = true;
  }
}

template <std::size_t N>
void MarchingCubesGUI<N>::getFaceCenter(std::size_t i,
                                        VectorType& result) const {
  Geometry::FaceVertex<double,3> fv(i);
  fv.evaluate(mValues, mValues.size(), result);
}

template <std::size_t N>
void MarchingCubesGUI<N>::computeTriangulations() {
  updateGrids();
  typedef TrilinearFunctor<CoordType, ValueType> FunctorType;
  FunctorType functor(mValues);
  typedef typename VolumeGridType::GridViewType GridViewType;
  typedef typename GridViewType::Codim<0>::Entity::Geometry Geometry;
  for (std::size_t i = 0; i<N; ++i) {
    mGridContainers[i].computeTriangulation(mGrids[i].gridView(), functor);
  }
  mGeometryContainer.computeTriangulation(functor, mValues.size());
  PlaneFunctor<FunctorType> planeFunctor(functor, mPlanePosition,
                                         mPlaneFirst, mPlaneSecond);
  mPlaneGridContainer.computeTriangulation(mPlaneGrid.gridView(), planeFunctor);
}

template <std::size_t N>
void MarchingCubesGUI<N>::addGeometryElement(const std::string& pattern,
                                             TriangulationType t) {
  GeometryParser<','> parser;
  Geometry::Element<double, 3> element;
  std::cout << "parsing: " << pattern << "\n";
  parser.parse(pattern, element);
  //if (element.valid()) {
  std::cout << "element valid!\n";
  mGeometryContainer.add(element, t);
  typedef TrilinearFunctor<CoordType, ValueType> FunctorType;
  FunctorType functor(mValues);
  mGeometryContainer.computeTriangulation(functor, 8);
  //} else {
  //std::cout << "element not valid!\n";
  //}
}

template <std::size_t N>
void MarchingCubesGUI<N>::removeGeometryElement(std::size_t i,
                                                TriangulationType t) {
  mGeometryContainer.remove(i,t);
  typedef TrilinearFunctor<CoordType, ValueType> FunctorType;
  FunctorType functor(mValues);
  mGeometryContainer.computeTriangulation(functor, mValues.size());
}


#endif //__MARCHINGCUBESGUI_H__
