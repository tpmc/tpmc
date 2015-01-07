// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TPMC_MARCHINGCUBESTABLES_HH
#define TPMC_MARCHINGCUBESTABLES_HH

namespace tpmc {
  enum SymmetryType {
    symmetric, nonsymmetric
  };

  template <SymmetryType symmetryType>
  struct MarchingCubesTables;

  template <>
  struct MarchingCubesTables<SymmetryType::nonsymmetric> {
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

    static int all_complex_vertex_count[];

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



  template <>
  struct MarchingCubesTables<SymmetryType::symmetric> {
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

    static int all_complex_vertex_count[];
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

#endif // TPMC_MARCHINGCUBESTABLES_HH
