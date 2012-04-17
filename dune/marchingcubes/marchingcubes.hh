// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef MARCHING_CUBES_HH_
#define MARCHING_CUBES_HH_

#include <dune/common/fvector.hh>
#include <dune/common/float_cmp.hh>
#include <dune/common/exceptions.hh>

namespace Dune {

  /** \brief Exception to signal user that he used a method in an unintended way
   */
  class IllegalArgumentException : public Dune::Exception {};

  /** \brief The 'marching cubes 33' algorithm.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
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

    MarchingCubes33(const thresholdFunctor & _threshFunctor = thresholdFunctor())
      : threshFunctor(_threshFunctor) {}

  private:

    /*
     * functor for defining and asserting numerical thresholds
     */
    const thresholdFunctor threshFunctor;
    /*
     * row containing information about a specific mc case. for details see
     * marchinglut.hh
     */
    typedef const short offsetRow[10];
    /*
     * contains offset-tables for different geometries. for details see
     * <code>marchinglut.hh</code>
     */
    static offsetRow * all_case_offsets[];
    /*
     * contains arrays for renumbering vertices. used for simplex and prism
     * to map the vertex numbers to the indices in the vertex-values array
     */
    static const short * const all_vertex_to_index[];
    /*
     * contains vertex_groups-tables for different geometries. for details
     * see <code>marchinglut.hh</code>
     */
    static const short * const all_vertex_groups[];
    /*
     * contains codim0-tables for different geometries. for details see
     * <code>marchinglut.hh</code>
     */
    static const short * const all_codim_0[][2];
    /*
     * contains element-groups-tables for different geometries. for details
     * see <code>marchinglut.hh</code>
     */
    static const short * const all_element_groups[][2];
    /*
     * contains codim1-tables for different geometries. for details see
     * <code>marchinglut.hh</code>
     */
    static const short * const all_codim_1[];
    /*
     * contains mc33-offset-tables for different geometries. for details see
     * <code>marchinglut.hh</code>
     */
    static const short * const all_mc33_offsets[];
    /*
     * contains test-tables for different geometries. for details see
     * <code>marchinglut.hh</code>
     */
    static const short * const all_face_tests[];

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
                             const sizeType vertex_count, size_t refCorner) const;

    /** \brief gets coordinates of the vertex represented by
     * <code>number<code> (either a vertex, edge or center number)
     */
    template <typename valueVector>
    void getCoordsFromNumber(const valueVector& vertex_values,
                             const sizeType vertex_count, const short number,
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
