// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include <cmath>
#include <tpmc/marchingcubestables.hh>

namespace tpmc {

  /* table specialization for non symmetric tables */

  int MarchingCubesTables<SymmetryType::nonsymmetric>::all_max_complex_vertex_count[]
      = { 0,                                    0,
          0,                                    table_any1d_max_complex_vertex_count,
          0,                                    table_simplex2d_max_complex_vertex_count,
          table_cube2d_max_complex_vertex_count,    table_simplex3d_max_complex_vertex_count,
          table_pyramid3d_max_complex_vertex_count, table_prism3d_max_complex_vertex_count,
          0,                                    table_cube3d_max_complex_vertex_count };

  /*
   * Case offset tables (e.g. table_cube2d_cases offsets) for different
   * types of elements and dimensions.
   */
  typename MarchingCubesTables<SymmetryType::nonsymmetric>::offsetRow *
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_case_offsets[] = {0, 0, 0, table_any1d_cases_offsets,
                        0, table_simplex2d_cases_offsets,
                        table_cube2d_cases_offsets,
                        table_simplex3d_cases_offsets,
                        table_pyramid3d_cases_offsets,
                        table_prism3d_cases_offsets,
                        0, table_cube3d_cases_offsets};

  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_case_vertices[] = {0, 0, 0, table_any1d_vertices,
                         0, table_simplex2d_vertices,
                         table_cube2d_vertices, table_simplex3d_vertices,
                         table_pyramid3d_vertices, table_prism3d_vertices,
                         0, table_cube3d_vertices};

  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_vertex_to_index[] = {0, 0, 0, table_any1d_vertex_to_index,
                           0, table_simplex2d_vertex_to_index,
                           table_cube2d_vertex_to_index,
                           table_simplex3d_vertex_to_index,
                           table_pyramid3d_vertex_to_index,
                           table_prism3d_vertex_to_index,
                           0, table_cube3d_vertex_to_index};

  /*
   * vertex_groups tables (e.g. table_cube2d_vertex_groups) for different
   * types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_vertex_groups[] = {0, 0, 0, table_any1d_vertex_groups,
                         0, table_simplex2d_vertex_groups,
                         table_cube2d_vertex_groups,
                         table_simplex3d_vertex_groups,
                         table_pyramid3d_vertex_groups,
                         table_prism3d_vertex_groups,
                         0, table_cube3d_vertex_groups};

  /*
   * Codimension 0 element tables (e.g. table_cube2d_codim_0) for different
   * types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_codim_0[][2] = {{0, 0}, {0, 0}, {0, 0},
                      {table_any1d_codim_0_interior,
                       table_any1d_codim_0_exterior}, {0, 0},
                      {table_simplex2d_codim_0_interior,
                       table_simplex2d_codim_0_exterior},
                      {table_cube2d_codim_0_interior,
                       table_cube2d_codim_0_exterior},
                      {table_simplex3d_codim_0_interior,
                       table_simplex3d_codim_0_exterior},
                      {table_pyramid3d_codim_0_interior,
                       table_pyramid3d_codim_0_exterior},
                      {table_prism3d_codim_0_interior,
                       table_prism3d_codim_0_exterior}, {0, 0},
                      {table_cube3d_codim_0_interior,
                       table_cube3d_codim_0_exterior}};

  /*
   * element group tables (e.g. table_cube2d_codim_0_exterior_groups)
   * for different types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_element_groups[][2] = {{0, 0}, {0, 0}, {0, 0},
                             {table_any1d_interior_groups,
                              table_any1d_exterior_groups}, {0, 0},
                             {table_simplex2d_interior_groups,
                              table_simplex2d_exterior_groups},
                             {table_cube2d_interior_groups,
                              table_cube2d_exterior_groups},
                             {table_simplex3d_interior_groups,
                              table_simplex3d_exterior_groups},
                             {table_pyramid3d_interior_groups,
                              table_pyramid3d_exterior_groups},
                             {table_prism3d_interior_groups,
                              table_prism3d_exterior_groups}, {0, 0},
                             {table_cube3d_interior_groups,
                              table_cube3d_exterior_groups}};

  /*
   * Codimension 1 element tables (e.g. table_cube2d_codim_1) for different
   * types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_codim_1[] = {0, 0, 0, table_any1d_codim_1,
                   0, table_simplex2d_codim_1,
                   table_cube2d_codim_1, table_simplex3d_codim_1,
                   table_pyramid3d_codim_1, table_prism3d_codim_1, 0,
                   table_cube3d_codim_1};

  /*
   * MC33 offset tables (e.g. table_cube2d_mc33_offsets) for
   * different types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_mc33_offsets[] = {0, 0, 0, 0, 0, 0,
                        table_cube2d_mc33_offsets, 0,
                        table_pyramid3d_mc33_offsets,
                        table_prism3d_mc33_offsets, 0,
                        table_cube3d_mc33_offsets};

  /*
   * Test face tables (e.g. table_cube2d_mc33_face_test_order) for
   * different types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_face_tests[] = {0, 0, 0, 0, 0, 0,
                      table_cube2d_mc33_face_test_order, 0,
                      table_pyramid3d_mc33_face_test_order,
                      table_prism3d_mc33_face_test_order, 0,
                      table_cube3d_mc33_face_test_order};

  const short * const
  MarchingCubesTables<SymmetryType::nonsymmetric>::
  all_complex_vertices[] = {0, 0, 0, 0, 0, 0,
                        table_cube2d_complex_vertices, 0,
                        table_pyramid3d_complex_vertices,
                        table_prism3d_complex_vertices, 0,
                        table_cube3d_complex_vertices};


  /** table secialization for symmetric cases */

  int MarchingCubesTables<SymmetryType::symmetric>::all_max_complex_vertex_count[]
      = { 0,                                    0,
          0,                                    table_any1d_max_complex_vertex_count,
          0,                                    table_simplex2d_max_complex_vertex_count,
          table_cube2d_max_complex_vertex_count,    table_simplex3d_max_complex_vertex_count,
          table_pyramid3d_max_complex_vertex_count, table_prism3d_max_complex_vertex_count,
          0,                                    table_cube3dsym_max_complex_vertex_count };
  /*
   * Case offset tables (e.g. table_cube2d_cases offsets) for different
   * types of elements and dimensions.
   */
  typename MarchingCubesTables<SymmetryType::symmetric>::offsetRow *
  MarchingCubesTables<SymmetryType::symmetric>::
  all_case_offsets[] = {0, 0, 0, table_any1d_cases_offsets,
                        0, table_simplex2d_cases_offsets,
                        table_cube2d_cases_offsets,
                        table_simplex3d_cases_offsets,
                        table_pyramid3d_cases_offsets,
                        table_prism3d_cases_offsets,
                        0, table_cube3dsym_cases_offsets};

  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_case_vertices[] = {0, 0, 0, table_any1d_vertices,
                         0, table_simplex2d_vertices,
                         table_cube2d_vertices, table_simplex3d_vertices,
                         table_pyramid3d_vertices, table_prism3d_vertices,
                         0, table_cube3dsym_vertices};

  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_vertex_to_index[] = {0, 0, 0, table_any1d_vertex_to_index,
                           0, table_simplex2d_vertex_to_index,
                           table_cube2d_vertex_to_index,
                           table_simplex3d_vertex_to_index,
                           table_pyramid3d_vertex_to_index,
                           table_prism3d_vertex_to_index,
                           0, table_cube3d_vertex_to_index};

  /*
   * vertex_groups tables (e.g. table_cube2d_vertex_groups) for different
   * types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_vertex_groups[] = {0, 0, 0, table_any1d_vertex_groups,
                         0, table_simplex2d_vertex_groups,
                         table_cube2d_vertex_groups,
                         table_simplex3d_vertex_groups,
                         table_pyramid3d_vertex_groups,
                         table_prism3d_vertex_groups,
                         0, table_cube3dsym_vertex_groups};

  /*
   * Codimension 0 element tables (e.g. table_cube2d_codim_0) for different
   * types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_codim_0[][2] = {{0, 0}, {0, 0}, {0, 0},
                      {table_any1d_codim_0_interior,
                       table_any1d_codim_0_exterior}, {0, 0},
                      {table_simplex2d_codim_0_interior,
                       table_simplex2d_codim_0_exterior},
                      {table_cube2d_codim_0_interior,
                       table_cube2d_codim_0_exterior},
                      {table_simplex3d_codim_0_interior,
                       table_simplex3d_codim_0_exterior},
                      {table_pyramid3d_codim_0_interior,
                       table_pyramid3d_codim_0_exterior},
                      {table_prism3d_codim_0_interior,
                       table_prism3d_codim_0_exterior}, {0, 0},
                      {table_cube3dsym_codim_0_interior,
                       table_cube3dsym_codim_0_exterior}};

  /*
   * element group tables (e.g. table_cube2d_codim_0_exterior_groups)
   * for different types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_element_groups[][2] = {{0, 0}, {0, 0}, {0, 0},
                             {table_any1d_interior_groups,
                              table_any1d_exterior_groups}, {0, 0},
                             {table_simplex2d_interior_groups,
                              table_simplex2d_exterior_groups},
                             {table_cube2d_interior_groups,
                              table_cube2d_exterior_groups},
                             {table_simplex3d_interior_groups,
                              table_simplex3d_exterior_groups},
                             {table_pyramid3d_interior_groups,
                              table_pyramid3d_exterior_groups},
                             {table_prism3d_interior_groups,
                              table_prism3d_exterior_groups}, {0, 0},
                             {table_cube3dsym_interior_groups,
                              table_cube3dsym_exterior_groups}};

  /*
   * Codimension 1 element tables (e.g. table_cube2d_codim_1) for different
   * types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_codim_1[] = {0, 0, 0, table_any1d_codim_1,
                   0, table_simplex2d_codim_1,
                   table_cube2d_codim_1, table_simplex3d_codim_1,
                   table_pyramid3d_codim_1, table_prism3d_codim_1, 0,
                   table_cube3dsym_codim_1};

  /*
   * MC33 offset tables (e.g. table_cube2d_mc33_offsets) for
   * different types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_mc33_offsets[] = {0, 0, 0, 0, 0, 0,
                        table_cube2d_mc33_offsets, 0,
                        table_pyramid3d_mc33_offsets,
                        table_prism3d_mc33_offsets, 0,
                        table_cube3dsym_mc33_offsets};

  /*
   * Test face tables (e.g. table_cube2d_mc33_face_test_order) for
   * different types of elements and dimensions.
   */
  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_face_tests[] = {0, 0, 0, 0, 0, 0,
                      table_cube2d_mc33_face_test_order, 0,
                      table_pyramid3d_mc33_face_test_order,
                      table_prism3d_mc33_face_test_order, 0,
                      table_cube3dsym_mc33_face_test_order};

  const short * const
  MarchingCubesTables<SymmetryType::symmetric>::
  all_complex_vertices[] = {0, 0, 0, 0, 0, 0,
                            table_cube2d_complex_vertices, 0,
                            table_pyramid3d_complex_vertices,
                            table_prism3d_complex_vertices, 0,
                            table_cube3dsym_complex_vertices};

} // end namespace tpmc
