// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TPMC_MARCHINGCUBES_HH
#define TPMC_MARCHINGCUBES_HH

#include <tpmc/aberthfunctor.hh>
#include <tpmc/marchingcubestables.hh>
#include <tpmc/geometrytype.hh>

namespace tpmc
{
  /** \brief Exception to signal user that a method or configuration has not been implemented
   */
  class NotImplementedException : public std::exception {};

  enum TriangulationType
  {
    Interior,
    Exterior,
    Interface
  };

  /** \brief The 'topology preserving marching cubes' algorithm.
   */
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType symmetryType = SymmetryType::nonsymmetric,
            typename IntersectionFunctor = AberthFunctor<Coordinate> >
  class MarchingCubes {
    typedef size_t sizeType;
    typedef typename Coordinate::value_type ctype;
  public:

    template <typename InputIterator>
    sizeType getKey(InputIterator valuesBegin, InputIterator valuesEnd, const bool use_mc_33) const;

    template <typename InputIterator, typename OutputIterator>
    void getVertices(InputIterator valuesBegin, InputIterator valuesEnd, sizeType key,
                     std::vector<int>& vertexToIndex, OutputIterator out) const;

    int getMaximalVertexCount(GeometryType type) const;

    template <typename OutputIterator>
    void getElements(GeometryType geometry, sizeType key, TriangulationType type,
                     OutputIterator out) const;

    template <typename OutputIterator>
    void getVertexGroups(GeometryType geometry, sizeType key, OutputIterator out) const;

    template <typename OutputIterator>
    void getElementGroups(GeometryType geometry, sizeType key, TriangulationType type,
                          OutputIterator out) const;

    MarchingCubes(const thresholdFunctor& _threshFunctor = thresholdFunctor())
        : threshFunctor(_threshFunctor) {}

  private:

    /*
     * functor for defining and asserting numerical thresholds
     */
    const thresholdFunctor threshFunctor;

    /*
     * class containing tables as static members specialized by
     * symmetry type.
     */
    typedef MarchingCubesTables<symmetryType> Tables;

    /** \brief Test if the face center is covered by the surface.
     *
     * This test is needed to choose between ambiguous MC33 cases.
     */
    bool testAmbiguousFace(valueType cornerA, valueType cornerB,
                           valueType cornerC, valueType cornerD, bool inverse) const;

    /** \brief Only to be called on cube. Tests if <code>refCorner</code> is
     * connected to its diagonally opposed corner
     *
     * This test is needed to choose between ambiguous MC33 cases.
     */
    template <typename InputIterator>
    bool testAmbiguousCenter(InputIterator valuesBegin, InputIterator valuesEnd, sizeType refCorner,
                             sizeType refFace) const;

    /** \brief gets coordinates of the vertex represented by
     * <code>number<code> (either a vertex, edge or center number)
     */
    template <typename InputIterator>
    Coordinate getCoordsFromNumber(InputIterator valuesBegin, InputIterator valuesEnd,
                                   short number) const;

    /** \brief gets coordinates of the vertex on the face with given id
     */
    template <typename InputIterator>
    Coordinate getCoordsFromFaceId(InputIterator valuesBegin, InputIterator valuesEnd,
                                   short faceid) const;
    /** \brief gets coordinates of center vertex with given id
     */
    template <typename InputIterator>
    Coordinate getCoordsFromCenterId(InputIterator valuesBegin, InputIterator valuesEnd,
                                     short faceid) const;
    /** \brief gets coordinates of root vertex with given id
     */
    template <typename InputIterator>
    Coordinate getCoordsFromRootId(InputIterator valuesBegin, InputIterator valuesEnd,
                                   short faceid) const;
    /** \brief gets coordinates of the vertex on the face with given ids
     */
    template <typename InputIterator>
    Coordinate getCoordsFromRectangularFace(InputIterator valuesBegin, InputIterator valuesEnd,
                                            short a, short b, short c, short d, short faceid) const;
    /** \brief gets coordinates of the vertex on the face with given ids
     */
    template <typename InputIterator>
    Coordinate getCoordsFromTriangularFace(InputIterator valuesBegin, InputIterator valuesEnd,
                                           short a, short b, short c, short faceid) const;
    /** \brief gets coordinates of the first point of an edge given by its
     * <code>number</code>
     */
    template <typename InputIterator>
    Coordinate getCoordsFromEdgeNumber(InputIterator valuesBegin, InputIterator valuesEnd,
                                       char number) const;
  };
}

#include "marchingcubes_impl.hh"

#endif // TPMC_MARCHINGCUBES_HH
