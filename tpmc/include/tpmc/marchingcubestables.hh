// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_MARCHINGCUBESTABLES_HH
#define DUNE_MARCHINGCUBESTABLES_HH

namespace Dune {
  enum SymmetryType {
    symmetric, nonsymmetric
  };

  template <typename valueType, int dim, typename thresholdFunctor,
      SymmetryType symmetryType, typename intersectionFunctor>
  struct MarchingCubes33Tables;

  template <typename valueType, int dim, typename thresholdFunctor,
      typename intersectionFunctor>
  struct MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::nonsymmetric,
      intersectionFunctor> {
    /*
     * row containing information about a specific mc case. for details see
     * marchinglut.hh
     */
    typedef const unsigned short offsetRow[10];
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
    static const short * const all_case_vertices[];
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
  };



  template <typename valueType, int dim, typename thresholdFunctor,
      typename intersectionFunctor>
  struct MarchingCubes33Tables<valueType,dim,thresholdFunctor,
      SymmetryType::symmetric,
      intersectionFunctor> {
    /*
     * row containing information about a specific mc case. for details see
     * marchinglut.hh
     */
    typedef const unsigned short offsetRow[10];
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
    static const short * const all_case_vertices[];
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
  };
}

#include "marchingcubestables.cc"

#endif
