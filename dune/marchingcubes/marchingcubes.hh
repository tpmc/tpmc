// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef MARCHING_CUBES_HH_
#define MARCHING_CUBES_HH_

#include <dune/common/fvector.hh>
#include <dune/common/float_cmp.hh>
#include <dune/common/exceptions.hh>

//#include <dune/marchingcubes/newtonfunctor.hh>
#include <dune/marchingcubes/aberthfunctor.hh>
#include "marchingcubestables.hh"

namespace Dune {

  /** \brief Exception to signal user that he used a method in an unintended way
   */
  class IllegalArgumentException : public Dune::Exception {};
  /** \brief Exception to signal user that a method or configuration has not been implemented
   */
  class NotImplementedException : public Dune::Exception {};

  /** \brief The 'marching cubes 33' algorithm.
   */
  //template <typename valueType, int dim, typename thresholdFunctor,
  //          class intersectionFunctor = NewtonFunctor<valueType> >
  template <typename valueType, int dim, typename thresholdFunctor,
      SymmetryType symmetryType = SymmetryType::nonsymmetric,
      class intersectionFunctor = AberthFunctor<valueType> >
  class MarchingCubes33 {
    typedef size_t sizeType;
    typedef double ctype;
    typedef Dune::FieldVector<ctype, dim> point;
  public:
    template <typename valueVector>
    sizeType getKey(const valueVector& vertex_values,
                    const sizeType vertex_count,
                    const bool use_mc_33) const;
    template <typename valueVector>
    void getElements(const valueVector& vertex_values,
                     const sizeType vertex_count,
                     const sizeType key,
                     const bool codim_1_not_0,
                     const bool exterior_not_interior,
                     std::vector<std::vector<point> >& elements) const;
    void getVertexGroups(const sizeType vertex_count,
                         const sizeType key,
                         std::vector<short>& vertex_groups) const;
    void getElementGroups(const sizeType vertex_count,
                          const sizeType key,
                          const bool exterior_not_interior,
                          std::vector<short>& element_groups) const;
    void getNormal(const std::vector<point>& element, point& coord) const;

    MarchingCubes33(const thresholdFunctor & _threshFunctor = thresholdFunctor())
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
    typedef MarchingCubes33Tables<valueType,dim,thresholdFunctor,
        symmetryType,intersectionFunctor> Tables;

    /** \brief Test if the face center is covered by the surface.
     *
     * This test is needed to choose between ambiguous MC33 cases.
     */
    bool testAmbiguousFace(const valueType corner_a, const valueType cornerB,
                           const valueType cornerC, const valueType cornerD, bool inverse) const;

    /** \brief Only to be called on cube. Tests if <code>refCorner</code> is
     * connected to its diagonally opposed corner
     *
     * This test is needed to choose between ambiguous MC33 cases.
     */
    template <typename valueVector>
    bool testAmbiguousCenter(const valueVector& vertex_values,
                             const sizeType vertex_count, size_t refCorner
                             , size_t refFace) const;

    /** \brief gets coordinates of the vertex represented by
     * <code>number<code> (either a vertex, edge or center number)
     */
    template <typename valueVector>
    void getCoordsFromNumber(const valueVector& vertex_values,
                             const sizeType vertex_count, const short number,
                             point& coord) const;
    /** \brief gets coordinates of the vertex on the face with given id
     */
    template <typename valueVector>
    void getCoordsFromFaceId(const valueVector& vertex_values,
                             const sizeType vertex_count, short faceid,
                             point& coord) const;
    /** \brief gets coordinates of the vertex on the face with given ids
     */
    template <typename valueVector>
    void getCoordsFromRectangularFace(const valueVector& vertex_values,
                                      const sizeType vertex_count, short a,
                                      short b, short c, short d, short faceid,
                                      point& coord) const;
    /** \brief gets coordinates of the vertex on the face with given ids
     */
    template <typename valueVector>
    void getCoordsFromTriangularFace(const valueVector& vertex_values,
                                     const sizeType vertex_count, short a,
                                     short b, short c, short faceid,
                                     point& coord) const;
    /** \brief gets coordinates of the first point of an edge given by its
     * <code>number</code>
     */
    template <typename valueVector>
    void getCoordsFromEdgeNumber(const valueVector& vertexValues,
                                 const sizeType vertexCount, char number,
                                 point& coord) const;
  };

} // end namespace Dune


#include "marchingcubes.cc"

#endif /* MARCHING_CUBES_HH_ */
