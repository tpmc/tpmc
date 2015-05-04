// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TPMC_MARCHINGCUBES_HH
#define TPMC_MARCHINGCUBES_HH

#include <tpmc/aberthfunctor.hh>
#include <tpmc/marchingcubestables.hh>
#include <tpmc/marchinglut.hh>
#include <tpmc/geometrytype.hh>
#include <tpmc/fieldtraits.hh>
#include <tpmc/thresholdfunctor.hh>

namespace tpmc
{
  /** \brief Exception to signal user that a method or configuration has not been implemented
   */
  class NotImplementedException : public std::exception {};

  enum ReconstructionType
  {
    InteriorDomain,
    ExteriorDomain,
    Interface
  };

  enum AlgorithmType
  {
    simpleMC,
    fullTPMC
  };

  /** \brief The 'topology preserving marching cubes' algorithm.
   */
  template <typename valueType, int dim, typename Coordinate,
            typename thresholdFunctor = ThresholdFunctor<valueType>,
            SymmetryType::Value symmetryType = SymmetryType::nonsymmetric,
            typename IntersectionFunctor = AberthFunctor<Coordinate> >
  class MarchingCubes {
    typedef size_t size_type;
    typedef typename FieldTraits<Coordinate>::field_type ctype;
  public:

    template <typename InputIterator>
    size_type getKey(InputIterator valuesBegin, InputIterator valuesEnd) const;

    /** \brief calculates the coordinates of all complex vertices used in a
     * reconstruction for a given key
     *
     * The resulting vertices are of type Coordinate and are stored using
     * the output iterator. A complex vertex denotes any vertex but the
     * vertices of the reference element. The use of this method makes sure
     * that no complex vertex for a specific set of corner values has to
     * be computed more than once.
     */
    template <typename InputIterator, typename OutputIterator>
    void getVertices(InputIterator valuesBegin, InputIterator valuesEnd, size_type key,
                     OutputIterator out) const;

    int getMaximalVertexCount(GeometryType type) const;

    /** \brief return the specific reconstruction for a given key and geometry type
     *
     * The resulting Elements are stored as std::vector<int> in the given output
     * iterator. An element is represented by its vertex indices. A vertex can be
     * either negative or non-negative. If a vertex index i is negative, it represents
     * the (-i-1)th corner of the reference element in the numbering of the reference
     * cube. If i is non-negative, it represents the i-th vertex returned by a
     * call of getVertices().
     */
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
     * remember which mc algorithm to use
     */
    const AlgorithmType algorithmType;

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
                                            short a, short b, short c, short d) const;
    /** \brief gets coordinates of the vertex on the face with given ids
     */
    template <typename InputIterator>
    Coordinate getCoordsFromTriangularFace(InputIterator valuesBegin, InputIterator valuesEnd,
                                           short a, short b, short c) const;
    /** \brief gets coordinates of the first point of an edge given by its
     * <code>number</code>
     */
    Coordinate getCoordsFromReferenceCorner(short number) const;
  };
}

#include "marchingcubes_impl.hh"

#endif // TPMC_MARCHINGCUBES_HH
