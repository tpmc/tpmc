// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef __MARCHINGCUBESGUI_H__
#define __MARCHINGCUBESGUI_H__

#include <vector>
#include <memory>
#include <dune/marchingcubes/marchingcubes.hh>
#include <dune/marchingcubes/thresholdfunctor.hh>
#include <dune/common/float_cmp.hh>
#include <dune/grid/sgrid.hh>
#include <dune/grid/common/mcmgmapper.hh>
#include "marchingcubescontainer.hh"
#include "trilinearfunctor.hh"
#include "planefunctor.hh"

template <std::size_t N>
class MarchingCubesGUI {
public:
  typedef double ValueType;
  typedef double CoordType;
  typedef Dune::SGrid<3,3,CoordType> VolumeGridType;
  typedef Dune::SGrid<2,2,CoordType> PlaneGridType;
  typedef Element<ValueType, 3>::VectorType VectorType;
  typedef Element<ValueType, 2>::VectorType PlaneVectorType;
  typedef std::vector<Element<ValueType, 3> > VolumeTriangulationType;
  typedef std::vector<Element<ValueType, 2> > PlaneTriangulationType;
  static const int TRIANGULATION_COUNT = N;

  MarchingCubesGUI();
  void computeTriangulations();
  void getFaceCenter(std::size_t i, VectorType& result) const;
  std::size_t getFaceCount() const { return 6; }
  ValueType getVertexValue(std::size_t i) const { return mVertexValues[i]; }
  void setVertexValue(std::size_t i, ValueType v) { mVertexValues[i] = v; }
  std::size_t getRefinements(std::size_t i) const { return mRefinements[i]; }
  void setRefinements(std::size_t i, std::size_t v) { mRefinements[i] = v; mGridValid[i] = false; }
  const VectorType& getPlanePosition() const { return mPlanePosition; }
  void setPlanePosition(const VectorType& v) { mPlanePosition = v; }
  const VectorType& getPlaneFirst() const { return mPlaneFirst; }
  void setPlaneFirst(const VectorType& v) { mPlaneFirst = v; }
  const VectorType& getPlaneSecond() const { return mPlaneSecond; }
  void setPlaneSecond(const VectorType& v) { mPlaneSecond = v; }
  VolumeTriangulationType::const_iterator fbegin(std::size_t i) const { return mGridContainers[i].fbegin(); }
  VolumeTriangulationType::const_iterator fend(std::size_t i) const { return mGridContainers[i].fend(); }
  PlaneTriangulationType::const_iterator pibegin() const { return mPlaneGridContainer.ibegin(); }
  PlaneTriangulationType::const_iterator piend() const { return mPlaneGridContainer.iend(); }
  PlaneTriangulationType::const_iterator pfbegin() const { return mPlaneGridContainer.fbegin(); }
  PlaneTriangulationType::const_iterator pfend() const { return mPlaneGridContainer.fend(); }
private:
  ValueType mVertexValues[8];
  VectorType mPlanePosition;
  VectorType mPlaneFirst;
  VectorType mPlaneSecond;
  std::shared_ptr<VolumeGridType> mGrids[N];
  std::shared_ptr<PlaneGridType> mPlaneGrid;
  MarchingCubesContainer<CoordType, 3> mGridContainers[N];
  MarchingCubesContainer<CoordType, 2> mPlaneGridContainer;
  std::size_t mRefinements[N];
  bool mGridValid[N];
  std::size_t mPlaneGridRefinements;
  bool mPlaneGridValid;
  void updateGrids();
};

template <std::size_t N>
MarchingCubesGUI<N>::MarchingCubesGUI()
  : mPlanePosition(0), mPlaneFirst(0), mPlaneSecond(0),
    mPlaneGridRefinements(4), mPlaneGridValid(false) {
  std::fill(mVertexValues, mVertexValues+8, 1);
  std::fill(mGridValid, mGridValid+N, false);
  std::fill(mRefinements, mRefinements+N, 0);
  // start with face 4
  mPlaneFirst[0] = 1;
  mPlaneSecond[1] = 1;
  updateGrids();
}

template <std::size_t N>
void MarchingCubesGUI<N>::updateGrids() {
  for (std::size_t i = 0; i<N; ++i) {
    if (!mGridValid[i]) {
      mGrids[i] = std::shared_ptr<VolumeGridType>(new VolumeGridType);
      mGrids[i]->globalRefine(mRefinements[i]);
      mGridValid[i] = true;;
    }
  }
  if (!mPlaneGridValid) {
    mPlaneGrid = std::shared_ptr<PlaneGridType>(new PlaneGridType);
    mPlaneGrid->globalRefine(mPlaneGridRefinements);
    mPlaneGridValid = true;
  }
}

template <std::size_t N>
void MarchingCubesGUI<N>::getFaceCenter(std::size_t i,
                                        VectorType& result) const {
  static const short faces[][4] = {{0,2,4,6}, {1,3,5,7}, {0,1,4,5},
                                   {2,3,6,7}, {0,1,2,3}, {4,5,6,7}};
  // const, first dir, second dir
  static const short dirs[][3] = {{0,1,2}, {0,1,2}, {1,0,2}, {1,0,2},
                                  {2,0,1}, {2,0,1}};
  static const ValueType constvalues[] = {0.0, 1.0, 0.0, 1.0, 0.0, 1.0};
  ValueType a = mVertexValues[faces[i][0]],
            b = mVertexValues[faces[i][1]],
            c = mVertexValues[faces[i][2]],
            d = mVertexValues[faces[i][3]];
  ValueType factor = 1.0/(a-b-c+d);
  result[dirs[i][0]] = constvalues[i];
  result[dirs[i][1]] = factor*(a-c);
  result[dirs[i][2]] = factor*(a-b);
}

template <std::size_t N>
void MarchingCubesGUI<N>::computeTriangulations() {
  updateGrids();
  typedef TrilinearFunctor<CoordType, ValueType> FunctorType;
  FunctorType functor(mVertexValues);
  typedef VolumeGridType::LeafGridView LeafGridView;
  typedef typename LeafGridView::Codim<0>::Entity::Geometry Geometry;
  for (std::size_t i = 0; i<N; ++i) {
    LeafGridView leafView = mGrids[i]->leafView();
    mGridContainers[i].computeTriangulation(leafView, functor);
  }
  typedef PlaneGridType::LeafGridView PlaneLeafGridView;
  PlaneFunctor<FunctorType> planeFunctor(functor, mPlanePosition,
                                         mPlaneFirst, mPlaneSecond);
  PlaneLeafGridView planeView = mPlaneGrid->leafView();
  mPlaneGridContainer.computeTriangulation(planeView, planeFunctor);
}


#endif //__MARCHINGCUBESGUI_H__
