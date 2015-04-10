// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TPMC_MARCHINGCUBES_HH
#define TPMC_MARCHINGCUBES_HH

#include <tpmc/aberthfunctor.hh>
#include <tpmc/marchingcubestables.hh>
#include <tpmc/marchinglut.hh>
#include <tpmc/geometrytype.hh>
#include <tpmc/fieldtraits.hh>

namespace tpmc
{
  /** \brief Exception to signal user that a method or configuration has not been implemented
   */
  class NotImplementedException : public std::exception {};

  enum ReconstructionType
  {
    Interior,
    Exterior,
    Interface
  };

  enum AlgorithmType
  {
    simpleMC,
    fullTPMC
  };

  class ReconstructionContext
  {
  public:
    ReconstructionContext() :
      vertexToIndex(max_complex_vertex_count + VERTICES_ON_REFERENCE_COUNT)
    {}

    int index(int vertex) const {
      return vertexToIndex[vertex];
    }
  private:
    template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
              SymmetryType::Value symmetryType, class intersectionFunctor>
    friend class MarchingCubes;
    std::vector<int> vertexToIndex;
  };

  /** \brief The 'topology preserving marching cubes' algorithm.
   */
  template <typename valueType, int dim, typename Coordinate, typename thresholdFunctor,
            SymmetryType::Value symmetryType = SymmetryType::nonsymmetric,
            typename IntersectionFunctor = AberthFunctor<Coordinate> >
  class MarchingCubes {
    typedef size_t size_type;
    typedef typename FieldTraits<Coordinate>::field_type ctype;
  public:

    template <typename InputIterator>
    size_type getKey(InputIterator valuesBegin, InputIterator valuesEnd) const;

    template <typename InputIterator, typename OutputIterator>
    void getVertices(InputIterator valuesBegin, InputIterator valuesEnd, size_type key,
                     ReconstructionContext& context, OutputIterator out) const;

    int getMaximalVertexCount(GeometryType type) const;

    template <typename OutputIterator>
    void getElements(GeometryType geometry, size_type key, ReconstructionType type,
                     OutputIterator out) const;

    template <typename OutputIterator>
    void getVertexGroups(GeometryType geometry, size_type key, OutputIterator out) const;

    template <typename OutputIterator>
    void getElementGroups(GeometryType geometry, size_type key, ReconstructionType type,
                          OutputIterator out) const;

    MarchingCubes(AlgorithmType _alorithmType = AlgorithmType::fullTPMC,
                  const thresholdFunctor& _threshFunctor = thresholdFunctor())
        : algorithmType(_alorithmType)
        , threshFunctor(_threshFunctor)
    {
    }

  private:

    /*
     * functor for defining and asserting numerical thresholds
     */
    const thresholdFunctor threshFunctor;

    /*
     * remember which mc algorithm to use
     */
    const AlgorithmType algorithmType;

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
    bool testAmbiguousCenter(InputIterator valuesBegin, InputIterator valuesEnd, size_type refCorner,
                             size_type refFace) const;

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
