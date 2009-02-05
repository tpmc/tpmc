// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef MARCHING_CUBES_HH_
#define MARCHING_CUBES_HH_

#include "marchinglut.hh"
#include <dune/common/fvector.hh>
#include <dune/common/float_cmp.hh>

namespace Dune {

  /*
   * Contains marching cubes' 33 algorithm.
   */
  template <typename valueType, int dim, typename thresholdFunctor, typename baseElement>
  class MarchingCubesAlgorithm {
    typedef size_t sizeType;
    typedef valueType* valueVector;
    typedef double ctype;
    typedef Dune::FieldVector<ctype, dim> point;
  public:
    bool getOffsets(const valueVector& vertexValues, const sizeType vertexCount,
                    const bool useMc33, char * offsets);
    void getElements(const valueVector& vertexValues,
                     const sizeType vertexCount, const char * offsets,
                     std::vector<std::vector<point> >& codim0);

  private:
    /*
     * \brief Test if the face center is covered by the surface.
     *
     * This test is needed to chose between ambiguous MC33 cases.
     */
    bool testFaceIsSurface(const valueType cornerA, const valueType cornerB,
                           const valueType cornerC, const valueType cornerD, const bool notInverted) const;

    void getCoordsFromNumber(const valueVector& vertexValues,
                             const sizeType vertexCount, char number,
                             point& coords);

    void getCoordsFromEdgeNumber(const valueVector& vertexValues,
                                 const sizeType vertexCount, char number,
                                 point& coord);
  };

} // end namespace Dune


#include "marchingcubes.cc"

#endif /* MARCHING_CUBES_HH_ */
