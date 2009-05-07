// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef MARCHING_CUBES_HH_
#define MARCHING_CUBES_HH_

#include <dune/common/fvector.hh>
#include <dune/common/float_cmp.hh>
#include <dune/common/exceptions.hh>
#include <dune/grid/common/referenceelements.hh>

namespace Dune {
  /*
   * Exception to signal user that he used a method in a
   * not-intended way.
   */
  class IllegalArgumentException : public Dune::Exception {};

  /*
   * Contains marching cubes' 33 algorithm.
   */
  template <typename valueType, int dim, typename thresholdFunctor>
  class MarchingCubes33 {
    typedef size_t sizeType;
    typedef double ctype;
    typedef Dune::FieldVector<ctype, dim> point;
  public:
    template <typename valueVector>
    sizeType getKey(const valueVector& vertex_values,
                    const sizeType vertex_count, const bool use_mc_33);
    template <typename valueVector>
    void getElements(const valueVector& vertex_values,
                     const sizeType vertex_count,        const sizeType key,
                     const bool codim_1_not_0,
                     std::vector<std::vector<point> >& elements);

  private:
    /*
     * TODO: Comment
     */
    typedef const short offsetRow[5];
    static offsetRow * all_case_offsets[];
    static const short * const all_codim_0[];
    static const short * const all_codim_1[];
    static const short * const all_mc33_offsets[];
    static const short * const all_face_tests[];
    /*
     * \brief Test if the face center is covered by the surface.
     *
     * This test is needed to chose between ambiguous MC33 cases.
     */
    bool testAmbiguousFace(const valueType corner_a, const valueType cornerB,
                           const valueType cornerC, const valueType cornerD, bool inverse) const;

    template <typename valueVector>
    bool testAmbiguousCenter(const valueVector& vertex_values,
                             const sizeType vertex_count, size_t refCorner) const;

    template <typename valueVector>
    void getCoordsFromNumber(const valueVector& vertex_values,
                             const sizeType vertex_count, const short number,
                             point& coord) const;

    template <typename valueVector>
    void getCoordsFromEdgeNumber(const valueVector& vertexValues,
                                 const sizeType vertexCount, char number,
                                 point& coord) const;
  };

} // end namespace Dune


#include "marchingcubes.cc"

#endif /* MARCHING_CUBES_HH_ */
